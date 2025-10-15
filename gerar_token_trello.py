#!/usr/bin/env python3
"""
Gerador de link para obter o Token do Trello
"""

api_key = "8a752bd4a6a57bb608ba432319bb5317"

# URL para gerar o token manualmente
url = f"https://trello.com/1/authorize?expiration=never&name=DisparadorEmail&scope=read,write&response_type=token&key={api_key}"

print("="*70)
print("🔐 GERAR TOKEN DO TRELLO")
print("="*70)
print()
print("📋 Sua API Key está correta:")
print(f"   {api_key}")
print()
print("⚠️  O 'Segredo' mostrado na página NÃO é o Token!")
print("   Você precisa GERAR um Token separadamente.")
print()
print("="*70)
print("🎯 PASSO A PASSO:")
print("="*70)
print()
print("1. Copie esta URL completa:")
print()
print(url)
print()
print("2. Cole no navegador e pressione ENTER")
print()
print("3. Você verá uma página pedindo autorização")
print()
print("4. Clique no botão 'Permitir' ou 'Allow'")
print()
print("5. Você será redirecionado para uma página que mostra o TOKEN")
print()
print("6. COPIE o token completo (64 caracteres)")
print()
print("7. Cole aqui quando estiver pronto")
print()
print("="*70)
print()

# Esperar o usuário colar o token
token = input("🎫 Cole o TOKEN aqui (64 caracteres): ").strip()

if len(token) != 64:
    print(f"\n⚠️  Atenção! O token deveria ter 64 caracteres, você colou {len(token)}")
    print("   Certifique-se de copiar o token COMPLETO")
else:
    print("\n✅ Token parece correto!")

print()
print("🧪 Testando credenciais...")

import requests

try:
    url_test = 'https://api.trello.com/1/members/me/boards'
    params = {'key': api_key, 'token': token}
    
    response = requests.get(url_test, params=params, timeout=10)
    
    if response.status_code == 200:
        boards = response.json()
        
        print()
        print("="*70)
        print("✅ SUCESSO! CREDENCIAIS VÁLIDAS!")
        print("="*70)
        print()
        print(f"📊 {len(boards)} board(s) encontrado(s):")
        print()
        
        for board in boards:
            print(f"📋 {board['name']}")
            print(f"   ID: {board['id']}")
            print(f"   URL: {board['url']}")
            print()
        
        # Salvar no banco
        print("💾 Salvando no banco de dados...")
        
        import database as db
        conn = db.get_db_connection()
        cur = conn.cursor()
        cur.execute('''
            UPDATE integracoes_config 
            SET trello_api_key = %s,
                trello_token = %s,
                data_atualizacao = NOW()
        ''', (api_key, token))
        conn.commit()
        cur.close()
        conn.close()
        
        print("✅ Salvo com sucesso!")
        print()
        print("🎉 Configuração concluída!")
        print()
        print("📋 Próximos passos:")
        print("   1. Acesse o painel '🔌 Integrações' no Streamlit")
        print("   2. Configure o Board ID e List ID")
        print("   3. Teste a integração")
        
    else:
        print()
        print(f"❌ Erro {response.status_code}: {response.text}")
        print()
        print("💡 Possíveis problemas:")
        print("   • Token incorreto ou incompleto")
        print("   • Token não foi autorizado (não clicou em 'Allow')")
        print("   • API Key e Token são de contas diferentes")
        
except Exception as e:
    print(f"\n❌ Erro: {e}")
