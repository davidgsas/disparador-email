"""
Script para limpar notificações duplicadas
Mantém apenas a primeira notificação de cada lote
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

import database as db
import psycopg2.extras

print("="*60)
print("🧹 LIMPEZA DE NOTIFICAÇÕES DUPLICADAS")
print("="*60)

conn = db.get_db_connection()
cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

# Buscar notificações duplicadas por lote
print("\n📊 Analisando notificações duplicadas...\n")

cur.execute("""
    SELECT 
        lote_id,
        COUNT(*) as total,
        MIN(id) as primeira_id,
        MAX(data_criacao) as ultima_data
    FROM notificacoes
    WHERE lote_id IS NOT NULL
    GROUP BY lote_id
    HAVING COUNT(*) > 1
    ORDER BY lote_id
""")

duplicadas = cur.fetchall()

if not duplicadas:
    print("✅ Nenhuma notificação duplicada encontrada!")
    cur.close()
    conn.close()
    exit(0)

print(f"⚠️  Encontrados {len(duplicadas)} lotes com notificações duplicadas:\n")

total_para_remover = 0
for dup in duplicadas:
    qtd_duplicadas = dup['total'] - 1
    total_para_remover += qtd_duplicadas
    print(f"  Lote #{dup['lote_id']}: {dup['total']} notificações (remover {qtd_duplicadas})")

print(f"\n📝 Total de notificações a remover: {total_para_remover}")

# Pedir confirmação
resposta = input("\n❓ Deseja remover as duplicadas? (s/N): ")

if resposta.lower() != 's':
    print("❌ Operação cancelada")
    cur.close()
    conn.close()
    exit(0)

print("\n🗑️  Removendo notificações duplicadas...\n")

# Para cada lote, manter apenas a primeira notificação
removidas = 0
for dup in duplicadas:
    lote_id = dup['lote_id']
    primeira_id = dup['primeira_id']
    
    # Remover todas exceto a primeira
    cur.execute("""
        DELETE FROM notificacoes
        WHERE lote_id = %s AND id != %s
        RETURNING id
    """, (lote_id, primeira_id))
    
    ids_removidos = cur.fetchall()
    qtd = len(ids_removidos)
    removidas += qtd
    
    print(f"  ✓ Lote #{lote_id}: {qtd} notificações removidas")

conn.commit()

print(f"\n✅ Total removido: {removidas} notificações")
print(f"✅ Mantidas: {len(duplicadas)} notificações (uma por lote)")

# Estatísticas finais
cur.execute("SELECT COUNT(*) FROM notificacoes")
result = cur.fetchone()
total_final = result['count'] if isinstance(result, dict) else result[0]

cur.execute("SELECT COUNT(*) FROM notificacoes WHERE lida = false")
result = cur.fetchone()
nao_lidas = result['count'] if isinstance(result, dict) else result[0]

print(f"\n📊 ESTATÍSTICAS FINAIS:")
print(f"  Total de notificações: {total_final}")
print(f"  Não lidas: {nao_lidas}")
print(f"  Lidas: {total_final - nao_lidas}")

cur.close()
conn.close()

print("\n" + "="*60)
print("✅ LIMPEZA CONCLUÍDA")
print("="*60)
