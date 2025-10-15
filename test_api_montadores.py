#!/usr/bin/env python3
"""
Script de teste para verificar se a integração com montadores está funcionando
"""

from database import get_envios_montagem_sem_api, get_montador_by_name
import json

print("🔍 Testando integração de montadores com API...\n")

# 1. Verificar se função get_montador_by_name existe
print("1️⃣ Testando get_montador_by_name...")
try:
    # Tentar buscar um montador qualquer
    montador = get_montador_by_name("Teste")
    print(f"   ✅ Função funciona (retornou: {montador})")
except Exception as e:
    print(f"   ❌ Erro: {e}")

# 2. Verificar envios pendentes
print("\n2️⃣ Verificando envios de montadores pendentes...")
try:
    envios = get_envios_montagem_sem_api()
    print(f"   ℹ️  Encontrados {len(envios)} envios pendentes")
    
    if envios:
        print("\n   📋 Detalhes dos envios:")
        for envio in envios[:3]:  # Mostrar apenas os 3 primeiros
            print(f"\n   Envio #{envio['id']}:")
            print(f"      Montador: {envio.get('montador_nome', 'N/A')}")
            print(f"      Período: {envio.get('periodo', 'N/A')}")
            print(f"      Valor: R$ {envio.get('valor_total', 0):.2f}")
            print(f"      Data envio: {envio.get('data_envio', 'N/A')}")
            
            # Verificar detalhes JSONB
            detalhes = envio.get('detalhes', {})
            if isinstance(detalhes, str):
                detalhes = json.loads(detalhes)
            
            qtd_os = detalhes.get('quantidade_os', 0) if detalhes else 0
            print(f"      Quantidade OS: {qtd_os}")
    else:
        print("   ⚠️  Nenhum envio pendente encontrado")
        print("   💡 Dica: Crie um envio de montagem para testar")
        
except Exception as e:
    print(f"   ❌ Erro: {e}")
    import traceback
    traceback.print_exc()

# 3. Teste de preparação de payload (mock)
print("\n3️⃣ Simulando preparação de payload...")
if envios:
    try:
        from api_upload_client import APIUploadClient
        
        client = APIUploadClient()
        envio_teste = envios[0]
        
        print(f"   📦 Preparando payload para envio #{envio_teste['id']}...")
        payload = client.preparar_payload(envio_teste, tipo='montagem')
        
        print(f"   ✅ Payload gerado com sucesso:")
        print(f"      Nome: {payload.get('nome')}")
        print(f"      Email: {payload.get('email')}")
        print(f"      Período: {payload.get('periodo')}")
        print(f"      Valor: R$ {payload.get('valor_total'):.2f}")
        print(f"      Quantidade OS: {payload.get('quantidade_os')}")
        print(f"      Data envio: {payload.get('data_envio')}")
        print(f"      Lote ID: {payload.get('lote_id')}")
        print(f"      Tipo: {payload.get('tipo')}")
        
    except Exception as e:
        print(f"   ❌ Erro ao preparar payload: {e}")
        import traceback
        traceback.print_exc()
else:
    print("   ⏭️  Pulando (sem envios para testar)")

print("\n✅ Teste concluído!")
