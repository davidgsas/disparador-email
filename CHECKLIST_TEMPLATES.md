# ✅ CHECKLIST: Templates de Email para Montadores

## 🎯 Use este checklist para garantir que tudo está funcionando

---

## 📋 Antes de Começar

- [ ] Sistema Streamlit está rodando
- [ ] Você está autenticado no Microsoft Graph
- [ ] Acesso à página "Montagem (Montadores)"

---

## 🔧 Configuração Inicial (FAZER UMA VEZ)

### Passo 1: Acessar Configurações
- [ ] Clique em "Montagem (Montadores)" no menu lateral
- [ ] Clique em "Enviar Pagamentos"
- [ ] Localize "⚙️ Configurações de E-mail (Montador)" na sidebar direita

### Passo 2: Ver Variáveis Disponíveis
- [ ] Clique em "ℹ️ Variáveis Disponíveis para Templates"
- [ ] Revise a lista de variáveis disponíveis
- [ ] Copie as variáveis que deseja usar (incluindo `{{` e `}}`)

### Passo 3: Configurar Assunto
- [ ] No campo "Assunto (Montadores)", digite o assunto do email
- [ ] Use variáveis como `{{periodo_relatorio}}` se quiser
- [ ] Exemplo: `Relatório de Pagamento - {{periodo_relatorio}}`
- [ ] Clique fora do campo para salvar automaticamente

### Passo 4: Configurar Corpo do Email
- [ ] No campo "Corpo do E-mail (Montadores)", digite o corpo
- [ ] **IMPORTANTE**: Inclua a variável `{{link}}` no corpo
- [ ] Use outras variáveis se desejar (ex: `{{total_geral}}`)
- [ ] Clique fora do campo para salvar automaticamente

### Passo 5: Verificar Salvamento
- [ ] Feche e reabra o Streamlit
- [ ] Volte para "Montagem (Montadores)" → "Enviar Pagamentos"
- [ ] Verifique se o assunto e corpo estão lá
- [ ] ✅ Se estiverem, o salvamento está funcionando!

---

## 📧 Template Recomendado

Use este template como base:

### Assunto:
```
Relatório de Pagamento de Montagem - {{periodo_relatorio}}
```

### Corpo:
```
Prezado {{nome_montador}},

Segue em anexo o relatório de pagamento do período {{periodo_relatorio}}.

💰 VALOR TOTAL: R$ {{total_geral}}

📎 LINK PARA ENVIO DE NOTA FISCAL:
{{link}}

⚠️ Por favor, envie a Nota Fiscal em até 5 dias úteis.

Em caso de dúvidas, entre em contato.

Atenciosamente,
Equipe Novo Mundo
```

---

## 🧪 Teste de Funcionamento

### Teste 1: Verificar Salvamento
- [ ] Digite algo no campo de assunto
- [ ] Clique fora do campo
- [ ] Feche o navegador
- [ ] Reabra o Streamlit
- [ ] Volte para a página de montadores
- [ ] ✅ O assunto que você digitou está lá?

### Teste 2: Enviar Email de Teste
- [ ] Adicione uma montagem manualmente ou via Excel
- [ ] Configure o template com a variável `{{link}}`
- [ ] Clique em "▶️ PROCESSAR E ENVIAR E-MAILS"
- [ ] Aguarde o envio
- [ ] Verifique o email recebido
- [ ] ✅ O link está no email?

### Teste 3: Verificar Link Gerado
- [ ] Após enviar o email, vá para "Histórico de Montagens"
- [ ] Localize o envio recente
- [ ] Procure a coluna "Link" ou "Status API"
- [ ] ✅ Há um link válido?

---

## 🔍 Verificação de Variáveis

Marque as variáveis que você está usando:

### Variáveis Básicas:
- [ ] `{{nome_montador}}` - Nome do montador
- [ ] `{{periodo_relatorio}}` - Período do relatório
- [ ] `{{link}}` - **Link de upload (ESSENCIAL!)**

### Variáveis Financeiras (Opcionais):
- [ ] `{{total_geral}}` - Valor total
- [ ] `{{total_comissao}}` - Comissão
- [ ] `{{total_auxilio}}` - Auxílio
- [ ] `{{percentual_comissao}}` - Percentual

---

## ⚠️ Possíveis Problemas e Soluções

### Problema 1: Template não salvou
**Sintomas:**
- Digitei o template mas ele desapareceu

**Soluções:**
- [ ] Certifique-se de clicar FORA do campo após digitar
- [ ] Aguarde 1-2 segundos antes de fechar o navegador
- [ ] Verifique se o arquivo `config.json` existe na raiz do projeto
- [ ] Execute: `cat /Users/davidgabriel/projetos/disparador-email/config.json`

### Problema 2: Link não aparece no email
**Sintomas:**
- Email enviado mas sem link
- Variável `{{link}}` aparece literalmente no email

**Soluções:**
- [ ] Certifique-se de usar `{{link}}` e não `{link}` (chaves duplas!)
- [ ] Verifique se o link foi gerado: vá para "Histórico de Montagens"
- [ ] Aguarde alguns segundos após o envio para o link ser gerado
- [ ] Execute o teste: `python teste_variavel_link.py`

### Problema 3: Email não enviado
**Sintomas:**
- Erro ao clicar em "PROCESSAR E ENVIAR"
- Status "❌ Erro"

**Soluções:**
- [ ] Verifique a autenticação do Microsoft Graph
- [ ] Certifique-se de que o montador existe no banco
- [ ] Verifique se há duplicidade (período já enviado)
- [ ] Veja os logs no terminal onde o Streamlit está rodando

---

## 📊 Validação Final

Após configurar tudo, faça este teste final:

- [ ] 1. Template de assunto salvo e carrega corretamente
- [ ] 2. Template de corpo salvo e carrega corretamente
- [ ] 3. Variável `{{link}}` incluída no corpo
- [ ] 4. Enviou um email de teste
- [ ] 5. Email recebido com link válido
- [ ] 6. Link abre a página de upload
- [ ] 7. Template continua salvo após reiniciar

### ✅ Se marcou TODOS os itens acima:
```
╔════════════════════════════════════════╗
║                                        ║
║  ✅ SISTEMA CONFIGURADO CORRETAMENTE! ║
║                                        ║
║  Você está pronto para usar! 🎉       ║
║                                        ║
╚════════════════════════════════════════╝
```

---

## 📞 Precisa de Ajuda?

### Documentação Disponível:
1. **GUIA_TEMPLATES_MONTADORES.md** - Guia de uso completo
2. **CORRECAO_TEMPLATES_MONTADORES.md** - Documentação técnica
3. **RESUMO_CORRECOES.md** - Resumo visual das mudanças

### Comandos Úteis:

```bash
# Ver arquivo de configuração
cat config.json

# Testar variável {{link}}
python teste_variavel_link.py

# Ver logs do Streamlit
# (já estão no terminal onde você rodou streamlit run)
```

---

## 🎓 Dicas Profissionais

### ✅ Boas Práticas:
- Use linguagem clara e profissional no email
- Sempre inclua `{{link}}` no corpo
- Adicione prazo para envio da NF (ex: "em até 5 dias úteis")
- Use emojis com moderação (📎, 💰, ⚠️)
- Teste o template antes de enviar para todos

### ❌ Evite:
- Esquecer de incluir `{{link}}` no corpo
- Usar chaves simples `{link}` ao invés de duplas `{{link}}`
- Templates muito longos (mantenha conciso)
- Excesso de variáveis desnecessárias
- Enviar sem testar primeiro

---

## 📅 Manutenção

### Semanal:
- [ ] Verificar se os templates continuam salvos
- [ ] Testar envio de email de teste

### Mensal:
- [ ] Revisar o template (está claro? profissional?)
- [ ] Verificar se há novas variáveis disponíveis
- [ ] Backup do arquivo `config.json`

### Quando Houver Problemas:
- [ ] Verificar logs do terminal
- [ ] Executar `python teste_variavel_link.py`
- [ ] Consultar documentação técnica

---

## 🏆 Você Está Pronto!

Se chegou até aqui e marcou todos os itens necessários, você está pronto para usar o sistema de templates de email para montadores!

**Próximos Passos:**
1. Finalize a configuração do seu template
2. Envie um email de teste
3. Use o sistema normalmente

**Lembre-se:**
- Templates são salvos AUTOMATICAMENTE
- A variável `{{link}}` é ESSENCIAL
- Consulte a documentação quando precisar

---

**Data**: 15 de Outubro de 2025  
**Status**: ✅ Sistema Operacional  
**Versão**: 2.0 (com suporte a `{{link}}`)

🎉 **BOA SORTE!** 🎉
