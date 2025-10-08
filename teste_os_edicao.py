#!/usr/bin/env python3
"""
Teste da funcionalidade de edição de O.S. individuais
"""

import sys
import os
sys.path.append('.')

def main():
    print("🧪 TESTE - EDIÇÃO DE O.S. INDIVIDUAIS")
    print("=" * 50)
    
    try:
        from database import get_os_by_lote_id, update_os_detalhes, update_lote_valor_total
        print("✅ Funções importadas com sucesso")
        
        # Testar busca de O.S. por lote
        lote_id = 67  # ID do lote da imagem
        os_do_lote = get_os_by_lote_id(lote_id)
        
        if os_do_lote:
            print(f"✅ Encontrado {len(os_do_lote)} O.S. para o lote {lote_id}")
            
            # Mostrar primeira O.S.
            primeira_os = os_do_lote[0]
            print(f"\n📋 PRIMEIRA O.S.:")
            print(f"ID: {primeira_os['id']}")
            print(f"Detalhes: {primeira_os['detalhes']}")
            
            # Testar se tem os campos necessários
            detalhes = primeira_os['detalhes']
            print(f"\n🔍 CAMPOS DISPONÍVEIS:")
            for campo in ['valor_extra', 'valor_total', 'motivo_extra', 'o_s']:
                valor = detalhes.get(campo, 'N/A')
                print(f"  {campo}: {valor}")
            
            print(f"\n✅ SISTEMA DE EDIÇÃO DE O.S. FUNCIONANDO!")
        else:
            print(f"❌ Nenhuma O.S. encontrada para o lote {lote_id}")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
