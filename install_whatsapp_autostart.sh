#!/bin/bash

# Script para instalar o serviço de inicialização automática do WhatsApp no macOS

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLIST_FILE="com.novomundo.whatsapp.plist"
LAUNCHAGENTS_DIR="$HOME/Library/LaunchAgents"

echo "🔧 Instalando serviço de inicialização automática do WhatsApp..."
echo ""

# Criar diretório LaunchAgents se não existir
mkdir -p "$LAUNCHAGENTS_DIR"

# Copiar arquivo plist
echo "📋 Copiando arquivo de configuração..."
cp "$SCRIPT_DIR/$PLIST_FILE" "$LAUNCHAGENTS_DIR/"

# Criar diretório de logs
mkdir -p "$SCRIPT_DIR/logs"

# Descarregar serviço anterior (se existir)
echo "🔄 Descarregando serviço anterior (se existir)..."
launchctl unload "$LAUNCHAGENTS_DIR/$PLIST_FILE" 2>/dev/null

# Carregar novo serviço
echo "🚀 Carregando serviço..."
launchctl load "$LAUNCHAGENTS_DIR/$PLIST_FILE"

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Serviço instalado com sucesso!"
    echo ""
    echo "📊 Comandos úteis:"
    echo "   • Verificar status: ./status_whatsapp_daemon.sh"
    echo "   • Parar serviço:    ./stop_whatsapp_daemon.sh"
    echo "   • Iniciar serviço:  ./start_whatsapp_daemon.sh"
    echo ""
    echo "📋 Logs em:"
    echo "   • $SCRIPT_DIR/logs/whatsapp_service.log"
    echo "   • $SCRIPT_DIR/logs/whatsapp_stdout.log"
    echo "   • $SCRIPT_DIR/logs/whatsapp_stderr.log"
    echo ""
    echo "🔗 URLs:"
    echo "   • Status: http://localhost:3000/status"
    echo "   • QR Code: http://localhost:3000/qr"
    echo ""
    echo "⚠️  O serviço será iniciado automaticamente:"
    echo "   • Na próxima reinicialização do Mac"
    echo "   • Se o processo morrer inesperadamente"
    echo ""
    echo "🔄 Para desinstalar o serviço automático, execute:"
    echo "   ./uninstall_whatsapp_autostart.sh"
else
    echo ""
    echo "❌ Erro ao instalar serviço"
    exit 1
fi
