"""
Script para gerar planilha Excel de exemplo com o novo campo Cliente
Execute: python gerar_planilha_exemplo.py
"""

import pandas as pd
from datetime import datetime, timedelta

# Dados de exemplo
dados_exemplo = [
    {
        "nome_prestador": "João Silva",
        "periodo": "10/2025",
        "o_s": "12345",
        "cliente": "Maria Santos",
        "localidade": "São Paulo - SP",
        "modalidade": "Instalação",
        "data_execucao": "01/10/2025",
        "valor_custo_prestador": 150.00,
        "valor_extra": 0.00,
        "motivo_extra": "",
        "valor_total": 150.00
    },
    {
        "nome_prestador": "João Silva",
        "periodo": "10/2025",
        "o_s": "12346",
        "cliente": "José Oliveira",
        "localidade": "Rio de Janeiro - RJ",
        "modalidade": "Manutenção",
        "data_execucao": "05/10/2025",
        "valor_custo_prestador": 200.00,
        "valor_extra": 50.00,
        "motivo_extra": "Urgência",
        "valor_total": 250.00
    },
    {
        "nome_prestador": "João Silva",
        "periodo": "10/2025",
        "o_s": "12347",
        "cliente": "Ana Costa",
        "localidade": "Belo Horizonte - MG",
        "modalidade": "Reparo",
        "data_execucao": "10/10/2025",
        "valor_custo_prestador": 180.00,
        "valor_extra": 20.00,
        "motivo_extra": "Material extra",
        "valor_total": 200.00
    },
]

# Criar DataFrame
df = pd.DataFrame(dados_exemplo)

# Salvar como Excel
nome_arquivo = "exemplo_prestadores_com_cliente.xlsx"
df.to_excel(nome_arquivo, index=False)

print(f"✅ Planilha de exemplo criada: {nome_arquivo}")
print(f"\n📋 Colunas incluídas:")
for col in df.columns:
    print(f"   - {col}")

print(f"\n📊 Total de linhas: {len(df)}")
print(f"\n💡 Use esta planilha como modelo para importar dados dos prestadores!")
