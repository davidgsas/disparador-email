#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Wrapper para iniciar o scheduler com as variáveis de ambiente corretas
"""
import os
import sys
import logging
from datetime import datetime

# Configurar logging logo no início
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scheduler.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

logger.info("="*60)
logger.info(f"INICIANDO run_scheduler.py - {datetime.now()}")
logger.info(f"Python: {sys.version}")
logger.info(f"CWD: {os.getcwd()}")
logger.info(f"Args: {sys.argv}")

# Configurar variáveis de ambiente necessárias para macOS
os.environ['DYLD_LIBRARY_PATH'] = '/opt/homebrew/lib:' + os.environ.get('DYLD_LIBRARY_PATH', '')
os.environ['PKG_CONFIG_PATH'] = '/opt/homebrew/lib/pkgconfig:' + os.environ.get('PKG_CONFIG_PATH', '')

logger.info("Variáveis de ambiente configuradas")

# Iniciar o scheduler
if __name__ == '__main__':
    try:
        logger.info("Importando scheduler_service...")
        import scheduler_service
        logger.info("scheduler_service importado com sucesso")
        
        # Executar o main() se não há comandos CLI
        if len(sys.argv) == 1:
            logger.info("Executando scheduler_service.main()...")
            scheduler_service.main()
        # Se há comandos CLI, o scheduler_service já os processou na importação
    except Exception as e:
        logger.error(f"ERRO ao executar scheduler: {e}")
        import traceback
        logger.error(traceback.format_exc())
        sys.exit(1)