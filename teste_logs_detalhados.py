#!/usr/bin/env python3
"""
Teste de notificação com logs detalhados para debug
"""

import sys
import os
sys.path.append('.')

def main():
    print("🔍 TESTE DE NOTIFICAÇÃO COM LOGS DETALHADOS")
    print("=" * 60)
    
    # Importar módulo
    try:
        from notificacao_nf import enviar_notificacao_nf_upload
        print("✅ Módulo importado com sucesso")
    except Exception as e:
        print(f"❌ Erro na importação: {e}")
        return
    
    # Dados de teste
    token_info = ("prestador", "LOG_TEST_123")
    dados_lote = {
        "prestador_nome": "TESTE COM LOGS DETALHADOS LTDA",
        "periodo": "01/10/2025 - 31/10/2025", 
        "valor_total": 9999.99
    }
    arquivo_nome = "NF_TESTE_LOGS.pdf"
    
    print(f"\n📋 DADOS DO TESTE:")
    print(f"Token Info: {token_info}")
    print(f"Dados Lote: {dados_lote}")
    print(f"Arquivo: {arquivo_nome}")
    
    print(f"\n🧪 EXECUTANDO TESTE SEM TOKEN (PREVIEW):")
    print("-" * 40)
    
    # Teste sem token
    resultado1 = enviar_notificacao_nf_upload(token_info, dados_lote, arquivo_nome, None, None)
    
    print(f"\n📊 RESULTADO SEM TOKEN:")
    import json
    print(json.dumps(resultado1, indent=2, ensure_ascii=False))
    
    print(f"\n🔑 EXECUTANDO TESTE COM TOKEN FAKE:")
    print("-" * 40)
    
    # Teste com token fake
    resultado2 = enviar_notificacao_nf_upload(token_info, dados_lote, arquivo_nome, "token_fake_123", None)
    
    print(f"\n📊 RESULTADO COM TOKEN FAKE:")
    print(json.dumps(resultado2, indent=2, ensure_ascii=False))
    
    print(f"\n" + "=" * 60)
    print("🏁 TESTE CONCLUÍDO - Verifique os logs acima")

if __name__ == "__main__":
    main()
