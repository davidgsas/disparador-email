# 🚀 Integração Automática com API no Momento do Envio

## 📋 Contexto

Anteriormente, o link de upload era gerado apenas quando o usuário clicava manualmente em "Enviar para API" na interface. Agora, o sistema gera o link **automaticamente** no momento do envio do email.

---

## ✅ Implementação Prestadores

### Localização
**Arquivo**: `streamlit_app.py` (linhas 365-372)

### Fluxo
1. Sistema cria lote no banco (`criar_lote_servico`)
2. **Imediatamente** chama API para gerar link (`enviar_lote_para_api`)
3. Link é salvo no banco automaticamente
4. Email é enviado com o link incluído no corpo/template

### Código
```python
lote_id = db.criar_lote_servico(prestador_info['id'], nome_prestador, periodo, total_geral, items_to_log)

# Enviar para API DV Processamento para gerar link de upload
link_upload = None
try:
    from api_upload_client import enviar_lote_para_api
    sucesso, mensagem, dados = enviar_lote_para_api(lote_id)
    if sucesso and dados:
        link_upload = dados.get('link')
except Exception as e:
    st.warning(f"⚠️ Não foi possível gerar link de upload: {str(e)}")

ctx = {
    "nome_prestador": nome_prestador, 
    "periodo": periodo, 
    "items": items_fmt, 
    "total_geral": total_geral, 
    "saudacao": saudacao, 
    "lote_id": lote_id,
    "link_upload": link_upload  # ✅ Disponível no template
}
```

**Status**: ✅ **JÁ IMPLEMENTADO**

---

## ✅ Implementação Montadores

### Localização
**Arquivo**: `database.py` (função `log_sent_montagem`)

### Fluxo
1. Sistema cria registro no banco (`INSERT INTO envios_montagem`)
2. **Imediatamente** chama API para gerar link
3. Link é salvo automaticamente via `client.enviar_e_salvar()`
4. Email já foi enviado, mas link fica disponível no histórico

### Código Modificado
```python
def log_sent_montagem(montador_id, group_details, conversation_id):
    conn = get_db_connection()
    now = datetime.datetime.now()
    
    # Extrair dados do group_details para colunas cache
    montador_nome = group_details.get('nome_montador')
    quantidade_os = len(group_details.get('items', []))
    valor_total = group_details.get('total_geral', 0)
    periodo_relatorio = group_details.get('periodo_relatorio', '')
    
    # Extrair período no formato MM/YYYY
    periodo = None
    if periodo_relatorio:
        primeira_data = periodo_relatorio.split(' - ')[0].strip()
        if '/' in primeira_data:
            partes = primeira_data.split('/')
            if len(partes) == 3:
                periodo = f"{partes[1]}/{partes[2]}"
    
    # Inserir registro no banco
    with conn.cursor() as cur:
        cur.execute(
            """INSERT INTO envios_montagem 
               (montador_id, data_envio, detalhes, conversation_id, montador_nome, quantidade_os, valor_total, periodo) 
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
               RETURNING id""",
            (montador_id, now, psycopg2.extras.Json(group_details), conversation_id, 
             montador_nome, quantidade_os, valor_total, periodo)
        )
        envio_id = cur.fetchone()[0]
    conn.commit()
    conn.close()
    
    # 🚀 ENVIAR PARA API IMEDIATAMENTE após criar o registro
    try:
        from api_upload_client import APIUploadClient
        
        print(f"🚀 Enviando envio #{envio_id} para API automaticamente...")
        client = APIUploadClient()
        sucesso, mensagem, dados = client.enviar_e_salvar(envio_id, tipo='montagem')
        
        if sucesso:
            print(f"   ✅ Link gerado: {dados.get('link', 'N/A')[:50]}...")
        else:
            print(f"   ⚠️  Erro ao gerar link: {mensagem}")
            # Não falha o envio do email se a API falhar
    except Exception as e:
        print(f"   ⚠️  Exceção ao chamar API: {e}")
        import traceback
        traceback.print_exc()
        # Não falha o envio do email se a API falhar
    
    return envio_id
```

**Status**: ✅ **IMPLEMENTADO AGORA**

---

## 🔄 Diferença entre os Fluxos

### Prestadores
```
1. Criar lote → 2. Gerar link → 3. Preparar email → 4. Enviar email
                                        ↑
                            link já disponível no template
```

### Montadores (Anterior)
```
1. Preparar email → 2. Enviar email → 3. Criar registro
                                            ↓
                                    link NÃO disponível
```

### Montadores (Novo)
```
1. Preparar email → 2. Enviar email → 3. Criar registro → 4. Gerar link (automático)
                                                                    ↓
                                                        link disponível no histórico
```

---

## ⚠️ Observação Importante

### Montadores: Link não vai no email inicial

Para **montadores**, o fluxo de envio é diferente:
- O email é enviado **ANTES** de criar o registro no banco
- Por isso, o link **não pode** estar no email inicial
- Mas agora o link é gerado **automaticamente logo após o envio**
- O link fica disponível no **histórico** do sistema

Se você quiser que o link **apareça no email do montador**, seria necessário:
1. Criar o registro no banco **ANTES** de enviar o email
2. Gerar o link
3. Incluir o link no template do email
4. Enviar o email

---

## 🎯 Resultado Esperado

### Antes
- Usuário enviava email para montador
- Tinha que ir na interface e clicar em "Enviar para API" manualmente
- Link era gerado apenas após esse clique

### Agora
- Usuário envia email para montador
- Sistema **automaticamente** gera o link nos bastidores
- Link aparece no histórico instantaneamente
- Não precisa clicar em nada manualmente

---

## 🧪 Como Testar

1. **Criar novo envio de montagem** pela interface
2. **Enviar o email** normalmente
3. **Ir no histórico** de montagens
4. **Verificar** se o link já está disponível (sem precisar clicar em "Enviar para API")

---

## 📊 Benefícios

✅ **Automação completa** - não precisa intervenção manual  
✅ **Experiência consistente** - ambos módulos funcionam igual  
✅ **Menos erros** - não depende de ação manual do usuário  
✅ **Mais rápido** - link gerado imediatamente  

---

**Data da Implementação**: 15 de Outubro de 2025  
**Arquivos Modificados**: `database.py` (função `log_sent_montagem`)
