"""
Script para testar e diagnosticar credenciais do Trello
"""

import requests


def testar_credenciais_trello():
    """Testa se as credenciais do Trello são válidas"""
    
    print("\n" + "="*70)
    print("🔐 TESTE DE CREDENCIAIS DO TRELLO")
    print("="*70)
    
    api_key = "9869e57754f5109c97773f9fca23ae4c"
    token = "8140b5528fb96969db573adfc7674f75eb1b41ada7afee01e1987fb649031c21"
    
    print(f"\n🔑 API Key: {api_key[:10]}...{api_key[-10:]}")
    print(f"🎫 Token: {token[:10]}...{token[-10:]}")
    
    # Teste 1: Verificar token
    print(f"\n1️⃣ Testando Token...")
    url = f"https://api.trello.com/1/tokens/{token}"
    params = {
        'key': api_key,
        'token': token
    }
    
    try:
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            print(f"   ✅ Token válido!")
            data = response.json()
            print(f"   👤 ID do membro: {data.get('idMember', 'N/A')}")
        elif response.status_code == 401:
            print(f"   ❌ Token ou API Key inválidos!")
            print(f"   Status: {response.status_code}")
            print(f"   Resposta: {response.text[:200]}")
            return False
        else:
            print(f"   ⚠️  Erro {response.status_code}: {response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"   ❌ Erro na requisição: {e}")
        return False
    
    # Teste 2: Listar boards do usuário
    print(f"\n2️⃣ Testando Listagem de Boards...")
    url = "https://api.trello.com/1/members/me/boards"
    
    try:
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            boards = response.json()
            print(f"   ✅ {len(boards)} board(s) encontrado(s)!")
            
            print(f"\n   Seus boards:")
            for board in boards[:5]:  # Mostrar apenas 5
                print(f"   • {board['name']:30s} → {board['id']}")
            
            # Verificar se o board específico existe
            board_id = "kcR2WofW"
            board_encontrado = any(b['id'] == board_id for b in boards)
            
            if board_encontrado:
                print(f"\n   ✅ Board 'kcR2WofW' encontrado!")
            else:
                print(f"\n   ⚠️  Board 'kcR2WofW' NÃO encontrado na sua conta")
                print(f"   Verifique se você tem acesso a este board")
                
        elif response.status_code == 401:
            print(f"   ❌ Não autorizado!")
            return False
        else:
            print(f"   ⚠️  Erro {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ Erro na requisição: {e}")
        return False
    
    # Teste 3: Acessar board específico
    print(f"\n3️⃣ Testando Acesso ao Board kcR2WofW...")
    url = "https://api.trello.com/1/boards/kcR2WofW"
    
    try:
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            board = response.json()
            print(f"   ✅ Board acessível!")
            print(f"   📋 Nome: {board['name']}")
            print(f"   🔗 URL: {board['url']}")
        elif response.status_code == 401:
            print(f"   ❌ Não autorizado para acessar este board!")
            print(f"   Verifique se suas credenciais têm permissão")
            return False
        elif response.status_code == 404:
            print(f"   ❌ Board não encontrado!")
            print(f"   Verifique o ID do board")
            return False
        else:
            print(f"   ⚠️  Erro {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ Erro na requisição: {e}")
        return False
    
    print(f"\n" + "="*70)
    print(f"✅ TODOS OS TESTES PASSARAM!")
    print(f"="*70)
    
    return True


if __name__ == '__main__':
    sucesso = testar_credenciais_trello()
    
    if not sucesso:
        print(f"\n💡 COMO CORRIGIR:\n")
        print(f"1. Acesse: https://trello.com/power-ups/admin")
        print(f"2. Crie uma nova Power-Up (ou use existente)")
        print(f"3. Copie a API Key")
        print(f"4. Clique em 'Token' e gere um novo token")
        print(f"5. Autorize o acesso")
        print(f"6. Copie o novo token")
        print(f"7. Atualize no painel de Integrações")
