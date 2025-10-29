#!/bin/bash

# Script para verificar status do serviço WhatsApp

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PID_FILE="$SCRIPT_DIR/whatsapp_service.pid"

if [ ! -f "$PID_FILE" ]; then
    echo "❌ Serviço WhatsApp não está rodando"
    exit 1
fi

PID=$(cat "$PID_FILE")

if ps -p $PID > /dev/null 2>&1; then
    echo "✅ Serviço WhatsApp está rodando"
    echo "📄 PID: $PID"
    echo "🔗 URL: http://localhost:3000"
    echo "📱 QR Code: http://localhost:3000/qr"
    
    # Verificar status via API
    STATUS=$(curl -s http://localhost:3000/status 2>/dev/null)
    if [ $? -eq 0 ]; then
        echo ""
        echo "📊 Status da API:"
        echo "$STATUS" | python3 -m json.tool 2>/dev/null || echo "$STATUS"
    fi
else
    echo "❌ PID $PID não está rodando"
    rm -f "$PID_FILE"
    exit 1
fi
