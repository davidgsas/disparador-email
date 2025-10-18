#!/bin/bash

# Script para rodar a aplicação Streamlit com as variáveis de ambiente corretas

# Definir variáveis de ambiente para bibliotecas do Homebrew
export DYLD_LIBRARY_PATH="/opt/homebrew/lib:$DYLD_LIBRARY_PATH"
export PKG_CONFIG_PATH="/opt/homebrew/lib/pkgconfig:$PKG_CONFIG_PATH"

# Ativar ambiente virtual
source venv/bin/activate

# Rodar aplicação
streamlit run streamlit_app.py
