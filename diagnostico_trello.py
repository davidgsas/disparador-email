"""
Diagnóstico de conectividade com API do Trello
Verifica se o problema é de rede, DNS ou API do Trello
"""

import requests
import time
import sys

print("=" * 60)
print("🔍 DIAGNÓSTICO DE CONECTIVIDADE TRELLO")
print("=" * 60)

# 1. Testar conectividade básica com Trello
print(f"\n1️⃣ Testando conectividade com trello.com...")
try:
    response = requests.get("https://trello.com", timeout=10)
    print(f"   ✅ Status: {response.status_code}")
except requests.exceptions.Timeout:
    print(f"   ❌ Timeout - Pode haver problema de rede")
except Exception as e:
    print(f"   ❌ Erro: {e}")

# 2. Testar API endpoint genérico
print(f"\n2️⃣ Testando API do Trello (endpoint público)...")
try:
    response = requests.get("https://api.trello.com/1/members/me", timeout=10)
    print(f"   Status: {response.status_code}")
    if response.status_code == 401:
        print(f"   ✅ API respondendo (401 é esperado sem auth)")
    else:
        print(f"   ⚠️  Status inesperado: {response.status_code}")
except requests.exceptions.Timeout:
    print(f"   ❌ Timeout - API do Trello está lenta ou inacessível")
except Exception as e:
    print(f"   ❌ Erro: {e}")

# 3. Testar com credenciais
print(f"\n3️⃣ Testando com suas credenciais...")
sys.path.insert(0, '/Users/david/Documents/GitHub/disparador-email')

try:
    from integracoes.trello_integration import TrelloIntegration
    
    trello = TrelloIntegration()
    
    if not trello.is_configured():
        print(f"   ❌ Credenciais não configuradas")
        sys.exit(1)
    
    # Testar endpoint simples
    url = "https://api.trello.com/1/members/me"
    params = {
        'key': trello.api_key,
        'token': trello.token
    }
    
    print(f"   Fazendo requisição autenticada...")
    response = requests.get(url, params=params, timeout=30)
    
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ Autenticação OK - Usuário: {data.get('fullName', 'N/A')}")
    else:
        print(f"   ⚠️  Status: {response.status_code}")
        
except requests.exceptions.Timeout:
    print(f"   ❌ Timeout - API não está respondendo")
    print(f"   Aguarde alguns minutos e tente novamente")
except Exception as e:
    print(f"   ❌ Erro: {e}")
    import traceback
    traceback.print_exc()

# 4. Testar criação de card simples
print(f"\n4️⃣ Testando criação de card (método simplificado)...")
try:
    url = "https://api.trello.com/1/cards"
    params = {
        'key': trello.api_key,
        'token': trello.token
    }
    data = {
        'idList': trello.list_id,
        'name': 'TESTE - Pode deletar',
        'desc': 'Card de teste automático'
    }
    
    print(f"   Enviando requisição (timeout: 60s)...")
    start = time.time()
    response = requests.post(url, params=params, json=data, timeout=60)
    elapsed = time.time() - start
    
    print(f"   ⏱️  Tempo: {elapsed:.2f}s")
    
    if response.status_code == 200:
        card_data = response.json()
        print(f"   ✅ Card criado: {card_data['shortUrl']}")
        print(f"   ⚠️  Lembre-se de deletar o card manualmente!")
    else:
        print(f"   ❌ Status: {response.status_code}")
        print(f"   Resposta: {response.text[:200]}")
        
except requests.exceptions.Timeout:
    print(f"   ❌ Timeout após 60 segundos")
    print(f"   A API do Trello está muito lenta ou indisponível")
    print(f"\n💡 RECOMENDAÇÃO:")
    print(f"   - Aguarde 5-10 minutos e tente novamente")
    print(f"   - Verifique https://trello.status.atlassian.com/ para status da API")
    
except Exception as e:
    print(f"   ❌ Erro: {e}")

print("\n" + "=" * 60)
print("Diagnóstico concluído!")
print("=" * 60)
