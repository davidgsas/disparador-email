#!/bin/bash

# Script para processar fila de WhatsApp em loop

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Arquivo PID
PID_FILE="whatsapp_queue_processor.pid"

# Salvar PID
echo $$ > "$PID_FILE"

echo "🔄 Processador de fila WhatsApp iniciado (PID: $$)"
echo "📁 Diretório: $SCRIPT_DIR"
echo "⏰ Processando a cada 60 segundos..."
echo ""

# Ativar ambiente virtual
source venv/bin/activate

# Loop infinito
while true; do
    # Executar processamento
    python processar_fila_whatsapp.py >> logs/whatsapp_queue.log 2>&1
    
    # Aguardar 60 segundos
    sleep 60
done
