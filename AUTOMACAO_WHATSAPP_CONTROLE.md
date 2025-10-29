# 📱 Controle de Envio de WhatsApp

## ✅ Implementado

### 1️⃣ Checkbox no Momento do Disparo

Agora nas telas de envio de emails (tanto prestadores quanto montadores), você verá uma checkbox:

```
📱 Enviar notificação por WhatsApp também? [✓]
```

**Como funciona:**
- **Marcada (padrão)**: Envia email + WhatsApp automaticamente
- **Desmarcada**: Envia apenas o email, sem WhatsApp

### 2️⃣ Feedback Visual

Após o envio, o relatório mostra o status do WhatsApp:

- `✅ Lote #123 Enviado 📱✅` - Email e WhatsApp enviados com sucesso
- `✅ Lote #123 Enviado 📱⚠️` - Email enviado, WhatsApp não configurado
- `✅ Lote #123 Enviado 📱❌` - Email enviado, erro no WhatsApp

### 3️⃣ Automação de NF Recebida

Quando um prestador ou montador anexa a Nota Fiscal pelo link, o sistema **automaticamente**:

1. Salva o arquivo no banco de dados
2. Atualiza o status para "N.F. RECEBIDA"
3. **Envia WhatsApp de confirmação** (se template estiver configurado)

Isso acontece sem precisar de ação manual!

---

## 🎯 Como Usar

### Enviar Email com WhatsApp

1. Vá em **Serviços (Prestadores)** ou **Montagem (Montadores)**
2. Configure os emails normalmente
3. Deixe a checkbox **"📱 Enviar notificação por WhatsApp também?"** marcada
4. Clique em **"▶️ ENVIAR E-MAILS PENDENTES"**
5. Veja o feedback no relatório final

### Enviar Apenas Email (sem WhatsApp)

1. **Desmarque** a checkbox antes de enviar
2. Só o email será enviado

### Configurar Templates de WhatsApp

1. Vá em **🤖 Automação WhatsApp**
2. Aba **Templates**
3. Configure os templates:
   - **📧 Email Enviado - Prestador**
   - **📧 Email Enviado - Montador**
   - **📄 NF Anexada - Prestador**
   - **📄 NF Anexada - Montador**

### Ativar/Desativar Automações

1. Vá em **🤖 Automação WhatsApp**
2. Aba **Triggers**
3. Ative/desative cada automação individualmente

---

## 🔧 Detalhes Técnicos

### Locais Modificados

**streamlit_app.py:**
- Linha ~327: Checkbox para prestadores
- Linha ~445: Integração WhatsApp após envio de email (prestadores)
- Linha ~983: Checkbox para montadores
- Linha ~1143: Integração WhatsApp após envio de email (montadores)

**database.py:**
- `salvar_nota_fiscal()`: Adiciona envio automático de WhatsApp
- `salvar_nota_fiscal_montagem()`: Adiciona envio automático de WhatsApp

### Fluxo de Automação

```
┌─────────────────────────────────────┐
│ Usuário clica "ENVIAR E-MAILS"      │
└───────────────┬─────────────────────┘
                │
                ▼
┌─────────────────────────────────────┐
│ Checkbox WhatsApp marcada?          │
└───────────────┬─────────────────────┘
                │
        ┌───────┴───────┐
        │ SIM           │ NÃO
        ▼               ▼
┌────────────────┐  ┌────────────────┐
│ Envia Email    │  │ Envia Email    │
│      +         │  │   (somente)    │
│ Envia WhatsApp │  └────────────────┘
└────────────────┘
        │
        ▼
┌─────────────────────────────────────┐
│ Relatório mostra status 📱✅/⚠️/❌  │
└─────────────────────────────────────┘
```

```
┌─────────────────────────────────────┐
│ Prestador/Montador anexa NF no link │
└───────────────┬─────────────────────┘
                │
                ▼
┌─────────────────────────────────────┐
│ API recebe arquivo e salva no banco │
└───────────────┬─────────────────────┘
                │
                ▼
┌─────────────────────────────────────┐
│ salvar_nota_fiscal() é chamada      │
└───────────────┬─────────────────────┘
                │
                ▼
┌─────────────────────────────────────┐
│ ✅ Envia WhatsApp automaticamente   │
│ "Sua NF foi recebida com sucesso!"  │
└─────────────────────────────────────┘
```

---

## 📋 Checklist de Uso

- [ ] WhatsApp conectado (veja no menu **📱 WhatsApp**)
- [ ] Templates configurados (veja em **🤖 Automação WhatsApp** > Templates)
- [ ] Triggers ativados (veja em **🤖 Automação WhatsApp** > Triggers)
- [ ] Telefone cadastrado nos prestadores/montadores
- [ ] Checkbox marcada no momento do envio (se quiser WhatsApp)

---

## 🐛 Troubleshooting

### WhatsApp não está sendo enviado

1. ✅ Verifique se o serviço está conectado: Menu **📱 WhatsApp** > Aba **Status**
2. ✅ Verifique se os templates estão configurados: **🤖 Automação WhatsApp** > Templates
3. ✅ Verifique se os triggers estão ativos: **🤖 Automação WhatsApp** > Triggers
4. ✅ Verifique se o prestador/montador tem telefone cadastrado
5. ✅ Veja o histórico para detalhes do erro: **🤖 Automação WhatsApp** > Histórico

### Como ver se funcionou

- **Histórico**: Menu **🤖 Automação WhatsApp** > Aba **Histórico**
- **Relatório**: Após enviar, veja o símbolo 📱 ao lado do status

---

## 📝 Notas

- O envio de WhatsApp NÃO bloqueia o envio de email
- Se o WhatsApp falhar, o email ainda será enviado normalmente
- Você pode ativar/desativar automações individuais sem desconectar o WhatsApp
- O histórico de WhatsApp fica salvo no banco de dados

---

**Desenvolvido em:** Janeiro 2025
