#!/bin/bash

# Script para parar o serviço WhatsApp

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PID_FILE="$SCRIPT_DIR/whatsapp_service.pid"

if [ ! -f "$PID_FILE" ]; then
    echo "❌ Serviço WhatsApp não está rodando"
    exit 1
fi

PID=$(cat "$PID_FILE")

if ps -p $PID > /dev/null 2>&1; then
    echo "🛑 Parando serviço WhatsApp (PID: $PID)..."
    kill $PID
    
    # Aguardar o processo terminar
    sleep 2
    
    if ps -p $PID > /dev/null 2>&1; then
        echo "⚠️  Forçando encerramento..."
        kill -9 $PID
    fi
    
    rm -f "$PID_FILE"
    echo "✅ Serviço WhatsApp parado"
else
    echo "⚠️  PID $PID não está rodando"
    rm -f "$PID_FILE"
fi
