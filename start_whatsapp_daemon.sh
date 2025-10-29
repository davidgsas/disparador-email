#!/bin/bash

# Script para iniciar serviço WhatsApp automaticamente

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_FILE="$SCRIPT_DIR/logs/whatsapp_service.log"
PID_FILE="$SCRIPT_DIR/whatsapp_service.pid"

# Criar diretório de logs se não existir
mkdir -p "$SCRIPT_DIR/logs"

# Função para verificar se o serviço já está rodando
is_running() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if ps -p $PID > /dev/null 2>&1; then
            return 0
        fi
    fi
    return 1
}

# Verificar se já está rodando
if is_running; then
    echo "✅ Serviço WhatsApp já está rodando (PID: $(cat $PID_FILE))"
    exit 0
fi

# Iniciar serviço
echo "🚀 Iniciando serviço WhatsApp..." | tee -a "$LOG_FILE"
cd "$SCRIPT_DIR"

# Iniciar em background e salvar PID
nohup npm start >> "$LOG_FILE" 2>&1 &
echo $! > "$PID_FILE"

# Aguardar alguns segundos para verificar se iniciou
sleep 5

if is_running; then
    echo "✅ Serviço WhatsApp iniciado com sucesso!" | tee -a "$LOG_FILE"
    echo "📄 PID: $(cat $PID_FILE)" | tee -a "$LOG_FILE"
    echo "📋 Logs em: $LOG_FILE" | tee -a "$LOG_FILE"
else
    echo "❌ Erro ao iniciar serviço WhatsApp" | tee -a "$LOG_FILE"
    rm -f "$PID_FILE"
    exit 1
fi
