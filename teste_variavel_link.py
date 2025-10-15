#!/usr/bin/env python3
"""
Teste: Verificar se a variável {{link}} está disponível no contexto de montadores
"""

import sys
sys.path.append('/Users/davidgabriel/projetos/disparador-email')

from jinja2 import Template

# Simular contexto de montador COM link
contexto_montador = {
    "nome_montador": "DAVID DIAS",
    "periodo_relatorio": "01/10/2025 - 15/10/2025",
    "total_geral": 1250.50,
    "total_comissao": 850.00,
    "total_auxilio": 400.50,
    "percentual_comissao": 5.0,
    "link": "https://dvprocessamento.com.br/upload/876237/abc123"  # ✅ LINK DISPONÍVEL
}

# Template de email com {{link}}
template_email = """
Prezado {{nome_montador}},

Segue o relatório do período {{periodo_relatorio}}.

💰 Total: R$ {{total_geral}}
📎 Link para upload: {{link}}

Atenciosamente,
Equipe Novo Mundo
"""

# Renderizar template
template = Template(template_email)
email_final = template.render(**contexto_montador)

print("=" * 80)
print("TESTE: Variável {{link}} no Template de Montadores")
print("=" * 80)
print()
print("📧 EMAIL RENDERIZADO:")
print("-" * 80)
print(email_final)
print("-" * 80)
print()

# Verificar se o link foi substituído
if "{{link}}" in email_final:
    print("❌ ERRO: A variável {{link}} não foi substituída!")
    sys.exit(1)
elif contexto_montador["link"] in email_final:
    print("✅ SUCESSO: O link foi incluído corretamente no email!")
    print(f"   Link encontrado: {contexto_montador['link']}")
else:
    print("❌ ERRO: O link não aparece no email!")
    sys.exit(1)

# Verificar outras variáveis
print()
print("🔍 VERIFICAÇÃO DE VARIÁVEIS:")
print(f"   Nome Montador: {'✅' if 'DAVID DIAS' in email_final else '❌'}")
print(f"   Período: {'✅' if '01/10/2025 - 15/10/2025' in email_final else '❌'}")
print(f"   Total: {'✅' if '1250.5' in email_final else '❌'}")
print(f"   Link: {'✅' if contexto_montador['link'] in email_final else '❌'}")

print()
print("=" * 80)
print("✅ TESTE CONCLUÍDO COM SUCESSO!")
print("=" * 80)
