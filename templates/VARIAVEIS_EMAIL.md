# Variáveis Disponíveis para Templates de Email

## Email para Prestadores (`email_template.html`)
As seguintes variáveis podem ser usadas no template de email para prestadores:

- `{{ intervalo }}`: Período do serviço (exemplo: "01/09/2025 a 30/09/2025")
- `{{ link_upload_nf }}`: Link único para upload da nota fiscal

## Email para Montadores (`montador_template.html`)
As seguintes variáveis podem ser usadas no template de email para montadores:

- `{{ nome_montador }}`: Nome do montador
- `{{ periodo_relatorio }}`: Período do relatório
- `{{ percentual_comissao }}`: Percentual de comissão aplicado
- `{{ total_comissao }}`: Valor total das comissões
- `{{ total_adicionais }}`: Valor total dos adicionais
- `{{ total_auxilio }}`: Valor total do auxílio semanal
- `{{ total_geral }}`: Valor total a receber
- `{{ link_upload_nf }}`: Link único para upload da nota fiscal

### Para cada item na lista de montagens (`{% for item in items %}`)
- `{{ item.boletim }}`: Número do boletim
- `{{ item.data_montagem }}`: Data da montagem
- `{{ item.cliente }}`: Nome do cliente
- `{{ item.nome_produto }}`: Nome do produto
- `{{ item.valor_venda }}`: Valor da venda
- `{{ item.comissao_editada }}`: Valor da comissão (se editada)
- `{{ item.comissao_calculada }}`: Valor da comissão calculada
- `{{ item.adicional }}`: Valor do adicional

## Como usar
Para usar estas variáveis nos templates, basta incluí-las entre chaves duplas. Por exemplo:

```html
Prezado {{ nome_montador }},

Seu relatório do período {{ periodo_relatorio }} está pronto.

Para enviar a nota fiscal, acesse: {{ link_upload_nf }}

<!-- Ou como botão HTML -->
<a href="{{ link_upload_nf }}" 
   style="background:#28a745; color:white; padding:10px 20px; text-decoration:none; border-radius:5px;">
    📤 ENVIAR NOTA FISCAL
</a>
```

## 📄 Upload de Nota Fiscal

A variável `{{ link_upload_nf }}` gera um link único e seguro para cada pagamento:

- **Validade**: 30 dias após geração
- **Formatos**: PDF, JPG, JPEG, PNG
- **Tamanho máximo**: 10MB
- **Segurança**: Token único que só pode ser usado uma vez
- **URL configurável**: Pode ser localhost (desenvolvimento) ou domínio personalizado (produção)

### Exemplos de uso:

**Link simples:**
```html
Faça o upload da nota fiscal: {{ link_upload_nf }}
```

**Botão estilizado:**
```html
<a href="{{ link_upload_nf }}" 
   style="display:inline-block; background:#007bff; color:white; padding:12px 25px; text-decoration:none; border-radius:5px; font-weight:bold;">
    📤 FAZER UPLOAD DA NOTA FISCAL
</a>
```

**Em texto corrido:**
```
Para finalizar o processo, acesse o link {{ link_upload_nf }} e faça o upload da sua nota fiscal.
```

**Nota**: Todas as variáveis numéricas são formatadas automaticamente com duas casas decimais usando o filtro `| format`. Por exemplo: `{{ "%.2f"|format(total_geral) }}`
