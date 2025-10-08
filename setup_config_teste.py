#!/usr/bin/env python3
"""
Script para forçar configuração de teste e verificar se funciona
"""

import json
from pathlib import Path

# Criar configuração de teste
config_teste = {
    "prestador_cc": "",
    "prestador_subject": "Novo Mundo Resolve | Nota Fiscal Eletrônica de Prestação de Serviços | Período: {{periodo}} | Prestador: {{nome_prestador}}",
    "prestador_body": "Olá, {{nome_prestador}}.\n\nEspero que esteja tudo bem.\n\nSegue em anexo a relação de boletins finalizados para emissão da nota fiscal referente aos serviços prestados no período de 07/10/2025 a 07/10/2025.\n\nInformamos que nosso sistema foi atualizado. Agora, a nota fiscal deve ser enviada exclusivamente pelo link abaixo, o que garante mais agilidade no processamento e pagamento.\nSomente as notas fiscais enviadas por esse novo sistema serão consideradas para pagamento.\n\n{{link_upload_nf}}\n\nA nota fiscal deve ser emitida com o mesmo valor indicado neste relatório e enviada em até 2 dias úteis após o recebimento deste e-mail.\nNotas enviadas após esse prazo serão incluídas no próximo fechamento.\n\nLembrando que a nota fiscal deve ser emitida para o CNPJ 01.534.080/0008-02.\n",
    "montador_cc": "",
    "montador_subject": "teste",
    "montador_body": "{{link_upload_nf}}",
    "notificacao_nf": {
        "emails": "tiodavidg3@gmail.com",
        "assunto": "🚨 NOTA FISCAL RECEBIDA - {{prestador_nome}} - Lote {{lote_id}}",
        "corpo": "🎉 NOVA NOTA FISCAL RECEBIDA!\n\n📋 **Detalhes do Upload:**\n• **Prestador:** {{prestador_nome}}\n• **Lote:** #{{lote_id}}\n• **Período:** {{periodo}}\n• **Valor Total:** R$ {{valor_total}}\n• **Data/Hora:** {{data_upload}}\n• **Arquivo:** {{arquivo_nome}}\n\n⚡ **Ação Necessária:**\nA nota fiscal foi recebida e está disponível para download no sistema.\n\n🔗 **Acesso Rápido:**\nAcesse o painel de uploads para fazer o download: {{sistema_url}}\n\n---\nEste é um email automático do sistema de gestão de notas fiscais.",
        "prioridade": "Alta",
        "ativo": True
    }
}

# Salvar configuração
config_file = Path("config.json")
with open(config_file, "w", encoding="utf-8") as f:
    json.dump(config_teste, f, indent=4, ensure_ascii=False)

print("✅ Configuração de teste salva com sucesso!")
print("🔄 Agora recarregue o Streamlit e teste novamente")
