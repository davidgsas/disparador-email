# Variáveis Disponíveis para Templates de Email

## Email para Prestadores (`email_template.html`)
As seguintes variáveis podem ser usadas no template de email para prestadores:

- `{{ intervalo }}`: Período do serviço (exemplo: "01/09/2025 a 30/09/2025")

## Email para Montadores (`montador_template.html`)
As seguintes variáveis podem ser usadas no template de email para montadores:

- `{{ nome_montador }}`: Nome do montador
- `{{ periodo_relatorio }}`: Período do relatório
- `{{ percentual_comissao }}`: Percentual de comissão aplicado
- `{{ total_comissao }}`: Valor total das comissões
- `{{ total_adicionais }}`: Valor total dos adicionais
- `{{ total_auxilio }}`: Valor total do auxílio semanal
- `{{ total_geral }}`: Valor total a receber

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
```

**Nota**: Todas as variáveis numéricas são formatadas automaticamente com duas casas decimais usando o filtro `| format`. Por exemplo: `{{ "%.2f"|format(total_geral) }}`
