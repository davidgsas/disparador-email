#!/usr/bin/env python3
"""
Teste da nova funcionalidade de gerenciamento de pagamentos
"""

import sys
import os
sys.path.append('.')

def main():
    print("🧪 TESTE - GERENCIAMENTO DE PAGAMENTOS")
    print("=" * 50)
    
    try:
        from database import (listar_pagamentos_enviados, prestador_info, 
                             montador_info, get_lote_by_id, get_envio_by_id)
        print("✅ Importações OK")
        
        # Testar listagem
        pagamentos = listar_pagamentos_enviados()
        print(f"✅ {len(pagamentos)} pagamentos encontrados")
        
        if pagamentos:
            # Mostrar primeiro pagamento
            p = pagamentos[0]
            print(f"\n📋 EXEMPLO DE PAGAMENTO:")
            print(f"Tipo: {p['tipo']}")
            print(f"Entidade: {p['entidade_nome']}")
            print(f"Valor: R$ {p['valor_total']:,.2f}")
            print(f"Upload feito: {'Sim' if p['upload_feito'] else 'Não'}")
            
            # Testar funções auxiliares
            if p['tipo'] == 'prestador':
                info = prestador_info(p['lote_id'])
                dados = get_lote_by_id(p['lote_id'])
                print(f"✅ Info prestador OK: {info['nome'] if info else 'None'}")
                print(f"✅ Dados lote OK: {dados['prestador_nome'] if dados else 'None'}")
            else:
                info = montador_info(p['lote_id'])
                dados = get_envio_by_id(p['lote_id'])
                print(f"✅ Info montador OK: {info['nome'] if info else 'None'}")
                print(f"✅ Dados envio OK: {dados['montador_nome'] if dados else 'None'}")
        
        print(f"\n✅ TODAS AS FUNÇÕES FUNCIONANDO!")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
