#!/usr/bin/env python3
"""
Teste específico para verificar se o sistema de anexos funciona
"""

import sys
import os
sys.path.append('.')

def criar_arquivo_teste():
    """Cria um arquivo PDF de teste"""
    arquivo_teste = "teste_anexo.pdf"
    
    # Criar um PDF simples de teste
    conteudo_pdf = b"""%PDF-1.4
1 0 obj
<<
/Type /Catalog
/Pages 2 0 R
>>
endobj

2 0 obj
<<
/Type /Pages
/Kids [3 0 R]
/Count 1
>>
endobj

3 0 obj
<<
/Type /Page
/Parent 2 0 R
/MediaBox [0 0 612 792]
/Contents 4 0 R
>>
endobj

4 0 obj
<<
/Length 44
>>
stream
BT
/F1 12 Tf
100 700 Td
(NOTA FISCAL DE TESTE) Tj
ET
endstream
endobj

xref
0 5
0000000000 65535 f 
0000000009 00000 n 
0000000058 00000 n 
0000000115 00000 n 
0000000204 00000 n 
trailer
<<
/Size 5
/Root 1 0 R
>>
startxref
297
%%EOF"""
    
    with open(arquivo_teste, "wb") as f:
        f.write(conteudo_pdf)
    
    return os.path.abspath(arquivo_teste)

def main():
    print("🧪 TESTE DE ANEXOS - SISTEMA DE NOTIFICAÇÃO")
    print("=" * 60)
    
    # Criar arquivo de teste
    arquivo_path = criar_arquivo_teste()
    print(f"✅ Arquivo de teste criado: {arquivo_path}")
    print(f"📁 Tamanho: {os.path.getsize(arquivo_path)} bytes")
    
    # Importar módulo
    try:
        from notificacao_nf import enviar_notificacao_nf_upload
        print("✅ Módulo importado com sucesso")
    except Exception as e:
        print(f"❌ Erro na importação: {e}")
        return
    
    # Dados de teste
    token_info = ("prestador", "ANEXO_TEST_123")
    dados_lote = {
        "prestador_nome": "EMPRESA COM ANEXO TESTE LTDA",
        "periodo": "01/10/2025 - 31/10/2025",
        "valor_total": 5000.00
    }
    arquivo_nome = "NF_TESTE_COM_ANEXO.pdf"
    
    print(f"\n📋 DADOS DO TESTE:")
    print(f"Token Info: {token_info}")
    print(f"Dados Lote: {dados_lote}")
    print(f"Arquivo Nome: {arquivo_nome}")
    print(f"Arquivo Path: {arquivo_path}")
    
    print(f"\n🧪 EXECUTANDO TESTE COM ANEXO (SEM TOKEN):")
    print("-" * 40)
    
    # Teste sem token (preview) mas COM anexo
    resultado1 = enviar_notificacao_nf_upload(
        token_info, 
        dados_lote, 
        arquivo_nome, 
        None,  # Sem token
        arquivo_path  # COM anexo
    )
    
    print(f"\n📊 RESULTADO COM ANEXO (PREVIEW):")
    import json
    print(json.dumps(resultado1, indent=2, ensure_ascii=False))
    
    print(f"\n🔑 EXECUTANDO TESTE COM ANEXO E TOKEN FAKE:")
    print("-" * 40)
    
    # Teste com token fake E anexo
    resultado2 = enviar_notificacao_nf_upload(
        token_info, 
        dados_lote, 
        arquivo_nome, 
        "token_fake_com_anexo",  # Token fake
        arquivo_path  # COM anexo
    )
    
    print(f"\n📊 RESULTADO COM ANEXO E TOKEN FAKE:")
    print(json.dumps(resultado2, indent=2, ensure_ascii=False))
    
    # Limpar arquivo de teste
    try:
        os.remove(arquivo_path)
        print(f"\n🧹 Arquivo de teste removido: {arquivo_path}")
    except:
        pass
    
    print(f"\n" + "=" * 60)
    print("🏁 TESTE DE ANEXOS CONCLUÍDO")
    print("💡 Se viu logs de 'Preparando anexo', o sistema funciona!")

if __name__ == "__main__":
    main()
