"""
Script de Teste - Sistema de Upload de Notas Fiscais
Demonstra o fluxo completo de integração com a API externa
"""

import sys
from pathlib import Path

# Adicionar o diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent))

from upload_api_client import upload_api
import database as db

def teste_completo():
    """Executa teste completo do fluxo de upload"""
    
    print("🧪 TESTE DO SISTEMA DE UPLOAD DE NOTAS FISCAIS")
    print("=" * 60)
    
    # 1. Verificar conectividade
    print("\n1️⃣ Verificando conectividade com API...")
    if upload_api.verificar_conexao():
        print("   ✅ API está online e acessível")
    else:
        print("   ⚠️  API não está acessível (normal em ambiente de teste)")
    
    # 2. Simular criação de lote
    print("\n2️⃣ Simulando criação de lote de serviço...")
    
    prestador_info = {
        'id': 1,
        'nome': 'João Silva Instalações LTDA',
        'email': 'joao.silva@empresa.com.br'
    }
    
    lote_info = {
        'periodo': '10/2025',
        'valor_total': 1250.50,
        'quantidade_os': 5,
        'data_envio': '2025-10-13T14:30:00'
    }
    
    lote_id = 99999  # ID de teste
    
    print(f"   📋 Lote ID: {lote_id}")
    print(f"   👤 Prestador: {prestador_info['nome']}")
    print(f"   💰 Valor Total: R$ {lote_info['valor_total']:.2f}")
    
    # 3. Criar link de upload
    print("\n3️⃣ Criando link de upload via API...")
    success, result = upload_api.criar_link_upload(lote_id, prestador_info, lote_info)
    
    if success:
        print("   ✅ Link criado com sucesso!")
        print(f"   🔗 URL: {result.get('upload_url')}")
        print(f"   🎫 Token: {result.get('token')}")
        print(f"   ⏰ Expira em: {result.get('expires_at')}")
        
        token = result.get('token')
        upload_url = result.get('upload_url')
        
        # 4. Salvar informações no banco
        print("\n4️⃣ Salvando informações no banco de dados...")
        print("   (Em produção, isso seria feito após criar o lote)")
        
        # 5. Consultar status
        print("\n5️⃣ Consultando status do upload...")
        success_status, status_result = upload_api.consultar_status(token)
        
        if success_status:
            print(f"   ✅ Status: {status_result.get('status')}")
            print(f"   📤 Upload realizado: {status_result.get('uploaded')}")
            
            if status_result.get('file_available'):
                print(f"   📄 Arquivo disponível!")
                
                # 6. Download do arquivo
                print("\n6️⃣ Fazendo download do arquivo...")
                save_path = f"uploads/nota_fiscal_lote_{lote_id}.pdf"
                success_download, message = upload_api.download_arquivo(token, save_path)
                
                if success_download:
                    print(f"   ✅ {message}")
                    print(f"   💾 Salvo em: {save_path}")
                else:
                    print(f"   ❌ Erro: {message}")
            else:
                print("   ℹ️  Arquivo ainda não foi enviado pelo prestador")
        else:
            print(f"   ❌ Erro ao consultar status: {status_result}")
    else:
        print(f"   ❌ Erro ao criar link: {result}")
        print("   ℹ️  Isso é esperado se a API externa ainda não está implementada")
    
    # 7. Demonstrar JSON que deve ser enviado
    print("\n" + "=" * 60)
    print("📤 JSON QUE SERÁ ENVIADO PARA A API EXTERNA:")
    print("=" * 60)
    
    import json
    exemplo_json = {
        "lote_id": 12345,
        "prestador": {
            "id": 10,
            "nome": "João Silva Instalações LTDA",
            "email": "joao.silva@empresa.com.br"
        },
        "lote_info": {
            "periodo": "10/2025",
            "valor_total": 1250.50,
            "quantidade_os": 5,
            "data_envio": "2025-10-13T14:30:00"
        },
        "metadata": {
            "sistema": "disparador-email",
            "versao": "1.0",
            "empresa": "Novo Mundo"
        }
    }
    
    print(json.dumps(exemplo_json, indent=2, ensure_ascii=False))
    
    print("\n" + "=" * 60)
    print("✅ TESTE CONCLUÍDO")
    print("=" * 60)
    print()
    print("📝 PRÓXIMOS PASSOS:")
    print("   1. Implementar a API externa seguindo API_UPLOAD_NOTAS_ESPECIFICACAO.md")
    print("   2. Configurar UPLOAD_API_URL e UPLOAD_API_KEY no arquivo .env")
    print("   3. Integrar no fluxo de envio de emails (streamlit_app.py)")
    print("   4. Criar job para consultar status periodicamente")
    print()

if __name__ == "__main__":
    teste_completo()
