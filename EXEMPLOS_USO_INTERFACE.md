# 📸 Exemplos de Uso da Interface de Upload

## 🎬 Cenários Práticos com Screenshots Textuais

---

## Cenário 1: Primeira Vez no Sistema

### 1.1 - Acessando a Interface

```
╔════════════════════════════════════════════════════════════════╗
║  DISPARADOR NOVO MUNDO                                         ║
╠════════════════════════════════════════════════════════════════╣
║                                                                 ║
║  MENU                                                          ║
║  ┌──────────────────────────────────────────────────────┐    ║
║  │ Dashboard de Pendências                               │    ║
║  │ Serviços (Prestadores)                                │    ║
║  │ Montagem (Montadores)                                 │    ║
║  │ ► 📤 Upload de Notas Fiscais  ◄◄◄ CLIQUE AQUI       │    ║
║  │ 🗄️ Backups do Banco                                  │    ║
║  └──────────────────────────────────────────────────────┘    ║
║                                                                 ║
║  Conectado como:                                               ║
║  projetos@novomundo.com.br                                     ║
║                                                                 ║
╚════════════════════════════════════════════════════════════════╝
```

### 1.2 - Tela Inicial (Primeira Vez)

```
╔════════════════════════════════════════════════════════════════╗
║  📤 Sistema de Upload de Notas Fiscais                         ║
╠════════════════════════════════════════════════════════════════╣
║                                                                 ║
║  🎯 Como Funciona o Sistema de Upload                          ║
║                                                                 ║
║  1. Disparo de Lote: Link único gerado automaticamente        ║
║  2. Prestador Acessa: Upload da nota fiscal                    ║
║  3. Consulta Automática: Sistema verifica periodicamente       ║
║  4. Download Automático: Arquivo baixado e vinculado           ║
║                                                                 ║
║  ──────────────────────────────────────────────────────────    ║
║                                                                 ║
║  📊 Status  │  📋 Histórico  │  ⚙️ Configurações              ║
║  ════════════════════════════════════════════════════════      ║
║                                                                 ║
║  ℹ️ Nenhum lote com sistema de upload encontrado.             ║
║                                                                 ║
║  💡 Dica: O sistema de upload é ativado automaticamente        ║
║  quando você:                                                   ║
║  1. Dispara um lote de serviços com a API configurada         ║
║  2. O link único é gerado e enviado no email ao prestador     ║
║                                                                 ║
╚════════════════════════════════════════════════════════════════╝
```

---

## Cenário 2: Após Enviar Primeiro Lote

### 2.1 - Lista com Lote Pendente

```
╔════════════════════════════════════════════════════════════════╗
║  📊 Status Atual dos Uploads                                    ║
╠════════════════════════════════════════════════════════════════╣
║                                                                 ║
║  Filtrar: [Todos ▼]        Ordenar: [Mais Recentes ▼]         ║
║                                                                 ║
║  ──────────────────────────────────────────────────────────    ║
║                                                                 ║
║  📈 Estatísticas                                                ║
║                                                                 ║
║  ┌──────────┬──────────┬──────────┬──────────┐                ║
║  │  Total   │ ⏳ Pend  │ ✅ OK    │ ⏰ Exp   │                ║
║  ├──────────┼──────────┼──────────┼──────────┤                ║
║  │    1     │    1     │    0     │    0     │                ║
║  │          │  100%    │   0%     │          │                ║
║  └──────────┴──────────┴──────────┴──────────┘                ║
║                                                                 ║
║  ──────────────────────────────────────────────────────────    ║
║                                                                 ║
║  📋 Lotes com Upload (1)                                        ║
║                                                                 ║
║  ┌────────────────────────────────────────────────────────┐   ║
║  │ ### Lote #123           João Silva Instalações    ⏳   │   ║
║  │                                                         │   ║
║  │ Período: 10/2025        Enviado: 13/10/2025 14:30     │   ║
║  │                                                         │   ║
║  │ ▼ ⏳ Aguardando Upload - Ver Detalhes                 │   ║
║  │                                                         │   ║
║  │   📊 Informações do Lote                               │   ║
║  │   ID: 123                                               │   ║
║  │   Prestador: João Silva Instalações                    │   ║
║  │   Valor: R$ 1.250,50                                   │   ║
║  │   Enviado: 13/10/2025 14:30:00                         │   ║
║  │                                                         │   ║
║  │   📤 Informações do Upload                             │   ║
║  │   Status: Aguardando Upload                            │   ║
║  │   Token: abc123xyz789unique...                         │   ║
║  │                                                         │   ║
║  │   Link de Upload:                                       │   ║
║  │   https://api-externa.com/upload/abc123xyz789unique    │   ║
║  │   [📋 Copiar Link]                                     │   ║
║  │                                                         │   ║
║  │   ────────────────────────────────────────────────     │   ║
║  │                                                         │   ║
║  │   🔧 Ações                                             │   ║
║  │   [🔄 Consultar Status Agora]  [🔗 Reenviar Link]    │   ║
║  └────────────────────────────────────────────────────────┘   ║
║                                                                 ║
╚════════════════════════════════════════════════════════════════╝
```

---

## Cenário 3: Consultando Status Manualmente

### 3.1 - Clicou em "Consultar Status Agora"

```
╔════════════════════════════════════════════════════════════════╗
║  🔄 Consultando status...                                       ║
╠════════════════════════════════════════════════════════════════╣
║                                                                 ║
║  ⏳ Aguarde, verificando na API externa...                     ║
║                                                                 ║
║  [████████████░░░░░░░░] 60%                                    ║
║                                                                 ║
╚════════════════════════════════════════════════════════════════╝
```

### 3.2 - Ainda Pendente

```
╔════════════════════════════════════════════════════════════════╗
║  ℹ️ Status da API: pending                                     ║
╠════════════════════════════════════════════════════════════════╣
║                                                                 ║
║  O prestador ainda não fez o upload da nota fiscal.            ║
║                                                                 ║
║  Link continua ativo e válido.                                 ║
║                                                                 ║
╚════════════════════════════════════════════════════════════════╝
```

### 3.3 - Arquivo Disponível!

```
╔════════════════════════════════════════════════════════════════╗
║  ✅ Nota fiscal disponível! Baixando arquivo...                ║
╠════════════════════════════════════════════════════════════════╣
║                                                                 ║
║  ✅ Arquivo salvo em: uploads/nota_fiscal_lote_123.pdf        ║
║                                                                 ║
║  Atualizando status do lote...                                 ║
║                                                                 ║
╚════════════════════════════════════════════════════════════════╝
```

### 3.4 - Status Atualizado

```
╔════════════════════════════════════════════════════════════════╗
║  ### Lote #123           João Silva Instalações    ✅          ║
║                                                                 ║
║  Período: 10/2025        Enviado: 13/10/2025 14:30            ║
║                                                                 ║
║  ▼ ✅ Nota Fiscal Recebida - Ver Detalhes                     ║
║                                                                 ║
║    📊 Informações do Lote                                       ║
║    ID: 123                                                      ║
║    Prestador: João Silva Instalações                           ║
║    Valor: R$ 1.250,50                                          ║
║                                                                 ║
║    📤 Informações do Upload                                     ║
║    Status: Nota Fiscal Recebida ✅                             ║
║    Arquivo: uploads/nota_fiscal_lote_123.pdf                   ║
║                                                                 ║
║    🔧 Ações                                                     ║
║    [⬇️ Baixar N.F.]  [🔗 Reenviar Link]                       ║
║                                                                 ║
╚════════════════════════════════════════════════════════════════╝
```

---

## Cenário 4: Histórico Completo

### 4.1 - Tab Histórico com Vários Lotes

```
╔════════════════════════════════════════════════════════════════╗
║  📋 Histórico Completo de Uploads                               ║
╠════════════════════════════════════════════════════════════════╣
║                                                                 ║
║  Lote  │ Prestador           │ Período │ Status    │ N.F.      ║
║  ──────┼─────────────────────┼─────────┼───────────┼─────────  ║
║  #125  │ João Silva          │ 10/2025 │ ⏳ Pend   │ ❌ Não    ║
║  #124  │ Maria Santos        │ 10/2025 │ ⏳ Pend   │ ❌ Não    ║
║  #123  │ Carlos Oliveira     │ 10/2025 │ ✅ OK     │ ✅ Sim    ║
║  #122  │ Ana Costa           │ 09/2025 │ ✅ OK     │ ✅ Sim    ║
║  #121  │ Pedro Souza         │ 09/2025 │ ✅ OK     │ ✅ Sim    ║
║  #120  │ Julia Lima          │ 09/2025 │ ⏰ Exp    │ ❌ Não    ║
║  #119  │ Roberto Alves       │ 08/2025 │ ✅ OK     │ ✅ Sim    ║
║                                                                 ║
║  ──────────────────────────────────────────────────────────    ║
║                                                                 ║
║  [📊 Exportar para Excel]                                      ║
║                                                                 ║
╚════════════════════════════════════════════════════════════════╝
```

### 4.2 - Após Clicar em Exportar

```
╔════════════════════════════════════════════════════════════════╗
║  ✅ Relatório gerado com sucesso!                              ║
╠════════════════════════════════════════════════════════════════╣
║                                                                 ║
║  [⬇️ Download Relatório Excel]                                 ║
║  historico_uploads_20251013_143000.xlsx                        ║
║                                                                 ║
╚════════════════════════════════════════════════════════════════╝
```

---

## Cenário 5: Configuração da API

### 5.1 - API Não Configurada

```
╔════════════════════════════════════════════════════════════════╗
║  ⚙️ Configurações da API de Upload                             ║
╠════════════════════════════════════════════════════════════════╣
║                                                                 ║
║  ⚠️ API de Upload não configurada!                             ║
║                                                                 ║
║  📝 Como Configurar                                             ║
║                                                                 ║
║  1. Edite o arquivo .env na raiz do projeto                    ║
║  2. Adicione as seguintes variáveis:                           ║
║                                                                 ║
║  ┌────────────────────────────────────────────────────────┐   ║
║  │ UPLOAD_API_URL="https://api-externa.novomundo.com.br" │   ║
║  │ UPLOAD_API_KEY="sua-chave-api-aqui"                   │   ║
║  └────────────────────────────────────────────────────────┘   ║
║                                                                 ║
║  3. Reinicie o sistema                                          ║
║                                                                 ║
║  📋 Passos para obter a API:                                   ║
║  • Entre em contato com desenvolvedor do sistema externo       ║
║  • Ele fornecerá a URL e a chave de autenticação              ║
║  • Documentação: API_UPLOAD_NOTAS_ESPECIFICACAO.md            ║
║                                                                 ║
╚════════════════════════════════════════════════════════════════╝
```

### 5.2 - API Configurada

```
╔════════════════════════════════════════════════════════════════╗
║  ⚙️ Configurações da API de Upload                             ║
╠════════════════════════════════════════════════════════════════╣
║                                                                 ║
║  ✅ API Configurada!                                            ║
║                                                                 ║
║  🔗 URL da API                    🔑 API Key                   ║
║  ─────────────────────────────    ──────────────────────       ║
║  https://api-externa.com          abc1**************xyz9       ║
║                                                                 ║
║  ──────────────────────────────────────────────────────────    ║
║                                                                 ║
║  🔍 Testar Conexão com a API                                    ║
║                                                                 ║
║  [🚀 Testar Conexão]                                           ║
║                                                                 ║
║  ──────────────────────────────────────────────────────────    ║
║                                                                 ║
║  🤖 Consulta Automática                                         ║
║                                                                 ║
║  Job de Consulta Automática de Notas Fiscais                   ║
║                                                                 ║
║  Para ativar a consulta automática:                            ║
║                                                                 ║
║  ┌────────────────────────────────────────────────────────┐   ║
║  │ $ crontab -e                                           │   ║
║  │                                                         │   ║
║  │ # Adicionar (executa a cada hora):                    │   ║
║  │ 0 * * * * cd /caminho && python job_consultar_notas.py│   ║
║  └────────────────────────────────────────────────────────┘   ║
║                                                                 ║
║  [▶️ Executar Consulta Manual Agora]                           ║
║                                                                 ║
║  ──────────────────────────────────────────────────────────    ║
║                                                                 ║
║  📚 Documentação                                                ║
║                                                                 ║
║  📄 API_UPLOAD_NOTAS_ESPECIFICACAO.md       [📖 Ver]          ║
║     Especificação completa da API                              ║
║                                                                 ║
║  📄 IMPLEMENTACAO_UPLOAD_NOTAS.md           [📖 Ver]          ║
║     Guia de implementação e integração                         ║
║                                                                 ║
║  📄 teste_upload_api.py                     [📖 Ver]          ║
║     Script de teste da API                                     ║
║                                                                 ║
║  📄 job_consultar_notas.py                  [📖 Ver]          ║
║     Job automático de consulta                                 ║
║                                                                 ║
╚════════════════════════════════════════════════════════════════╝
```

### 5.3 - Testando Conexão

```
╔════════════════════════════════════════════════════════════════╗
║  🔄 Testando conexão...                                         ║
╠════════════════════════════════════════════════════════════════╣
║                                                                 ║
║  Conectando a: https://api-externa.novomundo.com.br            ║
║  Autenticando com API Key...                                   ║
║                                                                 ║
║  [████████████████████] 100%                                   ║
║                                                                 ║
║  ✅ Conexão com a API está funcionando!                        ║
║                                                                 ║
║  API URL: https://api-externa.novomundo.com.br                 ║
║  Status: Online                                                 ║
║  Latência: 250ms                                                ║
║                                                                 ║
╚════════════════════════════════════════════════════════════════╝
```

---

## Cenário 6: Copiar Link para Reenviar

### 6.1 - Expandindo Detalhes do Lote

```
╔════════════════════════════════════════════════════════════════╗
║  ### Lote #123                                             ⏳  ║
║                                                                 ║
║  ▼ ⏳ Aguardando Upload - Ver Detalhes                         ║
║                                                                 ║
║  📤 Informações do Upload                                       ║
║  Status: Aguardando Upload                                      ║
║  Token: abc123xyz789unique...                                  ║
║                                                                 ║
║  Link de Upload:                                                ║
║  ┌────────────────────────────────────────────────────────┐   ║
║  │ https://api-externa.com/upload/abc123xyz789unique      │   ║
║  └────────────────────────────────────────────────────────┘   ║
║                                                                 ║
║  [📋 Copiar Link]  ◄◄◄ CLIQUE AQUI                            ║
║                                                                 ║
╚════════════════════════════════════════════════════════════════╝
```

### 6.2 - Após Clicar em Copiar

```
╔════════════════════════════════════════════════════════════════╗
║  ✅ Link copiado! (Ctrl+C para copiar da caixa acima)          ║
╠════════════════════════════════════════════════════════════════╣
║                                                                 ║
║  Agora você pode:                                               ║
║  • Colar no WhatsApp e enviar ao prestador                     ║
║  • Colar no email                                               ║
║  • Colar no SMS                                                 ║
║                                                                 ║
╚════════════════════════════════════════════════════════════════╝
```

---

## Cenário 7: Filtrando Lotes

### 7.1 - Filtrar Apenas Pendentes

```
╔════════════════════════════════════════════════════════════════╗
║  📊 Status Atual dos Uploads                                    ║
╠════════════════════════════════════════════════════════════════╣
║                                                                 ║
║  Filtrar: [Pendente ▼]  ◄◄◄    Ordenar: [Mais Recentes ▼]    ║
║                                                                 ║
║  ──────────────────────────────────────────────────────────    ║
║                                                                 ║
║  📋 Lotes com Upload (3)  ← Apenas pendentes                   ║
║                                                                 ║
║  ┌────────────────────────────────────────────────────────┐   ║
║  │ ### Lote #125    João Silva         10/2025      ⏳   │   ║
║  └────────────────────────────────────────────────────────┘   ║
║                                                                 ║
║  ┌────────────────────────────────────────────────────────┐   ║
║  │ ### Lote #124    Maria Santos       10/2025      ⏳   │   ║
║  └────────────────────────────────────────────────────────┘   ║
║                                                                 ║
║  ┌────────────────────────────────────────────────────────┐   ║
║  │ ### Lote #122    Pedro Costa        10/2025      ⏳   │   ║
║  └────────────────────────────────────────────────────────┘   ║
║                                                                 ║
╚════════════════════════════════════════════════════════════════╝
```

### 7.2 - Filtrar Apenas Completos

```
╔════════════════════════════════════════════════════════════════╗
║  Filtrar: [Completo ▼]  ◄◄◄    Ordenar: [Mais Recentes ▼]    ║
║                                                                 ║
║  📋 Lotes com Upload (5)  ← Apenas completos                   ║
║                                                                 ║
║  ┌────────────────────────────────────────────────────────┐   ║
║  │ ### Lote #123    Carlos Oliveira    10/2025      ✅   │   ║
║  │ [⬇️ Baixar N.F.]                                       │   ║
║  └────────────────────────────────────────────────────────┘   ║
║                                                                 ║
║  ┌────────────────────────────────────────────────────────┐   ║
║  │ ### Lote #121    Ana Costa          09/2025      ✅   │   ║
║  │ [⬇️ Baixar N.F.]                                       │   ║
║  └────────────────────────────────────────────────────────┘   ║
║                                                                 ║
╚════════════════════════════════════════════════════════════════╝
```

---

## Cenário 8: Baixando Nota Fiscal

### 8.1 - Lote com Arquivo Disponível

```
╔════════════════════════════════════════════════════════════════╗
║  ### Lote #123           Carlos Oliveira              ✅       ║
║                                                                 ║
║  ▼ ✅ Nota Fiscal Recebida - Ver Detalhes                     ║
║                                                                 ║
║  📊 Informações do Lote                                         ║
║  ID: 123                                                        ║
║  Prestador: Carlos Oliveira                                    ║
║  Valor: R$ 2.450,75                                            ║
║                                                                 ║
║  📤 Informações do Upload                                       ║
║  Status: Nota Fiscal Recebida ✅                               ║
║  Arquivo: uploads/nota_fiscal_lote_123.pdf                     ║
║  Tamanho: 245 KB                                                ║
║  Recebido em: 14/10/2025 10:15                                 ║
║                                                                 ║
║  🔧 Ações                                                       ║
║  [⬇️ Baixar N.F.]  ◄◄◄ CLIQUE AQUI                            ║
║                                                                 ║
╚════════════════════════════════════════════════════════════════╝
```

### 8.2 - Download Iniciado

```
╔════════════════════════════════════════════════════════════════╗
║  ⬇️ Preparando download...                                     ║
╠════════════════════════════════════════════════════════════════╣
║                                                                 ║
║  Arquivo: nota_fiscal_lote_123.pdf                             ║
║  Tamanho: 245 KB                                                ║
║                                                                 ║
║  [████████████████████] 100%                                   ║
║                                                                 ║
║  ✅ Download concluído!                                        ║
║  Arquivo salvo em: Downloads/nota_fiscal_lote_123.pdf          ║
║                                                                 ║
╚════════════════════════════════════════════════════════════════╝
```

---

## Cenário 9: Múltiplos Lotes na Dashboard

### 9.1 - Visão Geral com Estatísticas

```
╔════════════════════════════════════════════════════════════════╗
║  📊 Status Atual dos Uploads                                    ║
╠════════════════════════════════════════════════════════════════╣
║                                                                 ║
║  📈 Estatísticas                                                ║
║                                                                 ║
║  ┌──────────┬──────────┬──────────┬──────────┐                ║
║  │  Total   │ ⏳ Pend  │ ✅ OK    │ ⏰ Exp   │                ║
║  ├──────────┼──────────┼──────────┼──────────┤                ║
║  │   15     │    8     │    5     │    2     │                ║
║  │          │  53% ↑   │  33% ↓   │  13%     │                ║
║  └──────────┴──────────┴──────────┴──────────┘                ║
║                                                                 ║
║  ──────────────────────────────────────────────────────────    ║
║                                                                 ║
║  📋 Lotes com Upload (15)                                       ║
║                                                                 ║
║  Filtrar: [Todos ▼]        Ordenar: [Mais Recentes ▼]         ║
║                                                                 ║
║  ╔═══════════════════════════════════════════════════════╗    ║
║  ║ Lote #130  │ João Silva        │ 11/2025 │ Hoje │ ⏳ ║    ║
║  ╚═══════════════════════════════════════════════════════╝    ║
║                                                                 ║
║  ┌────────────────────────────────────────────────────────┐   ║
║  │ Lote #129  │ Maria Santos      │ 11/2025 │ Hoje │ ⏳ │   ║
║  └────────────────────────────────────────────────────────┘   ║
║                                                                 ║
║  ┌────────────────────────────────────────────────────────┐   ║
║  │ Lote #128  │ Carlos Oliveira   │ 10/2025 │ Ontem│ ✅ │   ║
║  └────────────────────────────────────────────────────────┘   ║
║                                                                 ║
║  ┌────────────────────────────────────────────────────────┐   ║
║  │ Lote #127  │ Ana Costa         │ 10/2025 │ 2d   │ ✅ │   ║
║  └────────────────────────────────────────────────────────┘   ║
║                                                                 ║
║  ... mais 11 lotes ...                                          ║
║                                                                 ║
╚════════════════════════════════════════════════════════════════╝
```

---

## Cenário 10: Ver Documentação

### 10.1 - Tab Configurações - Documentação

```
╔════════════════════════════════════════════════════════════════╗
║  📚 Documentação                                                ║
╠════════════════════════════════════════════════════════════════╣
║                                                                 ║
║  Arquivos de Documentação:                                      ║
║                                                                 ║
║  ┌────────────────────────────────────────────────────────┐   ║
║  │ 📄 API_UPLOAD_NOTAS_ESPECIFICACAO.md       [📖 Ver]   │   ║
║  │    Especificação completa da API para o desenvolvedor  │   ║
║  │    externo                                              │   ║
║  └────────────────────────────────────────────────────────┘   ║
║                                                                 ║
║  ┌────────────────────────────────────────────────────────┐   ║
║  │ 📄 IMPLEMENTACAO_UPLOAD_NOTAS.md           [📖 Ver]   │   ║
║  │    Guia de implementação e integração                  │   ║
║  └────────────────────────────────────────────────────────┘   ║
║                                                                 ║
║  ┌────────────────────────────────────────────────────────┐   ║
║  │ 📄 teste_upload_api.py                     [📖 Ver]   │   ║
║  │    Script de teste da API                              │   ║
║  └────────────────────────────────────────────────────────┘   ║
║                                                                 ║
║  ┌────────────────────────────────────────────────────────┐   ║
║  │ 📄 job_consultar_notas.py                  [📖 Ver]   │   ║
║  │    Job automático de consulta                          │   ║
║  └────────────────────────────────────────────────────────┘   ║
║                                                                 ║
╚════════════════════════════════════════════════════════════════╝
```

### 10.2 - Visualizando Documento

```
╔════════════════════════════════════════════════════════════════╗
║  📄 API_UPLOAD_NOTAS_ESPECIFICACAO.md                          ║
╠════════════════════════════════════════════════════════════════╣
║                                                                 ║
║  # API de Upload de Notas Fiscais - Especificação             ║
║                                                                 ║
║  ## Visão Geral                                                 ║
║                                                                 ║
║  Esta API permite que prestadores façam upload de notas        ║
║  fiscais através de um link único...                           ║
║                                                                 ║
║  ## Endpoints                                                   ║
║                                                                 ║
║  ### 1. POST /api/upload/create                                ║
║  Cria um link único para upload                                ║
║                                                                 ║
║  **Request:**                                                   ║
║  ```json                                                        ║
║  {                                                              ║
║    "lote_id": 12345,                                           ║
║    "prestador": {                                              ║
║      "nome": "João Silva"                                      ║
║    }                                                            ║
║  }                                                              ║
║  ```                                                            ║
║                                                                 ║
║  [Scroll para ver mais...]                                      ║
║                                                                 ║
╚════════════════════════════════════════════════════════════════╝
```

---

## 🎯 Resumo dos Cenários

| # | Cenário | Complexidade | Frequência |
|---|---------|--------------|------------|
| 1 | Primeira vez no sistema | Baixa | Uma vez |
| 2 | Após enviar lote | Baixa | Diária |
| 3 | Consultar status | Média | Conforme necessário |
| 4 | Ver histórico | Baixa | Semanal |
| 5 | Configurar API | Média | Uma vez |
| 6 | Copiar link | Baixa | Conforme necessário |
| 7 | Filtrar lotes | Baixa | Diária |
| 8 | Baixar nota fiscal | Baixa | Conforme recebimento |
| 9 | Dashboard completa | Baixa | Diária |
| 10 | Ver documentação | Baixa | Conforme necessário |

---

## 💡 Dicas para Cada Cenário

### Cenário 1 - Primeira Vez
- Leia as instruções na tela
- Vá para "Configurações" primeiro
- Configure a API antes de usar

### Cenário 2 - Após Enviar Lote
- Verifique se o lote apareceu na lista
- Copie o link para enviar ao prestador
- Não precisa consultar status imediatamente

### Cenário 3 - Consultar Status
- Use apenas se precisar verificar urgente
- Job automático faz isso a cada hora
- Se clicar várias vezes, pode sobrecarregar API

### Cenário 4 - Histórico
- Exporte relatórios mensalmente
- Use filtros para análises específicas
- Mantenha histórico organizado

### Cenário 5 - Configurar API
- Guarde a API Key em lugar seguro
- Teste conexão após configurar
- Se falhar, verifique URL e Key

### Cenário 6 - Copiar Link
- Verifique se link não expirou
- Envie via canal preferido do prestador
- Confirme recebimento

### Cenário 7 - Filtrar
- Use "Pendente" para ver o que falta
- Use "Completo" para conferências
- Use "Expirado" para reenvios

### Cenário 8 - Baixar N.F.
- Salve em local organizado
- Faça backup regular
- Vincule ao lote no sistema

### Cenário 9 - Dashboard
- Verifique métricas diariamente
- Acompanhe percentuais
- Identifique gargalos

### Cenário 10 - Documentação
- Consulte quando tiver dúvidas
- Compartilhe com equipe
- Mantenha atualizada

---

**Data de Criação:** 13 de outubro de 2025  
**Versão:** 1.0  
**Autor:** Sistema Disparador Novo Mundo
