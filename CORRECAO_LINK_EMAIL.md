# 🔧 CORREÇÃO CRÍTICA: Link Não Aparecia nos Emails

## 🚨 Problema Identificado

**Sintoma**: A variável `{{link}}` estava presente no template do email, mas o link não aparecia no email recebido.

**Causa Raiz**: 
1. **Prestadores**: Link era gerado mas não havia polling (espera) para garantir que estivesse disponível
2. **Prestadores**: Contexto usava `link_upload` mas template esperava `{{link}}`
3. **Ambos**: Tempo de espera de 1 segundo não era suficiente para API retornar o link

---

## ✅ Soluções Implementadas

### 1. Prestadores - Polling para Link

**Arquivo**: `streamlit_app.py` (linhas ~370-395)

#### Antes (PROBLEMA):
```python
# ❌ Não esperava o link estar disponível
link_upload = None
try:
    sucesso, mensagem, dados = enviar_lote_para_api(lote_id)
    if sucesso and dados:
        link_upload = dados.get('link')  # Pode estar vazio!
except Exception as e:
    st.warning(f"⚠️ Não foi possível gerar link")

ctx = {
    "link_upload": link_upload  # ❌ Nome errado + pode estar None
}
```

#### Depois (SOLUÇÃO):
```python
# ✅ Aguarda até 15 segundos pelo link
link_upload = ''
try:
    max_tentativas = 15
    tentativa = 0
    
    sucesso, mensagem, dados = enviar_lote_para_api(lote_id)
    
    if sucesso and dados:
        link_upload = dados.get('link', '')
        
        # Se não veio no retorno imediato, fazer polling
        if not link_upload:
            while tentativa < max_tentativas and not link_upload:
                time.sleep(1)
                tentativa += 1
                lote_salvo = db.get_lote_by_id(lote_id)
                if lote_salvo and lote_salvo.get('link_upload'):
                    link_upload = lote_salvo['link_upload']
                    print(f"✅ Link obtido em {tentativa}s")
                    break
except Exception as e:
    print(f"⚠️ Erro ao gerar link: {e}")

ctx = {
    "link": link_upload if link_upload else "⚠️ Link em processamento"
    # ✅ Nome correto: 'link' não 'link_upload'
}
```

---

### 2. Montadores - Feedback Visual + Polling

**Arquivo**: `streamlit_app.py` (linhas ~970-1000)

#### Melhorias:
```python
# ✅ Criar placeholders para feedback em tempo real
progress_placeholder = st.empty()
status_placeholder = st.empty()

# ✅ Mostrar progresso durante processamento
status_placeholder.info(f"⏳ Gerando link para {montador_info['nome']}...")

# ✅ Polling com feedback visual
max_tentativas = 15
while tentativa < max_tentativas and not link_gerado:
    time.sleep(1)
    tentativa += 1
    envio_salvo = db.get_envio_montagem_by_id(envio_id)
    if envio_salvo and envio_salvo.get('link_upload'):
        link_gerado = envio_salvo['link_upload']
        status_placeholder.success(f"✅ Link obtido em {tentativa}s")
        break
    else:
        status_placeholder.warning(f"⏳ Aguardando link... ({tentativa}/15s)")

if not link_gerado:
    status_placeholder.error(f"⚠️ Link não gerado após 15s")
```

---

### 3. Nova Função no Database

**Arquivo**: `database.py`

```python
def get_lote_by_id(lote_id):
    """Retorna lote pelo ID local"""
    conn = get_db_connection()
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        cur.execute('SELECT * FROM lotes_servico WHERE id = %s', (lote_id,))
        lote = cur.fetchone()
    conn.close()
    return lote
```

**Uso**: Permite buscar o lote completo (com link) durante o polling.

---

## 📊 Fluxo Corrigido

### Para Prestadores:

```
1. Criar lote no banco
2. Enviar para API (enviar_lote_para_api)
3. ✅ POLLING: Aguardar até 15s pelo link
   - Verificar a cada 1 segundo
   - Buscar lote atualizado com get_lote_by_id()
   - Parar quando link_upload estiver preenchido
4. Adicionar link ao contexto como 'link'
5. Renderizar templates com link disponível
6. Enviar email COM link
```

### Para Montadores:

```
1. Salvar envio no banco (log_sent_montagem)
   - API chamada automaticamente dentro da função
2. ✅ POLLING: Aguardar até 15s pelo link
   - Feedback visual para o usuário
   - Verificar a cada 1 segundo
   - Buscar envio com get_envio_montagem_by_id()
   - Parar quando link_upload estiver preenchido
3. Adicionar link ao contexto como 'link'
4. Renderizar templates com link disponível
5. Enviar email COM link
```

---

## 🎯 Variável Correta nos Templates

### ✅ Use: `{{link}}`

**Prestadores**:
```
Olá {{nome_prestador}},

Para enviar a Nota Fiscal, acesse:
{{link}}

Atenciosamente,
Equipe Novo Mundo
```

**Montadores**:
```
Olá {{nome_montador}},

Para enviar sua NF, acesse:
{{link}}

Período: {{periodo_relatorio}}
Total: R$ {{total_geral}}
```

---

## ⚠️ Tratamento de Erros

### Se Link Não For Gerado (timeout):

```python
ctx['link'] = "⚠️ Link em processamento - consulte o histórico"
```

**No email ficará**:
```
Para enviar a Nota Fiscal, acesse:
⚠️ Link em processamento - consulte o histórico
```

**Usuário pode**:
- Acessar "Histórico de Envios" ou "Histórico de Montagens"
- Procurar pelo lote/envio
- Copiar o link quando estiver disponível

---

## 🧪 Como Testar

### Teste 1: Prestador
```
1. Vá em "Serviços (Prestadores)" → "Enviar Boletins"
2. Configure o corpo do email com: "Link: {{link}}"
3. Adicione uma OS manualmente ou via Excel
4. Clique em "▶️ ENVIAR E-MAILS PENDENTES"
5. Aguarde até 15 segundos
6. Verifique o email recebido
7. ✅ O link deve estar presente e funcional
```

### Teste 2: Montador
```
1. Vá em "Montagem (Montadores)" → "Enviar Pagamentos"
2. Configure o corpo com: "Link: {{link}}"
3. Adicione uma montagem
4. Clique em "▶️ PROCESSAR E ENVIAR E-MAILS"
5. Observe o feedback visual (⏳ Aguardando link...)
6. Aguarde até aparecer "✅ Link obtido em Xs"
7. Verifique o email
8. ✅ O link deve estar presente
```

---

## 📈 Melhorias Implementadas

| Aspecto | Antes | Depois |
|---------|-------|--------|
| Tempo de espera | 1 segundo fixo | Até 15 segundos com polling |
| Feedback visual | Nenhum | ✅ Mensagens em tempo real |
| Verificação | Uma vez | ✅ A cada 1 segundo |
| Nome da variável | `link_upload` (prestador) | ✅ `link` (ambos) |
| Tratamento de erro | Exception genérica | ✅ Mensagem clara no email |

---

## 🔍 Logs de Debug

Durante o envio, você verá no terminal:

### Prestadores:
```
✅ Link prestador obtido em 3s: https://dvprocessamento.com.br/...
```

### Montadores:
```
🚀 Enviando envio #7 para API automaticamente...
✅ Link gerado: https://dvprocessamento.com.br/...
```

E na interface Streamlit:
```
⏳ Gerando link para DAVID DIAS...
⏳ Aguardando link... (1/15s)
⏳ Aguardando link... (2/15s)
✅ Link obtido em 3s: https://dvprocessa...
📧 Enviando email para DAVID DIAS...
✅ Email enviado para DAVID DIAS
```

---

## ✅ Checklist de Verificação

Para garantir que está funcionando:

- [ ] Template tem `{{link}}` no corpo (não `{{link_upload}}`)
- [ ] Ao enviar, vê mensagens de "Aguardando link..."
- [ ] Processo aguarda alguns segundos
- [ ] Vê mensagem "✅ Link obtido"
- [ ] Email recebido contém URL completa
- [ ] URL começa com `https://dvprocessamento.com.br/`
- [ ] Link abre página de upload ao clicar

---

## 🚀 Status

**Implementado**: 15 de Outubro de 2025  
**Testado**: Pendente (usuário deve testar)  
**Arquivos Modificados**:
- `streamlit_app.py` (linhas 365-405, 970-1040)
- `database.py` (nova função `get_lote_by_id`)

**Próximo Passo**: Testar com envio real e validar que link aparece no email.

---

**Resultado Esperado**: 
```
✅ Link SEMPRE presente no email
✅ Tempo de espera adequado (até 15s)
✅ Feedback visual durante processamento
✅ Mensagem clara se link não for gerado
```
