"""
Adiciona o job de backup automático ao banco de dados
"""

import database as db


def adicionar_job_backup():
    """Adiciona configuração do job de backup no banco"""
    
    conn = db.get_db_connection()
    cur = conn.cursor()
    
    try:
        print("🔧 Adicionando job de backup automático...")
        
        # Verificar se já existe
        cur.execute("SELECT COUNT(*) FROM jobs_config WHERE nome = 'backup_banco'")
        existe = cur.fetchone()[0] > 0
        
        if existe:
            print("   ℹ️  Job de backup já existe no banco")
            
            # Atualizar para garantir configuração correta
            cur.execute("""
                UPDATE jobs_config
                SET 
                    descricao = 'Backup automático do banco de dados PostgreSQL',
                    intervalo_minutos = 1440,
                    ativo = true
                WHERE nome = 'backup_banco'
            """)
            print("   ✅ Configuração atualizada")
        else:
            # Inserir novo job
            cur.execute("""
                INSERT INTO jobs_config (
                    nome,
                    descricao,
                    intervalo_minutos,
                    ativo
                ) VALUES (
                    'backup_banco',
                    'Backup automático do banco de dados PostgreSQL',
                    1440,
                    true
                )
            """)
            print("   ✅ Job de backup adicionado")
        
        conn.commit()
        
        # Mostrar configuração
        cur.execute("""
            SELECT nome, descricao, intervalo_minutos, ativo
            FROM jobs_config
            WHERE nome = 'backup_banco'
        """)
        
        job = cur.fetchone()
        nome, descricao, intervalo, ativo = job
        
        print(f"\n📊 Configuração do Job:")
        print(f"   Nome: {nome}")
        print(f"   Descrição: {descricao}")
        print(f"   Intervalo: {intervalo} minutos ({intervalo/60:.1f} horas)")
        print(f"   Status: {'ATIVO ✅' if ativo else 'DESATIVADO ⏸️'}")
        
        # Mostrar todos os jobs
        print(f"\n📋 Todos os Jobs Configurados:")
        cur.execute("""
            SELECT nome, descricao, intervalo_minutos, ativo
            FROM jobs_config
            ORDER BY nome
        """)
        
        for job in cur.fetchall():
            nome, descricao, intervalo, ativo = job
            status = "✅" if ativo else "⏸️"
            print(f"   {status} {nome:20s} - {descricao[:50]:50s} ({intervalo} min)")
        
        print(f"\n✅ Job de backup configurado com sucesso!")
        print(f"\n💡 Próximos passos:")
        print(f"   1. Recarregue o scheduler: ./manage_scheduler.sh reload")
        print(f"   2. Ou reinicie: ./manage_scheduler.sh restart")
        print(f"   3. Verifique os logs: tail -f scheduler.log")
        
    except Exception as e:
        print(f"❌ Erro ao adicionar job: {e}")
        conn.rollback()
        import traceback
        traceback.print_exc()
    finally:
        cur.close()
        conn.close()


if __name__ == '__main__':
    adicionar_job_backup()
