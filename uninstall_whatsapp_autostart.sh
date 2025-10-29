#!/bin/bash

# Script para desinstalar o serviço de inicialização automática do WhatsApp

PLIST_FILE="com.novomundo.whatsapp.plist"
LAUNCHAGENTS_DIR="$HOME/Library/LaunchAgents"

echo "🗑️  Desinstalando serviço de inicialização automática do WhatsApp..."
echo ""

# Descarregar serviço
echo "🔄 Descarregando serviço..."
launchctl unload "$LAUNCHAGENTS_DIR/$PLIST_FILE" 2>/dev/null

# Remover arquivo plist
if [ -f "$LAUNCHAGENTS_DIR/$PLIST_FILE" ]; then
    echo "🗑️  Removendo arquivo de configuração..."
    rm "$LAUNCHAGENTS_DIR/$PLIST_FILE"
fi

# Parar serviço se estiver rodando
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [ -f "$SCRIPT_DIR/whatsapp_service.pid" ]; then
    echo "🛑 Parando serviço..."
    "$SCRIPT_DIR/stop_whatsapp_daemon.sh"
fi

echo ""
echo "✅ Serviço desinstalado com sucesso!"
echo ""
echo "💡 Para iniciar manualmente, use:"
echo "   ./start_whatsapp_daemon.sh"
