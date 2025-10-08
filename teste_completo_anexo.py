#!/usr/bin/env python3
"""
Teste completo do sistema de notificação com anexo
"""

import sys
import os
import tempfile
sys.path.append('.')

def criar_arquivo_teste():
    """Cria um arquivo PDF de teste"""
    conteudo_pdf = b"""%PDF-1.4
1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj
2 0 obj<</Type/Pages/Kids[3 0 R]/Count 1>>endobj
3 0 obj<</Type/Page/Parent 2 0 R/MediaBox[0 0 612 792]/Contents 4 0 R>>endobj
4 0 obj<</Length 44>>stream
BT /F1 12 Tf 100 700 Td (TESTE ANEXO) Tj ET
endstream endobj
xref 0 5
0000000000 65535 f 
0000000009 00000 n 
0000000058 00000 n 
0000000115 00000 n 
0000000204 00000 n 
trailer<</Size 5/Root 1 0 R>>
startxref 297
%%EOF"""
    
    # Criar arquivo temporário
    with tempfile.NamedTemporaryFile(mode="wb", suffix=".pdf", delete=False) as f:
        f.write(conteudo_pdf)
        return f.name

def main():
    print("🧪 TESTE COMPLETO - NOTIFICAÇÃO COM ANEXO")
    print("=" * 60)
    
    # Criar arquivo de teste
    arquivo_path = criar_arquivo_teste()
    print(f"✅ Arquivo de teste criado: {arquivo_path}")
    print(f"📁 Tamanho: {os.path.getsize(arquivo_path)} bytes")
    
    try:
        # Importar módulos
        from notificacao_nf import enviar_notificacao_nf_upload, get_cached_access_token
        print("✅ Módulos importados com sucesso")
        
        # Verificar token
        token = get_cached_access_token()
        if token:
            print("🔑 Token válido encontrado!")
        else:
            print("⚠️ Token não disponível - será gerado preview")
        
        # Dados de teste
        token_info = ("prestador", "LOTE_TESTE_2025")
        dados_lote = {
            "prestador_nome": "EMPRESA TESTE COM ANEXO LTDA",
            "periodo": "01/10/2025 - 31/10/2025",
            "valor_total": 7500.00
        }
        arquivo_nome = "NF_TESTE_COM_ANEXO_REAL.pdf"
        
        print(f"\n📋 DADOS DO TESTE:")
        print(f"Token Info: {token_info}")
        print(f"Dados Lote: {dados_lote}")
        print(f"Arquivo Nome: {arquivo_nome}")
        print(f"Arquivo Path: {arquivo_path}")
        
        print(f"\n🚀 EXECUTANDO TESTE COMPLETO:")
        print("-" * 40)
        
        # Executar notificação
        resultado = enviar_notificacao_nf_upload(
            token_info, 
            dados_lote, 
            arquivo_nome, 
            token,  # Token do cache (pode ser None)
            arquivo_path  # Arquivo real
        )
        
        print(f"\n📊 RESULTADO:")
        import json
        print(json.dumps(resultado, indent=2, ensure_ascii=False))
        
        if resultado.get("preview"):
            print(f"\n📧 PREVIEW DETALHADO:")
            preview = resultado["preview"]
            print(f"Para: {preview['para']}")
            print(f"Assunto: {preview['assunto']}")
            print(f"Prioridade: {preview['prioridade']}")
            if preview.get('anexo'):
                print(f"Anexo: {preview['anexo']}")
            print(f"Corpo:\n{preview['corpo']}")
        
    finally:
        # Limpar arquivo de teste
        try:
            os.unlink(arquivo_path)
            print(f"\n🧹 Arquivo de teste removido")
        except:
            pass
    
    print(f"\n" + "=" * 60)
    print("🏁 TESTE COMPLETO CONCLUÍDO")

if __name__ == "__main__":
    main()
