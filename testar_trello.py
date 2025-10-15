"""
Script de teste da integração Trello
Verifica se tudo está funcionando corretamente
"""

import database as db
from integracoes.trello_integration import TrelloIntegration


def testar_integracao():
    """Testa a integração com Trello"""
    
    print("\n" + "="*60)
    print("🧪 TESTE DE INTEGRAÇÃO COM TRELLO")
    print("="*60)
    
    # 1. Verificar se tabelas existem
    print("\n1️⃣  Verificando tabelas...")
    conn = db.get_db_connection()
    cur = conn.cursor()
    
    try:
        cur.execute("SELECT COUNT(*) FROM integracoes_config")
        count = cur.fetchone()[0]
        print(f"   ✅ Tabela integracoes_config: {count} registro(s)")
        
        cur.execute("SELECT COUNT(*) FROM trello_cards")
        count = cur.fetchone()[0]
        print(f"   ✅ Tabela trello_cards: {count} card(s) criado(s)")
        
    except Exception as e:
        print(f"   ❌ Erro ao verificar tabelas: {e}")
        return False
    finally:
        cur.close()
        conn.close()
    
    # 2. Carregar configuração
    print("\n2️⃣  Carregando configuração...")
    trello = TrelloIntegration()
    
    config = trello.config
    
    if config.get('trello_api_key'):
        print(f"   ✅ API Key: {config['trello_api_key'][:10]}...")
    else:
        print("   ⚠️  API Key não configurada")
    
    if config.get('trello_token'):
        print(f"   ✅ Token: {config['trello_token'][:10]}...")
    else:
        print("   ⚠️  Token não configurado")
    
    if config.get('trello_board_id'):
        print(f"   ✅ Board ID: {config['trello_board_id']}")
    else:
        print("   ⚠️  Board ID não configurado")
    
    if config.get('trello_list_id'):
        print(f"   ✅ List ID: {config['trello_list_id']}")
    else:
        print("   ⚠️  List ID não configurado")
    
    if config.get('trello_ativo'):
        print("   ✅ Integração: ATIVA")
    else:
        print("   ⚠️  Integração: DESATIVADA")
    
    # 3. Verificar se está configurado
    print("\n3️⃣  Verificando status...")
    if trello.is_configured():
        print("   ✅ Integração está pronta para uso!")
    else:
        print("   ⚠️  Integração não está configurada completamente")
        print("\n   📋 Para configurar:")
        print("   1. Acesse o Streamlit")
        print("   2. Vá em '🔌 Integrações'")
        print("   3. Configure as credenciais do Trello")
        print("   4. Ative a integração")
        return False
    
    # 4. Testar conexão (se configurado)
    print("\n4️⃣  Testando conexão...")
    boards = trello.listar_boards()
    
    if boards:
        print(f"   ✅ Conexão OK! Encontrados {len(boards)} board(s)")
        print(f"\n   Boards disponíveis:")
        for i, board in enumerate(boards[:3], 1):  # Mostrar apenas 3
            print(f"   {i}. {board['name']}")
        if len(boards) > 3:
            print(f"   ... e mais {len(boards) - 3} board(s)")
    else:
        print("   ❌ Não foi possível conectar ao Trello")
        print("   Verifique suas credenciais")
        return False
    
    # 5. Testar listagem de listas
    print("\n5️⃣  Testando listagem de listas...")
    listas = trello.listar_listas(trello.board_id)
    
    if listas:
        print(f"   ✅ Encontradas {len(listas)} lista(s) no board")
        for i, lista in enumerate(listas, 1):
            marcador = "👉" if lista['id'] == trello.list_id else "  "
            print(f"   {marcador} {i}. {lista['name']}")
    else:
        print("   ❌ Não foi possível listar listas")
        return False
    
    # 6. Oferecer criar card de teste
    print("\n6️⃣  Teste de criação de card")
    print("   ⚠️  Deseja criar um card de teste no Trello?")
    print("   (Este card será criado no board configurado)")
    
    resposta = input("\n   Digite 's' para criar ou Enter para pular: ").strip().lower()
    
    if resposta == 's':
        print("\n   Criando card de teste...")
        
        result = trello.criar_card_download(
            lote_id=0,
            prestador_nome="🧪 Teste de Integração",
            montador_nome="Sistema Automático",
            arquivos_baixados=[
                "teste_arquivo_1.pdf",
                "teste_arquivo_2.xml",
                "teste_arquivo_3.jpg"
            ],
            nota_fiscal="NF-TESTE-001"
        )
        
        if result:
            print(f"   ✅ Card criado com sucesso!")
            print(f"   🔗 URL: {result['shortUrl']}")
            print(f"   📋 ID: {result['id']}")
        else:
            print("   ❌ Erro ao criar card de teste")
            return False
    else:
        print("   ⏭️  Pulando criação de card de teste")
    
    # Resumo final
    print("\n" + "="*60)
    print("✅ TODOS OS TESTES PASSARAM!")
    print("="*60)
    print("\n📚 Documentação: INTEGRACAO_TRELLO.md")
    print("🎯 Próximo passo: Aguardar que o job baixe arquivos")
    print("                 e um card será criado automaticamente!\n")
    
    return True


if __name__ == '__main__':
    testar_integracao()
