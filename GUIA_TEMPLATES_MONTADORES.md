# 📖 Guia Rápido: Templates de Email para Montadores

## 🎯 O Que Mudou?

### ✅ Agora Você Pode:

1. **Usar a variável `{{link}}`** no corpo do email
   - O link de upload será incluído automaticamente no email

2. **Digitar o template UMA VEZ** 
   - O sistema salva automaticamente ao alterar qualquer campo
   - Não precisa mais digitar toda vez!

3. **Usar mais variáveis** no email
   - Valores financeiros, percentuais, etc.

---

## 🚀 Como Usar (Passo a Passo)

### 1. Configurar o Template (PRIMEIRA VEZ)

1. Acesse: **Montagem (Montadores)** → **Enviar Pagamentos**

2. Na **sidebar direita**, encontre: **"⚙️ Configurações de E-mail (Montador)"**

3. Configure **UMA VEZ**:

   **Assunto:**
   ```
   Relatório de Pagamento - {{periodo_relatorio}}
   ```

   **Corpo do Email:**
   ```
   Prezado {{nome_montador}},

   Segue em anexo o relatório de pagamento do período {{periodo_relatorio}}.

   💰 Total a receber: R$ {{total_geral}}

   📎 Para enviar sua Nota Fiscal, acesse o link abaixo:
   {{link}}

   Em caso de dúvidas, entre em contato.

   Atenciosamente,
   Equipe Novo Mundo
   ```

4. **PRONTO!** O sistema salvou automaticamente ✅

---

### 2. Usar o Template Salvo

1. Toda vez que voltar ao sistema, o template estará lá
2. Basta processar e enviar os emails normalmente
3. O link será incluído automaticamente no email!

---

## 📝 Variáveis Disponíveis

Clique em **"ℹ️ Variáveis Disponíveis para Templates"** na interface para ver todas.

### Principais Variáveis:

| Variável | O Que Mostra | Exemplo |
|----------|--------------|---------|
| `{{nome_montador}}` | Nome do montador | DAVID DIAS |
| `{{periodo_relatorio}}` | Período do relatório | 01/10/2025 - 15/10/2025 |
| `{{link}}` | **Link de upload** | https://dvprocessa... |
| `{{total_geral}}` | Valor total | 1250.50 |
| `{{total_comissao}}` | Comissão | 850.00 |
| `{{total_auxilio}}` | Auxílio | 400.50 |
| `{{percentual_comissao}}` | Percentual de comissão | 5.0 |

---

## 💡 Exemplos de Templates

### Template Simples:
```
Olá {{nome_montador}},

Seu relatório está pronto: {{link}}

Atenciosamente,
Equipe Novo Mundo
```

### Template Completo:
```
Prezado {{nome_montador}},

Segue o relatório do período {{periodo_relatorio}}.

VALORES:
• Comissão ({{percentual_comissao}}%): R$ {{total_comissao}}
• Auxílio Semanal: R$ {{total_auxilio}}
• TOTAL: R$ {{total_geral}}

📎 ENVIE SUA NOTA FISCAL:
{{link}}

Em caso de dúvidas, entre em contato.

Atenciosamente,
Equipe Novo Mundo
```

### Template Marketing:
```
🎉 Olá, {{nome_montador}}!

Temos boas notícias! Seu pagamento está pronto.

💰 Valor Total: R$ {{total_geral}}
📅 Período: {{periodo_relatorio}}

📋 Para finalizar, envie sua NF:
👉 {{link}}

Continue com esse ótimo trabalho! 🚀

Equipe Novo Mundo
```

---

## ❓ Perguntas Frequentes

### P: Preciso salvar manualmente?
**R:** NÃO! O sistema salva automaticamente ao alterar qualquer campo.

### P: O link demora para aparecer?
**R:** O sistema aguarda 1 segundo para gerar o link antes de enviar o email.

### P: Posso mudar o template depois?
**R:** SIM! Basta alterar os campos. O sistema salvará automaticamente.

### P: O que acontece se não usar `{{link}}`?
**R:** O email será enviado sem o link. Use a variável para incluir o link!

### P: Posso usar múltiplas variáveis?
**R:** SIM! Use quantas variáveis quiser. Exemplo:
```
Olá {{nome_montador}},
Período: {{periodo_relatorio}}
Total: R$ {{total_geral}}
Link: {{link}}
```

---

## 🔍 Onde Está Salvo?

Os templates são salvos em:
```
/Users/davidgabriel/projetos/disparador-email/config.json
```

Você pode abrir este arquivo para ver os templates salvos.

**Estrutura:**
```json
{
  "montador_cc": "projetos.qualidade@novomundo.com.br",
  "montador_subject": "Seu assunto aqui",
  "montador_body": "Seu corpo de email aqui com {{link}}"
}
```

---

## ⚠️ Importante

1. **Use chaves duplas**: `{{link}}` e não `{link}`
2. **O link é gerado automaticamente**: Não precisa fazer nada especial
3. **Templates são compartilhados**: Todos os usuários do sistema veem o mesmo template

---

## 🎓 Resumo

| Ação | Como Fazer |
|------|------------|
| Ver variáveis disponíveis | Clique em "ℹ️ Variáveis Disponíveis" |
| Editar template | Altere os campos na sidebar |
| Salvar template | Automático! Não precisa fazer nada |
| Usar link no email | Adicione `{{link}}` no corpo |
| Ver template salvo | Reabra o sistema - estará lá |

---

## 🆘 Precisa de Ajuda?

- O template não salvou? Verifique se alterou o campo e saiu do foco (clicou fora)
- O link não aparece? Verifique se usou `{{link}}` com chaves duplas
- Dúvidas sobre variáveis? Clique em "ℹ️ Variáveis Disponíveis"

---

**Versão**: 15 de Outubro de 2025  
**Sistema**: Disparador de Emails Novo Mundo  
**Status**: ✅ Operacional
