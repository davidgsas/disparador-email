#!/usr/bin/env python3
"""
Script para configurar valores padrão completos no config.json
"""

import json
from pathlib import Path

def setup_default_config():
    config_file = Path("config.json")
    
    # Configuração completa com valores padrão
    default_config = {
        "prestador_cc": "projetos.qualidade@novomundo.com.br",
        "prestador_subject": "Novo Mundo Resolve | Nota Fiscal Eletrônica de Prestação de Serviços | Período: {{periodo}} | Prestador: {{nome_prestador}}",
        "prestador_body": "Olá, {{nome_prestador}}.\n\nEspero que esteja tudo bem.\n\nSegue em anexo a relação de boletins finalizados para emissão da nota fiscal referente aos serviços prestados no período de {{periodo}}.\n\nInformamos que nosso sistema foi atualizado. Agora, a nota fiscal deve ser enviada exclusivamente pelo link abaixo, o que garante mais agilidade no processamento e pagamento.\nSomente as notas fiscais enviadas por esse novo sistema serão consideradas para pagamento.\n\n{{link_upload_nf}}\n\nA nota fiscal deve ser emitida com o mesmo valor indicado neste relatório e enviada em até 2 dias úteis após o recebimento deste e-mail.\nNotas enviadas após esse prazo serão incluídas no próximo fechamento.\n\nLembrando que a nota fiscal deve ser emitida para o CNPJ 01.534.080/0008-02.\n\nAtenciosamente,\nEquipe Novo Mundo",
        "montador_cc": "projetos.qualidade@novomundo.com.br",
        "montador_subject": "Relatório de Pagamento de Montagem - Período: {{periodo_relatorio}}",
        "montador_body": "Olá, {{nome_montador}},\n\nSegue em anexo o seu relatório de pagamento de montagens referente ao período de {{periodo_relatorio}}.\n\nPara enviar a nota fiscal, utilize o link: {{link_upload_nf}}\n\nQualquer dúvida, estamos à disposição.\n\nAtenciosamente,\nEquipe Novo Mundo",
        "notificacao_nf": {
            "emails": "tiodavidg3@gmail.com",
            "assunto": "🚨 NOTA FISCAL RECEBIDA - {{prestador_nome}} - Lote {{lote_id}}",
            "corpo": "🎉 NOVA NOTA FISCAL RECEBIDA!\n\n📋 **Detalhes do Upload:**\n• **Prestador:** {{prestador_nome}}\n• **Lote:** #{{lote_id}}\n• **Período:** {{periodo}}\n• **Valor Total:** R$ {{valor_total}}\n• **Data/Hora:** {{data_upload}}\n• **Arquivo:** {{arquivo_nome}}\n\n⚡ **Ação Necessária:**\nA nota fiscal foi recebida e está disponível para download no sistema.\n\n🔗 **Acesso Rápido:**\nAcesse o painel de uploads para fazer o download: {{sistema_url}}\n\n---\nEste é um email automático do sistema de gestão de notas fiscais.",
            "prioridade": "Alta",
            "ativo": True
        }
    }
    
    # Se já existe arquivo, preservar notificacao_nf
    if config_file.exists():
        try:
            with open(config_file, "r", encoding="utf-8") as f:
                existing_config = json.load(f)
            
            # Preservar configurações de notificação se existirem
            if "notificacao_nf" in existing_config:
                default_config["notificacao_nf"] = existing_config["notificacao_nf"]
                
        except Exception as e:
            print(f"⚠️  Erro ao ler config existente: {e}")
    
    # Salvar configuração
    with open(config_file, "w", encoding="utf-8") as f:
        json.dump(default_config, f, indent=4, ensure_ascii=False)
    
    print("✅ Configurações padrão aplicadas!")
    print(f"📁 Arquivo: {config_file.absolute()}")
    print("\n📋 Configurações aplicadas:")
    print(f"• Prestador CC: {default_config['prestador_cc']}")
    print(f"• Prestador Subject: {default_config['prestador_subject'][:50]}...")
    print(f"• Montador CC: {default_config['montador_cc']}")
    print(f"• Notificações ativas: {default_config['notificacao_nf']['ativo']}")

if __name__ == "__main__":
    setup_default_config()
