# 🛠️ COMANDOS ÚTEIS - INTEGRAÇÃO TRELLO

## 🚀 Instalação e Setup

```bash
# 1. Navegar para o projeto
cd /Users/davidgabriel/projetos/disparador-email

# 2. Ativar ambiente virtual
source .venv/bin/activate

# 3. Criar tabelas no banco
.venv/bin/python3 setup_integracoes.py

# 4. Verificar tabelas criadas
.venv/bin/python3 -c "
import database as db
conn = db.get_db_connection()
cur = conn.cursor()
cur.execute(\"SELECT COUNT(*) FROM integracoes_config\")
print(f'✅ integracoes_config: {cur.fetchone()[0]} registro')
cur.execute(\"SELECT COUNT(*) FROM trello_cards\")
print(f'✅ trello_cards: {cur.fetchone()[0]} cards')
cur.close()
conn.close()
"
```

## 🧪 Testes

```bash
# Teste completo da integração
.venv/bin/python3 testar_trello.py

# Exemplos interativos de uso
.venv/bin/python3 exemplos_trello.py

# Teste de configuração rápido
.venv/bin/python3 -c "
from integracoes.trello_integration import TrelloIntegration
t = TrelloIntegration()
print('✅ Configurado' if t.is_configured() else '❌ Não configurado')
"
```

## 📊 Consultas ao Banco

```bash
# Ver configuração atual
.venv/bin/python3 -c "
import database as db
conn = db.get_db_connection()
cur = conn.cursor()
cur.execute('SELECT trello_ativo, trello_board_id, trello_list_id FROM integracoes_config WHERE id=1')
r = cur.fetchone()
print(f'Ativo: {r[0]}')
print(f'Board: {r[1]}')
print(f'Lista: {r[2]}')
"

# Total de cards criados
.venv/bin/python3 -c "
import database as db
conn = db.get_db_connection()
cur = conn.cursor()
cur.execute('SELECT COUNT(*) FROM trello_cards')
print(f'Total de cards: {cur.fetchone()[0]}')
"

# Cards criados hoje
.venv/bin/python3 -c "
import database as db
conn = db.get_db_connection()
cur = conn.cursor()
cur.execute('SELECT COUNT(*) FROM trello_cards WHERE DATE(data_criacao)=CURRENT_DATE')
print(f'Cards hoje: {cur.fetchone()[0]}')
"

# Últimos 5 cards
.venv/bin/python3 -c "
import database as db
conn = db.get_db_connection()
cur = conn.cursor()
cur.execute('SELECT lote_id, card_url, data_criacao FROM trello_cards ORDER BY data_criacao DESC LIMIT 5')
for r in cur.fetchall():
    print(f'Lote #{r[0]}: {r[1]} ({r[2].strftime(\"%d/%m/%Y %H:%M\")})')
"

# Verificar se lote tem card
.venv/bin/python3 -c "
import database as db
lote_id = 123  # Altere aqui
conn = db.get_db_connection()
cur = conn.cursor()
cur.execute('SELECT card_url FROM trello_cards WHERE lote_id=%s', (lote_id,))
r = cur.fetchone()
print(f'Card: {r[0]}' if r else 'Sem card')
"
```

## 🔧 Gerenciamento

```bash
# Ativar integração
.venv/bin/python3 -c "
import database as db
conn = db.get_db_connection()
cur = conn.cursor()
cur.execute('UPDATE integracoes_config SET trello_ativo=true WHERE id=1')
conn.commit()
print('✅ Integração ativada')
"

# Desativar integração
.venv/bin/python3 -c "
import database as db
conn = db.get_db_connection()
cur = conn.cursor()
cur.execute('UPDATE integracoes_config SET trello_ativo=false WHERE id=1')
conn.commit()
print('✅ Integração desativada')
"

# Limpar histórico de cards (cuidado!)
.venv/bin/python3 -c "
import database as db
conn = db.get_db_connection()
cur = conn.cursor()
cur.execute('DELETE FROM trello_cards')
conn.commit()
print('✅ Histórico limpo')
"
```

## 📝 Logs

```bash
# Ver logs do job em tempo real
tail -f scheduler.log | grep -i trello

# Ver últimas 50 linhas com "Trello"
tail -n 1000 scheduler.log | grep -i trello

# Ver apenas erros do Trello
tail -n 1000 scheduler.log | grep -E "(Trello|trello)" | grep -E "(Erro|erro|❌)"

# Ver apenas sucessos do Trello
tail -n 1000 scheduler.log | grep -E "(Trello|trello)" | grep -E "(criado|✅)"
```

## 🎯 Executar Job Manualmente

```bash
# Executar job de consulta (criará cards se houver arquivos)
.venv/bin/python3 job_consultar_notas.py

# Ver apenas saída relacionada ao Trello
.venv/bin/python3 job_consultar_notas.py 2>&1 | grep -i trello
```

## 🔍 Debug

```bash
# Verificar importação
.venv/bin/python3 -c "
from integracoes.trello_integration import TrelloIntegration
print('✅ Importação OK')
"

# Ver configuração completa
.venv/bin/python3 -c "
from integracoes.trello_integration import TrelloIntegration
t = TrelloIntegration()
print('Config:', t.config)
print('Configurado:', t.is_configured())
"

# Testar API do Trello
.venv/bin/python3 -c "
from integracoes.trello_integration import TrelloIntegration
t = TrelloIntegration()
boards = t.listar_boards()
print(f'Boards encontrados: {len(boards) if boards else 0}')
"

# Criar card de teste via linha de comando
.venv/bin/python3 -c "
from integracoes.trello_integration import TrelloIntegration
t = TrelloIntegration()
if t.is_configured():
    r = t.criar_card_download(
        lote_id=0,
        prestador_nome='Teste CLI',
        montador_nome='Sistema',
        arquivos_baixados=['teste.pdf'],
        nota_fiscal='TEST-001'
    )
    print(f'Card criado: {r[\"shortUrl\"]}' if r else 'Erro')
else:
    print('❌ Não configurado')
"
```

## 🗄️ Backup e Restore

```bash
# Backup da configuração
.venv/bin/python3 -c "
import database as db
import json
conn = db.get_db_connection()
cur = conn.cursor()
cur.execute('SELECT * FROM integracoes_config WHERE id=1')
cols = [desc[0] for desc in cur.description]
data = dict(zip(cols, cur.fetchone()))
with open('backup_trello_config.json', 'w') as f:
    json.dump(data, f, indent=2, default=str)
print('✅ Backup salvo em backup_trello_config.json')
"

# Backup do histórico de cards
.venv/bin/python3 -c "
import database as db
import json
conn = db.get_db_connection()
cur = conn.cursor()
cur.execute('SELECT * FROM trello_cards')
cols = [desc[0] for desc in cur.description]
data = [dict(zip(cols, row)) for row in cur.fetchall()]
with open('backup_trello_cards.json', 'w') as f:
    json.dump(data, f, indent=2, default=str)
print(f'✅ Backup de {len(data)} cards salvo em backup_trello_cards.json')
"
```

## 📚 Documentação

```bash
# Abrir documentação completa
open INTEGRACAO_TRELLO.md

# Abrir quick start
open QUICKSTART_TRELLO.md

# Abrir resumo
open RESUMO_INTEGRACAO_TRELLO.md

# Ver diagrama de fluxo
cat DIAGRAMA_TRELLO.txt
```

## 🌐 URLs Úteis

```bash
# Abrir painel do Trello Power-Ups
open "https://trello.com/power-ups/admin"

# Abrir documentação da API do Trello
open "https://developer.atlassian.com/cloud/trello/rest/api-group-cards/"

# Ver board configurado (substitua {board_id})
open "https://trello.com/b/{board_id}"
```

## 🔐 Segurança

```bash
# Ver apenas primeiros caracteres das credenciais (seguro)
.venv/bin/python3 -c "
import database as db
conn = db.get_db_connection()
cur = conn.cursor()
cur.execute('SELECT trello_api_key, trello_token FROM integracoes_config WHERE id=1')
key, token = cur.fetchone()
print(f'API Key: {key[:10]}...' if key else 'Não configurado')
print(f'Token: {token[:10]}...' if token else 'Não configurado')
"

# Verificar se credenciais estão no código (não devem estar!)
grep -r "trello_api_key\|trello_token" --include="*.py" --exclude="setup_integracoes.py" --exclude="*integration.py" . || echo "✅ Nenhuma credencial no código"
```

## 📊 Estatísticas

```bash
# Relatório completo
.venv/bin/python3 -c "
import database as db
from datetime import datetime
conn = db.get_db_connection()
cur = conn.cursor()

print('='*60)
print('📊 ESTATÍSTICAS DA INTEGRAÇÃO TRELLO')
print('='*60)

cur.execute('SELECT COUNT(*) FROM trello_cards')
print(f'\n📋 Total de cards: {cur.fetchone()[0]}')

cur.execute('SELECT COUNT(*) FROM trello_cards WHERE DATE(data_criacao)=CURRENT_DATE')
print(f'📅 Cards hoje: {cur.fetchone()[0]}')

cur.execute('SELECT COUNT(*) FROM trello_cards WHERE data_criacao >= NOW() - INTERVAL \"7 days\"')
print(f'📆 Última semana: {cur.fetchone()[0]}')

cur.execute('SELECT data_criacao FROM trello_cards ORDER BY data_criacao DESC LIMIT 1')
r = cur.fetchone()
if r:
    print(f'\n⏰ Último card: {r[0].strftime(\"%d/%m/%Y %H:%M\")}')

cur.execute('SELECT trello_ativo FROM integracoes_config WHERE id=1')
print(f'\n⚡ Status: {\"ATIVO\" if cur.fetchone()[0] else \"DESATIVADO\"}')
"
```

## 🚨 Troubleshooting

```bash
# Verificar se tabelas existem
.venv/bin/python3 -c "
import database as db
conn = db.get_db_connection()
cur = conn.cursor()
try:
    cur.execute('SELECT 1 FROM integracoes_config LIMIT 1')
    print('✅ Tabela integracoes_config: OK')
except:
    print('❌ Tabela integracoes_config: NÃO EXISTE')
try:
    cur.execute('SELECT 1 FROM trello_cards LIMIT 1')
    print('✅ Tabela trello_cards: OK')
except:
    print('❌ Tabela trello_cards: NÃO EXISTE')
"

# Recriar tabelas (se necessário)
.venv/bin/python3 setup_integracoes.py

# Verificar dependências
.venv/bin/python3 -c "
import requests
print(f'✅ requests {requests.__version__}')
"
```

## 🎯 Atalhos Rápidos

```bash
# Alias úteis (adicione ao ~/.zshrc)
alias trello-test='.venv/bin/python3 testar_trello.py'
alias trello-exemplos='.venv/bin/python3 exemplos_trello.py'
alias trello-stats='.venv/bin/python3 -c "from integracoes.trello_integration import TrelloIntegration; t=TrelloIntegration(); print(\"Config:\", t.is_configured())"'
alias trello-logs='tail -f scheduler.log | grep -i trello'
```

## 📞 Ajuda

```bash
# Ver todos os métodos disponíveis
.venv/bin/python3 -c "
from integracoes.trello_integration import TrelloIntegration
import inspect
print('Métodos disponíveis:')
for name, method in inspect.getmembers(TrelloIntegration, predicate=inspect.isfunction):
    if not name.startswith('_'):
        print(f'  • {name}()')
"

# Ver documentação de um método
.venv/bin/python3 -c "
from integracoes.trello_integration import TrelloIntegration
print(TrelloIntegration.criar_card_download.__doc__)
"
```

---

**💡 Dica:** Adicione esses comandos aos seus favoritos ou crie scripts personalizados!
