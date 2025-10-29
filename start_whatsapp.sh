#!/bin/bash

echo "🚀 INICIANDO SERVIÇO WHATSAPP"
echo "=============================="
echo ""

# Verificar se as dependências estão instaladas
if [ ! -d "node_modules" ]; then
    echo "❌ Dependências não instaladas!"
    echo ""
    echo "Execute primeiro:"
    echo "  ./install_whatsapp.sh"
    echo ""
    exit 1
fi

# Verificar se o serviço já está rodando
if lsof -Pi :3000 -sTCP:LISTEN -t >/dev/null ; then
    echo "⚠️  Já existe um serviço rodando na porta 3000!"
    echo ""
    read -p "Deseja parar o serviço anterior? (s/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Ss]$ ]]; then
        echo "🛑 Parando serviço anterior..."
        kill $(lsof -t -i:3000)
        sleep 2
    else
        echo "❌ Cancelando..."
        exit 1
    fi
fi

# Iniciar serviço
echo "🚀 Iniciando serviço WhatsApp..."
echo ""
echo "📱 IMPORTANTE:"
echo "   1. O QR Code aparecerá no terminal"
echo "   2. Ou acesse: http://localhost:3000/qr"
echo "   3. Escaneie com WhatsApp > Menu > Aparelhos conectados"
echo ""

npm start
