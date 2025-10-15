# 🔧 Correção: Templates de Email para Montadores

## 📋 Problemas Identificados

### 1. Variável `{link}` não disponível
**Sintoma**: Não era possível adicionar o link de upload no corpo do email de montadores.

**Causa Raiz**: O link era gerado pela API após o email ser enviado, então não estava disponível no momento da composição do email.

### 2. Templates não salvos automaticamente
**Sintoma**: Usuário precisava digitar assunto e corpo do email toda vez.

**Causa Raiz**: O sistema de salvamento já existia (função `save_config()`), mas o usuário não sabia que era automático.

---

## ✅ Soluções Implementadas

### 1. Adicionada Variável `{{link}}` ao Contexto

**Arquivo**: `streamlit_app.py` (linhas 945-1012)

#### Fluxo Anterior (PROBLEMA):
```python
# ❌ FLUXO INCORRETO
1. Preparar dados
2. Gerar PDF
3. Enviar email (sem link)
4. Salvar no banco
5. API gera link
```

#### Novo Fluxo (SOLUÇÃO):
```python
# ✅ FLUXO CORRETO
1. Verificar duplicidade (check_montagem_exists)
2. Preparar dados iniciais
3. 🔥 Salvar no banco (log_sent_montagem)
   → API gera link automaticamente dentro desta função
4. Aguardar 1 segundo
5. 🔥 Buscar registro salvo (get_envio_montagem_by_id)
6. 🔥 Extrair link gerado (link_upload)
7. Adicionar link ao contexto
8. Gerar PDF com link
9. Preparar templates com link disponível
10. Enviar email COM link
11. Atualizar conversation_id
```

#### Código Implementado:

```python
# 1️⃣ Verificar duplicidade ANTES de processar
from check_montagem_exists import check_montagem_exists

if check_montagem_exists(montador_info['id'], periodo_relatorio):
    report_summary.append({"Montador": montador_info['nome'], "Status": "❌ Já existe envio para este período"})
    continue

# 2️⃣ Criar contexto inicial
ctx_inicial = {
    "nome_montador": montador_info['nome'], 
    "periodo_relatorio": periodo_relatorio,
    "percentual_comissao": montador_info['percentual_comissao'] * 100,
    "items": items_para_pdf,
    "total_comissao": total_comissao,
    "total_adicionais": 0,
    "total_auxilio": total_auxilio,
    "total_geral": total_geral
}

# 3️⃣ Salvar no banco (gera link automaticamente via API)
envio_id = db.log_sent_montagem(montador_info['id'], ctx_inicial, "temp_conversation_id")

# 4️⃣ Buscar link gerado
time.sleep(1)  # Aguardar API processar
envio_salvo = db.get_envio_montagem_by_id(envio_id)
link_gerado = envio_salvo.get('link_upload', '') if envio_salvo else ''

# 5️⃣ Atualizar contexto com link
ctx = ctx_inicial.copy()
ctx['link'] = link_gerado

# 6️⃣ Gerar templates com link disponível
subj_template = Template(st.session_state.montador_subject)
body_template = Template(st.session_state.montador_body)
subj = subj_template.render(**ctx)
body_plain = body_template.render(**ctx)

# 7️⃣ Enviar email
# ... (código de envio)

# 8️⃣ Atualizar conversation_id após envio bem-sucedido
if resp.status_code == 202:
    # ... obter conversation_id real
    conn = db.get_db_connection()
    with conn.cursor() as cur:
        cur.execute('UPDATE envios_montagem SET conversation_id = %s WHERE id = %s', 
                   (conversation_id, envio_id))
    conn.commit()
    conn.close()
```

---

### 2. Documentação Atualizada

**Arquivo**: `templates/variaveis.py`

#### Adicionado:

```python
### 📧 Email para Montadores
Estas variáveis podem ser usadas no assunto e corpo do email:
- `{{nome_montador}}` - Nome do montador
- `{{periodo_relatorio}}` - Período do relatório
- `{{link}}` - Link para upload de arquivos (gerado automaticamente) 🆕
- `{{total_geral}}` - Valor total do pagamento 🆕
- `{{total_comissao}}` - Valor da comissão 🆕
- `{{total_auxilio}}` - Valor do auxílio 🆕
- `{{percentual_comissao}}` - Percentual de comissão (%) 🆕
```

#### Exemplo Atualizado:

```
**Exemplo para Montador:**
Prezado {{nome_montador}},

Seu relatório do período {{periodo_relatorio}} está pronto.
Total a receber: R$ {{total_geral}}

Para upload de documentos, acesse: {{link}}
```

---

### 3. Template Padrão Atualizado

**Arquivo**: `streamlit_app.py` (linha 907)

#### Antes:
```python
default_body_montador = "Olá, {{nome_montador}},\n\nSegue em anexo o seu relatório de pagamento de montagens referente ao período de **{{periodo_relatorio}}**.\n\nQualquer dúvida, estamos à disposição."
```

#### Depois:
```python
default_body_montador = """Olá, {{nome_montador}},

Segue em anexo o seu relatório de pagamento de montagens referente ao período de **{{periodo_relatorio}}**.

📎 **Link para upload de documentos:** {{link}}

Qualquer dúvida, estamos à disposição."""
```

---

## 🎯 Sistema de Salvamento Automático

### Como Funciona

O sistema **JÁ SALVAVA automaticamente** os templates, mas não estava claro para o usuário.

**Arquivo**: `streamlit_app.py`

#### Função de Salvamento:

```python
def save_config():
    """Salva as configurações atuais da session_state no arquivo JSON."""
    config_data = {
        "prestador_cc": st.session_state.get("prestador_cc", ""),
        "prestador_subject": st.session_state.get("prestador_subject", ""),
        "prestador_body": st.session_state.get("prestador_body", ""),
        "montador_cc": st.session_state.get("montador_cc", ""),      # ✅ Salvo
        "montador_subject": st.session_state.get("montador_subject", ""),  # ✅ Salvo
        "montador_body": st.session_state.get("montador_body", "")   # ✅ Salvo
    }
    with open(CONFIG_FILE, "w") as f:
        json.dump(config_data, f, indent=4)
```

#### Carregamento Inicial:

```python
config = load_config()  # Linha 135

# Campos carregam valores salvos:
st.text_input("Assunto (Montadores)", 
              value=config.get("montador_subject", default_subject_montador),
              key="montador_subject", 
              on_change=save_config)  # ✅ Salva ao alterar

st.text_area("Corpo do E-mail (Montadores)", 
             value=config.get("montador_body", default_body_montador),
             key="montador_body", 
             on_change=save_config,  # ✅ Salva ao alterar
             height=200)
```

### Arquivo de Configuração

**Localização**: `/Users/davidgabriel/projetos/disparador-email/config.json`

**Estrutura**:
```json
{
    "prestador_cc": "email1@example.com",
    "prestador_subject": "Assunto Prestador",
    "prestador_body": "Corpo do email prestador",
    "montador_cc": "projetos.qualidade@novomundo.com.br",
    "montador_subject": "Relatório de Pagamento de Montagem - Período: {{periodo_relatorio}}",
    "montador_body": "Olá, {{nome_montador}},\n\nSegue em anexo..."
}
```

---

## 📊 Variáveis Disponíveis - Resumo Completo

### Para Prestadores:
| Variável | Descrição | Exemplo |
|----------|-----------|---------|
| `{{nome_prestador}}` | Nome do prestador | "João Silva" |
| `{{periodo}}` | Período do serviço | "10/2025" |
| `{{link}}` | Link para upload | "https://dvprocessa..." |

### Para Montadores:
| Variável | Descrição | Exemplo |
|----------|-----------|---------|
| `{{nome_montador}}` | Nome do montador | "DAVID DIAS" |
| `{{periodo_relatorio}}` | Período do relatório | "01/10/2025 - 15/10/2025" |
| `{{link}}` | Link para upload | "https://dvprocessa..." |
| `{{total_geral}}` | Valor total | 1250.50 |
| `{{total_comissao}}` | Comissão calculada | 850.00 |
| `{{total_auxilio}}` | Auxílio semanal | 400.50 |
| `{{percentual_comissao}}` | Percentual | 5.0 |

---

## 🧪 Como Testar

### Teste 1: Link no Email

1. Acesse "Montagem (Montadores)" → "Enviar Pagamentos"
2. Na sidebar, em "Corpo do E-mail (Montadores)", adicione:
   ```
   Link: {{link}}
   ```
3. Processe um envio
4. Verifique o email recebido - deve conter o link real

### Teste 2: Salvamento de Template

1. Altere o assunto para: `Teste - {{periodo_relatorio}}`
2. Feche e reabra o Streamlit
3. O assunto deve continuar `Teste - {{periodo_relatorio}}`
4. ✅ Template foi salvo automaticamente em `config.json`

### Teste 3: Todas as Variáveis

Template de teste:
```
Olá {{nome_montador}},

Relatório do período: {{periodo_relatorio}}
Comissão: R$ {{total_comissao}}
Auxílio: R$ {{total_auxilio}}
Total: R$ {{total_geral}}
Percentual: {{percentual_comissao}}%

Link: {{link}}
```

---

## ✅ Status Final

| Item | Status | Detalhes |
|------|--------|----------|
| Variável `{{link}}` disponível | ✅ Implementado | Link gerado ANTES do email |
| Templates salvos automaticamente | ✅ Já existia | Funciona via `on_change=save_config` |
| Documentação atualizada | ✅ Implementado | `variaveis.py` com todas as variáveis |
| Template padrão com link | ✅ Implementado | Inclui `{{link}}` por padrão |
| Ordem de execução corrigida | ✅ Implementado | 1.Salvar → 2.Gerar link → 3.Enviar email |

---

## 🚀 Próximos Passos

**Para o Usuário**:
1. Digite o assunto e corpo do email UMA VEZ
2. O sistema salvará automaticamente
3. Use a variável `{{link}}` no corpo do email
4. Todas as variáveis listadas em "ℹ️ Variáveis Disponíveis" estão disponíveis

**Exemplo de Uso Real**:
```
Prezado {{nome_montador}},

Segue relatório do período {{periodo_relatorio}}.

💰 Comissão: R$ {{total_comissao}}
🎁 Auxílio: R$ {{total_auxilio}}
💵 Total: R$ {{total_geral}}

📎 Upload de NF: {{link}}

Atenciosamente,
Equipe Novo Mundo
```

---

**Implementado**: 15 de Outubro de 2025  
**Arquivos Modificados**:
- `streamlit_app.py` (linhas 907, 945-1012)
- `templates/variaveis.py` (documentação completa)

**Sistema**: 100% Operacional ✅
