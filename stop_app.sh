#!/bin/bash

# Script para parar todos os serviços

echo "🛑 Parando serviços do Braço Direito..."
echo ""

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Parar serviço WhatsApp
if [ -f "whatsapp_service.pid" ]; then
    echo "📱 Parando serviço WhatsApp..."
    ./stop_whatsapp_daemon.sh
    echo ""
fi

# Parar Streamlit (buscar processo)
STREAMLIT_PID=$(ps aux | grep "streamlit run" | grep -v grep | awk '{print $2}')
if [ ! -z "$STREAMLIT_PID" ]; then
    echo "🌐 Parando Streamlit (PID: $STREAMLIT_PID)..."
    kill $STREAMLIT_PID
    echo "✅ Streamlit parado"
    echo ""
fi

echo "✅ Todos os serviços foram parados"
