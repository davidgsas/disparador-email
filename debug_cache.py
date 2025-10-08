#!/usr/bin/env python3
"""
Analisa o conteúdo do cache de tokens
"""

import json
import time
from datetime import datetime

def main():
    print("🔍 ANÁLISE DO CACHE DE TOKENS")
    print("=" * 60)
    
    try:
        with open("token_cache.json", "r") as f:
            cache = json.load(f)
        
        access_tokens = cache.get("AccessToken", {})
        current_time = int(time.time())
        
        print(f"⏰ Timestamp atual: {current_time}")
        print(f"📅 Data/hora atual: {datetime.fromtimestamp(current_time)}")
        print(f"📊 Total de access tokens no cache: {len(access_tokens)}")
        
        for i, (key, token_info) in enumerate(access_tokens.items(), 1):
            print(f"\n🎫 TOKEN {i}:")
            print(f"   Chave: {key[:50]}...")
            
            expires_on = int(token_info.get("expires_on", "0"))
            cached_at = int(token_info.get("cached_at", "0"))
            
            print(f"   Cached at: {cached_at} ({datetime.fromtimestamp(cached_at)})")
            print(f"   Expires on: {expires_on} ({datetime.fromtimestamp(expires_on)})")
            print(f"   Diferença: {expires_on - current_time} segundos")
            
            if expires_on > current_time:
                print(f"   Status: ✅ VÁLIDO (expira em {(expires_on - current_time) // 60} minutos)")
            else:
                print(f"   Status: ❌ EXPIRADO (há {(current_time - expires_on) // 60} minutos)")
        
        print(f"\n" + "=" * 60)
        
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    main()
