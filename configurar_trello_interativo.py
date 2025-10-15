#!/usr/bin/env python3
"""
Script interativo para configurar Trello corretamente
"""

import requests
import database as db
import sys


def limpar_credencial(valor):
    """Remove espaços, quebras de linha e outros caracteres invisíveis"""
    return valor.strip().replace('\n', '').replace('\r', '').replace(' ', '')


def validar_api_key(api_key):
    """Valida se a API Key tem formato correto"""
    api_key = limpar_credencial(api_key)
    
    # API Key do Trello tem 32 caracteres hexadecimais
    if len(api_key) != 32:
        return False, f"API Key deve ter 32 caracteres (você tem {len(api_key)})"
    
    # Verificar se é hexadecimal
    try:
        int(api_key, 16)
    except ValueError:
        return False, "API Key deve conter apenas caracteres hexadecimais (0-9, a-f)"
    
    return True, "Formato correto"


def validar_token(token):
    """Valida se o Token tem formato correto"""
    token = limpar_credencial(token)
    
    # Token do Trello tem 64 caracteres hexadecimais
    if len(token) != 64:
        return False, f"Token deve ter 64 caracteres (você tem {len(token)})"
    
    # Verificar se é hexadecimal
    try:
        int(token, 16)
    except ValueError:
        return False, "Token deve conter apenas caracteres hexadecimais (0-9, a-f)"
    
    return True, "Formato correto"


def testar_credenciais(api_key, token):
    """Testa se as credenciais funcionam"""
    api_key = limpar_credencial(api_key)
    token = limpar_credencial(token)
    
    print("\n🔄 Testando credenciais...")
    
    try:
        url = 'https://api.trello.com/1/members/me/boards'
        params = {'key': api_key, 'token': token}
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            boards = response.json()
            return True, boards
        elif response.status_code == 401:
            return False, "Credenciais inválidas (401 Unauthorized)"
        else:
            return False, f"Erro {response.status_code}: {response.text[:100]}"
            
    except requests.exceptions.Timeout:
        return False, "Timeout - verifique sua conexão com a internet"
    except requests.exceptions.RequestException as e:
        return False, f"Erro de conexão: {str(e)}"
    except Exception as e:
        return False, f"Erro inesperado: {str(e)}"


def salvar_no_banco(api_key, token):
    """Salva credenciais no banco de dados"""
    try:
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
        
        return True, "Salvo com sucesso"
    except Exception as e:
        return False, f"Erro ao salvar: {str(e)}"


def main():
    print("="*70)
    print("🔧 CONFIGURAÇÃO INTERATIVA DO TRELLO")
    print("="*70)
    print()
    print("📖 Siga as instruções em: https://trello.com/power-ups/admin")
    print()
    print("⚠️  IMPORTANTE:")
    print("   • API Key tem 32 caracteres")
    print("   • Token tem 64 caracteres")
    print("   • Cole EXATAMENTE como aparece (sem espaços)")
    print()
    print("-"*70)
    print()
    
    # Obter API Key
    while True:
        api_key = input("🔑 Cole a API Key (32 caracteres): ").strip()
        
        if not api_key:
            print("❌ Você não colou nada. Tente novamente.\n")
            continue
        
        api_key = limpar_credencial(api_key)
        valido, msg = validar_api_key(api_key)
        
        if valido:
            print(f"✅ {msg}")
            print(f"   Caracteres: {len(api_key)}")
            print(f"   Preview: {api_key[:8]}...{api_key[-8:]}")
            break
        else:
            print(f"❌ {msg}")
            print(f"   Você colou: {len(api_key)} caracteres")
            if len(api_key) < 50:
                print(f"   Conteúdo: {api_key}")
            print()
            continuar = input("   Tentar novamente? (s/n): ").lower()
            if continuar != 's':
                print("\n❌ Configuração cancelada")
                return
            print()
    
    print()
    
    # Obter Token
    while True:
        token = input("🎫 Cole o Token (64 caracteres): ").strip()
        
        if not token:
            print("❌ Você não colou nada. Tente novamente.\n")
            continue
        
        token = limpar_credencial(token)
        valido, msg = validar_token(token)
        
        if valido:
            print(f"✅ {msg}")
            print(f"   Caracteres: {len(token)}")
            print(f"   Preview: {token[:8]}...{token[-8:]}")
            break
        else:
            print(f"❌ {msg}")
            print(f"   Você colou: {len(token)} caracteres")
            if len(token) < 100:
                print(f"   Conteúdo: {token}")
            print()
            continuar = input("   Tentar novamente? (s/n): ").lower()
            if continuar != 's':
                print("\n❌ Configuração cancelada")
                return
            print()
    
    # Testar credenciais
    sucesso, resultado = testar_credenciais(api_key, token)
    
    if sucesso:
        boards = resultado
        print("\n" + "="*70)
        print("✅ SUCESSO! Credenciais válidas!")
        print("="*70)
        print(f"\n📊 {len(boards)} board(s) encontrado(s):")
        print()
        
        for i, board in enumerate(boards, 1):
            print(f"{i}. {board['name']}")
            print(f"   ID: {board['id']}")
            print(f"   URL: {board['url']}")
            print()
        
        # Salvar no banco
        print("💾 Salvando no banco de dados...")
        salvo, msg = salvar_no_banco(api_key, token)
        
        if salvo:
            print(f"✅ {msg}")
            print()
            print("🎉 Configuração concluída com sucesso!")
            print()
            print("📋 Próximos passos:")
            print("   1. Acesse o painel '🔌 Integrações' no Streamlit")
            print("   2. Configure o Board ID e List ID")
            print("   3. Teste criando um card")
        else:
            print(f"❌ {msg}")
            print()
            print("⚠️  As credenciais funcionam, mas não foram salvas no banco.")
            print("   Você pode salvá-las manualmente no painel de Integrações.")
    else:
        print("\n" + "="*70)
        print("❌ ERRO: Credenciais inválidas")
        print("="*70)
        print(f"\nMotivo: {resultado}")
        print()
        print("💡 Possíveis causas:")
        print("   1. API Key ou Token incorretos")
        print("   2. Você colou apenas parte da credencial")
        print("   3. As credenciais expiraram")
        print("   4. Você não autorizou o Token")
        print()
        print("🔄 Tente novamente:")
        print("   1. Acesse: https://trello.com/power-ups/admin")
        print("   2. Gere NOVAS credenciais")
        print("   3. Execute este script novamente")
        print()
        print(f"   Comando: .venv/bin/python3 {__file__}")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Configuração cancelada pelo usuário")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Erro inesperado: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
