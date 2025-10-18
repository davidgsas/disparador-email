#!/usr/bin/env python3
"""
Wrapper para iniciar o scheduler com as configurações corretas do macOS
"""
import os
import sys

# CRÍTICO: Configurar variáveis de ambiente ANTES de importar qualquer biblioteca
os.environ['DYLD_LIBRARY_PATH'] = '/opt/homebrew/lib:' + os.environ.get('DYLD_LIBRARY_PATH', '')
os.environ['PKG_CONFIG_PATH'] = '/opt/homebrew/lib/pkgconfig:' + os.environ.get('PKG_CONFIG_PATH', '')

# Adicionar diretório atual ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Importar e executar o scheduler
if __name__ == '__main__':
    import scheduler_service
    # O scheduler_service.py já tem a lógica de verificação de argumentos no final
