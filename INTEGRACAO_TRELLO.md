# 🔌 Integração com Trello

Sistema de criação automática de cards no Trello quando prestadores anexam arquivos de notas fiscais.

## 📋 Índice

- [Visão Geral](#visão-geral)
- [Como Funciona](#como-funciona)
- [Configuração](#configuração)
- [Estrutura dos Cards](#estrutura-dos-cards)
- [Arquivos Criados](#arquivos-criados)
- [Banco de Dados](#banco-de-dados)

---

## 🎯 Visão Geral

A integração com Trello automatiza a criação de cards sempre que:
1. Um prestador anexa arquivos de nota fiscal no sistema
2. O job automático detecta e baixa os arquivos
3. Um card é criado no Trello com todas as informações do lote

**Benefícios:**
- ✅ Rastreamento automático de notas fiscais recebidas
- ✅ Centralização de informações no Trello
- ✅ Checklist automática dos arquivos baixados
- ✅ Labels coloridas para organização
- ✅ Histórico completo de cards criados

---

## ⚙️ Como Funciona

### Fluxo Automático

```
1. Prestador anexa arquivos no link de upload
         ↓
2. Job automático (consulta_notas) consulta a API
         ↓
3. Arquivos são baixados para uploads/lote_XX/
         ↓
4. Sistema verifica se Trello está configurado
         ↓
5. Card é criado automaticamente com:
   - Título: "📦 Lote #X - Nome do Prestador"
   - Descrição: Informações completas do lote
   - Checklist: Lista de arquivos baixados
   - Label: Verde (sucesso)
         ↓
6. Link do card é salvo no banco de dados
         ↓
7. Histórico fica disponível no painel
```

### Quando NÃO criar card

- ⚠️ Integração desativada no painel
- ⚠️ Credenciais não configuradas
- ⚠️ Arquivos já foram baixados anteriormente (evita duplicação)
- ⚠️ Erro na API do Trello (não interrompe o fluxo principal)

---

## 🔧 Configuração

### Passo 1: Obter Credenciais do Trello

1. **Criar Power-Up:**
   - Acesse: https://trello.com/power-ups/admin
   - Clique em **"New"** para criar uma nova Power-Up
   - Dê um nome (ex: "Disparador de Emails")
   - Copie a **API Key** gerada

2. **Gerar Token:**
   - Na mesma página, clique em **"Token"** ou **"Generate a Token"**
   - Autorize o aplicativo
   - Copie o **Token** gerado (válido por 30 dias ou indefinidamente)

### Passo 2: Configurar no Sistema

1. Abra o sistema Streamlit
2. Vá em **"🔌 Integrações"** no menu lateral
3. Na aba **"📋 Trello"**, cole:
   - **API Key**: A chave copiada
   - **Token**: O token gerado

### Passo 3: Obter IDs do Board e Lista

1. No painel, clique em **"🔍 Listar Boards"**
2. Encontre o board desejado e copie o **Board ID**
3. Cole o Board ID no campo
4. Clique em **"📋 Listar Listas"**
5. Encontre a lista desejada (ex: "To Do", "Pendentes") e copie o **List ID**
6. Cole o List ID no campo

### Passo 4: Ativar Integração

1. Marque a checkbox **"Ativar integração com Trello"**
2. Clique em **"💾 Salvar"**

### Passo 5: Testar

1. Clique em **"✨ Criar Card Teste"**
2. Verifique se o card foi criado no seu board
3. Se funcionar, a integração está pronta! 🎉

---

## 📦 Estrutura dos Cards

### Título
```
📦 Lote #123 - Nome do Prestador
```

### Descrição
```markdown
## 📋 Informações do Lote

**Lote:** #123
**Prestador:** João Silva Serviços
**Montador:** Maria Santos
**Data/Hora:** 14/10/2025 às 14:30
**Nota Fiscal:** NF-12345

## 📎 Arquivos Baixados (3)

1. `nota_fiscal_12345.pdf`
2. `danfe_12345.xml`
3. `recibo_pagamento.pdf`

---
*Card criado automaticamente pelo Sistema de Disparador de Emails*
```

### Checklist
```
☐ nota_fiscal_12345.pdf
☐ danfe_12345.xml
☐ recibo_pagamento.pdf
```

### Label
- 🟢 **Verde**: Arquivos baixados com sucesso

---

## 📁 Arquivos Criados

### 1. `integracoes/trello_integration.py` (352 linhas)
**Classe principal da integração**

```python
class TrelloIntegration:
    """Cliente para integração com a API do Trello"""
    
    def criar_card_download(lote_id, prestador_nome, montador_nome, 
                           arquivos_baixados, nota_fiscal)
    def listar_boards()
    def listar_listas(board_id)
    def is_configured()
```

**Principais métodos:**
- `criar_card_download()`: Cria card com informações do lote
- `_montar_descricao()`: Formata a descrição do card
- `_adicionar_label()`: Adiciona label colorida
- `_criar_checklist()`: Cria checklist dos arquivos
- `_salvar_card_criado()`: Registra no banco
- `listar_boards()`: Lista boards do usuário (configuração)
- `listar_listas()`: Lista listas de um board (configuração)

### 2. `integracoes/__init__.py`
**Módulo de integrações**
```python
from .trello_integration import TrelloIntegration
```

### 3. `painel_integracoes.py` (350 linhas)
**Interface Streamlit para configuração**

**Funcionalidades:**
- ✅ Formulário de configuração de credenciais
- ✅ Teste de conexão com Trello
- ✅ Listagem de boards disponíveis
- ✅ Listagem de listas de um board
- ✅ Criação de card de teste
- ✅ Histórico dos últimos 20 cards criados
- ✅ Tab para futuras integrações (Slack, Teams, etc)

### 4. `setup_integracoes.py` (99 linhas)
**Script de criação das tabelas**

```bash
python setup_integracoes.py
```

### 5. `job_consultar_notas.py` (modificado)
**Adicionada integração automática**

```python
# Linha 11: Import adicionado
from integracoes.trello_integration import TrelloIntegration

# Linhas 145-183: Lógica de criação de card
try:
    trello = TrelloIntegration()
    if trello.is_configured():
        card_result = trello.criar_card_download(...)
        if card_result:
            print(f"✅ Card Trello criado: {card_result['shortUrl']}")
except Exception as e:
    print(f"⚠️ Erro ao criar card Trello: {e}")
    # Não interrompe o fluxo
```

### 6. `streamlit_app.py` (modificado)
**Menu de integrações adicionado**

```python
# Linha 156: Nova opção no menu
app_mode = st.sidebar.selectbox("Selecione a Página", [
    ...
    "🔌 Integrações",
    ...
])

# Linhas 1783-1785: Rota para o painel
elif app_mode == "🔌 Integrações":
    from painel_integracoes import mostrar_painel_integracoes
    mostrar_painel_integracoes()
```

---

## 🗄️ Banco de Dados

### Tabela: `integracoes_config`
Armazena configurações de todas as integrações.

```sql
CREATE TABLE integracoes_config (
    id INTEGER PRIMARY KEY DEFAULT 1,
    
    -- Trello
    trello_api_key TEXT,
    trello_token TEXT,
    trello_board_id TEXT,
    trello_list_id TEXT,
    trello_ativo BOOLEAN DEFAULT FALSE,
    
    -- Futuras integrações
    -- slack_webhook TEXT,
    -- teams_webhook TEXT,
    
    data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT single_row CHECK (id = 1)
);
```

**Características:**
- ✅ Apenas 1 registro (id = 1)
- ✅ Permite múltiplas integrações no futuro
- ✅ Credenciais são sensíveis (armazenadas com segurança)

### Tabela: `trello_cards`
Rastreia todos os cards criados no Trello.

```sql
CREATE TABLE trello_cards (
    id SERIAL PRIMARY KEY,
    lote_id INTEGER NOT NULL,
    card_id TEXT NOT NULL,
    card_url TEXT NOT NULL,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT unique_lote_card UNIQUE(lote_id)
);

CREATE INDEX idx_trello_cards_lote ON trello_cards(lote_id);
```

**Características:**
- ✅ Um card por lote (unique constraint)
- ✅ Índice para busca rápida por lote
- ✅ Armazena URL curta do card (ex: https://trello.com/c/abc123)
- ✅ Histórico completo de criações

**Consultas úteis:**

```sql
-- Cards criados hoje
SELECT * FROM trello_cards 
WHERE DATE(data_criacao) = CURRENT_DATE;

-- Verificar se lote já tem card
SELECT card_url FROM trello_cards WHERE lote_id = 123;

-- Últimos 20 cards
SELECT * FROM trello_cards 
ORDER BY data_criacao DESC 
LIMIT 20;
```

---

## 🔒 Segurança

### Credenciais
- 🔐 API Key e Token são armazenados no banco de dados
- 🔐 Campos exibidos como `type="password"` no Streamlit
- 🔐 Não são exibidos nos logs do sistema

### API do Trello
- ✅ Usa HTTPS para todas as requisições
- ✅ Token pode ser revogado a qualquer momento
- ✅ Permissões limitadas ao board configurado

### Tratamento de Erros
- ⚠️ Erros na API do Trello não interrompem o job principal
- ⚠️ Logs informativos para debug
- ⚠️ Validação de configuração antes de cada operação

---

## 🎨 Customizações Futuras

### Labels Personalizadas
Atualmente usa label verde. Para customizar:

```python
# Em trello_integration.py, linha ~165
self._adicionar_label(card_id, 'green')  # Alterar cor: red, yellow, blue, etc
```

### Campos Customizados
Adicionar custom fields ao card:

```python
def _adicionar_custom_fields(self, card_id, campos):
    url = f"{self.base_url}/cards/{card_id}/customFieldItems"
    # Implementar lógica
```

### Webhooks do Trello
Receber notificações quando cards são atualizados:

```python
def criar_webhook(self, callback_url):
    url = f"{self.base_url}/webhooks"
    # Implementar lógica
```

---

## 📊 Monitoramento

### Verificar Status
```bash
# Ver logs do job
tail -f scheduler.log | grep "Trello"
```

### Métricas
- Total de cards criados: Consultar `trello_cards`
- Taxa de sucesso: Verificar logs
- Última criação: Dashboard do sistema

### Painel de Histórico
- Acessível em: **🔌 Integrações > Histórico de Cards Criados**
- Mostra últimos 20 cards
- Link direto para cada card no Trello

---

## 🆘 Troubleshooting

### Problema: "Integração Trello não configurada"
**Solução:**
1. Acesse **🔌 Integrações**
2. Preencha todos os campos obrigatórios
3. Ative a checkbox "Ativar integração"
4. Clique em "💾 Salvar"

### Problema: "Erro ao listar boards"
**Causas possíveis:**
- ❌ API Key ou Token inválidos
- ❌ Token expirado
- ❌ Sem conexão com internet

**Solução:**
- Regere o token no Trello
- Verifique as credenciais

### Problema: "Erro ao criar card"
**Causas possíveis:**
- ❌ Board ID ou List ID incorretos
- ❌ Permissões insuficientes
- ❌ Lista arquivada ou board deletado

**Solução:**
- Use "🔍 Listar Boards" e "📋 Listar Listas" para obter IDs corretos
- Verifique se a lista está ativa no Trello

### Problema: Cards duplicados
**Prevenção implementada:**
- ✅ Constraint UNIQUE na tabela `trello_cards(lote_id)`
- ✅ Verificação de `status_arquivo` no job
- ✅ Um card por lote garantido

---

## 🚀 Próximas Integrações

### Planejadas
- 📱 **Slack**: Notificações em canais
- 💬 **Microsoft Teams**: Mensagens em channels
- 🎮 **Discord**: Webhooks para servidores
- 📧 **Telegram**: Bot para notificações
- 🔔 **Webhook Genérico**: POST HTTP customizado

### Como Adicionar
1. Criar arquivo em `integracoes/nova_integracao.py`
2. Adicionar campos em `integracoes_config`
3. Criar seção no `painel_integracoes.py`
4. Integrar no job correspondente

---

## 📝 Changelog

### v1.0.0 (14/10/2025)
- ✅ Integração inicial com Trello
- ✅ Criação automática de cards
- ✅ Painel de configuração
- ✅ Histórico de cards
- ✅ Testes de conexão
- ✅ Documentação completa

---

## 📞 Suporte

Em caso de dúvidas:
1. Consulte esta documentação
2. Verifique os logs do sistema
3. Teste a conexão no painel de integrações
4. Revise as configurações de credenciais

---

**Sistema de Disparador de Emails - Integração Trello v1.0**
