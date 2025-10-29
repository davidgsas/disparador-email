#!/bin/bash

# Script para rodar a aplicação Streamlit com as variáveis de ambiente corretas

echo "🚀 Iniciando Braço Direito..."
echo ""

# Definir variáveis de ambiente para bibliotecas do Homebrew
export DYLD_LIBRARY_PATH="/opt/homebrew/lib:$DYLD_LIBRARY_PATH"
export PKG_CONFIG_PATH="/opt/homebrew/lib/pkgconfig:$PKG_CONFIG_PATH"

# Obter diretório do script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Criar diretório de logs se não existir
mkdir -p logs

# Verificar e iniciar serviço WhatsApp
echo "📱 Verificando serviço WhatsApp..."
if [ -f "whatsapp_service.pid" ]; then
    PID=$(cat whatsapp_service.pid)
    if ps -p $PID > /dev/null 2>&1; then
        echo "✅ Serviço WhatsApp já está rodando (PID: $PID)"
    else
        echo "⚠️  PID antigo encontrado, removendo..."
        rm -f whatsapp_service.pid
        echo "🚀 Iniciando serviço WhatsApp..."
        ./start_whatsapp_daemon.sh
    fi
else
    echo "🚀 Iniciando serviço WhatsApp..."
    ./start_whatsapp_daemon.sh
fi

# Iniciar processador de fila WhatsApp em background
echo "🔄 Iniciando processador de fila WhatsApp..."
if [ -f "whatsapp_queue_processor.pid" ]; then
    PID=$(cat whatsapp_queue_processor.pid)
    if ps -p $PID > /dev/null 2>&1; then
        echo "✅ Processador de fila já está rodando (PID: $PID)"
    else
        echo "⚠️  PID antigo encontrado, removendo..."
        rm -f whatsapp_queue_processor.pid
        echo "🚀 Iniciando processador de fila..."
        nohup ./start_queue_processor.sh > logs/queue_processor.log 2>&1 &
        sleep 2
    fi
else
    echo "🚀 Iniciando processador de fila..."
    nohup ./start_queue_processor.sh > logs/queue_processor.log 2>&1 &
    sleep 2
fi

echo ""
echo "🌐 Iniciando interface Streamlit..."
echo ""

# Ativar ambiente virtual
source venv/bin/activate

# Rodar aplicação
streamlit run streamlit_app.py

