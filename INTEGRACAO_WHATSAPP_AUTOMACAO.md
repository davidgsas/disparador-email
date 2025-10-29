# 🤖 Como Integrar Automação WhatsApp no Sistema

## 📍 Onde Adicionar as Chamadas

### 1. Quando Enviar Email para Prestador

**Arquivo:** `streamlit_app.py` ou onde você envia os emails

**Antes:**
```python
# Código atual de envio de email
send_email(
    to=prestador_email,
    subject=subject,
    body=body,
    attachments=[arquivo_pdf]
)

# Salvar no banco
db.add_lote_servico(...)
```

**Depois (com WhatsApp):**
```python
# Código atual de envio de email
send_email(
    to=prestador_email,
    subject=subject,
    body=body,
    attachments=[arquivo_pdf]
)

# Salvar no banco
lote_id = db.add_lote_servico(...)

# NOVO: Enviar WhatsApp também
from whatsapp_triggers import whatsapp_automation

resultado_whats = whatsapp_automation.enviar_prestador_email_enviado(
    prestador_id=prestador_id,
    periodo=periodo_formatado,  # Ex: "01-31/10/2025"
    valor=valor_total,          # Ex: 1500.00
    link=link_upload            # Link da API
)

if resultado_whats.get("success"):
    st.success("✅ Email e WhatsApp enviados!")
else:
    st.warning(f"⚠️ Email enviado, mas WhatsApp falhou: {resultado_whats.get('error')}")
```

### 2. Quando Prestador Anexar Nota Fiscal

**Arquivo:** Onde você processa o upload de NF do prestador

**Antes:**
```python
# Código atual de processar NF
db.update_lote_status(lote_id, "NF Recebida")
db.update_lote_nf_info(lote_id, numero_nf, arquivo_path)
```

**Depois (com WhatsApp):**
```python
# Código atual de processar NF
db.update_lote_status(lote_id, "NF Recebida")
db.update_lote_nf_info(lote_id, numero_nf, arquivo_path)

# NOVO: Notificar por WhatsApp
from whatsapp_triggers import whatsapp_automation

# Buscar dados do lote
lote = db.get_lote_by_id(lote_id)

resultado_whats = whatsapp_automation.enviar_prestador_nf_recebida(
    prestador_id=lote['prestador_id'],
    periodo=lote['periodo'],
    valor=lote['valor_total'],
    numero_nf=numero_nf
)

if resultado_whats.get("success"):
    print("✅ Confirmação WhatsApp enviada")
```

### 3. Quando Enviar Email para Montador

**Arquivo:** `streamlit_app.py` (seção de montadores)

**Antes:**
```python
# Código atual de envio de email
send_email(
    to=montador_email,
    subject=subject,
    body=body,
    attachments=[relatorio_pdf]
)

# Salvar no banco
db.add_envio_montagem(...)
```

**Depois (com WhatsApp):**
```python
# Código atual de envio de email
send_email(
    to=montador_email,
    subject=subject,
    body=body,
    attachments=[relatorio_pdf]
)

# Salvar no banco
envio_id = db.add_envio_montagem(...)

# NOVO: Enviar WhatsApp também
from whatsapp_triggers import whatsapp_automation

resultado_whats = whatsapp_automation.enviar_montador_email_enviado(
    montador_id=montador_id,
    periodo=periodo_relatorio,  # Ex: "Outubro/2025"
    valor_total=valor_total,    # Ex: 2300.00
    quantidade_os=len(os_list)  # Quantidade de OSs
)

if resultado_whats.get("success"):
    st.success("✅ Email e WhatsApp enviados!")
else:
    st.warning(f"⚠️ Email enviado, mas WhatsApp falhou: {resultado_whats.get('error')}")
```

### 4. Quando Montador Anexar Nota Fiscal

**Arquivo:** Onde você processa o upload de NF do montador

**Antes:**
```python
# Código atual de processar NF
db.update_envio_montagem_status(envio_id, "NF Recebida")
db.update_envio_montagem_nf(envio_id, numero_nf, arquivo_path)
```

**Depois (com WhatsApp):**
```python
# Código atual de processar NF
db.update_envio_montagem_status(envio_id, "NF Recebida")
db.update_envio_montagem_nf(envio_id, numero_nf, arquivo_path)

# NOVO: Notificar por WhatsApp
from whatsapp_triggers import whatsapp_automation

# Buscar dados do envio
envio = db.get_envio_montagem_by_id(envio_id)

resultado_whats = whatsapp_automation.enviar_montador_nf_recebida(
    montador_id=envio['montador_id'],
    periodo=envio['periodo'],
    valor_total=envio['valor_total'],
    numero_nf=numero_nf
)

if resultado_whats.get("success"):
    print("✅ Confirmação WhatsApp enviada")
```

---

## 📝 Exemplo Completo de Integração

### Cenário: Envio de Email para Prestador (streamlit_app.py)

```python
# Localizar esta função no seu código:
def enviar_email_prestador(prestador_id, periodo, valor_total, os_list, arquivo_pdf):
    """Envia email e WhatsApp para prestador"""
    
    # 1. Buscar dados do prestador
    prestador = db.get_prestador_by_id(prestador_id)
    
    # 2. Preparar dados do email
    subject = f"Nota Fiscal | Período: {periodo} | Prestador: {prestador['nome']}"
    body = f"Segue relatório para emissão de NF no valor de R$ {valor_total:,.2f}"
    
    # 3. Enviar EMAIL
    try:
        send_email(
            to=prestador['email'],
            subject=subject,
            body=body,
            attachments=[arquivo_pdf]
        )
        st.success(f"✅ Email enviado para {prestador['nome']}")
    except Exception as e:
        st.error(f"❌ Erro ao enviar email: {e}")
        return False
    
    # 4. Salvar no banco
    lote_id = db.add_lote_servico(
        prestador_id=prestador_id,
        periodo=periodo,
        valor_total=valor_total,
        os_list=os_list,
        anexo_path=arquivo_pdf
    )
    
    # 5. NOVO: Enviar WHATSAPP (se configurado)
    if prestador.get('telefone'):
        from whatsapp_triggers import whatsapp_automation
        
        with st.spinner("📱 Enviando WhatsApp..."):
            resultado_whats = whatsapp_automation.enviar_prestador_email_enviado(
                prestador_id=prestador_id,
                periodo=periodo,
                valor=valor_total,
                link=prestador.get('link_upload', '#')
            )
            
            if resultado_whats.get("success"):
                st.success(f"✅ WhatsApp enviado para {prestador['nome']}")
            else:
                st.warning(f"⚠️ Não foi possível enviar WhatsApp: {resultado_whats.get('error')}")
    else:
        st.info(f"ℹ️ Prestador {prestador['nome']} não tem telefone cadastrado")
    
    return True
```

---

## 🎯 Checklist de Implementação

### Passo 1: Configurar Templates
- [ ] Acesse: Menu → **🤖 Automação WhatsApp** → **📝 Templates**
- [ ] Revise os templates padrão
- [ ] Customize conforme necessário
- [ ] Salve as alterações

### Passo 2: Ativar Gatilhos
- [ ] Acesse: Menu → **🤖 Automação WhatsApp** → **⚡ Gatilhos**
- [ ] Ative os gatilhos desejados:
  - ✅ Email Enviado - Prestador
  - ✅ NF Anexada - Prestador
  - ✅ Email Enviado - Montador
  - ✅ NF Anexada - Montador
- [ ] Salve as configurações

### Passo 3: Adicionar Telefones
- [ ] Acesse: Menu → **📱 WhatsApp** → **⚙️ Configurações**
- [ ] Cadastre telefones dos prestadores
- [ ] Cadastre telefones dos montadores
- [ ] Verifique formato: 5511999999999

### Passo 4: Integrar no Código
- [ ] Adicione imports: `from whatsapp_triggers import whatsapp_automation`
- [ ] Adicione chamadas após envio de email
- [ ] Adicione chamadas após recebimento de NF
- [ ] Teste com um prestador/montador

### Passo 5: Testar
- [ ] Envie um email de teste
- [ ] Verifique se WhatsApp foi enviado
- [ ] Anexe uma NF de teste
- [ ] Verifique confirmação no WhatsApp
- [ ] Veja histórico em **🤖 Automação** → **📊 Histórico**

---

## 🔧 Configuração Rápida

### 1. Rodar Migrations
```bash
# No terminal Python
python3 << EOF
import database as db
db.run_migrations()
print("✅ Tabelas criadas!")
EOF
```

### 2. Popular Templates Padrão
```python
# Executar uma vez para criar templates padrão
from whatsapp_triggers import whatsapp_automation
print("✅ Templates carregados na interface")
```

### 3. Testar Conexão
```bash
# Verificar se WhatsApp está conectado
curl http://localhost:3000/status
```

---

## 📊 Monitoramento

### Ver Histórico de Envios
```sql
-- No banco de dados
SELECT 
    n.data_envio,
    n.tipo,
    p.nome as prestador,
    m.nome as montador,
    n.status
FROM notificacoes_whatsapp n
LEFT JOIN prestadores p ON n.prestador_id = p.id
LEFT JOIN montadores m ON n.montador_id = m.id
ORDER BY n.data_envio DESC
LIMIT 50;
```

### Verificar Templates Ativos
```sql
SELECT nome, tipo, ativo 
FROM templates_whatsapp 
WHERE ativo = TRUE;
```

### Verificar Gatilhos Ativos
```sql
SELECT evento, ativo 
FROM automacao_whatsapp 
WHERE ativo = TRUE;
```

---

## 💡 Dicas

1. **Sempre verifique se há telefone** antes de tentar enviar
2. **Use try/except** para não quebrar o fluxo se WhatsApp falhar
3. **Email tem prioridade** - WhatsApp é complementar
4. **Monitore o histórico** para ver se está funcionando
5. **Customize os templates** de acordo com seu tom de comunicação

---

## 🐛 Troubleshooting

### WhatsApp não envia
- Verifique se o serviço está rodando: `./status_whatsapp_daemon.sh`
- Verifique se está conectado: http://localhost:3000/status
- Verifique se há telefone cadastrado
- Veja logs: `tail -f logs/whatsapp_service.log`

### Template não aparece
- Execute migrations: `db.run_migrations()`
- Verifique se salvou corretamente na aba Templates
- Veja no banco: `SELECT * FROM templates_whatsapp`

### Gatilho não dispara
- Verifique se está ativo na aba Gatilhos
- Veja no banco: `SELECT * FROM automacao_whatsapp WHERE ativo = TRUE`
- Verifique se o template existe

---

**✅ Tudo pronto para automatizar!**
