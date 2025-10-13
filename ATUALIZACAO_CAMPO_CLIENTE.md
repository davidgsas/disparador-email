# Atualização: Campo Cliente no Relatório de Prestadores

## 📋 Mudanças Implementadas

### 1. Template PDF Atualizado
- **Arquivo**: `templates/invoice_template.html`
- Adicionada coluna "Cliente" na tabela do relatório PDF
- A coluna aparece após "O.S" e antes de "Modalidade de Serviço"

### 2. Lançamento Manual Atualizado
- **Arquivo**: `streamlit_app.py`
- Adicionado campo "Cliente" no formulário de lançamento manual
- Campo posicionado entre "O.S" e "Modalidade"

### 3. Processamento de Dados
- Sistema agora processa e exibe o campo "cliente" no PDF
- Se o campo não existir nos dados, aparecerá "-" (hífen)

## 📊 Estrutura do Excel para Importação

Para importar via Excel, a planilha deve conter as seguintes colunas:

### Colunas Obrigatórias:
- `nome_prestador` ou `Nome_Prestador` - Nome do prestador
- `periodo` ou `Período` - Período do serviço
- `data_execucao` ou `Data_Execucao` - Data de execução
- `o_s` ou `O.S` ou `OS` - Número da ordem de serviço

### Colunas Opcionais:
- `cliente` ou `Cliente` - **NOVO** - Nome do cliente
- `localidade` ou `Localidade` - **NOVO** - Localidade do serviço
- `modalidade` ou `Modalidade` - Tipo de serviço
- `valor_custo_prestador` - Valor base
- `valor_extra` - Valor adicional
- `motivo_extra` - Motivo do valor extra
- `valor_total` - Valor total (calculado automaticamente se não fornecido)

## 🔍 Exemplo de Uso

### Lançamento Manual
1. Acesse "Serviços (Prestadores)" > "Enviar Boletins"
2. Na aba "Lançamento Manual", preencha:
   - Prestador
   - Período
   - O.S
   - **Cliente** ← NOVO CAMPO
   - Modalidade
   - Data de Execução
   - Valores

### Importação via Excel

Exemplo de estrutura do Excel:

| nome_prestador | periodo  | o_s    | cliente        | localidade         | modalidade | data_execucao | valor_custo_prestador | valor_extra | motivo_extra | valor_total |
|---------------|----------|--------|----------------|-------------------|------------|---------------|----------------------|-------------|--------------|-------------|
| João Silva    | 10/2025  | 12345  | Maria Santos   | São Paulo - SP    | Instalação | 01/10/2025    | 150.00               | 0.00        |              | 150.00      |
| João Silva    | 10/2025  | 12346  | José Oliveira  | Rio de Janeiro-RJ | Manutenção | 05/10/2025    | 200.00               | 50.00       | Urgência     | 250.00      |

## 📄 PDF Gerado

O relatório PDF agora inclui as colunas Cliente e Localidade:

```
┌──────┬────────────────┬──────────────────┬────────────┬─────────────────┬──────────┬──────────────┬────────────────────┬─────────────┐
│ O.S  │    Cliente     │   Localidade     │ Modalidade │ Data de Execução│ Valor(R$)│Valor Extra(R$)│ Motivo Valor Extra │ Valor Total │
├──────┼────────────────┼──────────────────┼────────────┼─────────────────┼──────────┼──────────────┼────────────────────┼─────────────┤
│12345 │ Maria Santos   │ São Paulo - SP   │ Instalação │   01/10/2025    │  150.00  │    0.00      │         -          │   150.00    │
│12346 │ José Oliveira  │Rio de Janeiro-RJ │ Manutenção │   05/10/2025    │  200.00  │   50.00      │     Urgência       │   250.00    │
└──────┴────────────────┴──────────────────┴────────────┴─────────────────┴──────────┴──────────────┴────────────────────┴─────────────┘
```

## ✅ Compatibilidade com Dados Antigos

- **Dados sem o campo "cliente"**: Aparecerá "-" no relatório
- **Lotes já enviados**: Não são afetados (mantêm estrutura original)
- **Importação de planilhas antigas**: Continuam funcionando normalmente

## 🔄 Migração de Dados Existentes

Os dados já cadastrados no banco continuam funcionando. O campo "cliente" é **opcional**, então:

- ✅ Planilhas novas **com** cliente: Campo será exibido no PDF
- ✅ Planilhas antigas **sem** cliente: Mostrará "-" no PDF
- ✅ Lançamentos manuais: Campo disponível para preenchimento

## 🎯 Próximos Passos (Opcional)

Se quiser adicionar o campo cliente retroativamente aos dados existentes:

1. Acesse "Histórico de Envios"
2. Verifique os lotes enviados
3. Os novos lotes já incluirão automaticamente o campo cliente

---

**Data da Atualização**: 13 de outubro de 2025
**Versão**: 2.1.0
