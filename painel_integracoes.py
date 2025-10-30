"""
Painel de Configuração de Integrações
Interface para configurar integrações externas (Trello, Slack, etc)
"""

import streamlit as st
import database as db
from integracoes.trello_integration import TrelloIntegration


def mostrar_painel_integracoes():
    """Exibe o painel de configuração de integrações"""
    
    st.title("Integrações")
    st.markdown("Configure integrações com serviços externos")
    
    # Tabs para diferentes integrações
    tab_trello, tab_futuras = st.tabs([
        "📋 Trello",
        "🔮 Futuras Integrações"
    ])
    
    with tab_trello:
        configurar_trello()
    
    with tab_futuras:
        st.info("💡 Em breve: Slack, Microsoft Teams, Discord e mais!")


def configurar_trello():
    """Interface de configuração do Trello"""
    
    st.header("📋 Integração com Trello")
    
    st.markdown("""
    ### Como configurar:
    
    1. **Obter API Key:**
       - Acesse: https://trello.com/power-ups/admin
       - Clique em "New" para criar uma Power-Up
       - Copie a **API Key**
    
    2. **Obter Token:**
       - Na mesma página, clique em "Token" (ou "Generate a Token")
       - Autorize o aplicativo
       - Copie o **Token**
    
    3. **Obter IDs do Board e Lista:**
       - Use o botão "Testar Conexão" abaixo para listar seus boards e listas
       - Copie os IDs desejados
    
    ---
    """)
    
    # Carrega configuração atual
    config = carregar_config_trello()
    
    # Formulário de configuração
    with st.form("form_trello"):
        st.subheader("🔑 Credenciais")
        
        col1, col2 = st.columns(2)
        
        with col1:
            api_key = st.text_input(
                "API Key",
                value=config.get('trello_api_key', ''),
                type="password",
                help="Sua chave de API do Trello"
            )
        
        with col2:
            token = st.text_input(
                "Token",
                value=config.get('trello_token', ''),
                type="password",
                help="Seu token de autorização do Trello"
            )
        
        st.subheader("📍 Destino dos Cards")
        
        col3, col4 = st.columns(2)
        
        with col3:
            board_id = st.text_input(
                "Board ID",
                value=config.get('trello_board_id', ''),
                help="ID do board onde os cards serão criados"
            )
        
        with col4:
            list_id = st.text_input(
                "List ID",
                value=config.get('trello_list_id', ''),
                help="ID da lista onde os cards serão criados"
            )
        
        st.subheader("⚙️ Configurações")
        
        trello_ativo = st.checkbox(
            "Ativar integração com Trello",
            value=config.get('trello_ativo', False),
            help="Quando ativo, cards serão criados automaticamente ao baixar arquivos"
        )
        
        col_btn1, col_btn2 = st.columns([1, 4])
        
        with col_btn1:
            submitted = st.form_submit_button(
                "💾 Salvar",
                type="primary",
                use_container_width=True
            )
        
        if submitted:
            salvar_config_trello(api_key, token, board_id, list_id, trello_ativo)
            st.success("✅ Configuração salva com sucesso!")
            st.rerun()
    
    # Seção de testes
    st.markdown("---")
    st.subheader("🧪 Testar Integração")
    
    col_test1, col_test2, col_test3 = st.columns(3)
    
    with col_test1:
        if st.button("🔍 Listar Boards", use_container_width=True):
            testar_listar_boards()
    
    with col_test2:
        if st.button("📋 Listar Listas", use_container_width=True):
            testar_listar_listas()
    
    with col_test3:
        if st.button("✨ Criar Card Teste", use_container_width=True):
            testar_criar_card()
    
    # Histórico de cards criados
    mostrar_historico_cards()


def carregar_config_trello():
    """Carrega a configuração atual do Trello"""
    conn = db.get_db_connection()
    cur = conn.cursor()
    
    try:
        cur.execute("""
            SELECT 
                trello_api_key,
                trello_token,
                trello_board_id,
                trello_list_id,
                trello_ativo
            FROM integracoes_config
            WHERE id = 1
        """)
        
        result = cur.fetchone()
        
        if result:
            return {
                'trello_api_key': result[0] or '',
                'trello_token': result[1] or '',
                'trello_board_id': result[2] or '',
                'trello_list_id': result[3] or '',
                'trello_ativo': result[4] or False
            }
        else:
            return {}
            
    except Exception as e:
        st.error(f"❌ Erro ao carregar configuração: {e}")
        return {}
    finally:
        cur.close()
        conn.close()


def salvar_config_trello(api_key, token, board_id, list_id, ativo):
    """Salva a configuração do Trello"""
    conn = db.get_db_connection()
    cur = conn.cursor()
    
    try:
        cur.execute("""
            UPDATE integracoes_config
            SET 
                trello_api_key = %s,
                trello_token = %s,
                trello_board_id = %s,
                trello_list_id = %s,
                trello_ativo = %s,
                data_atualizacao = NOW()
            WHERE id = 1
        """, (api_key, token, board_id, list_id, ativo))
        
        conn.commit()
        
    except Exception as e:
        st.error(f"❌ Erro ao salvar configuração: {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()


def testar_listar_boards():
    """Testa a conexão listando boards"""
    with st.spinner("Conectando ao Trello..."):
        try:
            trello = TrelloIntegration()
            boards = trello.listar_boards()
            
            if boards:
                st.success(f"✅ Conexão OK! Encontrados {len(boards)} boards")
                
                st.markdown("### Seus Boards:")
                for board in boards:
                    with st.expander(f"📋 {board['name']}"):
                        st.code(f"Board ID: {board['id']}")
                        st.markdown(f"**URL:** {board['url']}")
            else:
                st.error("❌ Não foi possível listar boards. Verifique suas credenciais.")
        except ValueError as e:
            st.error(f"❌ {str(e)}")
            
            if "inválidos" in str(e):
                st.info("""
                **💡 Como corrigir:**
                
                1. Acesse: https://trello.com/power-ups/admin
                2. Crie uma nova Power-Up (ou use uma existente)
                3. Copie a **API Key** 
                4. Clique em **Token** e gere um novo token
                5. Cole as novas credenciais acima e salve
                """)
        except Exception as e:
            st.error(f"❌ Erro inesperado: {str(e)}")


def testar_listar_listas():
    """Testa listando listas de um board"""
    trello = TrelloIntegration()
    
    if not trello.config.get('trello_board_id'):
        st.warning("⚠️ Configure o Board ID primeiro")
        return
    
    with st.spinner("Carregando listas..."):
        listas = trello.listar_listas(trello.board_id)
        
        if listas:
            st.success(f"✅ Encontradas {len(listas)} listas")
            
            st.markdown("### Listas do Board:")
            for lista in listas:
                with st.expander(f"📝 {lista['name']}"):
                    st.code(f"List ID: {lista['id']}")
        else:
            st.error("❌ Não foi possível listar listas. Verifique o Board ID.")


def testar_criar_card():
    """Cria um card de teste"""
    trello = TrelloIntegration()
    
    if not trello.is_configured():
        st.warning("⚠️ Configure todos os campos e ative a integração primeiro")
        return
    
    with st.spinner("Criando card de teste..."):
        result = trello.criar_card_download(
            lote_id=0,
            prestador_nome="Teste de Integração",
            montador_nome="Sistema",
            arquivos_baixados=["teste1.pdf", "teste2.xml"],
            nota_fiscal="NF-TESTE-001"
        )
        
        if result:
            st.success("✅ Card de teste criado com sucesso!")
            st.markdown(f"**Link do card:** {result['shortUrl']}")
            st.balloons()
        else:
            st.error("❌ Erro ao criar card. Verifique os logs.")


def mostrar_historico_cards():
    """Mostra o histórico de cards criados"""
    st.markdown("---")
    st.subheader("📊 Histórico de Cards Criados")
    
    conn = db.get_db_connection()
    cur = conn.cursor()
    
    try:
        cur.execute("""
            SELECT 
                tc.id,
                tc.lote_id,
                tc.card_url,
                tc.data_criacao,
                u.prestador_nome
            FROM trello_cards tc
            LEFT JOIN uploads u ON tc.lote_id = u.id
            ORDER BY tc.data_criacao DESC
            LIMIT 20
        """)
        
        cards = cur.fetchall()
        
        if cards:
            st.markdown(f"*Últimos 20 cards criados ({len(cards)} encontrados)*")
            
            for card in cards:
                card_id, lote_id, card_url, data_criacao, prestador = card
                
                col1, col2, col3, col4 = st.columns([1, 2, 2, 1])
                
                with col1:
                    st.markdown(f"**#{lote_id}**")
                
                with col2:
                    st.markdown(f"{prestador or 'N/A'}")
                
                with col3:
                    st.markdown(f"🕒 {data_criacao.strftime('%d/%m/%Y %H:%M')}")
                
                with col4:
                    st.markdown(f"[🔗 Abrir]({card_url})")
        else:
            st.info("ℹ️ Nenhum card criado ainda")
            
    except Exception as e:
        st.error(f"❌ Erro ao carregar histórico: {e}")
    finally:
        cur.close()
        conn.close()


if __name__ == '__main__':
    mostrar_painel_integracoes()
