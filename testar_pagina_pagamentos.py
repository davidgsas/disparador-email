"""
Teste da página de pagamentos vencidos
"""
import sys
sys.path.insert(0, '/Users/david/Documents/GitHub/disparador-email')

print("="*60)
print("🧪 TESTE DA PÁGINA DE PAGAMENTOS VENCIDOS")
print("="*60)

# 1. Testar importação
print("\n1️⃣ Testando importação...")
try:
    from pagina_pagamentos_vencidos import pagina_pagamentos_vencidos, classificar_pagamentos, mostrar_card_pagamento
    print("   ✅ Módulo importado com sucesso")
except Exception as e:
    print(f"   ❌ Erro na importação: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# 2. Testar função do banco
print("\n2️⃣ Testando função get_todos_pagamentos_pendentes...")
try:
    from database import get_todos_pagamentos_pendentes
    resultado = get_todos_pagamentos_pendentes()
    print(f"   ✅ Função executada")
    print(f"   📊 Serviços: {len(resultado['servicos'])}")
    print(f"   📊 Montagens: {len(resultado['montagens'])}")
except Exception as e:
    print(f"   ❌ Erro: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# 3. Testar classificação
print("\n3️⃣ Testando classificação de pagamentos...")
try:
    if resultado['servicos']:
        categorias = classificar_pagamentos(resultado['servicos'])
        print(f"   ✅ Classificação executada")
        print(f"   🔴 Vencidos: {len(categorias['vencidos'])}")
        print(f"   ⚠️  Hoje: {len(categorias['hoje'])}")
        print(f"   🟡 Amanhã: {len(categorias['amanha'])}")
        print(f"   🟢 2-3 dias: {len(categorias['proximos_3dias'])}")
        print(f"   🔵 4-10 dias: {len(categorias['proximos_10dias'])}")
        print(f"   ⚪ >10 dias: {len(categorias['futuros'])}")
        
        # Mostrar detalhes
        if categorias['vencidos']:
            print(f"\n   📋 Exemplo de vencido:")
            v = categorias['vencidos'][0]
            print(f"      ID: {v['id']}")
            print(f"      Prestador: {v['prestador_nome']}")
            print(f"      Dias: {v['dias_para_vencimento']}")
            print(f"      Vencimento: {v.get('data_vencimento_pagamento')}")
        
        if categorias['proximos_10dias']:
            print(f"\n   📋 Exemplo de próximo (4-10 dias):")
            p = categorias['proximos_10dias'][0]
            print(f"      ID: {p['id']}")
            print(f"      Prestador: {p['prestador_nome']}")
            print(f"      Dias: {p['dias_para_vencimento']}")
            print(f"      Vencimento: {p.get('data_vencimento_pagamento')}")
    else:
        print(f"   ℹ️  Nenhum serviço pendente para classificar")
        
except Exception as e:
    print(f"   ❌ Erro: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# 4. Verificar dados completos
print("\n4️⃣ Verificando estrutura dos dados...")
try:
    if resultado['servicos']:
        exemplo = resultado['servicos'][0]
        print(f"   ✅ Campos disponíveis:")
        for key in exemplo.keys():
            valor = exemplo[key]
            if valor is not None:
                print(f"      • {key}: {type(valor).__name__}")
            else:
                print(f"      • {key}: None")
except Exception as e:
    print(f"   ❌ Erro: {e}")

print("\n" + "="*60)
print("✅ Teste concluído!")
print("="*60)
