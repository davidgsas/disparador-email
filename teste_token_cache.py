#!/usr/bin/env python3
"""
Teste para verificar se o sistema consegue obter o token do cache
"""

import sys
import os
sys.path.append('.')

def main():
    print("🧪 TESTE DE TOKEN DO CACHE")
    print("=" * 50)
    
    # Importar função
    try:
        from notificacao_nf import get_cached_access_token
        print("✅ Função importada com sucesso")
    except Exception as e:
        print(f"❌ Erro na importação: {e}")
        return
    
    # Testar obtenção do token
    print("\n🔑 Tentando obter token do cache...")
    token = get_cached_access_token()
    
    if token:
        print(f"✅ TOKEN ENCONTRADO!")
        print(f"📝 Primeiros 50 caracteres: {token[:50]}...")
        print(f"📏 Tamanho total: {len(token)} caracteres")
        
        # Verificar se é um JWT válido
        if token.startswith("eyJ"):
            print("✅ Token parece ser um JWT válido")
        else:
            print("⚠️ Token não parece ser um JWT")
    else:
        print("❌ NENHUM TOKEN ENCONTRADO")
    
    print("\n" + "=" * 50)

if __name__ == "__main__":
    main()
