# 🤖 Como Configurar Automação WhatsApp

## 📝 Passo 1: Editar Templates

### Onde:
**Menu: 🤖 Automação WhatsApp → Aba "Templates de Mensagens"**

### Como fazer:

1. **Selecione um template** no dropdown:
   - `📤 Envio Inicial - Prestador`
   - `✅ NF Recebida - Prestador`
   - `📤 Envio Inicial - Montador`
   - `✅ NF Recebida - Montador`

2. **Edite o texto** no campo "Editar Template"
   - Use as **variáveis disponíveis** mostradas na coluna direita
   - Exemplo: `{{nome_prestador}}`, `{{periodo}}`, `{{valor}}`

3. **Clique em "💾 Salvar Alterações"**
   - ✅ Aparecerá "Template salvo com sucesso!"
   - 🎈 Balões de comemoração

4. **Teste o template** (opcional)
   - Clique em "🧪 Testar"
   - Veja como ficará a mensagem com dados de exemplo

---

## ⚡ Passo 2: Vincular Templates aos Gatilhos

### Onde:
**Menu: 🤖 Automação WhatsApp → Aba "Gatilhos Automáticos"**

### Gatilhos disponíveis:

#### 📧 Email Enviado - Prestador
- **Quando dispara:** Ao enviar email solicitando NF (com checkbox WhatsApp marcado)
- **Template padrão:** `prestador_envio_inicial`

#### 📄 NF Anexada - Prestador
- **Quando dispara:** Quando prestador anexa NF no link
- **Template padrão:** `prestador_nf_recebida`

#### 📧 Email Enviado - Montador
- **Quando dispara:** Ao enviar email de pagamento (com checkbox WhatsApp marcado)
- **Template padrão:** `montador_envio_inicial`

#### 📄 NF Anexada - Montador
- **Quando dispara:** Quando montador anexa NF no link
- **Template padrão:** `montador_nf_recebida`

### Como configurar:

1. **Expanda o gatilho** que deseja configurar
2. **Marque/Desmarque "✅ Ativo"**
   - ✅ Marcado = gatilho funcionando
   - ☐ Desmarcado = gatilho desativado
3. **Escolha o template** no dropdown "📝 Template"
   - Você pode trocar por qualquer template do mesmo tipo
4. **Clique em "💾 Salvar"**

---

## 🎯 Exemplo de Uso Completo

### Cenário: Personalizar mensagem de prestador

1. **Vá em Templates**
   - Selecione "📤 Envio Inicial - Prestador"
   - Edite a mensagem:
   ```
   🧾 *Olá {{nome_prestador}}!*
   
   Seu serviço do período {{periodo}} foi aprovado!
   💰 Valor: R$ {{valor}}
   
   📧 Verifique seu email para os próximos passos.
   🔗 Link de upload: {{link}}
   
   Obrigado! 🙏
   ```
   - Clique em "💾 Salvar Alterações"

2. **Vá em Gatilhos**
   - Expanda "📧 Email Enviado - Prestador"
   - Marque "✅ Ativo"
   - Confirme que o template é "prestador_envio_inicial"
   - Clique em "💾 Salvar"

3. **Teste enviando um email**
   - Vá em "Serviços (Prestadores)"
   - Deixe a checkbox "📱 Enviar notificação por WhatsApp também?" marcada
   - Envie o email
   - ✅ O WhatsApp será enviado automaticamente com sua mensagem personalizada!

---

## 📊 Verificar Histórico

### Onde:
**Menu: 🤖 Automação WhatsApp → Aba "Histórico"**

Aqui você pode:
- ✅ Ver todos os WhatsApps enviados
- ✅ Filtrar por prestador/montador
- ✅ Filtrar por status (enviado/erro)
- ✅ Ver mensagens enviadas
- ✅ Ver erros (se houver)

---

## ✅ Checklist Rápido

Antes de usar:
- [ ] WhatsApp conectado (Menu "📱 WhatsApp")
- [ ] Templates editados e salvos
- [ ] Gatilhos ativados e com templates vinculados
- [ ] Prestadores/Montadores têm telefone cadastrado

Para enviar:
- [ ] Checkbox "📱 Enviar notificação por WhatsApp também?" marcada
- [ ] Enviar email normalmente
- [ ] Verificar relatório (aparece 📱✅ se enviou)
- [ ] Confirmar no histórico WhatsApp

---

## 🔧 Troubleshooting

### "Template não configurado"
✅ **Solução:** Vá em Gatilhos → Verifique se o template está selecionado → Salve

### "Prestador sem telefone"
✅ **Solução:** Vá em "Gerenciar Prestadores" → Adicione telefone no formato correto (ex: 5511999999999)

### "WhatsApp não conectado"
✅ **Solução:** Vá em "📱 WhatsApp" → Aba "Status" → Conecte pelo QR Code

### Template não está salvando
✅ **Solução:** 
1. Edite o template
2. Clique em "💾 Salvar Alterações" (não apenas sair da tela)
3. Aguarde a mensagem de confirmação
4. Verifique em Gatilhos se o template aparece no dropdown

---

## 💡 Dicas

1. **Use emojis** nas mensagens para deixar mais atrativas
2. **Teste primeiro** com um prestador/montador de teste
3. **Monitore o histórico** nos primeiros envios
4. **Personalize as mensagens** para cada tipo de situação
5. **Deixe os gatilhos de NF sempre ativos** - assim o prestador recebe confirmação automática

---

**Desenvolvido em:** Janeiro 2025
