"""
Script para inicializar templates e automações WhatsApp
Execute este script para criar os templates e triggers padrão
"""

import database as db


def inicializar_templates_whatsapp():
    """Cria templates padrão no banco de dados"""
    
    templates_default = [
        {
            "nome": "prestador_envio_inicial",
            "tipo": "prestador",
            "template": """🧾 *Nota Fiscal - Novo Mundo Resolve*

Olá, *{{nome_prestador}}*!

📅 *Período:* {{periodo}}
💰 *Valor:* R$ {{valor}}

Acabamos de enviar um email com os detalhes para emissão da nota fiscal.

📧 Verifique sua caixa de entrada
🔗 Use o link enviado para fazer o upload da NF

⚠️ *IMPORTANTE:* A nota deve ser enviada exclusivamente pelo link do email.

Obrigado! 🙏""",
            "variaveis": ["nome_prestador", "periodo", "valor", "link"]
        },
        {
            "nome": "prestador_nf_recebida",
            "tipo": "prestador",
            "template": """✅ *Nota Fiscal Recebida!*

Olá, *{{nome_prestador}}*!

📄 Confirmamos o recebimento da sua nota fiscal:

📅 *Período:* {{periodo}}
💰 *Valor:* R$ {{valor}}
🔢 *Número NF:* {{numero_nf}}
📅 *Recebida em:* {{data_recebimento}}

Sua nota está sendo processada e o pagamento será efetuado conforme o prazo acordado.

Obrigado! 🙏""",
            "variaveis": ["nome_prestador", "periodo", "valor", "numero_nf", "data_recebimento"]
        },
        {
            "nome": "montador_envio_inicial",
            "tipo": "montador",
            "template": """💰 *Relatório de Pagamento - Montagem*

Olá, *{{nome_montador}}*!

📅 *Período:* {{periodo_relatorio}}
💵 *Valor Total:* R$ {{valor_total}}
🔧 *OSs Finalizadas:* {{quantidade_os}}

Acabamos de enviar um email com o relatório detalhado de pagamento.

📧 Verifique sua caixa de entrada
📊 O relatório contém todas as montagens realizadas

Em breve efetuaremos o pagamento.

Obrigado pelo excelente trabalho! 💪""",
            "variaveis": ["nome_montador", "periodo_relatorio", "valor_total", "quantidade_os"]
        },
        {
            "nome": "montador_nf_recebida",
            "tipo": "montador",
            "template": """✅ *Nota Fiscal Recebida!*

Olá, *{{nome_montador}}*!

📄 Confirmamos o recebimento da sua nota fiscal:

📅 *Período:* {{periodo_relatorio}}
💰 *Valor:* R$ {{valor_total}}
🔢 *Número NF:* {{numero_nf}}
📅 *Recebida em:* {{data_recebimento}}

Sua nota está sendo processada.

Obrigado! 🙏""",
            "variaveis": ["nome_montador", "periodo_relatorio", "valor_total", "numero_nf", "data_recebimento"]
        }
    ]
    
    conn = db.get_db_connection()
    cursor = conn.cursor()
    
    created_count = 0
    updated_count = 0
    
    for tpl in templates_default:
        # Verificar se já existe
        cursor.execute(
            "SELECT id FROM templates_whatsapp WHERE nome = %s",
            (tpl['nome'],)
        )
        existe = cursor.fetchone()
        
        if existe:
            # Atualizar template existente
            cursor.execute("""
                UPDATE templates_whatsapp
                SET template = %s, tipo = %s, variaveis = %s, ativo = TRUE
                WHERE nome = %s
            """, (tpl['template'], tpl['tipo'], tpl['variaveis'], tpl['nome']))
            updated_count += 1
            print(f"✅ Template '{tpl['nome']}' atualizado")
        else:
            # Criar novo template
            cursor.execute("""
                INSERT INTO templates_whatsapp (nome, tipo, template, variaveis, ativo)
                VALUES (%s, %s, %s, %s, TRUE)
            """, (tpl['nome'], tpl['tipo'], tpl['template'], tpl['variaveis']))
            created_count += 1
            print(f"✅ Template '{tpl['nome']}' criado")
    
    conn.commit()
    conn.close()
    
    print(f"\n📝 Templates: {created_count} criados, {updated_count} atualizados")
    return created_count + updated_count


def inicializar_automacoes_whatsapp():
    """Cria automações padrão no banco de dados"""
    
    automacoes_default = [
        {
            "evento": "envio_email_prestador",
            "template_id": "prestador_envio_inicial",
            "ativo": True
        },
        {
            "evento": "nf_recebida_prestador",
            "template_id": "prestador_nf_recebida",
            "ativo": True
        },
        {
            "evento": "envio_email_montador",
            "template_id": "montador_envio_inicial",
            "ativo": True
        },
        {
            "evento": "nf_recebida_montador",
            "template_id": "montador_nf_recebida",
            "ativo": True
        }
    ]
    
    conn = db.get_db_connection()
    cursor = conn.cursor()
    
    created_count = 0
    updated_count = 0
    
    for auto in automacoes_default:
        # Verificar se já existe
        cursor.execute(
            "SELECT id FROM automacao_whatsapp WHERE evento = %s",
            (auto['evento'],)
        )
        existe = cursor.fetchone()
        
        if existe:
            # Atualizar automação existente
            cursor.execute("""
                UPDATE automacao_whatsapp
                SET template_id = %s, ativo = %s
                WHERE evento = %s
            """, (auto['template_id'], auto['ativo'], auto['evento']))
            updated_count += 1
            print(f"✅ Automação '{auto['evento']}' atualizada")
        else:
            # Criar nova automação
            cursor.execute("""
                INSERT INTO automacao_whatsapp (evento, template_id, ativo)
                VALUES (%s, %s, %s)
            """, (auto['evento'], auto['template_id'], auto['ativo']))
            created_count += 1
            print(f"✅ Automação '{auto['evento']}' criada")
    
    conn.commit()
    conn.close()
    
    print(f"\n⚡ Automações: {created_count} criadas, {updated_count} atualizadas")
    return created_count + updated_count


if __name__ == "__main__":
    print("🚀 Inicializando sistema de automação WhatsApp...\n")
    
    print("=" * 60)
    print("TEMPLATES")
    print("=" * 60)
    templates_count = inicializar_templates_whatsapp()
    
    print("\n" + "=" * 60)
    print("AUTOMAÇÕES (TRIGGERS)")
    print("=" * 60)
    automacoes_count = inicializar_automacoes_whatsapp()
    
    print("\n" + "=" * 60)
    print("✅ INICIALIZAÇÃO CONCLUÍDA!")
    print("=" * 60)
    print(f"Total: {templates_count} templates, {automacoes_count} automações")
    print("\nAgora você pode:")
    print("  1. Ir em '🤖 Automação WhatsApp' no Streamlit")
    print("  2. Aba 'Templates' para ver/editar os templates")
    print("  3. Aba 'Gatilhos' para ativar/desativar automações")
    print("  4. Testar enviando um email com WhatsApp marcado")
