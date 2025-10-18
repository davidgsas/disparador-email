#!/usr/bin/env python3
"""
Script para iniciar o scheduler com as variáveis de ambiente corretas
"""
import os
import sys

# CRÍTICO: Configurar variáveis de ambiente ANTES de importar qualquer biblioteca
os.environ['DYLD_LIBRARY_PATH'] = '/opt/homebrew/lib:' + os.environ.get('DYLD_LIBRARY_PATH', '')
os.environ['PKG_CONFIG_PATH'] = '/opt/homebrew/lib/pkgconfig:' + os.environ.get('PKG_CONFIG_PATH', '')

# Agora podemos importar o scheduler
import scheduler_service

if __name__ == '__main__':
    print("🚀 Iniciando scheduler com configurações do macOS...")
    scheduler_service.main()
