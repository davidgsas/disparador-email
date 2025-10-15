"""
Exemplos de uso da integração Trello
Demonstra como usar a classe TrelloIntegration manualmente
"""

from integracoes.trello_integration import TrelloIntegration


def exemplo_1_verificar_configuracao():
    """Exemplo 1: Verificar se está configurado"""
    print("\n" + "="*60)
    print("EXEMPLO 1: Verificar configuração")
    print("="*60)
    
    trello = TrelloIntegration()
    
    if trello.is_configured():
        print("✅ Integração está configurada e ativa!")
        print(f"   Board ID: {trello.board_id}")
        print(f"   List ID: {trello.list_id}")
    else:
        print("❌ Integração não está configurada")
        print("   Configure em: Streamlit → 🔌 Integrações")


def exemplo_2_listar_boards():
    """Exemplo 2: Listar todos os boards"""
    print("\n" + "="*60)
    print("EXEMPLO 2: Listar boards")
    print("="*60)
    
    trello = TrelloIntegration()
    boards = trello.listar_boards()
    
    if boards:
        print(f"✅ Encontrados {len(boards)} board(s):\n")
        for i, board in enumerate(boards, 1):
            print(f"{i}. {board['name']}")
            print(f"   ID: {board['id']}")
            print(f"   URL: {board['url']}")
            print()
    else:
        print("❌ Não foi possível listar boards")


def exemplo_3_listar_listas():
    """Exemplo 3: Listar listas de um board"""
    print("\n" + "="*60)
    print("EXEMPLO 3: Listar listas do board configurado")
    print("="*60)
    
    trello = TrelloIntegration()
    
    if not trello.board_id:
        print("❌ Board ID não configurado")
        return
    
    listas = trello.listar_listas(trello.board_id)
    
    if listas:
        print(f"✅ Encontradas {len(listas)} lista(s):\n")
        for i, lista in enumerate(listas, 1):
            marcador = "👉" if lista['id'] == trello.list_id else "  "
            print(f"{marcador} {i}. {lista['name']}")
            print(f"   ID: {lista['id']}")
            print()
    else:
        print("❌ Não foi possível listar listas")


def exemplo_4_criar_card_simples():
    """Exemplo 4: Criar um card simples"""
    print("\n" + "="*60)
    print("EXEMPLO 4: Criar card de exemplo")
    print("="*60)
    
    trello = TrelloIntegration()
    
    if not trello.is_configured():
        print("❌ Configure a integração primeiro")
        return
    
    # Criar card
    result = trello.criar_card_download(
        lote_id=999,  # ID fictício
        prestador_nome="Exemplo Prestador LTDA",
        montador_nome="Exemplo Montador",
        arquivos_baixados=[
            "exemplo_arquivo_1.pdf",
            "exemplo_arquivo_2.xml"
        ],
        nota_fiscal="NF-EXEMPLO-001"
    )
    
    if result:
        print("✅ Card criado com sucesso!")
        print(f"   ID: {result['id']}")
        print(f"   URL: {result['shortUrl']}")
        print(f"   Nome: {result['name']}")
    else:
        print("❌ Erro ao criar card")


def exemplo_5_verificar_card_existe():
    """Exemplo 5: Verificar se lote já tem card"""
    print("\n" + "="*60)
    print("EXEMPLO 5: Verificar se lote já tem card")
    print("="*60)
    
    import database as db
    
    lote_id = 123  # Altere para um ID real
    
    conn = db.get_db_connection()
    cur = conn.cursor()
    
    try:
        cur.execute("""
            SELECT card_id, card_url, data_criacao
            FROM trello_cards
            WHERE lote_id = %s
        """, (lote_id,))
        
        result = cur.fetchone()
        
        if result:
            print(f"✅ Lote #{lote_id} já tem card no Trello")
            print(f"   Card ID: {result[0]}")
            print(f"   URL: {result[1]}")
            print(f"   Criado em: {result[2]}")
        else:
            print(f"ℹ️  Lote #{lote_id} ainda não tem card")
            
    except Exception as e:
        print(f"❌ Erro: {e}")
    finally:
        cur.close()
        conn.close()


def exemplo_6_historico_cards():
    """Exemplo 6: Ver histórico de cards criados"""
    print("\n" + "="*60)
    print("EXEMPLO 6: Histórico de cards criados")
    print("="*60)
    
    import database as db
    
    conn = db.get_db_connection()
    cur = conn.cursor()
    
    try:
        cur.execute("""
            SELECT 
                tc.lote_id,
                tc.card_url,
                tc.data_criacao,
                u.prestador_nome
            FROM trello_cards tc
            LEFT JOIN uploads u ON tc.lote_id = u.id
            ORDER BY tc.data_criacao DESC
            LIMIT 10
        """)
        
        cards = cur.fetchall()
        
        if cards:
            print(f"✅ Últimos {len(cards)} cards criados:\n")
            for i, (lote_id, url, data, prestador) in enumerate(cards, 1):
                print(f"{i}. Lote #{lote_id} - {prestador or 'N/A'}")
                print(f"   URL: {url}")
                print(f"   Data: {data.strftime('%d/%m/%Y %H:%M')}")
                print()
        else:
            print("ℹ️  Nenhum card criado ainda")
            
    except Exception as e:
        print(f"❌ Erro: {e}")
    finally:
        cur.close()
        conn.close()


def exemplo_7_criar_card_completo():
    """Exemplo 7: Criar card com todos os parâmetros"""
    print("\n" + "="*60)
    print("EXEMPLO 7: Criar card completo")
    print("="*60)
    
    trello = TrelloIntegration()
    
    if not trello.is_configured():
        print("❌ Configure a integração primeiro")
        return
    
    # Dados completos
    result = trello.criar_card_download(
        lote_id=888,
        prestador_nome="Empresa XYZ Serviços LTDA",
        montador_nome="Montador ABC",
        arquivos_baixados=[
            "nota_fiscal_2024_001.pdf",
            "danfe_2024_001.xml",
            "recibo_pagamento_2024_001.pdf",
            "comprovante_deposito.jpg"
        ],
        nota_fiscal="NF-2024-001"
    )
    
    if result:
        print("✅ Card completo criado com sucesso!")
        print(f"   Nome: {result['name']}")
        print(f"   URL: {result['shortUrl']}")
        print(f"   Descrição: {len(result.get('desc', ''))} caracteres")
        print("\n   O card inclui:")
        print("   • Título formatado")
        print("   • Descrição completa")
        print("   • Checklist com 4 itens")
        print("   • Label verde")
        print("   • Registro no banco")
    else:
        print("❌ Erro ao criar card")


def exemplo_8_estatisticas():
    """Exemplo 8: Estatísticas de uso"""
    print("\n" + "="*60)
    print("EXEMPLO 8: Estatísticas de uso")
    print("="*60)
    
    import database as db
    from datetime import datetime, timedelta
    
    conn = db.get_db_connection()
    cur = conn.cursor()
    
    try:
        # Total de cards
        cur.execute("SELECT COUNT(*) FROM trello_cards")
        total = cur.fetchone()[0]
        print(f"📊 Total de cards criados: {total}")
        
        # Cards hoje
        cur.execute("""
            SELECT COUNT(*) FROM trello_cards
            WHERE DATE(data_criacao) = CURRENT_DATE
        """)
        hoje = cur.fetchone()[0]
        print(f"📊 Cards criados hoje: {hoje}")
        
        # Cards últimos 7 dias
        cur.execute("""
            SELECT COUNT(*) FROM trello_cards
            WHERE data_criacao >= NOW() - INTERVAL '7 days'
        """)
        semana = cur.fetchone()[0]
        print(f"📊 Cards criados nos últimos 7 dias: {semana}")
        
        # Cards últimos 30 dias
        cur.execute("""
            SELECT COUNT(*) FROM trello_cards
            WHERE data_criacao >= NOW() - INTERVAL '30 days'
        """)
        mes = cur.fetchone()[0]
        print(f"📊 Cards criados nos últimos 30 dias: {mes}")
        
        # Primeiro card
        cur.execute("""
            SELECT data_criacao FROM trello_cards
            ORDER BY data_criacao ASC
            LIMIT 1
        """)
        primeiro = cur.fetchone()
        if primeiro:
            print(f"\n📅 Primeiro card criado em: {primeiro[0].strftime('%d/%m/%Y %H:%M')}")
        
        # Último card
        cur.execute("""
            SELECT data_criacao FROM trello_cards
            ORDER BY data_criacao DESC
            LIMIT 1
        """)
        ultimo = cur.fetchone()
        if ultimo:
            print(f"📅 Último card criado em: {ultimo[0].strftime('%d/%m/%Y %H:%M')}")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
    finally:
        cur.close()
        conn.close()


def menu_principal():
    """Menu interativo de exemplos"""
    print("\n" + "="*60)
    print("🧪 EXEMPLOS DE USO - INTEGRAÇÃO TRELLO")
    print("="*60)
    print("\nEscolha um exemplo:\n")
    print("1. Verificar configuração")
    print("2. Listar boards")
    print("3. Listar listas do board")
    print("4. Criar card simples")
    print("5. Verificar se lote tem card")
    print("6. Ver histórico de cards")
    print("7. Criar card completo")
    print("8. Ver estatísticas")
    print("0. Sair")
    
    escolha = input("\nOpção: ").strip()
    
    if escolha == "1":
        exemplo_1_verificar_configuracao()
    elif escolha == "2":
        exemplo_2_listar_boards()
    elif escolha == "3":
        exemplo_3_listar_listas()
    elif escolha == "4":
        exemplo_4_criar_card_simples()
    elif escolha == "5":
        exemplo_5_verificar_card_existe()
    elif escolha == "6":
        exemplo_6_historico_cards()
    elif escolha == "7":
        exemplo_7_criar_card_completo()
    elif escolha == "8":
        exemplo_8_estatisticas()
    elif escolha == "0":
        print("\n👋 Até logo!")
        return False
    else:
        print("\n❌ Opção inválida")
    
    return True


if __name__ == '__main__':
    continuar = True
    while continuar:
        continuar = menu_principal()
        if continuar:
            input("\nPressione Enter para continuar...")
