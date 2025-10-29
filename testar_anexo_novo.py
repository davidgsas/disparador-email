#!/usr/bin/env python3
"""
Script para testar WhatsApp quando uma NF é anexada
Simula o que acontece quando um arquivo é enviado via link
"""

import database as db
import sys

if len(sys.argv) < 2:
    print("Uso: python testar_anexo_novo.py <lote_id>")
    print("\nLotes disponíveis em aberto:")
    
    conn = db.get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        SELECT id, prestador_nome, periodo, valor_total
        FROM lotes_servico 
        WHERE status = 'Em Aberto'
        ORDER BY id DESC 
        LIMIT 10
    ''')
    lotes = cur.fetchall()
    conn.close()
    
    for l in lotes:
        print(f"  #{l[0]:3} - {l[1]:40} - {l[2]:15} - R$ {l[3]:.2f}")
    
    sys.exit(1)

lote_id = int(sys.argv[1])

print(f"\n🧪 TESTE: Simulando anexo de NF no lote #{lote_id}")
print("="*60)

# Simular anexo de arquivo (fake path)
fake_file = f"uploads/lote_{lote_id}/nota_teste_{lote_id}.pdf"

print(f"\n📄 Arquivo fake: {fake_file}")
print(f"🔧 Chamando db.salvar_nota_fiscal()...\n")

# Chamar função que deve disparar o WhatsApp
db.salvar_nota_fiscal(lote_id, fake_file)

print("\n✅ Teste concluído!")
print("\nVerifique:")
print("1. Se o status do lote mudou para 'N.F. RECEBIDA'")
print("2. Se um WhatsApp foi enviado (verifique no celular)")
print("3. Se foi registrado na tabela notificacoes_whatsapp")
