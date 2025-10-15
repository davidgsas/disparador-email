# 📋 ÍNDICE - INTEGRAÇÃO TRELLO

## 📚 Documentação

| Arquivo | Descrição | Quando Usar |
|---------|-----------|-------------|
| **[QUICKSTART_TRELLO.md](QUICKSTART_TRELLO.md)** | Guia rápido de configuração (5 min) | ⭐ Comece aqui! |
| **[INTEGRACAO_TRELLO.md](INTEGRACAO_TRELLO.md)** | Documentação completa e detalhada | Referência completa |
| **[RESUMO_INTEGRACAO_TRELLO.md](RESUMO_INTEGRACAO_TRELLO.md)** | Resumo executivo da implementação | Visão geral |
| **[DIAGRAMA_TRELLO.txt](DIAGRAMA_TRELLO.txt)** | Fluxo visual do sistema | Entender o fluxo |
| **[COMANDOS_TRELLO.md](COMANDOS_TRELLO.md)** | Comandos úteis de linha de comando | Debug e admin |

## 🛠️ Scripts

| Script | Função | Comando |
|--------|--------|---------|
| **setup_integracoes.py** | Cria tabelas no banco | `.venv/bin/python3 setup_integracoes.py` |
| **testar_trello.py** | Teste completo da integração | `.venv/bin/python3 testar_trello.py` |
| **exemplos_trello.py** | Exemplos interativos de uso | `.venv/bin/python3 exemplos_trello.py` |

## 📦 Módulos

| Módulo | Descrição | Local |
|--------|-----------|-------|
| **TrelloIntegration** | Classe principal da integração | `integracoes/trello_integration.py` |
| **Painel Integrações** | Interface de configuração | `painel_integracoes.py` |

## 🎯 Fluxo Rápido

### 1️⃣ Instalação
```bash
cd /Users/davidgabriel/projetos/disparador-email
.venv/bin/python3 setup_integracoes.py
```

### 2️⃣ Configuração
1. Obter credenciais: https://trello.com/power-ups/admin
2. Streamlit → "🔌 Integrações"
3. Configurar API Key, Token, Board ID, List ID
4. Ativar e salvar

### 3️⃣ Teste
```bash
.venv/bin/python3 testar_trello.py
```

### 4️⃣ Uso Automático
Aguarde que prestadores anexem arquivos → Cards criados automaticamente! 🎉

## 🔗 Links Úteis

- **Trello Power-Ups:** https://trello.com/power-ups/admin
- **API Trello Docs:** https://developer.atlassian.com/cloud/trello/rest/
- **Streamlit:** Menu lateral → "🔌 Integrações"

## 📊 Estrutura

```
integracoes/
├── __init__.py
└── trello_integration.py ← Lógica principal

Raiz:
├── painel_integracoes.py ← Interface Streamlit
├── job_consultar_notas.py ← Cria cards automaticamente
├── setup_integracoes.py ← Setup inicial
├── testar_trello.py ← Testes
├── exemplos_trello.py ← Exemplos
└── INTEGRACAO_TRELLO.md ← Documentação
```

## 🗄️ Banco de Dados

```sql
-- Configurações
integracoes_config (id, trello_api_key, trello_token, ...)

-- Histórico
trello_cards (id, lote_id, card_id, card_url, data_criacao)
```

## ✨ Funcionalidades

- ✅ Criação automática de cards
- ✅ Checklist com arquivos baixados
- ✅ Labels coloridas
- ✅ Descrição completa do lote
- ✅ Prevenção de duplicatas
- ✅ Histórico de cards
- ✅ Testes de conexão
- ✅ Listagem de boards/listas
- ✅ Interface de configuração

## 🎓 Tutoriais

### Para Usuários
→ [QUICKSTART_TRELLO.md](QUICKSTART_TRELLO.md)

### Para Desenvolvedores
→ [INTEGRACAO_TRELLO.md](INTEGRACAO_TRELLO.md)  
→ [exemplos_trello.py](exemplos_trello.py)

### Para Administradores
→ [COMANDOS_TRELLO.md](COMANDOS_TRELLO.md)

## 🚨 Troubleshooting

| Problema | Solução | Documentação |
|----------|---------|--------------|
| "Não configurado" | Configure credenciais no painel | [QUICKSTART](QUICKSTART_TRELLO.md) |
| "Erro ao listar boards" | Verifique API Key e Token | [INTEGRACAO](INTEGRACAO_TRELLO.md#troubleshooting) |
| Cards duplicados | Impossível (constraint único) | [RESUMO](RESUMO_INTEGRACAO_TRELLO.md#prevenção-de-duplicatas) |
| Ver logs | `tail -f scheduler.log \| grep Trello` | [COMANDOS](COMANDOS_TRELLO.md#logs) |

## 📞 Suporte

**Antes de pedir ajuda, consulte:**
1. [QUICKSTART_TRELLO.md](QUICKSTART_TRELLO.md) - Configuração básica
2. [INTEGRACAO_TRELLO.md](INTEGRACAO_TRELLO.md) - Troubleshooting detalhado
3. [COMANDOS_TRELLO.md](COMANDOS_TRELLO.md) - Debug avançado

**Executar testes:**
```bash
.venv/bin/python3 testar_trello.py
```

**Ver exemplos:**
```bash
.venv/bin/python3 exemplos_trello.py
```

## 🎉 Começar Agora

**Caminho mais rápido:**
1. Leia: [QUICKSTART_TRELLO.md](QUICKSTART_TRELLO.md) (5 min)
2. Execute: `.venv/bin/python3 setup_integracoes.py`
3. Configure: Streamlit → "🔌 Integrações"
4. Teste: `.venv/bin/python3 testar_trello.py`
5. ✅ Pronto! Sistema funcionando automaticamente

---

**Dúvidas?** Consulte a documentação acima ou execute os scripts de teste.
