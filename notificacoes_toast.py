"""
Sistema de Notificações Toast para Streamlit
Exibe notificações flutuantes automáticas
"""

import streamlit as st
import database as db
import psycopg2.extras
from datetime import datetime


def processar_notificacoes_toast():
    """
    Processa notificações não lidas e exibe como toasts
    Marca como lidas ANTES de exibir para evitar reexibição
    """
    
    # Inicializar estado de controle
    if 'notificacoes_processadas_session' not in st.session_state:
        st.session_state.notificacoes_processadas_session = set()
    
    # Buscar notificações não lidas
    notificacoes = db.get_notificacoes_nao_lidas()
    
    if not notificacoes:
        return
    
    # Limitar a 5 notificações por vez para não sobrecarregar
    notificacoes = notificacoes[:5]
    
    # Processar cada notificação
    for notif in notificacoes:
        notif_id = notif['id']
        
        # Verificar se já foi processada nesta sessão
        if notif_id in st.session_state.notificacoes_processadas_session:
            continue
        
        # IMPORTANTE: Marcar como lida ANTES de exibir
        # Isso evita que apareça novamente caso a página recarregue
        db.marcar_notificacao_lida(notif_id)
        
        # Adicionar ao cache da sessão
        st.session_state.notificacoes_processadas_session.add(notif_id)
        
        # Determinar o ícone do toast baseado no tipo
        tipo = notif.get('tipo', 'info')
        titulo = notif['titulo']
        mensagem = notif['mensagem']
        
        # Mapear tipo para ícone do Streamlit
        icones_map = {
            'nf_recebida': '📥',
            'erro': '❌',
            'sucesso': '✅',
            'aviso': '⚠️',
            'info': 'ℹ️'
        }
        toast_icon = icones_map.get(tipo, notif.get('icone', '📢'))
        
        # Exibir toast
        st.toast(
            f"**{titulo}**\n\n{mensagem}",
            icon=toast_icon
        )


def limpar_cache_notificacoes():
    """Limpa o cache de notificações da sessão"""
    if 'notificacoes_processadas_session' in st.session_state:
        st.session_state.notificacoes_processadas_session.clear()
        
        
def marcar_todas_como_lidas():
    """Marca todas as notificações não lidas como lidas"""
    conn = db.get_db_connection()
    cur = conn.cursor()
    
    cur.execute("UPDATE notificacoes SET lida = true WHERE lida = false")
    affected = cur.rowcount
    
    conn.commit()
    cur.close()
    conn.close()
    
    return affected


def mostrar_historico_notificacoes_sidebar():
    """
    Mostra histórico de notificações no sidebar (opcional)
    Útil para usuário revisar notificações antigas
    """
    
    # Buscar todas notificações recentes (últimos 7 dias)
    conn = db.get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    
    cur.execute("""
        SELECT n.*, p.nome as prestador_nome
        FROM notificacoes n
        LEFT JOIN lotes_servico ls ON n.lote_id = ls.id
        LEFT JOIN prestadores p ON ls.prestador_id = p.id
        WHERE n.data_criacao >= NOW() - INTERVAL '7 days'
        ORDER BY n.data_criacao DESC
        LIMIT 20
    """)
    
    notificacoes = cur.fetchall()
    cur.close()
    conn.close()
    
    if not notificacoes:
        st.sidebar.info("📭 Nenhuma notificação recente")
        return
    
    with st.sidebar.expander(f"🔔 Notificações ({len(notificacoes)})", expanded=False):
        for notif in notificacoes:
            icone = '✉️' if notif['lida'] else '📩'
            tempo = notif['data_criacao'].strftime('%d/%m %H:%M')
            
            with st.container():
                st.markdown(f"{icone} **{notif['titulo']}**")
                st.caption(f"{notif['mensagem']}")
                st.caption(f"⏰ {tempo}")
                
                if not notif['lida']:
                    if st.button("✓ Marcar como lida", key=f"mark_{notif['id']}", use_container_width=True):
                        db.marcar_notificacao_lida(notif['id'])
                        st.rerun()
                
                st.divider()


def badge_contador_notificacoes():
    """
    Retorna o número de notificações não lidas
    Útil para exibir badge no menu
    """
    conn = db.get_db_connection()
    cur = conn.cursor()
    
    cur.execute("SELECT COUNT(*) FROM notificacoes WHERE lida = false")
    count = cur.fetchone()[0]
    
    cur.close()
    conn.close()
    
    return count


def criar_notificacao_toast(tipo, titulo, mensagem, lote_id=None, icone=None, prioridade=0):
    """
    Wrapper conveniente para criar notificação que será exibida como toast
    
    Args:
        tipo: Tipo da notificação (nf_recebida, erro, sucesso, aviso, info)
        titulo: Título da notificação
        mensagem: Mensagem detalhada
        lote_id: ID do lote relacionado (opcional)
        icone: Ícone emoji (opcional, usa padrão do tipo se não fornecido)
        prioridade: 0=normal, 1=alta (opcional)
    """
    
    # Definir ícones padrão por tipo se não fornecido
    if not icone:
        icones_padrao = {
            'nf_recebida': '📥',
            'erro': '❌',
            'sucesso': '✅',
            'aviso': '⚠️',
            'info': 'ℹ️'
        }
        icone = icones_padrao.get(tipo, '📢')
    
    # Criar notificação no banco
    db.criar_notificacao(
        tipo=tipo,
        titulo=titulo,
        mensagem=mensagem,
        lote_id=lote_id,
        icone=icone,
        prioridade=prioridade
    )


# Exemplo de uso no streamlit_app.py:
"""
# No início do app, logo após o login:
from notificacoes_toast import processar_notificacoes_toast, badge_contador_notificacoes

# Processar e exibir toasts automaticamente
processar_notificacoes_toast()

# No sidebar, mostrar contador
count = badge_contador_notificacoes()
if count > 0:
    st.sidebar.markdown(f"### 🔔 {count} nova(s) notificação(ões)")
"""
