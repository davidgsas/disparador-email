#!/bin/bash

# Script auxiliar para gerenciar o scheduler service
# Uso: ./manage_scheduler.sh [start|stop|restart|status|logs]

PYTHON_EXEC=".venv/bin/python"
SCHEDULER_SCRIPT="scheduler_service.py"
PID_FILE="scheduler.pid"
LOG_FILE="scheduler.log"

case "$1" in
    start)
        echo "🚀 Iniciando scheduler..."
        $PYTHON_EXEC $SCHEDULER_SCRIPT
        sleep 2
        if [ -f "$PID_FILE" ]; then
            PID=$(cat $PID_FILE)
            echo "✅ Scheduler iniciado com PID: $PID"
        else
            echo "❌ Falha ao iniciar scheduler"
            exit 1
        fi
        ;;
    
    stop)
        echo "🛑 Parando scheduler..."
        $PYTHON_EXEC $SCHEDULER_SCRIPT stop
        echo "✅ Scheduler parado"
        ;;
    
    restart)
        echo "🔄 Reiniciando scheduler..."
        $0 stop
        sleep 2
        $0 start
        ;;
    
    reload)
        echo "🔄 Recarregando configurações..."
        $PYTHON_EXEC $SCHEDULER_SCRIPT reload
        echo "✅ Configurações recarregadas"
        ;;
    
    status)
        echo "📊 Status do scheduler:"
        $PYTHON_EXEC $SCHEDULER_SCRIPT status
        ;;
    
    logs)
        if [ -f "$LOG_FILE" ]; then
            echo "📋 Logs do scheduler (últimas 50 linhas):"
            echo "----------------------------------------"
            tail -n 50 $LOG_FILE
        else
            echo "❌ Arquivo de log não encontrado"
        fi
        ;;
    
    follow)
        if [ -f "$LOG_FILE" ]; then
            echo "📋 Acompanhando logs em tempo real (Ctrl+C para sair):"
            echo "----------------------------------------"
            tail -f $LOG_FILE
        else
            echo "❌ Arquivo de log não encontrado"
        fi
        ;;
    
    *)
        echo "Uso: $0 {start|stop|restart|reload|status|logs|follow}"
        echo ""
        echo "Comandos:"
        echo "  start   - Inicia o scheduler em background"
        echo "  stop    - Para o scheduler"
        echo "  restart - Para e reinicia o scheduler"
        echo "  reload  - Recarrega configurações sem parar"
        echo "  status  - Verifica se o scheduler está rodando"
        echo "  logs    - Mostra últimas 50 linhas do log"
        echo "  follow  - Acompanha logs em tempo real"
        exit 1
        ;;
esac
