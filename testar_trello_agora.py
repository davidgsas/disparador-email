"""
Teste rápido da integração do Trello
"""

import sys
sys.path.insert(0, '/Users/david/Documents/GitHub/disparador-email')

from integracoes.trello_integration import TrelloIntegration
import requests

print("=" * 60)
print("🔍 TESTE DA INTEGRAÇÃO TRELLO")
print("=" * 60)

# Inicializar integração
trello = TrelloIntegration()

print(f"\n📋 Configuração carregada:")
print(f"   API Key: {'✅ Configurada' if trello.api_key else '❌ Não configurada'}")
print(f"   Token: {'✅ Configurado' if trello.token else '❌ Não configurado'}")
print(f"   Board ID: {trello.board_id if trello.board_id else '❌ Não configurado'}")
print(f"   List ID: {trello.list_id if trello.list_id else '❌ Não configurado'}")
print(f"   Ativo: {'✅ Sim' if trello.config.get('trello_ativo') else '❌ Não'}")
print(f"   Configuração válida: {'✅ Sim' if trello.is_configured() else '❌ Não'}")

if not trello.is_configured():
    print("\n❌ Integração não está configurada corretamente!")
    sys.exit(1)

print(f"\n🔌 Testando conexão com API do Trello...")

# Testar API - buscar informações do board
try:
    url = f"{trello.base_url}/boards/{trello.board_id}"
    params = {
        'key': trello.api_key,
        'token': trello.token
    }
    print(f"   Tentando conectar (timeout: 30s)...")
    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()
    board_data = response.json()
    print(f"✅ Board encontrado: {board_data['name']}")
    print(f"   URL: {board_data['url']}")
except requests.exceptions.Timeout:
    print(f"❌ Timeout ao conectar com Trello (API está lenta ou inacessível)")
    print(f"   Isso pode ser temporário. Tente novamente em alguns minutos.")
    sys.exit(1)
except requests.exceptions.RequestException as e:
    print(f"❌ Erro ao conectar com Trello: {e}")
    if hasattr(e, 'response') and e.response is not None:
        print(f"   Status: {e.response.status_code}")
        if e.response.status_code == 504:
            print(f"   ⚠️  504 Gateway Timeout - API do Trello está temporariamente indisponível")
            print(f"   Isso geralmente se resolve em alguns minutos. Tente novamente mais tarde.")
    sys.exit(1)

# Testar acesso à lista
try:
    url = f"{trello.base_url}/lists/{trello.list_id}"
    params = {
        'key': trello.api_key,
        'token': trello.token
    }
    print(f"   Verificando lista (timeout: 30s)...")
    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()
    list_data = response.json()
    print(f"✅ Lista encontrada: {list_data['name']}")
except requests.exceptions.Timeout:
    print(f"❌ Timeout ao acessar lista")
    sys.exit(1)
except requests.exceptions.RequestException as e:
    print(f"❌ Erro ao acessar lista: {e}")
    if hasattr(e, 'response') and e.response is not None and hasattr(e.response, 'text'):
        print(f"   Resposta: {e.response.text[:200]}")
    sys.exit(1)

# Testar criação de card de teste
print(f"\n🧪 Testando criação de card...")
try:
    card_result = trello.criar_card_download(
        lote_id=99999,
        prestador_nome="TESTE AUTOMÁTICO",
        montador_nome="",
        arquivos_baixados=["teste.pdf"],
        nota_fiscal="NF-TESTE-123",
        valor_lote=1500.00
    )
    
    if card_result:
        print(f"✅ Card de teste criado com sucesso!")
        print(f"   ID: {card_result['id']}")
        print(f"   URL: {card_result['shortUrl']}")
        print(f"\n⚠️  Lembre-se de deletar o card de teste manualmente no Trello!")
    else:
        print(f"❌ Falha ao criar card de teste")
        
except Exception as e:
    print(f"❌ Erro ao criar card: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("Teste concluído!")
print("=" * 60)
