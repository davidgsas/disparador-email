#!/bin/bash
# Script de Backup Rápido - Uso simples via linha de comando

# Cores para output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo ""
echo "🗄️  Backup Rápido do Banco de Dados"
echo "===================================="
echo ""

# Ir para o diretório do script
cd "$(dirname "$0")"

# Ativar ambiente virtual
if [ -d ".venv" ]; then
    source .venv/bin/activate
else
    echo -e "${RED}❌ Ambiente virtual não encontrado${NC}"
    exit 1
fi

# Executar backup
python backup_database.py --auto

if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}✅ Backup realizado com sucesso!${NC}"
    echo ""
    echo "📋 Listar backups: python backup_database.py"
    echo ""
else
    echo ""
    echo -e "${RED}❌ Erro ao realizar backup${NC}"
    exit 1
fi
