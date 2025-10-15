# 🚀 Quick Start - Integração Trello

## ⚡ Configuração Rápida (5 minutos)

### 1. Obter Credenciais do Trello

**API Key:**
```
1. Acesse: https://trello.com/power-ups/admin
2. Clique em "New"
3. Copie a API Key
```

**Token:**
```
1. Na mesma página, clique em "Token"
2. Autorize o app
3. Copie o Token
```

### 2. Configurar no Sistema

```
1. Abra o Streamlit
2. Menu lateral → "🔌 Integrações"
3. Cole API Key e Token
4. Clique em "🔍 Listar Boards" → copie Board ID
5. Clique em "📋 Listar Listas" → copie List ID
6. Marque "Ativar integração"
7. Clique em "💾 Salvar"
8. Clique em "✨ Criar Card Teste" para validar
```

### 3. Pronto!

Agora, toda vez que um prestador anexar arquivos e o job automático baixar, um card será criado automaticamente no Trello! 🎉

---

## 📦 O que é criado automaticamente

Quando arquivos são baixados, o sistema cria:

```
📋 Card no Trello com:
├── 📝 Título: "📦 Lote #X - Nome do Prestador"
├── 📄 Descrição: Todas as informações do lote
├── ✅ Checklist: Lista de todos os arquivos baixados
├── 🏷️  Label: Verde (sucesso)
└── 🔗 Link: Salvo no banco de dados
```

---

## 🧪 Testar a Integração

```bash
cd /Users/davidgabriel/projetos/disparador-email
.venv/bin/python3 testar_trello.py
```

Este script:
- ✅ Verifica tabelas
- ✅ Testa conexão com Trello
- ✅ Lista seus boards e listas
- ✅ Oferece criar card de teste

---

## 📊 Ver Histórico de Cards

```
1. Streamlit → "🔌 Integrações"
2. Role até o final da página
3. Veja "📊 Histórico de Cards Criados"
4. Clique em "🔗 Abrir" para ver o card no Trello
```

---

## 🔧 Arquivos Importantes

| Arquivo | Função |
|---------|--------|
| `integracoes/trello_integration.py` | Lógica da integração |
| `painel_integracoes.py` | Interface de configuração |
| `job_consultar_notas.py` | Job que cria cards |
| `INTEGRACAO_TRELLO.md` | Documentação completa |
| `testar_trello.py` | Script de teste |

---

## ⚠️ Troubleshooting Rápido

**Erro: "Integração não configurada"**
→ Configure todos os campos e ative no painel

**Erro: "Não foi possível listar boards"**
→ Verifique API Key e Token

**Erro: "Não foi possível criar card"**
→ Verifique Board ID e List ID

**Card duplicado?**
→ Impossível! Sistema garante 1 card por lote

---

## 📚 Documentação Completa

Para informações detalhadas, consulte: **[INTEGRACAO_TRELLO.md](INTEGRACAO_TRELLO.md)**

---

**✅ Sistema pronto para uso!**
