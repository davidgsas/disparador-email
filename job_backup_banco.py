"""
Job Automático de Backup do Banco de Dados
Cria backups periódicos do PostgreSQL
"""

import os
import subprocess
import datetime
from pathlib import Path
import database as db
import logging

# Configurar logger para este job
logger = logging.getLogger('JobBackupBanco')


def criar_backup_automatico():
    """
    Cria um backup automático do banco de dados PostgreSQL
    """
    
    logger.info(f"\n{'='*60}")
    logger.info(f"💾 JOB DE BACKUP AUTOMÁTICO DO BANCO")
    logger.info(f"{'='*60}")
    logger.info(f"⏰ Executado em: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    
    try:
        # Obter configurações do banco
        import os
        from dotenv import load_dotenv
        load_dotenv()
        
        db_name = os.getenv("DB_NAME", "prestadores")
        db_host = os.getenv("DB_HOST", "localhost")
        db_port = os.getenv("DB_PORT", "5432")
        db_user = os.getenv("DB_USER", "postgres")
        db_pass = os.getenv("DB_PASS", "")
        
        logger.info(f"\n📊 Configuração do Banco:")
        logger.info(f"   Database: {db_name}")
        logger.info(f"   Host: {db_host}")
        logger.info(f"   Port: {db_port}")
        logger.info(f"   User: {db_user}")
        
        # Criar diretório de backups se não existir
        backup_dir = Path("backups")
        backup_dir.mkdir(exist_ok=True)
        logger.info(f"\n📁 Diretório de backups: {backup_dir.absolute()}")
        
        # Gerar nome do arquivo com timestamp
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = backup_dir / f"backup_{timestamp}.sql"
        
        logger.info(f"\n💾 Criando backup: {backup_file.name}")
        
        # Comando pg_dump
        # Nota: PGPASSWORD deve estar configurado ou usar .pgpass
        cmd = [
            'pg_dump',
            '-h', db_host,
            '-p', db_port,
            '-U', db_user,
            '-d', db_name,
            '-F', 'p',  # Plain text format
            '-f', str(backup_file),
            '--verbose'
        ]
        
        # Executar pg_dump
        logger.info(f"   🔄 Executando pg_dump...")
        
        env = os.environ.copy()
        # Adicionar senha no ambiente para pg_dump
        if db_pass:
            env['PGPASSWORD'] = db_pass
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            env=env,
            timeout=300  # 5 minutos timeout
        )
        
        if result.returncode == 0:
            # Verificar tamanho do arquivo
            file_size = backup_file.stat().st_size
            file_size_mb = file_size / (1024 * 1024)
            
            logger.info(f"   ✅ Backup criado com sucesso!")
            logger.info(f"   📊 Tamanho: {file_size_mb:.2f} MB ({file_size:,} bytes)")
            
            # Criar notificação de sucesso
            titulo = "💾 Backup Automático Criado"
            mensagem = f"Backup do banco criado com sucesso: {backup_file.name} ({file_size_mb:.2f} MB)"
            
            db.criar_notificacao(
                tipo='sucesso',
                titulo=titulo,
                mensagem=mensagem,
                lote_id=None,
                icone='💾',
                prioridade=0
            )
            logger.info(f"   🔔 Notificação criada")
            
            # Limpar backups antigos (manter últimos 7 dias)
            limpar_backups_antigos(backup_dir, dias=7)
            
            return True
            
        else:
            error_msg = result.stderr or result.stdout or "Erro desconhecido"
            logger.info(f"   ❌ Erro ao criar backup:")
            logger.info(f"   {error_msg}")
            
            # Criar notificação de erro
            titulo = "❌ Erro no Backup Automático"
            mensagem = f"Falha ao criar backup: {error_msg[:100]}"
            
            db.criar_notificacao(
                tipo='erro',
                titulo=titulo,
                mensagem=mensagem,
                lote_id=None,
                icone='❌',
                prioridade=1
            )
            
            return False
            
    except FileNotFoundError as e:
        logger.info(f"\n❌ ERRO: pg_dump não encontrado no sistema")
        logger.info(f"   Instale o PostgreSQL client tools:")
        logger.info(f"   macOS: brew install postgresql")
        logger.info(f"   Linux: sudo apt-get install postgresql-client")
        return False
        
    except Exception as e:
        logger.info(f"\n❌ ERRO CRÍTICO: {str(e)}")
        import traceback
        traceback.print_exc()
        
        # Criar notificação de erro crítico
        titulo = "❌ Erro Crítico no Backup"
        mensagem = f"Erro ao executar backup: {str(e)[:100]}"
        
        try:
            db.criar_notificacao(
                tipo='erro',
                titulo=titulo,
                mensagem=mensagem,
                lote_id=None,
                icone='❌',
                prioridade=1
            )
        except:
            pass
        
        return False
    
    finally:
        logger.info(f"\n⏰ Concluído em: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        logger.info(f"{'='*60}\n")


def limpar_backups_antigos(backup_dir, dias=7):
    """
    Remove backups mais antigos que X dias
    
    Args:
        backup_dir: Diretório de backups
        dias: Número de dias para manter (padrão: 7)
    """
    
    logger.info(f"\n🧹 Limpando backups antigos (mais de {dias} dias)...")
    
    try:
        # Data limite
        limite = datetime.datetime.now() - datetime.timedelta(days=dias)
        limite_timestamp = limite.timestamp()
        
        # Listar todos os backups
        backups = sorted(backup_dir.glob("backup_*.sql"))
        
        removidos = 0
        tamanho_liberado = 0
        
        for backup in backups:
            # Verificar idade do arquivo
            mtime = backup.stat().st_mtime
            
            if mtime < limite_timestamp:
                # Arquivo antigo, remover
                tamanho = backup.stat().st_size
                data_backup = datetime.datetime.fromtimestamp(mtime)
                
                backup.unlink()
                removidos += 1
                tamanho_liberado += tamanho
                
                logger.info(f"   🗑️  Removido: {backup.name} ({data_backup.strftime('%d/%m/%Y')})")
        
        if removidos > 0:
            tamanho_mb = tamanho_liberado / (1024 * 1024)
            logger.info(f"   ✅ {removidos} backup(s) antigo(s) removido(s)")
            logger.info(f"   💾 Espaço liberado: {tamanho_mb:.2f} MB")
        else:
            logger.info(f"   ✅ Nenhum backup antigo para remover")
            
        # Mostrar total de backups mantidos
        backups_atuais = len(list(backup_dir.glob("backup_*.sql")))
        logger.info(f"   📊 Total de backups mantidos: {backups_atuais}")
        
    except Exception as e:
        logger.info(f"   ⚠️  Erro ao limpar backups antigos: {e}")


def listar_backups():
    """Lista todos os backups disponíveis"""
    
    backup_dir = Path("backups")
    
    if not backup_dir.exists():
        logger.info("📭 Nenhum backup encontrado")
        return
    
    backups = sorted(backup_dir.glob("backup_*.sql"), key=lambda x: x.stat().st_mtime, reverse=True)
    
    if not backups:
        logger.info("📭 Nenhum backup encontrado")
        return
    
    logger.info(f"\n📋 Backups Disponíveis ({len(backups)}):\n")
    
    for i, backup in enumerate(backups, 1):
        stat = backup.stat()
        size_mb = stat.st_size / (1024 * 1024)
        mtime = datetime.datetime.fromtimestamp(stat.st_mtime)
        idade_dias = (datetime.datetime.now() - mtime).days
        
        logger.info(f"{i:2d}. {backup.name}")
        logger.info(f"    📅 Data: {mtime.strftime('%d/%m/%Y %H:%M:%S')}")
        logger.info(f"    💾 Tamanho: {size_mb:.2f} MB")
        logger.info(f"    ⏰ Idade: {idade_dias} dia(s)")
        logger.info()


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "list":
        listar_backups()
    else:
        criar_backup_automatico()
