#!/usr/bin/env python3
"""
Script de teste para verificar o sistema de notificações
"""

import json
from pathlib import Path
import sys
sys.path.append('.')

from notificacao_nf import preview_notificacao, enviar_notificacao_nf_upload

def main():
    print("🧪 TESTE DO SISTEMA DE NOTIFICAÇÕES")
    print("=" * 50)
    
    # 1. Verificar se config existe
    config_file = Path("config.json")
    if config_file.exists():
        with open(config_file, "r", encoding="utf-8") as f:
            config = json.load(f)
        
        print("✅ Arquivo config.json encontrado")
        
        if "notificacao_nf" in config:
            print("✅ Configuração de notificação encontrada")
            notif_config = config["notificacao_nf"]
            print(f"📧 Emails: {notif_config.get('emails', 'NÃO DEFINIDO')}")
            print(f"🏷️  Assunto: {notif_config.get('assunto', 'NÃO DEFINIDO')}")
            print(f"⚡ Ativo: {notif_config.get('ativo', False)}")
            print(f"📈 Prioridade: {notif_config.get('prioridade', 'NÃO DEFINIDO')}")
        else:
            print("❌ Configuração de notificação NÃO encontrada")
            return
    else:
        print("❌ Arquivo config.json não encontrado")
        return
    
    print("\n" + "=" * 50)
    print("🧪 TESTANDO PREVIEW...")
    
    # 2. Testar preview
    resultado = preview_notificacao("prestador", "TEST123", "invoice_test.pdf")
    
    if resultado.get("success", False) or "preview" in resultado:
        print("✅ Preview gerado com sucesso!")
        if "preview" in resultado:
            preview = resultado["preview"]
            print(f"📧 Para: {', '.join(preview['para'])}")
            print(f"📋 Assunto: {preview['assunto']}")
            print(f"⚡ Prioridade: {preview['prioridade']}")
            print(f"📝 Corpo (primeiros 100 chars): {preview['corpo'][:100]}...")
        
        print("\n" + "=" * 50)
        print("🚀 SIMULANDO ENVIO COMPLETO...")
        
        # 3. Testar função completa sem token (para debug)
        dados_teste = {
            "prestador_nome": "EMPRESA TESTE LTDA",
            "periodo": "01/10/2025 - 31/10/2025",
            "valor_total": 9876.54
        }
        
        resultado_completo = enviar_notificacao_nf_upload(
            ("prestador", "LOTE999"),
            dados_teste,
            "NF_TESTE_COMPLETA.pdf",
            access_token=None  # Sem token para ver preview
        )
        
        if "preview" in resultado_completo:
            print("✅ Teste completo - Preview gerado!")
            preview_completo = resultado_completo["preview"]
            print(f"📧 Destinatários: {', '.join(preview_completo['para'])}")
            print(f"📋 Assunto Final: {preview_completo['assunto']}")
            print(f"⚡ Prioridade: {preview_completo['prioridade']}")
            print(f"\n📝 CORPO COMPLETO:")
            print("-" * 40)
            print(preview_completo['corpo'])
            print("-" * 40)
        else:
            print(f"❌ Erro no teste completo: {resultado_completo.get('message', 'Erro desconhecido')}")
    else:
        print(f"❌ Erro no preview: {resultado.get('message', 'Erro desconhecido')}")
        if "error" in resultado:
            print(f"🔍 Detalhes: {resultado['error']}")

if __name__ == "__main__":
    main()
