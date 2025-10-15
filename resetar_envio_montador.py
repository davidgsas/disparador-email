#!/usr/bin/env python3
"""
Script para resetar um envio de montador e permitir novo teste
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

import database as db

def resetar_envio(envio_id):
    """Reseta um envio de montador para estado inicial"""
    
    print(f"🔄 Resetando envio #{envio_id}...")
    
    # Buscar envio atual
    conn = db.get_db_connection()
    with conn.cursor() as cur:
        cur.execute('SELECT * FROM envios_montagem WHERE id = %s', (envio_id,))
        cols = [desc[0] for desc in cur.description]
        row = cur.fetchone()
        
        if not row:
            print(f"❌ Envio #{envio_id} não encontrado!")
            conn.close()
            return False
        
        envio = dict(zip(cols, row))
        
        print(f"\n📋 Dados atuais:")
        print(f"   Montador: {envio['montador_nome']}")
        print(f"   Período: {envio['periodo']}")
        print(f"   Quantidade OS: {envio['quantidade_os']}")
        print(f"   Valor Total: {envio['valor_total']}")
        print(f"   Status: {envio['status']}")
        print(f"   ID Controle: {envio['id_controle']}")
        print(f"   Link: {envio['link_upload']}")
        
        # Resetar campos da API
        cur.execute('''
            UPDATE envios_montagem 
            SET id_controle = NULL,
                link_upload = NULL,
                validade_link = NULL,
                status_api = 0,
                data_envio_api = NULL,
                upload_hash = NULL,
                status_arquivo = 0,
                data_ultima_consulta = NULL,
                nota_fiscal_path = NULL,
                api_message = NULL,
                status = 'Em Aberto'
            WHERE id = %s
        ''', (envio_id,))
        
        conn.commit()
        
    conn.close()
    
    print(f"\n✅ Envio #{envio_id} resetado com sucesso!")
    print(f"\n💡 Agora você pode:")
    print(f"   1. Executar o job de envio para API: python job_enviar_api.py")
    print(f"   2. Ou criar um novo envio com dados diferentes pela interface")
    
    return True

def deletar_envio(envio_id):
    """Deleta completamente um envio de montador"""
    
    print(f"🗑️  Deletando envio #{envio_id}...")
    
    conn = db.get_db_connection()
    with conn.cursor() as cur:
        # Verificar se existe
        cur.execute('SELECT montador_nome, periodo FROM envios_montagem WHERE id = %s', (envio_id,))
        row = cur.fetchone()
        
        if not row:
            print(f"❌ Envio #{envio_id} não encontrado!")
            conn.close()
            return False
        
        montador, periodo = row
        print(f"   Montador: {montador}")
        print(f"   Período: {periodo}")
        
        # Deletar
        cur.execute('DELETE FROM envios_montagem WHERE id = %s', (envio_id,))
        conn.commit()
    
    conn.close()
    
    print(f"\n✅ Envio #{envio_id} deletado com sucesso!")
    return True

if __name__ == '__main__':
    print("="*60)
    print("🔧 GERENCIADOR DE ENVIOS DE MONTADORES")
    print("="*60)
    
    if len(sys.argv) < 2:
        print("\n⚠️  Uso:")
        print("   python resetar_envio_montador.py <envio_id> [acao]")
        print("\nAções:")
        print("   resetar (padrão) - Limpa dados da API mas mantém o envio")
        print("   deletar          - Remove completamente o envio")
        print("\nExemplos:")
        print("   python resetar_envio_montador.py 4")
        print("   python resetar_envio_montador.py 4 resetar")
        print("   python resetar_envio_montador.py 4 deletar")
        sys.exit(1)
    
    envio_id = int(sys.argv[1])
    acao = sys.argv[2] if len(sys.argv) > 2 else 'resetar'
    
    print(f"\n🎯 Envio ID: {envio_id}")
    print(f"🎯 Ação: {acao}")
    print()
    
    if acao == 'deletar':
        deletar_envio(envio_id)
    else:
        resetar_envio(envio_id)
