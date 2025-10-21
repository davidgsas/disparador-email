#!/usr/bin/env python3
"""
Serviço de Jobs Automáticos - VERSÃO MELHORADA
Executa jobs agendados em background com melhorias de confiabilidade

MELHORIAS:
- Health check automático
- Retry logic com backoff exponencial
- Timeout para evitar jobs travados
- Logging detalhado
- Monitoramento de performance
- Recuperação automática de falhas
"""

import sys
import os
import signal
import time
import logging
import traceback
from pathlib import Path
from datetime import datetime, timedelta
from threading import Thread, Event
import multiprocessing
from functools import wraps

# CRÍTICO: Configurar método de spawn para evitar crashes no macOS
if sys.platform == 'darwin':
    multiprocessing.set_start_method('spawn', force=True)

# Adicionar diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent))

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR, EVENT_JOB_MISSED
import database as db

# Configurar logging com mais detalhes
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [%(levelname)s] - %(name)s - %(message)s',
    handlers=[
        logging.FileHandler('scheduler.log'),
        logging.FileHandler('scheduler_errors.log', encoding='utf-8'),  # Log separado para erros
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('SchedulerService')

# Configurações globais
HEALTH_CHECK_INTERVAL = 300  # 5 minutos
MAX_RETRIES = 3
RETRY_BACKOFF = [60, 300, 900]  # 1min, 5min, 15min
JOB_TIMEOUT = 600  # 10 minutos por job
MIN_INTERVAL_SECONDS = 30  # Intervalo mínimo entre execuções

# Variáveis globais
scheduler = None
running = True
health_check_thread = None
job_stats = {}  # Estatísticas de execução dos jobs


def timeout_decorator(timeout_seconds):
    """Decorator para adicionar timeout em funções"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = [None]
            exception = [None]
            
            def target():
                try:
                    result[0] = func(*args, **kwargs)
                except Exception as e:
                    exception[0] = e
            
            thread = Thread(target=target, daemon=True)
            thread.start()
            thread.join(timeout=timeout_seconds)
            
            if thread.is_alive():
                raise TimeoutError(f"Job excedeu timeout de {timeout_seconds}s")
            
            if exception[0]:
                raise exception[0]
            
            return result[0]
        return wrapper
    return decorator


def retry_on_failure(max_retries=MAX_RETRIES):
    """Decorator para retry com backoff exponencial"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_retries - 1:
                        wait_time = RETRY_BACKOFF[min(attempt, len(RETRY_BACKOFF) - 1)]
                        logger.warning(
                            f"⚠️  Tentativa {attempt + 1}/{max_retries} falhou. "
                            f"Aguardando {wait_time}s antes de tentar novamente. Erro: {e}"
                        )
                        time.sleep(wait_time)
                    else:
                        logger.error(f"❌ Todas as {max_retries} tentativas falharam")
            
            raise last_exception
        return wrapper
    return decorator


def atualizar_estatisticas(job_nome, sucesso, tempo_execucao, erro=None):
    """Atualiza estatísticas de execução do job"""
    if job_nome not in job_stats:
        job_stats[job_nome] = {
            'total_execucoes': 0,
            'sucessos': 0,
            'falhas': 0,
            'tempo_total': 0,
            'ultimo_sucesso': None,
            'ultima_falha': None,
            'erros_consecutivos': 0
        }
    
    stats = job_stats[job_nome]
    stats['total_execucoes'] += 1
    stats['tempo_total'] += tempo_execucao
    
    if sucesso:
        stats['sucessos'] += 1
        stats['ultimo_sucesso'] = datetime.now()
        stats['erros_consecutivos'] = 0
    else:
        stats['falhas'] += 1
        stats['ultima_falha'] = datetime.now()
        stats['erros_consecutivos'] += 1
    
    # Log de estatísticas
    taxa_sucesso = (stats['sucessos'] / stats['total_execucoes']) * 100
    tempo_medio = stats['tempo_total'] / stats['total_execucoes']
    
    logger.info(
        f"📊 Stats {job_nome}: {stats['total_execucoes']} exec, "
        f"{taxa_sucesso:.1f}% sucesso, {tempo_medio:.1f}s médio"
    )
    
    # Alertar se muitos erros consecutivos
    if stats['erros_consecutivos'] >= 3:
        logger.error(
            f"🚨 ALERTA: Job '{job_nome}' com {stats['erros_consecutivos']} "
            f"erros consecutivos!"
        )


@timeout_decorator(JOB_TIMEOUT)
@retry_on_failure(max_retries=2)
def executar_job_consultar_notas():
    """Executa job de consulta de notas fiscais"""
    job_nome = 'consultar_notas'
    inicio = time.time()
    
    try:
        logger.info(f"🔍 Iniciando job: {job_nome}")
        
        # Verificar se job está ativo
        job_config = db.get_job_config(job_nome)
        if not job_config or not job_config['ativo']:
            logger.info(f"⏸️  Job {job_nome} não está ativo, pulando")
            return
        
        # Importar e executar
        import importlib
        import job_consultar_notas
        from integracoes import trello_integration
        
        # Reload para pegar mudanças
        importlib.reload(trello_integration)
        importlib.reload(job_consultar_notas)
        
        job_consultar_notas.processar_uploads_pendentes()
        
        tempo_execucao = time.time() - inicio
        mensagem = f"Job executado com sucesso em {tempo_execucao:.1f}s"
        
        db.registrar_execucao_job(job_nome, sucesso=True, mensagem=mensagem)
        atualizar_estatisticas(job_nome, True, tempo_execucao)
        logger.info(f"✅ {job_nome}: {mensagem}")
        
    except TimeoutError as e:
        tempo_execucao = time.time() - inicio
        mensagem = f"Timeout após {tempo_execucao:.1f}s"
        db.registrar_execucao_job(job_nome, sucesso=False, mensagem=mensagem)
        atualizar_estatisticas(job_nome, False, tempo_execucao, str(e))
        logger.error(f"⏰ {job_nome}: {mensagem}")
        raise
        
    except Exception as e:
        tempo_execucao = time.time() - inicio
        mensagem = f"Erro: {str(e)}"
        db.registrar_execucao_job(job_nome, sucesso=False, mensagem=mensagem)
        atualizar_estatisticas(job_nome, False, tempo_execucao, str(e))
        logger.error(f"❌ {job_nome}: {mensagem}")
        logger.error(traceback.format_exc())
        raise


@timeout_decorator(JOB_TIMEOUT)
@retry_on_failure(max_retries=2)
def executar_job_enviar_api():
    """Executa job de envio para API"""
    job_nome = 'enviar_api'
    inicio = time.time()
    
    try:
        logger.info(f"📤 Iniciando job: {job_nome}")
        
        # Verificar se job está ativo
        job_config = db.get_job_config(job_nome)
        if not job_config or not job_config['ativo']:
            logger.info(f"⏸️  Job {job_nome} não está ativo, pulando")
            return
        
        from api_upload_client import enviar_lotes_pendentes
        resultado = enviar_lotes_pendentes()
        
        tempo_execucao = time.time() - inicio
        mensagem = (
            f"Processados: {resultado['total']}, "
            f"Sucesso: {resultado['sucesso']}, "
            f"Erros: {resultado['erro']} "
            f"em {tempo_execucao:.1f}s"
        )
        
        sucesso = resultado['erro'] == 0
        db.registrar_execucao_job(job_nome, sucesso=sucesso, mensagem=mensagem)
        atualizar_estatisticas(job_nome, sucesso, tempo_execucao)
        logger.info(f"✅ {job_nome}: {mensagem}")
        
    except Exception as e:
        tempo_execucao = time.time() - inicio
        mensagem = f"Erro: {str(e)}"
        db.registrar_execucao_job(job_nome, sucesso=False, mensagem=mensagem)
        atualizar_estatisticas(job_nome, False, tempo_execucao, str(e))
        logger.error(f"❌ {job_nome}: {mensagem}")
        logger.error(traceback.format_exc())
        raise


@timeout_decorator(JOB_TIMEOUT)
@retry_on_failure(max_retries=2)
def executar_job_backup_banco():
    """Executa job de backup do banco de dados"""
    job_nome = 'backup_banco'
    inicio = time.time()
    
    try:
        logger.info(f"💾 Iniciando job: {job_nome}")
        
        # Verificar se job está ativo
        job_config = db.get_job_config(job_nome)
        if not job_config or not job_config['ativo']:
            logger.info(f"⏸️  Job {job_nome} não está ativo, pulando")
            return
        
        from job_backup_banco import criar_backup_automatico
        sucesso = criar_backup_automatico()
        
        tempo_execucao = time.time() - inicio
        
        if sucesso:
            mensagem = f"Backup criado com sucesso em {tempo_execucao:.1f}s"
            db.registrar_execucao_job(job_nome, sucesso=True, mensagem=mensagem)
            atualizar_estatisticas(job_nome, True, tempo_execucao)
            logger.info(f"✅ {job_nome}: {mensagem}")
        else:
            mensagem = f"Falha ao criar backup após {tempo_execucao:.1f}s"
            db.registrar_execucao_job(job_nome, sucesso=False, mensagem=mensagem)
            atualizar_estatisticas(job_nome, False, tempo_execucao)
            logger.error(f"❌ {job_nome}: {mensagem}")
            raise Exception(mensagem)
        
    except Exception as e:
        tempo_execucao = time.time() - inicio
        mensagem = f"Erro: {str(e)}"
        db.registrar_execucao_job(job_nome, sucesso=False, mensagem=mensagem)
        atualizar_estatisticas(job_nome, False, tempo_execucao, str(e))
        logger.error(f"❌ {job_nome}: {mensagem}")
        logger.error(traceback.format_exc())
        raise


# Mapa de jobs disponíveis
JOBS_DISPONIVEIS = {
    'consultar_notas': executar_job_consultar_notas,
    'enviar_api': executar_job_enviar_api,
    'backup_banco': executar_job_backup_banco
}


def health_check():
    """Verifica saúde do sistema de jobs periodicamente"""
    logger.info("🏥 Health check iniciado")
    
    while running:
        try:
            time.sleep(HEALTH_CHECK_INTERVAL)
            
            if not running:
                break
            
            logger.info("🏥 Executando health check...")
            
            # Verificar se scheduler está rodando
            if scheduler and scheduler.running:
                jobs_ativos = scheduler.get_jobs()
                logger.info(f"✅ Scheduler rodando com {len(jobs_ativos)} jobs")
                
                # Verificar cada job
                for job in jobs_ativos:
                    next_run = job.next_run_time
                    if next_run:
                        tempo_ate = (next_run - datetime.now()).total_seconds()
                        logger.info(f"   {job.name}: próxima execução em {tempo_ate/60:.1f}min")
                
                # Verificar estatísticas
                for job_nome, stats in job_stats.items():
                    if stats['erros_consecutivos'] >= 5:
                        logger.error(
                            f"🚨 CRÍTICO: Job '{job_nome}' com {stats['erros_consecutivos']} "
                            "erros consecutivos! Requer atenção!"
                        )
                    elif stats['total_execucoes'] > 0:
                        taxa = (stats['sucessos'] / stats['total_execucoes']) * 100
                        if taxa < 50:
                            logger.warning(
                                f"⚠️  Job '{job_nome}' com taxa de sucesso baixa: {taxa:.1f}%"
                            )
            else:
                logger.error("❌ Scheduler não está rodando!")
            
            # Testar conexão com banco
            try:
                db.get_jobs_config()
                logger.info("✅ Conexão com banco OK")
            except Exception as e:
                logger.error(f"❌ Erro ao conectar com banco: {e}")
        
        except Exception as e:
            logger.error(f"❌ Erro no health check: {e}")
            logger.error(traceback.format_exc())


def listener_eventos_scheduler(event):
    """Escuta eventos do scheduler para logging"""
    if event.exception:
        logger.error(f"❌ Job {event.job_id} falhou: {event.exception}")
    elif event.code == EVENT_JOB_EXECUTED:
        logger.debug(f"✅ Job {event.job_id} executado")
    elif event.code == EVENT_JOB_MISSED:
        logger.warning(f"⚠️  Job {event.job_id} perdeu execução agendada")


def configurar_jobs():
    """Configura todos os jobs a partir do banco de dados"""
    global scheduler
    
    logger.info("⚙️  Configurando jobs...")
    
    # Remover jobs existentes
    scheduler.remove_all_jobs()
    
    # Buscar configurações
    jobs_config = db.get_jobs_config()
    
    jobs_configurados = 0
    for job_config in jobs_config:
        nome = job_config['nome']
        ativo = job_config['ativo']
        intervalo = job_config['intervalo_minutos']
        
        # Validar intervalo mínimo
        if intervalo * 60 < MIN_INTERVAL_SECONDS:
            logger.warning(
                f"⚠️  Job '{nome}': intervalo de {intervalo}min é muito curto. "
                f"Mínimo: {MIN_INTERVAL_SECONDS/60}min"
            )
            intervalo = MIN_INTERVAL_SECONDS / 60
        
        if not ativo:
            logger.info(f"⏸️  Job '{nome}' está desativado")
            continue
        
        if nome not in JOBS_DISPONIVEIS:
            logger.warning(f"⚠️  Job '{nome}' não encontrado")
            continue
        
        # Adicionar job
        funcao_job = JOBS_DISPONIVEIS[nome]
        
        scheduler.add_job(
            func=funcao_job,
            trigger=IntervalTrigger(minutes=intervalo),
            id=nome,
            name=nome,
            replace_existing=True,
            max_instances=1,  # Evitar execuções paralelas
            misfire_grace_time=300  # 5 minutos de tolerância
        )
        
        # Atualizar próxima execução
        proxima = datetime.now() + timedelta(minutes=intervalo)
        db.atualizar_proxima_execucao_job(nome, proxima)
        
        logger.info(f"✅ Job '{nome}': a cada {intervalo}min, próxima às {proxima.strftime('%H:%M')}")
        jobs_configurados += 1
    
    logger.info(f"✅ {jobs_configurados} jobs configurados")
    return jobs_configurados


def recarregar_configuracoes(signum=None, frame=None):
    """Recarrega configurações dos jobs"""
    logger.info("🔄 Recarregando configurações...")
    try:
        jobs_configurados = configurar_jobs()
        logger.info(f"✅ Configurações recarregadas ({jobs_configurados} jobs)")
    except Exception as e:
        logger.error(f"❌ Erro ao recarregar: {e}")
        logger.error(traceback.format_exc())


def parar_servico(signum=None, frame=None):
    """Para o serviço graciosamente"""
    global running, health_check_thread
    
    logger.info("🛑 Parando serviço...")
    running = False
    
    # Parar health check
    if health_check_thread and health_check_thread.is_alive():
        logger.info("Aguardando health check finalizar...")
        health_check_thread.join(timeout=5)
    
    # Parar scheduler
    if scheduler:
        logger.info("Parando scheduler...")
        scheduler.shutdown(wait=True)
    
    logger.info("✅ Serviço parado com sucesso")
    sys.exit(0)


def verificar_pid_file():
    """Verifica se já existe uma instância rodando"""
    pid_file = Path('scheduler.pid')
    
    if pid_file.exists():
        try:
            with open(pid_file, 'r') as f:
                old_pid = int(f.read().strip())
            
            try:
                os.kill(old_pid, 0)
                logger.error(f"❌ Serviço já rodando (PID: {old_pid})")
                return False
            except OSError:
                pid_file.unlink()
        except Exception as e:
            logger.warning(f"⚠️  Erro ao verificar PID: {e}")
    
    with open(pid_file, 'w') as f:
        f.write(str(os.getpid()))
    
    return True


def remover_pid_file():
    """Remove o arquivo PID"""
    pid_file = Path('scheduler.pid')
    if pid_file.exists():
        try:
            pid_file.unlink()
        except:
            pass


def main():
    global scheduler, running, health_check_thread
    
    logger.info("="*70)
    logger.info("🚀 SERVIÇO DE JOBS AUTOMÁTICOS - VERSÃO MELHORADA")
    logger.info("="*70)
    
    if not verificar_pid_file():
        sys.exit(1)
    
    try:
        # Criar scheduler
        scheduler = BackgroundScheduler(
            timezone='America/Sao_Paulo',
            daemon=True,
            job_defaults={
                'coalesce': True,  # Combinar execuções perdidas
                'max_instances': 1  # Evitar execuções paralelas
            }
        )
        
        # Adicionar listener de eventos
        scheduler.add_listener(
            listener_eventos_scheduler,
            EVENT_JOB_EXECUTED | EVENT_JOB_ERROR | EVENT_JOB_MISSED
        )
        
        # Configurar sinais
        signal.signal(signal.SIGINT, parar_servico)
        signal.signal(signal.SIGTERM, parar_servico)
        signal.signal(signal.SIGHUP, recarregar_configuracoes)
        
        # Configurar jobs
        jobs_configurados = configurar_jobs()
        
        if jobs_configurados == 0:
            logger.warning("⚠️  Nenhum job configurado. Serviço rodando em modo idle.")
        
        # Iniciar scheduler
        scheduler.start()
        logger.info("✅ Scheduler iniciado")
        
        # Iniciar health check em thread separada
        health_check_thread = Thread(target=health_check, daemon=True)
        health_check_thread.start()
        logger.info("✅ Health check iniciado")
        
        logger.info("="*70)
        logger.info("📊 Jobs Configurados:")
        for job in scheduler.get_jobs():
            logger.info(f"   🔹 {job.name}: próxima execução em {job.next_run_time}")
        logger.info("="*70)
        
        logger.info("\n💡 Comandos:")
        logger.info("   - Parar: Ctrl+C ou kill <PID>")
        logger.info("   - Recarregar: kill -HUP <PID>")
        logger.info("   - Logs: tail -f scheduler.log")
        logger.info("   - Erros: tail -f scheduler_errors.log")
        logger.info("\n🔄 Serviço rodando...\n")
        
        # Loop principal
        while running:
            time.sleep(1)
    
    except KeyboardInterrupt:
        logger.info("\n⚠️  Interrompido pelo usuário")
        parar_servico()
    
    except Exception as e:
        logger.error(f"❌ Erro fatal: {e}")
        logger.error(traceback.format_exc())
        parar_servico()
        sys.exit(1)
    
    finally:
        remover_pid_file()


if __name__ == "__main__":
    # CLI
    if len(sys.argv) > 1:
        comando = sys.argv[1].lower()
        pid_file = Path('scheduler.pid')
        
        if comando == "stop":
            if pid_file.exists():
                with open(pid_file, 'r') as f:
                    pid = int(f.read().strip())
                try:
                    os.kill(pid, signal.SIGTERM)
                    print(f"✅ Sinal de parada enviado (PID: {pid})")
                except OSError:
                    print(f"❌ Processo {pid} não encontrado")
                    pid_file.unlink()
            else:
                print("❌ Serviço não está rodando")
            sys.exit(0)
        
        elif comando == "reload":
            if pid_file.exists():
                with open(pid_file, 'r') as f:
                    pid = int(f.read().strip())
                try:
                    os.kill(pid, signal.SIGHUP)
                    print(f"✅ Configurações recarregadas (PID: {pid})")
                except OSError:
                    print(f"❌ Processo {pid} não encontrado")
            else:
                print("❌ Serviço não está rodando")
            sys.exit(0)
        
        elif comando == "status":
            if pid_file.exists():
                with open(pid_file, 'r') as f:
                    pid = int(f.read().strip())
                try:
                    os.kill(pid, 0)
                    print(f"✅ Serviço rodando (PID: {pid})")
                    jobs_config = db.get_jobs_config()
                    print("\n📊 Jobs:")
                    for job in jobs_config:
                        status = "✅" if job['ativo'] else "⏸️"
                        print(f"   {status} {job['nome']}: {job['intervalo_minutos']}min")
                        if job['ultima_execucao']:
                            print(f"      Última: {job['ultima_execucao']}")
                except OSError:
                    print(f"❌ Processo {pid} não encontrado")
                    pid_file.unlink()
            else:
                print("❌ Serviço não está rodando")
            sys.exit(0)
        
        else:
            print(f"❌ Comando desconhecido: {comando}")
            print("\nComandos: start | stop | reload | status")
            sys.exit(1)
    
    main()
