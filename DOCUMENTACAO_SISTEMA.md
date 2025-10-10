# 📋 DOCUMENTAÇÃO COMPLETA DO SISTEMA DISPARADOR DE EMAIL

## 🎯 VISÃO GERAL DO SISTEMA

O **Disparador de Email Novo Mundo** é um sistema completo de gestão e envio de emails para prestadores de serviço e montadores, desenvolvido com Streamlit e PostgreSQL. O sistema automatiza o processo de envio de relatórios, boletins e notas fiscais.

## 🏗️ ARQUITETURA DO SISTEMA

### Frontend Atual (Streamlit)
- **Framework:** Streamlit
- **Arquivo Principal:** `streamlit_app.py`
- **Interface:** Single Page Application com navegação por abas
- **Estado:** Gerenciado via `st.session_state`

### Backend
- **Banco de Dados:** PostgreSQL
- **ORM:** psycopg2 (raw SQL)
- **Arquivo Principal:** `database.py`
- **Autenticação:** Microsoft Office 365 via MSAL

### Estrutura de Arquivos
```
disparador-email/
├── streamlit_app.py          # Interface principal Streamlit
├── database.py               # Funções de banco de dados
├── config.json               # Configurações de email salvas
├── check_montagem_exists.py  # Verificação de duplicatas
├── templates/
│   ├── invoice_template.html     # Template PDF prestadores
│   ├── montador_template.html    # Template PDF montadores
│   ├── email_template.html       # Template base email
│   └── variaveis.py             # Variáveis disponíveis
└── frontend/                     # Front alternativo (vazio)
    ├── index.html
    ├── assets/css/style.css
    └── assets/js/app.js
```

## 📊 ESTRUTURA DO BANCO DE DADOS

### Tabelas Principais

#### 1. **prestadores**
```sql
- id (SERIAL PRIMARY KEY)
- nome (TEXT NOT NULL UNIQUE)
- email (TEXT NOT NULL)
- emails_adicionais (TEXT)
- fornecedor_id (TEXT UNIQUE)
- regra_envio (TEXT)
- dias_envio (TEXT)
```

#### 2. **montadores**
```sql
- id (SERIAL PRIMARY KEY)
- nome (TEXT NOT NULL)
- identificador (TEXT NOT NULL UNIQUE)
- email (TEXT NOT NULL)
- emails_adicionais (TEXT)
- percentual_comissao (REAL NOT NULL)
- auxilio_semanal (REAL NOT NULL)
- ativo (BOOLEAN DEFAULT TRUE)
- fornecedor_id (TEXT UNIQUE)
- regra_envio (TEXT)
- dias_envio (TEXT)
```

#### 3. **lotes_servico**
```sql
- id (SERIAL PRIMARY KEY)
- prestador_id (INTEGER REFERENCES prestadores(id))
- prestador_nome (TEXT)
- periodo (TEXT NOT NULL)
- valor_total (REAL NOT NULL)
- data_envio (TIMESTAMP NOT NULL)
- status (TEXT DEFAULT 'Em Aberto')
- conversation_id (TEXT)
- anexo_path (TEXT)
```

#### 4. **os_enviadas**
```sql
- id (SERIAL PRIMARY KEY)
- lote_id (INTEGER REFERENCES lotes_servico(id) ON DELETE CASCADE)
- os_numero (TEXT NOT NULL UNIQUE)
- detalhes (JSONB)
```

#### 5. **envios_montagem**
```sql
- id (SERIAL PRIMARY KEY)
- montador_id (INTEGER REFERENCES montadores(id))
- data_envio (TIMESTAMP NOT NULL)
- status (TEXT DEFAULT 'Em Aberto')
- detalhes (JSONB)
- conversation_id (TEXT)
- anexo_path (TEXT)
```

#### 6. **envios_ignorados**
```sql
- id (SERIAL PRIMARY KEY)
- tipo (TEXT NOT NULL)
- entidade_id (INTEGER NOT NULL)
- ano (INTEGER)
- periodo_chave (TEXT)
- data_ignorada (TIMESTAMP)
```

#### 7. **os_blacklist**
```sql
- id (SERIAL PRIMARY KEY)
- prestador_id (INTEGER REFERENCES prestadores(id))
- os_numero (TEXT NOT NULL)
- data_adicao (TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
- motivo (TEXT)
```

#### 8. **boletins_blacklist**
```sql
- id (SERIAL PRIMARY KEY)
- montador_id (INTEGER REFERENCES montadores(id))
- boletim (TEXT NOT NULL)
- data_adicao (TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
- motivo (TEXT)
```

## 🚀 FUNCIONALIDADES PRINCIPAIS

### 1. DASHBOARD DE PENDÊNCIAS
**Localização:** `app_mode == "Dashboard de Pendências"`

**Funcionalidades:**
- ✅ Verificação automática de pendências diárias
- ✅ Lista prestadores com envios pendentes hoje
- ✅ Lista montadores com envios pendentes hoje
- ✅ Botão "Ignorar Envio" para cada pendência
- ✅ Sistema de regras de envio (Semanal, Mensal, Quinzenal)

**Funções utilizadas:**
- `verificar_pendencias(entidades, tipo)`
- `db.get_envios_na_semana()`
- `db.foi_ignorado_na_semana()`
- `db.ignorar_envio_semanal()`

### 2. SERVIÇOS (PRESTADORES)
**Localização:** `app_mode == "Serviços (Prestadores)"`

#### 2.1 Enviar Boletins
**Funcionalidades:**
- ✅ Lançamento manual de boletins
- ✅ Importação via Excel
- ✅ Verificação de O.S. já enviadas
- ✅ Verificação de O.S. na blacklist
- ✅ Geração automática de PDF
- ✅ Envio via Microsoft Graph API
- ✅ Templates configuráveis de email
- ✅ Sistema de variáveis ({{nome_prestador}}, {{periodo}})
- ✅ Múltiplos emails por prestador

**Campos do formulário manual:**
- Prestador (selectbox)
- Período (text_input)
- O.S (text_input)
- Modalidade (text_input)
- Data de Execução (date_input)
- Valor (number_input)
- Valor Extra (number_input)
- Motivo Valor Extra (text_input)

**Campos obrigatórios do Excel:**
- nome_prestador
- periodo
- data_execucao
- o_s

#### 2.2 Gerenciar Prestadores
**Funcionalidades:**
- ✅ Cadastro de novos prestadores
- ✅ Edição de prestadores existentes
- ✅ Configuração de regras de envio
- ✅ Gerenciamento de emails adicionais
- ✅ Sistema de blacklist de O.S.
- ✅ Adição/remoção de O.S. na blacklist

**Campos obrigatórios:**
- Nome
- E-mail Principal
- Número do Fornecedor

**Campos opcionais:**
- E-mails Adicionais
- Regra de Envio
- Dias de Envio

#### 2.3 Histórico de Envios
**Funcionalidades:**
- ✅ Visualização de todos os lotes enviados
- ✅ Filtro por status (Em Aberto, Pago, Cancelado, N.F. RECEBIDA)
- ✅ Detalhes de cada lote
- ✅ Alteração de status
- ✅ Download de anexos
- ✅ Exclusão de lotes

#### 2.4 Editor de PDF (Serviços)
**Funcionalidades:**
- ✅ Edição do template HTML do PDF
- ✅ Preview em tempo real
- ✅ Salvamento automático

### 3. MONTAGEM (MONTADORES)
**Localização:** `app_mode == "Montagem (Montadores)"`

#### 3.1 Enviar Pagamentos
**Funcionalidades:**
- ✅ Lançamento manual de montagens
- ✅ Importação via Excel
- ✅ Verificação de boletins já enviados
- ✅ Verificação de boletins na blacklist
- ✅ Cálculo automático de comissões
- ✅ Cálculo de auxílio semanal
- ✅ Geração de PDF personalizado
- ✅ Templates configuráveis de email
- ✅ Múltiplos emails por montador

**Campos do formulário manual:**
- Montador (selectbox)
- Boletim Montagem (text_input)
- Data da Montagem (date_input)
- Média de Valor Venda (number_input)
- Cliente (text_input)
- Nome do Produto (text_input)

**Campos obrigatórios do Excel:**
- identificador_do_montador
- identificador_boletim_montagem
- data_da_montagem
- media_de_valor_venda
- nome_produto

#### 3.2 Gerenciar Montadores
**Funcionalidades:**
- ✅ Cadastro de novos montadores
- ✅ Edição de montadores existentes
- ✅ Configuração de percentual de comissão
- ✅ Configuração de auxílio semanal
- ✅ Status ativo/inativo
- ✅ Configuração de regras de envio
- ✅ Sistema de blacklist de boletins
- ✅ Histórico completo por montador

**Campos obrigatórios:**
- Nome Completo
- Identificador do Montador
- E-mail Principal
- Número do Fornecedor

#### 3.3 Histórico de Montagens
**Funcionalidades:**
- ✅ Visualização de todos os pagamentos
- ✅ Filtro por status
- ✅ Editor de detalhes inline
- ✅ Alteração de comissões editadas
- ✅ Adição de valores extras
- ✅ Recálculo automático de totais

## 🔧 CONFIGURAÇÕES AVANÇADAS

### Sistema de Templates
**Localização:** `config.json` e `st.session_state`

**Configurações salvas:**
- prestador_cc
- prestador_subject
- prestador_body
- montador_cc
- montador_subject
- montador_body

### Variáveis de Template
**Para Prestadores:**
- {{nome_prestador}}
- {{periodo}}
- {{saudacao}}
- {{lote_id}}

**Para Montadores:**
- {{nome_montador}}
- {{periodo_relatorio}}
- {{percentual_comissao}}
- {{total_geral}}

### Sistema de Regras de Envio
**Tipos disponíveis:**
1. **Nenhuma** - Sem regra automática
2. **Semanal** - Envio em dia específico da semana
3. **Mensal (Dia Fixo)** - Envio em dia(s) específico(s) do mês
4. **Quinzenal** - Envio em dois dias específicos do mês

## 🔐 SISTEMA DE AUTENTICAÇÃO

### Microsoft Office 365 Integration
- **Biblioteca:** MSAL (Microsoft Authentication Library)
- **Scopes:** ["Mail.Send", "Mail.ReadWrite"]
- **Cache:** Arquivo `token_cache.json`
- **Fluxo:** Device Code Flow

### Estados de Login
1. Token válido em cache ✅
2. Device Code Flow ⏳
3. Erro de autenticação ❌

## 📈 FLUXOS DE PROCESSAMENTO

### Fluxo de Envio de Prestadores
1. **Input:** Manual ou Excel
2. **Validação:** Campos obrigatórios
3. **Verificação:** O.S. já enviadas/blacklist
4. **Agrupamento:** Por prestador e período
5. **Geração:** PDF com template
6. **Envio:** Via Microsoft Graph API
7. **Log:** Salvar lote no banco
8. **Conversation ID:** Associar resposta do email

### Fluxo de Envio de Montadores
1. **Input:** Manual ou Excel
2. **Validação:** Campos obrigatórios
3. **Verificação:** Boletins já enviados/blacklist
4. **Cálculos:** Comissão + auxílio semanal
5. **Agrupamento:** Por montador
6. **Geração:** PDF com template
7. **Envio:** Via Microsoft Graph API
8. **Log:** Salvar envio no banco

## 🛡️ SISTEMAS DE PROTEÇÃO

### Blacklist
- **O.S. (Prestadores):** Impede reenvio de O.S. específicas
- **Boletins (Montadores):** Impede reenvio de boletins específicos
- **Motivos:** Campo opcional para justificativa

### Verificação de Duplicatas
- **check_montagem_exists():** Verifica período + montador
- **check_os_list():** Verifica O.S. já enviadas
- **check_boletim_list():** Verifica boletins já enviados

### Sistema de Ignorar Envios
- **Temporário:** Ignora apenas na semana atual
- **Por entidade:** Prestador ou montador específico
- **Dashboard:** Exibe pendências mesmo ignoradas

## 📧 SISTEMA DE EMAILS

### Estrutura do Email
- **Destinatários:** Email principal + emails adicionais
- **CC:** Configurável por tipo (prestador/montador)
- **Templates:** HTML com variáveis
- **Anexos:** PDF gerado dinamicamente

### Templates HTML
- **invoice_template.html:** Relatórios de prestadores
- **montador_template.html:** Relatórios de montadores
- **Responsivos:** Visualização otimizada
- **Editáveis:** Interface para modificação

## 📁 GESTÃO DE STATUS

### Status de Lotes/Envios
1. **Em Aberto** - Enviado mas não pago
2. **Pago** - Pagamento confirmado
3. **Cancelado** - Cancelado por algum motivo
4. **N.F. RECEBIDA** - Nota fiscal recebida

### Anexos
- **Upload:** Sistema para anexar N.F. recebidas
- **Download:** Acesso aos arquivos anexados
- **Storage:** Caminho salvo no banco

## 🔄 INTEGRAÇÕES EXTERNAS

### Microsoft Graph API
- **Endpoint:** https://graph.microsoft.com/v1.0/me/sendMail
- **Autenticação:** Bearer token
- **Anexos:** Base64 encoded
- **Conversation ID:** Tracking de emails

### PostgreSQL
- **Conexão:** Via variáveis de ambiente (.env)
- **Migrations:** Automáticas na inicialização
- **Transações:** Controle de integridade

## 🚨 PONTOS CRÍTICOS PARA MIGRAÇÃO

### Funcionalidades que NÃO PODEM ser perdidas:
1. ✅ Todos os formulários de entrada (manual + Excel)
2. ✅ Sistema completo de configuração de emails
3. ✅ Dashboard de pendências com regras de envio
4. ✅ Blacklists de O.S. e boletins
5. ✅ Sistema de múltiplos emails por pessoa
6. ✅ Editor de templates de PDF
7. ✅ Histórico completo com filtros e edição
8. ✅ Sistema de status e anexos
9. ✅ Autenticação Office 365
10. ✅ Todas as validações e verificações de duplicata

### Estados da Aplicação que devem ser mantidos:
- **st.session_state.manual_entries** - Lista de prestadores manuais
- **st.session_state.manual_montagem_entries** - Lista de montadores manuais  
- **st.session_state.access_token** - Token de autenticação
- **st.session_state.user** - Usuário logado
- **Configurações persistentes em config.json**

### Dados de entrada que devem funcionar:
- **Excel de prestadores** com campos específicos
- **Excel de montadores** com campos específicos
- **Formulários manuais** com todas as validações
- **Upload de arquivos** de anexo

Esta documentação garante que NENHUMA funcionalidade será perdida na migração para Bootstrap!
