"""
Script de diagnóstico de notificações
Identifica e corrige problemas com o sistema de notificações
"""

import database as db


def diagnosticar_notificacoes():
    """Diagnostica problemas com notificações"""
    
    print("\n" + "="*70)
    print("🔍 DIAGNÓSTICO DO SISTEMA DE NOTIFICAÇÕES")
    print("="*70)
    
    conn = db.get_db_connection()
    cur = conn.cursor()
    
    try:
        # 1. Contadores gerais
        print("\n📊 ESTATÍSTICAS GERAIS:")
        
        cur.execute("SELECT COUNT(*) FROM notificacoes")
        total = cur.fetchone()[0]
        print(f"   Total de notificações: {total}")
        
        cur.execute("SELECT COUNT(*) FROM notificacoes WHERE lida = false")
        nao_lidas = cur.fetchone()[0]
        print(f"   Não lidas: {nao_lidas}")
        print(f"   Lidas: {total - nao_lidas}")
        
        # 2. Verificar duplicatas por lote
        print("\n🔍 VERIFICAÇÃO DE DUPLICATAS:")
        
        cur.execute("""
            SELECT lote_id, COUNT(*) as qtd, 
                   array_agg(id ORDER BY data_criacao) as ids,
                   array_agg(data_criacao ORDER BY data_criacao) as datas
            FROM notificacoes
            WHERE lote_id IS NOT NULL
            GROUP BY lote_id
            HAVING COUNT(*) > 1
            ORDER BY qtd DESC
            LIMIT 20
        """)
        
        duplicatas = cur.fetchall()
        
        if duplicatas:
            print(f"   ⚠️  {len(duplicatas)} lotes com notificações duplicadas:")
            total_duplicatas = 0
            
            for lote_id, qtd, ids, datas in duplicatas:
                print(f"\n   Lote #{lote_id}: {qtd} notificações")
                print(f"      IDs: {ids}")
                for i, data in enumerate(datas, 1):
                    print(f"         {i}. {data.strftime('%d/%m/%Y %H:%M:%S')}")
                total_duplicatas += (qtd - 1)
            
            print(f"\n   📊 Total de duplicatas: {total_duplicatas}")
            
            # Oferecer limpeza
            print("\n❓ Deseja remover as duplicatas?")
            print("   (Manterá apenas a PRIMEIRA notificação de cada lote)")
            resposta = input("   Digite 's' para confirmar: ").strip().lower()
            
            if resposta == 's':
                print("\n🧹 Removendo duplicatas...")
                
                removidos = 0
                for lote_id, qtd, ids, datas in duplicatas:
                    # Manter apenas o primeiro ID, remover os outros
                    ids_para_remover = ids[1:]  # Todos exceto o primeiro
                    
                    for notif_id in ids_para_remover:
                        cur.execute("DELETE FROM notificacoes WHERE id = %s", (notif_id,))
                        removidos += 1
                        print(f"   ✓ Removida notificação #{notif_id} do lote #{lote_id}")
                
                conn.commit()
                print(f"\n✅ {removidos} duplicatas removidas!")
            else:
                print("   ⏭️  Limpeza cancelada")
        else:
            print("   ✅ Nenhuma duplicata encontrada")
        
        # 3. Notificações sem lote
        print("\n📋 NOTIFICAÇÕES SEM LOTE:")
        
        cur.execute("SELECT COUNT(*) FROM notificacoes WHERE lote_id IS NULL")
        sem_lote = cur.fetchone()[0]
        print(f"   Total: {sem_lote}")
        
        if sem_lote > 0:
            cur.execute("""
                SELECT id, tipo, titulo, data_criacao
                FROM notificacoes
                WHERE lote_id IS NULL
                ORDER BY data_criacao DESC
                LIMIT 5
            """)
            print("   Últimas 5:")
            for notif_id, tipo, titulo, data in cur.fetchall():
                print(f"      #{notif_id} [{tipo}] {titulo[:40]}...")
        
        # 4. Últimas notificações criadas
        print("\n📝 ÚLTIMAS 10 NOTIFICAÇÕES CRIADAS:")
        
        cur.execute("""
            SELECT id, tipo, titulo, lida, data_criacao, lote_id
            FROM notificacoes
            ORDER BY data_criacao DESC
            LIMIT 10
        """)
        
        for row in cur.fetchall():
            notif_id, tipo, titulo, lida, data, lote_id = row
            status_icone = "✓" if lida else "○"
            lote_txt = f"Lote #{lote_id}" if lote_id else "Sem lote"
            data_txt = data.strftime("%d/%m/%Y %H:%M")
            
            print(f"   {status_icone} #{notif_id:3d} [{tipo:12s}] {titulo[:35]:35s} | {lote_txt:10s} | {data_txt}")
        
        # 5. Distribuição por tipo
        print("\n📊 DISTRIBUIÇÃO POR TIPO:")
        
        cur.execute("""
            SELECT tipo, COUNT(*) as qtd, 
                   SUM(CASE WHEN lida THEN 1 ELSE 0 END) as lidas,
                   SUM(CASE WHEN NOT lida THEN 1 ELSE 0 END) as nao_lidas
            FROM notificacoes
            GROUP BY tipo
            ORDER BY qtd DESC
        """)
        
        for tipo, qtd, lidas, nao_lidas in cur.fetchall():
            print(f"   {tipo:15s}: {qtd:3d} total ({lidas:3d} lidas, {nao_lidas:3d} não lidas)")
        
        # 6. Notificações antigas não lidas
        print("\n⏰ NOTIFICAÇÕES ANTIGAS NÃO LIDAS:")
        
        cur.execute("""
            SELECT COUNT(*)
            FROM notificacoes
            WHERE lida = false
            AND data_criacao < NOW() - INTERVAL '7 days'
        """)
        antigas = cur.fetchone()[0]
        
        if antigas > 0:
            print(f"   ⚠️  {antigas} notificações com mais de 7 dias não lidas")
            
            resposta = input("   Deseja marcar como lidas? (s/n): ").strip().lower()
            if resposta == 's':
                cur.execute("""
                    UPDATE notificacoes
                    SET lida = true
                    WHERE lida = false
                    AND data_criacao < NOW() - INTERVAL '7 days'
                """)
                conn.commit()
                print(f"   ✅ {antigas} notificações antigas marcadas como lidas")
        else:
            print("   ✅ Nenhuma notificação antiga pendente")
        
        # 7. Resumo final
        print("\n" + "="*70)
        print("📋 RESUMO DO DIAGNÓSTICO")
        print("="*70)
        
        cur.execute("SELECT COUNT(*) FROM notificacoes")
        total_final = cur.fetchone()[0]
        
        cur.execute("SELECT COUNT(*) FROM notificacoes WHERE lida = false")
        nao_lidas_final = cur.fetchone()[0]
        
        print(f"   Total de notificações: {total_final}")
        print(f"   Não lidas: {nao_lidas_final}")
        print(f"   Lidas: {total_final - nao_lidas_final}")
        
        if duplicatas:
            print(f"   ⚠️  Duplicatas encontradas: Recomenda-se limpeza")
        else:
            print("   ✅ Sistema sem duplicatas")
        
        print("\n✅ Diagnóstico concluído!")
        
    except Exception as e:
        print(f"\n❌ Erro durante diagnóstico: {e}")
        import traceback
        traceback.print_exc()
    finally:
        cur.close()
        conn.close()


if __name__ == '__main__':
    diagnosticar_notificacoes()
