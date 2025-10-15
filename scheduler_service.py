#!/usr/bin/env python3
"""
Serviço de Jobs Automáticos
Executa jobs agendados em background usando APScheduler

Este serviço roda continuamente e executa os jobs conforme configurado no banco de dados.
"""

import sys
import os
import signal
import time
import logging
from pathlib import Path
from datetime import datetime, timedelta
import multiprocessing

# CRÍTICO: Configurar método de spawn para evitar crashes no macOS
# macOS tem problemas com fork em processos multi-threaded
if sys.platform == 'darwin':  # macOS
    multiprocessing.set_start_method('spawn', force=True)

# Adicionar diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent))

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import database as db

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scheduler.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('SchedulerService')

# Variável global para o scheduler
scheduler = None
running = True


def executar_job_consultar_notas():
    """Executa job de consulta de notas fiscais"""
    job_nome = 'consultar_notas'
    logger.info(f"🔍 Iniciando job: {job_nome}")
    
    try:
        # Verificar se job está ativo antes de executar
        job_config = db.get_job_config(job_nome)
        if not job_config or not job_config['ativo']:
            logger.info(f"⏸️  Job {job_nome} não está ativo, pulando execução")
            return
        
        # Importar e executar o job
        from job_consultar_notas import processar_uploads_pendentes
        
        processar_uploads_pendentes()
        
        mensagem = "Job executado com sucesso"
        db.registrar_execucao_job(job_nome, sucesso=True, mensagem=mensagem)
        logger.info(f"✅ {job_nome}: {mensagem}")
        
    except Exception as e:
        mensagem = f"Erro: {str(e)}"
        db.registrar_execucao_job(job_nome, sucesso=False, mensagem=mensagem)
        logger.error(f"❌ {job_nome}: {mensagem}", exc_info=True)


def executar_job_enviar_api():
    """Executa job de envio para API"""
    job_nome = 'enviar_api'
    logger.info(f"📤 Iniciando job: {job_nome}")
    
    try:
        # Verificar se job está ativo antes de executar
        job_config = db.get_job_config(job_nome)
        if not job_config or not job_config['ativo']:
            logger.info(f"⏸️  Job {job_nome} não está ativo, pulando execução")
            return
        
        # Importar cliente da API
        from api_upload_client import enviar_lotes_pendentes
        
        resultado = enviar_lotes_pendentes()
        
        mensagem = f"Processados: {resultado['total']}, Sucesso: {resultado['sucesso']}, Erros: {resultado['erro']}"
        
        sucesso = resultado['erro'] == 0
        db.registrar_execucao_job(job_nome, sucesso=sucesso, mensagem=mensagem)
        logger.info(f"✅ {job_nome}: {mensagem}")
        
    except Exception as e:
        mensagem = f"Erro: {str(e)}"
        db.registrar_execucao_job(job_nome, sucesso=False, mensagem=mensagem)
        logger.error(f"❌ {job_nome}: {mensagem}", exc_info=True)


# Mapa de jobs disponíveis
JOBS_DISPONIVEIS = {
    'consultar_notas': executar_job_consultar_notas,
    'enviar_api': executar_job_enviar_api
}


def configurar_jobs():
    """Configura todos os jobs a partir do banco de dados"""
    global scheduler
    
    logger.info("⚙️  Configurando jobs...")
    
    # Remover todos os jobs existentes
    scheduler.remove_all_jobs()
    
    # Buscar configurações do banco
    jobs_config = db.get_jobs_config()
    
    for job_config in jobs_config:
        nome = job_config['nome']
        ativo = job_config['ativo']
        intervalo = job_config['intervalo_minutos']
        
        if not ativo:
            logger.info(f"⏸️  Job '{nome}' está desativado")
            continue
        
        if nome not in JOBS_DISPONIVEIS:
            logger.warning(f"⚠️  Job '{nome}' não encontrado nos jobs disponíveis")
            continue
        
        # Adicionar job ao scheduler
        funcao_job = JOBS_DISPONIVEIS[nome]
        
        scheduler.add_job(
            func=funcao_job,
            trigger=IntervalTrigger(minutes=intervalo),
            id=nome,
            name=nome,
            replace_existing=True
        )
        
        # Calcular próxima execução
        proxima = datetime.now() + timedelta(minutes=intervalo)
        db.atualizar_proxima_execucao_job(nome, proxima)
        
        logger.info(f"✅ Job '{nome}' configurado: a cada {intervalo} minutos")
    
    logger.info("✅ Configuração de jobs concluída")


def recarregar_configuracoes(signum=None, frame=None):
    """Recarrega configurações dos jobs"""
    logger.info("🔄 Recarregando configurações...")
    configurar_jobs()


def parar_servico(signum=None, frame=None):
    """Para o serviço graciosamente"""
    global running
    logger.info("🛑 Parando serviço...")
    running = False
    
    if scheduler:
        scheduler.shutdown()
    
    logger.info("✅ Serviço parado")
    sys.exit(0)


def verificar_pid_file():
    """Verifica se já existe uma instância rodando"""
    pid_file = Path('scheduler.pid')
    
    if pid_file.exists():
        try:
            with open(pid_file, 'r') as f:
                old_pid = int(f.read().strip())
            
            # Verificar se processo ainda existe
            try:
                os.kill(old_pid, 0)
                logger.error(f"❌ Serviço já está rodando (PID: {old_pid})")
                logger.error("   Para parar: kill <PID> ou python scheduler_service.py stop")
                return False
            except OSError:
                # Processo não existe mais, remover PID file
                pid_file.unlink()
        except Exception as e:
            logger.warning(f"⚠️  Erro ao verificar PID file: {e}")
    
    # Criar novo PID file
    with open(pid_file, 'w') as f:
        f.write(str(os.getpid()))
    
    return True


def remover_pid_file():
    """Remove o arquivo PID"""
    pid_file = Path('scheduler.pid')
    if pid_file.exists():
        pid_file.unlink()


def main():
    global scheduler, running
    
    logger.info("="*70)
    logger.info("🚀 SERVIÇO DE JOBS AUTOMÁTICOS")
    logger.info("="*70)
    
    # Verificar se já está rodando
    if not verificar_pid_file():
        sys.exit(1)
    
    try:
        # Criar scheduler
        scheduler = BackgroundScheduler(
            timezone='America/Sao_Paulo',
            daemon=True
        )
        
        # Configurar sinais
        signal.signal(signal.SIGINT, parar_servico)
        signal.signal(signal.SIGTERM, parar_servico)
        signal.signal(signal.SIGHUP, recarregar_configuracoes)
        
        # Configurar jobs
        configurar_jobs()
        
        # Iniciar scheduler
        scheduler.start()
        logger.info("✅ Scheduler iniciado")
        
        logger.info("="*70)
        logger.info("📊 Jobs configurados:")
        for job in scheduler.get_jobs():
            logger.info(f"   - {job.name}: próxima execução em {job.next_run_time}")
        logger.info("="*70)
        
        logger.info("\n💡 Comandos:")
        logger.info("   - Para parar: Ctrl+C ou kill <PID>")
        logger.info("   - Para recarregar config: kill -HUP <PID>")
        logger.info("   - Ver logs: tail -f scheduler.log")
        logger.info("\n🔄 Serviço rodando... (pressione Ctrl+C para parar)\n")
        
        # Loop principal
        while running:
            time.sleep(1)
    
    except KeyboardInterrupt:
        logger.info("\n⚠️  Interrompido pelo usuário")
        parar_servico()
    
    except Exception as e:
        logger.error(f"❌ Erro fatal: {e}", exc_info=True)
        parar_servico()
        sys.exit(1)
    
    finally:
        remover_pid_file()


if __name__ == "__main__":
    # Verificar argumentos
    if len(sys.argv) > 1:
        comando = sys.argv[1].lower()
        
        if comando == "stop":
            # Parar serviço
            pid_file = Path('scheduler.pid')
            if pid_file.exists():
                with open(pid_file, 'r') as f:
                    pid = int(f.read().strip())
                
                try:
                    os.kill(pid, signal.SIGTERM)
                    print(f"✅ Sinal de parada enviado para processo {pid}")
                except OSError:
                    print(f"❌ Processo {pid} não encontrado")
                    pid_file.unlink()
            else:
                print("❌ Serviço não está rodando")
            
            sys.exit(0)
        
        elif comando == "reload":
            # Recarregar configurações
            pid_file = Path('scheduler.pid')
            if pid_file.exists():
                with open(pid_file, 'r') as f:
                    pid = int(f.read().strip())
                
                try:
                    os.kill(pid, signal.SIGHUP)
                    print(f"✅ Sinal de recarga enviado para processo {pid}")
                except OSError:
                    print(f"❌ Processo {pid} não encontrado")
            else:
                print("❌ Serviço não está rodando")
            
            sys.exit(0)
        
        elif comando == "status":
            # Ver status
            pid_file = Path('scheduler.pid')
            if pid_file.exists():
                with open(pid_file, 'r') as f:
                    pid = int(f.read().strip())
                
                try:
                    os.kill(pid, 0)
                    print(f"✅ Serviço está rodando (PID: {pid})")
                    
                    # Mostrar jobs
                    jobs_config = db.get_jobs_config()
                    print("\n📊 Jobs configurados:")
                    for job in jobs_config:
                        status = "✅ Ativo" if job['ativo'] else "⏸️  Inativo"
                        print(f"   {job['nome']}: {status} - a cada {job['intervalo_minutos']}min")
                        if job['ultima_execucao']:
                            print(f"      Última execução: {job['ultima_execucao']}")
                        if job['proxima_execucao']:
                            print(f"      Próxima execução: {job['proxima_execucao']}")
                    
                except OSError:
                    print(f"❌ Processo {pid} não encontrado")
                    pid_file.unlink()
            else:
                print("❌ Serviço não está rodando")
            
            sys.exit(0)
        
        else:
            print(f"❌ Comando desconhecido: {comando}")
            print("\nComandos disponíveis:")
            print("  start   - Inicia o serviço")
            print("  stop    - Para o serviço")
            print("  reload  - Recarrega configurações")
            print("  status  - Ver status do serviço")
            sys.exit(1)
    
    # Iniciar serviço
    main()
