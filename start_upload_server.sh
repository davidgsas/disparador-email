#!/bin/bash

# Script para iniciar o servidor de upload de notas fiscais LOCAL
# Este script deve ser executado em paralelo com o aplicativo principal

echo "🚀 Iniciando servidor de Upload de Notas Fiscais (LOCAL)..."
echo "📍 Servidor rodará em: http://localhost:8502"
echo "🔧 Modo: Desenvolvimento Local"
echo ""

# Carregar variáveis de ambiente locais
if [ -f .env.local ]; then
    export $(cat .env.local | xargs)
    echo "✅ Variáveis de ambiente carregadas"
fi

# Ativar ambiente virtual
source .venv/bin/activate

echo "⏳ Iniciando servidor..."
echo "🌐 URL configurada: $UPLOAD_BASE_URL"

# Executar o streamlit na porta 8502 para upload de NF
.venv/bin/python -m streamlit run upload_nf.py --server.port 8502 --server.address localhost --server.headless false

echo "✅ Servidor de upload finalizado!"ipt para iniciar o servidor de upload de notas fiscais LOCAL
# Este script deve ser executado em paralelo com o aplicativo principal

echo "🚀 Iniciando servidor de Upload de Notas Fiscais (LOCAL)..."
echo "📍 Servidor rodará em: http://localhost:8502"
echo "� Modo: Desenvolvimento Local"
echo ""

# Definir ambiente como local
export AMBIENTE=local

# Ativar ambiente virtual e executar o streamlit na porta 8502 para upload de NF
source .venv/bin/activate
.venv/bin/python -m streamlit run upload_nf.py --server.port 8502 --server.address localhost --server.headless false

echo "✅ Servidor de upload iniciado!"
