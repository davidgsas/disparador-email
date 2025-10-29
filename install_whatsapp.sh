#!/bin/bash

echo "🚀 Instalando serviço WhatsApp..."
echo ""

# Verificar se o Node.js está instalado
if ! command -v node &> /dev/null; then
    echo "❌ Node.js não encontrado!"
    echo ""
    echo "📥 Instalando Node.js via Homebrew..."
    
    # Verificar se o Homebrew está instalado
    if ! command -v brew &> /dev/null; then
        echo "❌ Homebrew não encontrado!"
        echo ""
        echo "Para instalar o Homebrew, execute:"
        echo '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
        echo ""
        echo "Depois, execute este script novamente."
        exit 1
    fi
    
    # Instalar Node.js
    brew install node
    
    if [ $? -ne 0 ]; then
        echo "❌ Erro ao instalar Node.js"
        exit 1
    fi
fi

# Verificar versão do Node.js
NODE_VERSION=$(node -v)
echo "✅ Node.js instalado: $NODE_VERSION"

# Verificar versão do npm
NPM_VERSION=$(npm -v)
echo "✅ npm instalado: $NPM_VERSION"

echo ""
echo "📦 Instalando dependências..."
npm install

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Instalação concluída com sucesso!"
    echo ""
    echo "🚀 Para iniciar o serviço, execute:"
    echo "   npm start"
    echo ""
    echo "Ou para desenvolvimento:"
    echo "   npm run dev"
    echo ""
    echo "📱 Depois acesse http://localhost:3000/qr para conectar seu WhatsApp"
else
    echo "❌ Erro ao instalar dependências"
    exit 1
fi
