"""
Componente de notificações para o Streamlit
"""

import streamlit as st
import database as db


def mostrar_badge_notificacoes():
    """Mostra badge de notificações não lidas na sidebar"""
    num_notifs = db.contar_notificacoes_nao_lidas()
    
    if num_notifs > 0:
        st.sidebar.markdown(f"### 🔔 Notificações: **{num_notifs}**")
        if st.sidebar.button("📋 Ver Notificações", use_container_width=True):
            st.session_state['show_notifications'] = True


def mostrar_modal_notificacoes():
    """Mostra modal com notificações não lidas"""
    if st.session_state.get('show_notifications', False):
        with st.expander("🔔 **NOTIFICAÇÕES**", expanded=True):
            notifs = db.get_notificacoes_nao_lidas()
            
            if notifs:
                col1, col2 = st.columns([4, 1])
                with col2:
                    if st.button("✅ Marcar Todas Como Lidas"):
                        db.marcar_todas_notificacoes_lidas()
                        st.session_state['show_notifications'] = False
                        st.rerun()
                
                for notif in notifs:
                    with st.container():
                        col_n1, col_n2, col_n3 = st.columns([1, 6, 1])
                        
                        with col_n1:
                            st.markdown(f"## {notif['icone']}")
                        
                        with col_n2:
                            st.markdown(f"**{notif['titulo']}**")
                            st.caption(notif['mensagem'])
                            if notif.get('prestador_nome'):
                                st.caption(f"👤 {notif['prestador_nome']}")
                            st.caption(f"🕐 {notif['data_criacao'].strftime('%d/%m/%Y %H:%M')}")
                        
                        with col_n3:
                            if st.button("✓", key=f"read_{notif['id']}", help="Marcar como lida"):
                                db.marcar_notificacao_lida(notif['id'])
                                st.rerun()
                        
                        st.markdown("---")
            else:
                st.info("✅ Nenhuma notificação pendente")
                if st.button("Fechar"):
                    st.session_state['show_notifications'] = False
                    st.rerun()
