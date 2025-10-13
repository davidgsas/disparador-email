# 📚 INTEGRAÇÃO COM API DV PROCESSAMENTO
## Sistema de Upload de Notas Fiscais

**Data:** 13 de outubro de 2025  
**Versão:** 2.0 (Nova Especificação)

---

## 🎯 VISÃO GERAL

O sistema Disparador de E-mails agora está integrado com a **API DV Processamento** para gerenciamento de upload de notas fiscais. Após enviar um lote de serviços por email, o sistema automaticamente:

1. **Envia os dados** do lote para a API externa
2. **Recebe um link** único de upload
3. **Inclui o link** no email para o prestador
4. **Monitora** o status do upload
5. **Baixa** automaticamente a nota fiscal quando recebida

---

## 🔄 FLUXO COMPLETO

```
┌─────────────────────────────────────────────────────────────────┐
│ 1. USUÁRIO ENVIA LOTE VIA STREAMLIT                            │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│ 2. SISTEMA CRIA LOTE NO BANCO LOCAL                            │
│    └─ Tabela: lotes_servico                                    │
│    └─ Campos: prestador, periodo, valor_total, etc.            │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│ 3. ENVIA DADOS PARA API DV PROCESSAMENTO                       │
│    └─ Endpoint: POST https://api.link.dev.br/dvprocessamento/  │
│    └─ Header: X-API-Key                                        │
│    └─ Payload: JSON com dados do lote                          │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│ 4. API RETORNA RESPOSTA COM LINK                               │
│    └─ id_controle: ID único na API                             │
│    └─ link: URL para upload                                    │
│    └─ validade_link: Data de expiração                         │
│    └─ status: 0 (pendente)                                     │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│ 5. SISTEMA SALVA RESPOSTA NO BANCO                             │
│    └─ Atualiza lote com id_controle, link, validade            │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│ 6. ENVIA EMAIL COM PDF + LINK DE UPLOAD                        │
│    └─ Para: Prestador de serviço                               │
│    └─ Anexo: PDF com relatório                                 │
│    └─ Corpo: Inclui link para upload de NF                     │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│ 7. PRESTADOR ACESSA LINK E FAZ UPLOAD                          │
│    └─ Sistema externo (outro desenvolvedor)                    │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│ 8. SISTEMA VERIFICA STATUS (job automático ou manual)          │
│    └─ Status muda para 1 quando NF é recebida                  │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│ 9. ATUALIZA BANCO E INTERFACE                                  │
│    └─ status_api = 1                                           │
│    └─ status = "N.F. RECEBIDA"                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📊 MAPEAMENTO DE CAMPOS

### Do Banco Local → Para API

| Campo no Banco (`lotes_servico`) | Campo JSON Enviado | Tipo | Observação |
|----------------------------------|-------------------|------|------------|
| `prestador_nome` | `nome` | String | Nome completo da empresa/prestador |
| `email` (da tabela prestadores) | `email` | String | E-mail válido do prestador |
| `periodo` | `periodo` | String | Formato MM/YYYY |
| `valor_total` | `valor_total` | Decimal | Soma total das notas |
| (contagem de OS) | `quantidade_os` | Integer | Número total de ordens de serviço |
| `data_envio` | `data_envio` | String | Formato ISO YYYY-MM-DDTHH:MM:SS |
| `id` | `lote_id` | Integer | Identificador único do lote |

### Da API → Para Banco Local

| Campo JSON Recebido | Campo no Banco | Tipo | Descrição |
|---------------------|----------------|------|-----------|
| `id_controle` | `id_controle` | Integer | ID único gerado pela API |
| `link` | `link_upload` | Text | URL completa para upload |
| `validade_link` | `validade_link` | Date | Data de expiração (YYYY-MM-DD) |
| `status` | `status_api` | Integer | 0=pendente, 1=recebido |
| `message` | `api_message` | Text | Mensagem de confirmação |

---

## 🔧 ESTRUTURA DO BANCO DE DADOS

### Tabela: `lotes_servico`

**Novas Colunas Adicionadas:**

```sql
ALTER TABLE lotes_servico ADD COLUMN IF NOT EXISTS id_controle INTEGER;
ALTER TABLE lotes_servico ADD COLUMN IF NOT EXISTS link_upload TEXT;
ALTER TABLE lotes_servico ADD COLUMN IF NOT EXISTS validade_link DATE;
ALTER TABLE lotes_servico ADD COLUMN IF NOT EXISTS status_api INTEGER DEFAULT 0;
ALTER TABLE lotes_servico ADD COLUMN IF NOT EXISTS data_envio_api TIMESTAMP;
ALTER TABLE lotes_servico ADD COLUMN IF NOT EXISTS nota_fiscal_path TEXT;
ALTER TABLE lotes_servico ADD COLUMN IF NOT EXISTS api_message TEXT;
```

**Campos Existentes (mantidos):**
- `id` (PK)
- `prestador_id` (FK → prestadores)
- `prestador_nome`
- `periodo`
- `valor_total`
- `data_envio`
- `status`
- `conversation_id`
- `anexo_path`

---

## 📡 API DV PROCESSAMENTO

### Endpoint

```
POST https://api.link.dev.br/dvprocessamento/
```

### Autenticação

```
X-API-Key: DV_API_2025_CTRL_NOTAS_f8e9d2c1b4a6
```

### Headers

```http
Content-Type: application/json; charset=utf-8
X-API-Key: DV_API_2025_CTRL_NOTAS_f8e9d2c1b4a6
```

### Payload de Exemplo

```json
{
  "nome": "ACME Instalações Ltda",
  "email": "contato@acmeinstalacoes.com.br",
  "periodo": "10/2025",
  "valor_total": 15750.50,
  "quantidade_os": 23,
  "data_envio": "2025-10-13T14:30:00",
  "lote_id": 142
}
```

### Resposta de Sucesso (HTTP 200)

```json
{
  "success": true,
  "id_controle": 1,
  "lote_id": 142,
  "link": "https://api.link.com.br/dvprocessamento/envio-nf/7bd6a6b681b9f59cdc04e5d5fc3c237c",
  "validade_link": "2025-11-12",
  "status": 0,
  "message": "Registro criado com sucesso"
}
```

### Resposta de Erro (HTTP 4xx/5xx)

```json
{
  "success": false,
  "message": "Descrição do erro"
}
```

### Códigos de Status HTTP

- **200**: Sucesso
- **409**: Conflito (lote duplicado)
- **400**: Dados inválidos
- **401**: Não autorizado (API Key inválida)
- **500**: Erro interno do servidor

---

## 💻 ARQUIVOS DO SISTEMA

### 1. `database.py`

**Novas Funções Adicionadas:**

```python
# Salvar resposta da API
salvar_resposta_api(lote_id, id_controle, link, validade_link, status_api, message)

# Buscar lotes pendentes de envio
get_lotes_para_enviar_api()

# Atualizar status após NF recebida
atualizar_status_api(lote_id, status_api)

# Buscar lotes com link ativo
get_lotes_com_link_pendente()

# Buscar por ID de controle
get_lote_by_id_controle(id_controle)

# Verificar duplicidade
verificar_lote_duplicado(lote_id, periodo)
```

### 2. `api_upload_client.py` (NOVO)

Cliente Python para comunicação com a API.

**Classe Principal:** `APIUploadClient`

**Métodos:**
- `preparar_payload(lote)` - Monta JSON do payload
- `enviar_lote(lote)` - Envia POST para API
- `processar_resposta(resposta)` - Extrai campos da resposta
- `enviar_e_salvar(lote_id)` - Fluxo completo (envia + salva)

**Funções Auxiliares:**
- `enviar_lote_para_api(lote_id)` - Wrapper simples
- `enviar_lotes_pendentes()` - Processa todos pendentes

### 3. `job_enviar_api.py` (NOVO)

Job automático para enviar lotes pendentes.

**Funcionalidades:**
- Busca lotes sem `id_controle`
- Envia para API DV Processamento
- Registra logs em `logs/job_enviar_api.log`
- Retorna estatísticas de execução

**Uso:**
```bash
python job_enviar_api.py
```

**Cron (executar a cada hora):**
```cron
0 * * * * cd /path/projeto && python job_enviar_api.py >> logs/cron_api.log 2>&1
```

### 4. `streamlit_app.py`

**Modificações:**

#### A) Envio de Lotes (linha ~324)
```python
# Após criar lote, envia para API automaticamente
lote_id = db.criar_lote_servico(...)

from api_upload_client import enviar_lote_para_api
sucesso, mensagem, dados = enviar_lote_para_api(lote_id)

if sucesso:
    link_upload = dados.get('link')
    # Disponível para incluir no template de email
```

#### B) Histórico de Envios (linha ~496)
- Mostra ID de controle da API
- Exibe link de upload
- Mostra validade com contagem regressiva
- Indica se link expirou
- Botão para reenviar/gerar novo link
- Botão para enviar manualmente (se não foi enviado)

---

## 🎨 INTERFACE STREAMLIT

### Histórico de Envios

Para cada lote, exibe:

```
┌─────────────────────────────────────────────────────┐
│ 📤 Status do Upload da Nota Fiscal                 │
├─────────────────────────────────────────────────────┤
│                                                     │
│ 📤  Link enviado ao prestador                      │
│     ID Controle API: 142                           │
│     ✅ Válido até: 12/11/2025 (30 dias)            │
│                                                     │
│     🔗 Ver Link de Upload                          │
│     [Expandir para ver link completo]              │
│                                                     │
│     💬 Registro criado com sucesso                 │
│                                                     │
│     [🔄 Reenviar para API (Gerar Novo Link)]      │
│                                                     │
└─────────────────────────────────────────────────────┘
```

**Estados Visuais:**

| Emoji | Status | Descrição |
|-------|--------|-----------|
| 📤 | Pendente | Link enviado, aguardando NF |
| ✅ | Recebido | NF foi anexada pelo prestador |
| ⏰ | Expirado | Link passou da validade |
| 📧 | Sem Link | Ainda não foi enviado para API |

**Avisos de Validade:**
- ⏰ **Expirado** - Link passou da data
- ⚠️ **Hoje** - Link expira no dia atual
- ⚠️ **3 dias ou menos** - Alerta de vencimento próximo
- ✅ **Mais de 3 dias** - Válido normalmente

---

## 🔄 FLUXOS DE USO

### Fluxo 1: Envio Automático (Ideal)

1. Usuário preenche planilha no Streamlit
2. Clica em "Enviar E-mails"
3. Sistema cria lote no banco
4. **Automático**: Envia para API DV Processamento
5. **Automático**: Recebe link
6. **Automático**: Salva no banco
7. Envia email com PDF + link
8. Prestador recebe email e faz upload

### Fluxo 2: Envio Manual (Alternativa)

1. Lote foi criado mas API não respondeu
2. Usuário acessa "Histórico de Envios"
3. Clica em "🚀 Enviar para API Agora"
4. Sistema tenta enviar novamente
5. Se sucesso, link é gerado e salvo

### Fluxo 3: Reenvio (Link Expirado)

1. Link expirou (passou da validade)
2. Prestador não consegue mais fazer upload
3. Usuário acessa histórico
4. Clica em "🔄 Reenviar para API (Gerar Novo Link)"
5. Sistema limpa `id_controle` e reenvia
6. Nova link é gerado
7. Usuário pode reenviar email com novo link

---

## 🛡️ TRATAMENTO DE ERROS

### Erro 1: API Indisponível

**Sintoma:** Timeout ou erro de conexão

**Tratamento:**
```python
try:
    sucesso, mensagem, dados = enviar_lote_para_api(lote_id)
except requests.exceptions.Timeout:
    # API não respondeu em 30s
    st.warning("API não respondeu. Tente novamente mais tarde.")
except requests.exceptions.ConnectionError:
    # Sem conexão
    st.error("Erro de conexão com API.")
```

**Solução:**
- Job automático tentará novamente na próxima execução
- Usuário pode tentar manualmente no histórico

### Erro 2: Lote Duplicado (HTTP 409)

**Sintoma:** API retorna conflito

**Tratamento:**
```python
if resposta.status_code == 409:
    return False, None, "Lote já foi enviado anteriormente (duplicado)"
```

**Solução:**
- Sistema verifica `id_controle` antes de enviar
- Evita reenvios acidentais
- Para reenviar propositalmente, limpar `id_controle`

### Erro 3: Autenticação Inválida (HTTP 401)

**Sintoma:** API Key rejeitada

**Tratamento:**
- Sistema registra erro no log
- Notifica usuário

**Solução:**
- Verificar API Key em `api_upload_client.py`
- Confirmar com desenvolvedor externo

### Erro 4: Dados Inválidos (HTTP 400)

**Sintoma:** Payload rejeitado

**Causas Comuns:**
- Email inválido
- Período em formato errado
- Campos obrigatórios faltando

**Tratamento:**
- Sistema valida antes de enviar
- Log detalha qual campo está errado

**Solução:**
- Corrigir dados do prestador/lote
- Tentar envio novamente

---

## 📝 LOGS E MONITORAMENTO

### Arquivo de Log

```
logs/job_enviar_api.log
```

### Formato

```
2025-10-13 14:30:00 - INFO - ======================================================================
2025-10-13 14:30:00 - INFO - 🚀 Iniciando job de envio para API DV Processamento
2025-10-13 14:30:00 - INFO - ======================================================================
2025-10-13 14:30:05 - INFO - 📊 Processamento concluído:
2025-10-13 14:30:05 - INFO -    📦 Total de lotes: 3
2025-10-13 14:30:05 - INFO -    ✅ Enviados com sucesso: 3
2025-10-13 14:30:05 - INFO -    ❌ Erros: 0
2025-10-13 14:30:05 - INFO - 
2025-10-13 14:30:05 - INFO - 📝 Detalhes dos envios:
2025-10-13 14:30:05 - INFO -    ✅ Lote #142: Registro criado com sucesso
2025-10-13 14:30:05 - INFO -       🔗 Link gerado: https://api.link.com.br/dvprocessamento/envio-nf/7bd6a6b...
```

### Monitoramento

**Verificar status:**
```bash
tail -f logs/job_enviar_api.log
```

**Contar erros:**
```bash
grep "❌" logs/job_enviar_api.log | wc -l
```

**Últimos 20 envios:**
```bash
grep "Lote #" logs/job_enviar_api.log | tail -20
```

---

## 🚀 CONFIGURAÇÃO E DEPLOY

### 1. Pré-requisitos

```bash
# Instalar dependências
pip install requests python-dotenv psycopg2

# Criar diretório de logs
mkdir -p logs

# Criar diretório de uploads
mkdir -p uploads
```

### 2. Variáveis de Ambiente (.env)

```env
# Banco de Dados
DB_HOST=localhost
DB_NAME=email
DB_USER=seu_usuario
DB_PASS=sua_senha
DB_PORT=5432

# Microsoft Graph (Email)
CLIENT_ID=...
TENANT_ID=...
CLIENT_SECRET=...

# API DV Processamento (hardcoded no código por enquanto)
# Se precisar customizar, adicionar aqui e ler no api_upload_client.py
```

### 3. Rodar Migrações

```bash
python -c "import database; database.run_migrations()"
```

Isso criará as novas colunas na tabela `lotes_servico`.

### 4. Testar Cliente API

```bash
python api_upload_client.py
```

Deve buscar e enviar lotes pendentes.

### 5. Configurar Cron Job

```bash
crontab -e
```

Adicionar:
```cron
# Enviar lotes para API a cada hora
0 * * * * cd /Users/davidgabriel/projetos/disparador-email && /Users/davidgabriel/projetos/disparador-email/.venv/bin/python job_enviar_api.py >> logs/cron_api.log 2>&1
```

### 6. Iniciar Streamlit

```bash
streamlit run streamlit_app.py
```

---

## 🧪 TESTES

### Teste 1: Envio Manual de Lote

1. Acessar Streamlit
2. Ir em "Enviar Boletins"
3. Preencher planilha com um prestador
4. Enviar
5. Verificar no histórico se link foi gerado

**Resultado Esperado:**
- ✅ Email enviado
- ✅ Link gerado pela API
- ✅ ID de controle salvo no banco
- ✅ Validade exibida corretamente

### Teste 2: Job Automático

1. Criar lote no banco sem `id_controle`
2. Rodar: `python job_enviar_api.py`
3. Verificar log

**Resultado Esperado:**
- ✅ Lote identificado como pendente
- ✅ Enviado para API
- ✅ Resposta salva no banco
- ✅ Log registrado

### Teste 3: Reenvio de Link Expirado

1. Encontrar lote com link expirado
2. Clicar em "Reenviar para API"
3. Verificar novo link gerado

**Resultado Esperado:**
- ✅ `id_controle` limpo
- ✅ Novo envio realizado
- ✅ Novo link salvo
- ✅ Nova validade registrada

### Teste 4: Link Duplicado

1. Tentar enviar mesmo lote duas vezes
2. Sistema deve bloquear

**Resultado Esperado:**
- ❌ Erro: "Lote já foi enviado anteriormente"
- ✅ Banco não foi duplicado

---

## ❓ FAQ

### P: O que acontece se a API não responder?

**R:** O sistema registra o erro mas não bloqueia o envio do email. O job automático tentará novamente na próxima execução (a cada hora). O usuário também pode tentar manualmente no histórico.

### P: Posso alterar o link depois de enviado?

**R:** Não é possível editar um link existente, mas você pode gerar um **novo link** usando o botão "Reenviar para API". Isso cria um novo registro na API externa.

### P: Como sei se o prestador fez o upload?

**R:** O campo `status_api` mudará de 0 para 1 quando o prestador anexar a nota fiscal. Na interface, o emoji muda de 📤 para ✅.

### P: O link expira automaticamente?

**R:** Sim, a API define uma data de validade (campo `validade_link`). Após essa data, o prestador não consegue mais fazer upload. Você pode gerar um novo link se necessário.

### P: Preciso rodar o job manualmente?

**R:** Não. Se configurou o cron corretamente, o job roda automaticamente a cada hora. Mas você pode rodá-lo manualmente com `python job_enviar_api.py` se quiser forçar um envio imediato.

### P: Como incluir o link no email?

**R:** O link está disponível na variável `link_upload` do contexto do template. No template do email, use:

```jinja2
Para anexar a Nota Fiscal, acesse:
{{ link_upload }}
```

### P: E se o desenvolvedor externo mudar a API?

**R:** Você precisará atualizar:
- URL em `api_upload_client.py` (variável `API_URL`)
- API Key em `api_upload_client.py` (variável `API_KEY`)
- Mapeamento de campos se mudarem

---

## 📞 SUPORTE

### Contato

- **Desenvolvedor do Disparador:** (você)
- **Desenvolvedor da API Externa:** (outro dev)

### Documentação Adicional

- `DOCUMENTACAO_SISTEMA.md` - Documentação geral do sistema
- `PLANEJAMENTO_BOOTSTRAP.md` - Planejamento de melhorias
- `MIGRACAO_CONCLUIDA.md` - Histórico de migrações

### Logs de Erro

Se encontrar problemas, envie:
1. Arquivo `logs/job_enviar_api.log`
2. Screenshot do erro na interface
3. ID do lote com problema

---

## 📌 CHECKLIST DE IMPLEMENTAÇÃO

- [x] Criar colunas no banco de dados
- [x] Implementar funções em `database.py`
- [x] Criar cliente da API (`api_upload_client.py`)
- [x] Criar job automático (`job_enviar_api.py`)
- [x] Integrar com envio de emails
- [x] Atualizar interface Streamlit
- [x] Criar documentação completa
- [ ] **Testar com API real** (aguardando desenvolvedor externo)
- [ ] Configurar cron job em produção
- [ ] Adicionar link no template de email
- [ ] Treinar usuários

---

## 🎉 CONCLUSÃO

O sistema agora está **totalmente integrado** com a API DV Processamento. O fluxo é automático, mas oferece controles manuais quando necessário. A interface é intuitiva e mostra claramente o status de cada lote.

**Próximo Passo:** Aguardar desenvolvedor externo disponibilizar API em produção e testar com dados reais.

---

**Documento criado em:** 13 de outubro de 2025  
**Última atualização:** 13 de outubro de 2025  
**Versão:** 2.0
