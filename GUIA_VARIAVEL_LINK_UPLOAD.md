# 📧 GUIA: VARIÁVEL link_upload NOS EMAILS

## 🎯 O QUE É

A variável `link_upload` contém o link único gerado pela API DV Processamento para que o prestador possa anexar a Nota Fiscal.

---

## ✅ COMO USAR

### No Corpo do Email (Jinja2)

Você pode usar a variável `{{link_upload}}` em qualquer template de email para prestadores.

### Exemplo 1: Básico

```jinja2
Olá {{nome_prestador}},

Segue relatório do período {{periodo}}.

Para anexar a Nota Fiscal, acesse:
{{link_upload}}

Obrigado.
```

### Exemplo 2: Com Validação

```jinja2
Olá {{nome_prestador}},

Segue relatório do período {{periodo}}.

{% if link_upload %}
📎 Para anexar a Nota Fiscal:
{{link_upload}}

⚠️ Este link é válido por 30 dias.
{% else %}
📧 O link para anexo será enviado em breve.
{% endif %}

Obrigado.
```

### Exemplo 3: Completo com Instruções

```jinja2
{{saudacao}}, {{nome_prestador}}!

Segue em anexo o relatório de serviços do período **{{periodo}}**.

📊 Resumo:
• Valor Total: R$ {{total_geral}}
• Período: {{periodo}}
• Lote: #{{lote_id}}

{% if link_upload %}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📎 ANEXAR NOTA FISCAL
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Para anexar a Nota Fiscal, clique no link abaixo:

🔗 {{link_upload}}

⚠️ IMPORTANTE:
• Link válido por 30 dias
• Anexe arquivo em PDF
• Valor da NF deve corresponder ao relatório
• Em caso de dúvidas, responda este email

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{% else %}
⚠️ O link para anexar a Nota Fiscal será enviado em breve.
{% endif %}

Qualquer dúvida, estamos à disposição!

Atenciosamente,
Equipe Novo Mundo Resolve
```

---

## 📋 VARIÁVEIS DISPONÍVEIS

No template de email, você tem acesso a:

| Variável | Tipo | Descrição | Exemplo |
|----------|------|-----------|---------|
| `nome_prestador` | String | Nome do prestador | "ACME Instalações Ltda" |
| `periodo` | String | Período do lote | "10/2025" |
| `total_geral` | Number | Valor total | 15750.50 |
| `lote_id` | Integer | ID do lote | 142 |
| `saudacao` | String | Saudação automática | "Bom dia" / "Boa tarde" |
| `link_upload` | String | Link para upload de NF | "https://api.link.com.br/..." |
| `items` | List | Lista de OS do lote | [{"OS": "123", ...}, ...] |

---

## 🎨 ONDE CONFIGURAR

### 1. Via Interface Streamlit

1. Abrir Streamlit
2. Menu lateral: **"⚙️ Configurações de Envio (Serviços)"**
3. Campo: **"Corpo do E-mail"**
4. Editar texto e incluir `{{link_upload}}`
5. As mudanças são salvas automaticamente

### 2. Via config.json

Se usar arquivo de configuração:

```json
{
  "prestador_body": "Olá {{nome_prestador}},\n\nSegue relatório.\n\n{% if link_upload %}Link: {{link_upload}}{% endif %}\n\nObrigado."
}
```

---

## ⚙️ COMO FUNCIONA

### Fluxo:

```
1. Sistema cria lote no banco
   ↓
2. Envia dados para API DV Processamento
   ↓
3. API retorna link único
   ↓
4. Sistema salva link no banco
   ↓
5. Link é passado para variável {{link_upload}}
   ↓
6. Template Jinja2 renderiza o email
   ↓
7. Email enviado com link incluído
```

### Se API Falhar:

```
• link_upload = None
• Template usa {% if link_upload %} para verificar
• Mostra mensagem alternativa se não houver link
• Job automático tentará gerar link depois
```

---

## 🧪 TESTAR TEMPLATE

### No Streamlit:

1. Ir em "Enviar Boletins"
2. Editar template no campo "Corpo do E-mail"
3. Preencher planilha com dados teste
4. Enviar para um email seu
5. Verificar se link aparece corretamente

### Exemplo de Teste:

**Template:**
```jinja2
Teste: {{nome_prestador}} - {{periodo}}
Link: {{link_upload}}
```

**Resultado Esperado:**
```
Teste: ACME Instalações - 10/2025
Link: https://api.link.com.br/dvprocessamento/envio-nf/7bd6a6b...
```

---

## ⚠️ BOAS PRÁTICAS

### ✅ FAÇA:

```jinja2
{% if link_upload %}
🔗 Link: {{link_upload}}
{% else %}
⚠️ Link será enviado em breve
{% endif %}
```

### ❌ NÃO FAÇA:

```jinja2
Link: {{link_upload}}
(pode quebrar se link não existir)
```

### ✅ FORMATAÇÃO CLARA:

```jinja2
Para anexar a NF, acesse:
{{link_upload}}

(Link válido por 30 dias)
```

### ❌ FORMATAÇÃO CONFUSA:

```jinja2
Anexe aqui: {{link_upload}} valido 30 dias
```

---

## 📧 EXEMPLO COMPLETO (TEMPLATE RECOMENDADO)

```jinja2
{{saudacao}}, {{nome_prestador}}!

Segue em anexo o relatório de serviços referente ao período **{{periodo}}**.

📊 **Resumo do Lote #{{lote_id}}:**
• Valor Total: R$ {{total_geral}}
• Período: {{periodo}}

{% if link_upload %}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📎 **ANEXAR NOTA FISCAL**
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Para anexar a Nota Fiscal, acesse o link:

🔗 {{link_upload}}

⚠️ **IMPORTANTE:**
• Link válido por 30 dias
• Anexe arquivo em formato PDF
• Valor da NF deve corresponder ao valor do relatório
• Em caso de dúvidas, responda este email
{% else %}
⚠️ O link para anexar a Nota Fiscal será enviado em breve.
{% endif %}

Qualquer dúvida, estamos à disposição!

Atenciosamente,
**Equipe Novo Mundo Resolve**
```

---

## 🔄 TEMPLATE ATUAL (PADRÃO)

O sistema já vem com este template pré-configurado:

```jinja2
Segue a relação de boletins para emissão da nota fiscal de serviços entre **{{periodo}}**.

{% if link_upload %}
📎 Para anexar a Nota Fiscal, acesse o link abaixo:
{{link_upload}}

⚠️ Este link é válido por 30 dias.
{% else %}
📧 O link para anexar a Nota Fiscal será enviado em breve.
{% endif %}

Obrigado.
```

Você pode editar diretamente na interface Streamlit!

---

## 📝 NOTAS TÉCNICAS

### Sintaxe Jinja2

- `{{variavel}}` - Imprime valor da variável
- `{% if condicao %}...{% endif %}` - Condicional
- `{% if x %}...{% else %}...{% endif %}` - Condicional com alternativa

### Variável link_upload

- **Tipo:** String ou None
- **Formato:** URL completa (ex: "https://api.link.com.br/dvprocessamento/envio-nf/...")
- **Tamanho:** ~80-100 caracteres
- **Validade:** Definida pela API (geralmente 30 dias)

### Quando está Disponível

- ✅ Após lote ser enviado com sucesso
- ✅ Se API DV Processamento respondeu
- ❌ Se API estava fora do ar no momento
- ❌ Se ocorreu erro no envio

### Como Verificar

No histórico do Streamlit:
- 📤 = Link enviado (disponível)
- 📧 = Sem link (indisponível)

---

## 🚀 EXEMPLO DE USO REAL

### Cenário: Email para Prestador

**Dados:**
- Prestador: "ACME Instalações Ltda"
- Período: "10/2025"
- Valor: R$ 15.750,50
- Link gerado pela API

**Email Enviado:**

```
Assunto: Novo Mundo Resolve | Nota Fiscal | Período: 10/2025 | Prestador: ACME Instalações Ltda

Corpo:
──────────────────────────────────────────
Boa tarde, ACME Instalações Ltda!

Segue a relação de boletins para emissão da nota fiscal de serviços entre **10/2025**.

📎 Para anexar a Nota Fiscal, acesse o link abaixo:
https://api.link.com.br/dvprocessamento/envio-nf/7bd6a6b681b9f59cdc04e5d5fc3c237c

⚠️ Este link é válido por 30 dias.

Obrigado.

Atenciosamente,
Equipe Novo Mundo Resolve
──────────────────────────────────────────

Anexo: Relatorio_ACME_Instalacoes_Ltda_Lote_142.pdf
```

---

## ✅ CHECKLIST

Antes de enviar emails:

- [ ] Template configurado com `{{link_upload}}`
- [ ] Condicional `{% if link_upload %}` implementada
- [ ] Instruções claras para prestador
- [ ] Aviso de validade incluído
- [ ] Testado com email próprio
- [ ] Verificado que link aparece no email
- [ ] Testado clicando no link

---

## 📞 AJUDA

Se o link não aparecer no email:

1. Verificar "Histórico de Envios" no Streamlit
2. Ver se lote tem emoji 📤 (link gerado) ou 📧 (sem link)
3. Se 📧, clicar "Enviar para API Agora"
4. Copiar link manualmente e enviar por WhatsApp

---

**Data:** 13 de outubro de 2025  
**Versão:** 2.0
