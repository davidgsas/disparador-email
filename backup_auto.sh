#!/bin/bash
# Script de Backup Automático Diário
# Adicione ao crontab para executar automaticamente

cd "$(dirname "$0")"

# Ativar ambiente virtual se existir
if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

# Executar backup
python3 backup_database.py --auto

# Log
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Backup executado" >> backups/backup.log
