#!/usr/bin/env python3
"""
Script de teste para verificar se o scheduler pode ser iniciado
"""

import sys
from pathlib import Path

# Adicionar diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent))

print("🔍 Testando importações...")

try:
    print("   ✓ Importando database...")
    import database as db
    
    print("   ✓ Importando APScheduler...")
    from apscheduler.schedulers.background import BackgroundScheduler
    
    print("   ✓ Importando jobs...")
    import job_consultar_notas
    import job_enviar_api
    import job_backup_banco
    
    print("\n✅ Todas as importações funcionaram!")
    
    print("\n🔍 Testando conexão com banco de dados...")
    conn = db.get_db_connection()
    print("   ✓ Conexão OK!")
    conn.close()
    
    print("\n🔍 Verificando configuração dos jobs...")
    jobs = db.get_jobs_config()
    print(f"   ✓ {len(jobs)} jobs configurados")
    for job in jobs:
        status = "🟢 Ativo" if job['ativo'] else "🔴 Inativo"
        print(f"      {status} {job['nome']} - a cada {job['intervalo_minutos']} minutos")
    
    print("\n✅ Tudo pronto para iniciar o scheduler!")
    
except Exception as e:
    print(f"\n❌ Erro: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
