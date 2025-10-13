#!/usr/bin/env python3
"""
Sistema de Backup Automático do Banco de Dados PostgreSQL
Realiza backups completos e mantém histórico configurável
"""

import os
import subprocess
import datetime
from pathlib import Path
from dotenv import load_dotenv
import shutil

load_dotenv()

# Configurações
BACKUP_DIR = Path("backups")
MAX_BACKUPS = 30  # Manter últimos 30 backups
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "email")
DB_USER = os.getenv("DB_USER", "davidgabriel")
DB_PORT = os.getenv("DB_PORT", "5432")

def criar_diretorio_backup():
    """Cria o diretório de backups se não existir"""
    BACKUP_DIR.mkdir(exist_ok=True)
    return BACKUP_DIR

def gerar_nome_backup():
    """Gera nome do arquivo de backup com timestamp"""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"backup_{DB_NAME}_{timestamp}.sql"

def realizar_backup():
    """Realiza o backup do banco de dados usando pg_dump"""
    try:
        backup_dir = criar_diretorio_backup()
        backup_file = backup_dir / gerar_nome_backup()
        
        print(f"🔄 Iniciando backup do banco '{DB_NAME}'...")
        
        # Comando pg_dump
        cmd = [
            "pg_dump",
            "-h", DB_HOST,
            "-p", DB_PORT,
            "-U", DB_USER,
            "-F", "c",  # Formato custom (comprimido)
            "-b",  # Incluir large objects
            "-v",  # Verbose
            "-f", str(backup_file),
            DB_NAME
        ]
        
        # Executar backup
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            # Obter tamanho do arquivo
            size_mb = backup_file.stat().st_size / (1024 * 1024)
            print(f"✅ Backup concluído com sucesso!")
            print(f"📁 Arquivo: {backup_file}")
            print(f"📊 Tamanho: {size_mb:.2f} MB")
            return True, str(backup_file)
        else:
            print(f"❌ Erro ao realizar backup:")
            print(result.stderr)
            return False, result.stderr
            
    except Exception as e:
        print(f"❌ Erro ao realizar backup: {str(e)}")
        return False, str(e)

def listar_backups():
    """Lista todos os backups disponíveis"""
    if not BACKUP_DIR.exists():
        return []
    
    backups = sorted(
        BACKUP_DIR.glob("backup_*.sql"),
        key=lambda x: x.stat().st_mtime,
        reverse=True
    )
    
    return backups

def limpar_backups_antigos():
    """Remove backups antigos mantendo apenas os MAX_BACKUPS mais recentes"""
    backups = listar_backups()
    
    if len(backups) > MAX_BACKUPS:
        backups_para_remover = backups[MAX_BACKUPS:]
        print(f"\n🗑️  Removendo {len(backups_para_remover)} backup(s) antigo(s)...")
        
        for backup in backups_para_remover:
            backup.unlink()
            print(f"   Removido: {backup.name}")
        
        print(f"✅ Mantidos {MAX_BACKUPS} backups mais recentes")

def restaurar_backup(backup_file):
    """Restaura um backup específico"""
    try:
        if not Path(backup_file).exists():
            print(f"❌ Arquivo de backup não encontrado: {backup_file}")
            return False
        
        print(f"⚠️  ATENÇÃO: Isso irá SUBSTITUIR todos os dados do banco '{DB_NAME}'!")
        confirmacao = input("Digite 'CONFIRMAR' para prosseguir: ")
        
        if confirmacao != "CONFIRMAR":
            print("❌ Operação cancelada")
            return False
        
        print(f"🔄 Restaurando backup: {backup_file}")
        
        # Comando pg_restore
        cmd = [
            "pg_restore",
            "-h", DB_HOST,
            "-p", DB_PORT,
            "-U", DB_USER,
            "-d", DB_NAME,
            "-c",  # Clean (drop) database objects before recreating
            "-v",  # Verbose
            str(backup_file)
        ]
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print(f"✅ Backup restaurado com sucesso!")
            return True
        else:
            # pg_restore pode retornar warnings que não são erros críticos
            if "ERROR" in result.stderr:
                print(f"❌ Erro ao restaurar backup:")
                print(result.stderr)
                return False
            else:
                print(f"✅ Backup restaurado (com alguns warnings)")
                return True
            
    except Exception as e:
        print(f"❌ Erro ao restaurar backup: {str(e)}")
        return False

def exibir_menu():
    """Exibe o menu interativo"""
    print("\n" + "="*60)
    print("🗄️  SISTEMA DE BACKUP - BANCO DE DADOS")
    print("="*60)
    print(f"Banco: {DB_NAME}")
    print(f"Host: {DB_HOST}:{DB_PORT}")
    print(f"Diretório: {BACKUP_DIR.absolute()}")
    print("="*60)
    print("\n1. Criar novo backup")
    print("2. Listar backups disponíveis")
    print("3. Restaurar backup")
    print("4. Limpar backups antigos")
    print("5. Sair")
    print()

def main():
    """Função principal"""
    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ").strip()
        
        if opcao == "1":
            print()
            sucesso, info = realizar_backup()
            if sucesso:
                limpar_backups_antigos()
        
        elif opcao == "2":
            backups = listar_backups()
            if not backups:
                print("\n📭 Nenhum backup encontrado")
            else:
                print(f"\n📋 {len(backups)} backup(s) disponível(eis):\n")
                for i, backup in enumerate(backups, 1):
                    size_mb = backup.stat().st_size / (1024 * 1024)
                    mtime = datetime.datetime.fromtimestamp(backup.stat().st_mtime)
                    print(f"{i:2d}. {backup.name}")
                    print(f"    📊 {size_mb:.2f} MB | 📅 {mtime.strftime('%d/%m/%Y %H:%M:%S')}")
        
        elif opcao == "3":
            backups = listar_backups()
            if not backups:
                print("\n📭 Nenhum backup disponível para restaurar")
            else:
                print(f"\n📋 Backups disponíveis:\n")
                for i, backup in enumerate(backups, 1):
                    mtime = datetime.datetime.fromtimestamp(backup.stat().st_mtime)
                    print(f"{i}. {backup.name} ({mtime.strftime('%d/%m/%Y %H:%M:%S')})")
                
                try:
                    escolha = int(input("\nNúmero do backup para restaurar (0 para cancelar): "))
                    if escolha > 0 and escolha <= len(backups):
                        restaurar_backup(backups[escolha - 1])
                except ValueError:
                    print("❌ Opção inválida")
        
        elif opcao == "4":
            limpar_backups_antigos()
        
        elif opcao == "5":
            print("\n👋 Até logo!")
            break
        
        else:
            print("\n❌ Opção inválida")
        
        if opcao != "5":
            input("\nPressione ENTER para continuar...")

if __name__ == "__main__":
    import sys
    
    # Modo automático (sem interação)
    if len(sys.argv) > 1 and sys.argv[1] == "--auto":
        print(f"\n[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Executando backup automático...")
        sucesso, info = realizar_backup()
        if sucesso:
            limpar_backups_antigos()
        sys.exit(0 if sucesso else 1)
    
    # Modo interativo
    main()
