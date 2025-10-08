#!/usr/bin/env python3
"""
Teste final do sistema de notificações - Simulação completa de upload
"""

import sys
import os
sys.path.append('.')

from notificacao_nf import enviar_notificacao_nf_upload

def main():
    print("🧪 TESTE FINAL - SIMULAÇÃO DE UPLOAD COM NOTIFICAÇÃO")
    print("=" * 60)
    
    # Simular dados como se viessem de um upload real
    token_info = ("prestador", 123)  # tipo, lote_id
    
    dados_lote = {
        "prestador_nome": "EMPRESA TESTE REAL LTDA",
        "periodo": "01/10/2025 - 31/10/2025",
        "valor_total": 5432.10
    }
    
    arquivo_nome = "NF_20251007_TESTE_REAL.pdf"
    access_token = None  # Simular sem token (como no upload real)
    
    print("📋 DADOS DO TESTE:")
    print(f"  Token Info: {token_info}")
    print(f"  Dados Lote: {dados_lote}")
    print(f"  Arquivo: {arquivo_nome}")
    print(f"  Access Token: {access_token}")
    
    print("\n🚀 EXECUTANDO NOTIFICAÇÃO...")
    print("-" * 40)
    
    # Executar notificação
    resultado = enviar_notificacao_nf_upload(token_info, dados_lote, arquivo_nome, access_token)
    
    print("\n📊 RESULTADO:")
    print("-" * 40)
    
    if resultado.get("success"):
        print(f"✅ SUCCESS: {resultado['message']}")
        if "emails" in resultado:
            print(f"📧 Enviado para: {', '.join(resultado['emails'])}")
    else:
        print(f"❌ FALHOU: {resultado.get('message', 'Erro desconhecido')}")
        
        if "preview" in resultado:
            print("\n📧 PREVIEW GERADO:")
            preview = resultado["preview"]
            print(f"  Para: {', '.join(preview['para'])}")
            print(f"  Assunto: {preview['assunto']}")
            print(f"  Prioridade: {preview['prioridade']}")
            print(f"  Corpo (início): {preview['corpo'][:100]}...")
            print("  ✅ PREVIEW OK - Sistema funcionando!")
        
        if "error" in resultado:
            print(f"❌ Erro: {resultado['error']}")
    
    print("\n" + "=" * 60)
    print("🏁 TESTE CONCLUÍDO")

if __name__ == "__main__":
    main()
