"""
Sistema de Automação WhatsApp
Gerencia templates e triggers automáticos
"""

import streamlit as st
import database as db
from datetime import datetime


def mostrar_automacao_whatsapp():
    """Painel de automação WhatsApp"""
    
    st.title("Automação WhatsApp")
    
    # Tabs principais
    tab_templates, tab_triggers, tab_historico = st.tabs([
        "📝 Templates de Mensagens",
        "⚡ Gatilhos Automáticos", 
        "📊 Histórico"
    ])
    
    # ========== TAB TEMPLATES ==========
    with tab_templates:
        st.subheader("📝 Templates de Mensagens")
        
        # Carregar templates do banco
        try:
            conn = db.get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, nome, tipo, template, ativo, variaveis
                FROM templates_whatsapp
                WHERE ativo = TRUE
                ORDER BY tipo, nome
            """)
            templates_db = cursor.fetchall()
            conn.close()
            
            # Converter para dict
            templates_salvos = {}
            for t in templates_db:
                templates_salvos[t[1]] = {  # t[1] é o nome
                    'id': t[0],
                    'nome': t[1],
                    'tipo': t[2],
                    'template': t[3],
                    'ativo': t[4],
                    'variaveis': t[5]
                }
        except Exception as e:
            st.warning(f"⚠️ Erro ao carregar templates: {e}")
            templates_salvos = {}
        
        # Botão para criar novo
        col_titulo, col_btn = st.columns([4, 1])
        with col_btn:
            if st.button("➕ Novo Template", use_container_width=True):
                st.session_state['modo_edicao'] = 'novo'
                st.session_state['template_editando'] = None
                st.rerun()
        
        # Modo de edição
        modo = st.session_state.get('modo_edicao', 'lista')
        
        if modo == 'novo':
            # CRIAR NOVO TEMPLATE
            st.divider()
            st.markdown("### ➕ Criar Novo Template")
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                nome_template = st.text_input(
                    "Nome/ID do Template",
                    placeholder="ex: prestador_personalizado_1",
                    help="Use letras minúsculas, números e underscore. Ex: prestador_cobranca, montador_bonus"
                )
                
                tipo_template = st.selectbox(
                    "Tipo",
                    options=["prestador", "montador"],
                    help="Escolha se este template é para prestadores ou montadores"
                )
                
                texto_template = st.text_area(
                    "Mensagem",
                    height=300,
                    placeholder="Digite a mensagem aqui...\n\nUse variáveis como:\n{{nome_prestador}}\n{{periodo}}\n{{valor}}",
                    help="Use *texto* para negrito, _texto_ para itálico"
                )
            
            with col2:
                st.markdown("### 📋 Variáveis Disponíveis")
                
                if tipo_template == "prestador":
                    st.code("{{nome_prestador}}")
                    st.code("{{periodo}}")
                    st.code("{{valor}}")
                    st.code("{{link}}")
                    st.code("{{numero_nf}}")
                    st.code("{{data_recebimento}}")
                else:
                    st.code("{{nome_montador}}")
                    st.code("{{periodo_relatorio}}")
                    st.code("{{valor_total}}")
                    st.code("{{quantidade_os}}")
                    st.code("{{numero_nf}}")
                    st.code("{{data_recebimento}}")
            
            col_salvar, col_cancelar = st.columns(2)
            
            with col_salvar:
                if st.button("💾 Salvar Template", type="primary", use_container_width=True):
                    if not nome_template:
                        st.error("❌ Digite um nome para o template!")
                    elif not texto_template:
                        st.error("❌ Digite o texto da mensagem!")
                    else:
                        try:
                            conn = db.get_db_connection()
                            cursor = conn.cursor()
                            
                            cursor.execute("""
                                INSERT INTO templates_whatsapp 
                                (nome, tipo, template, ativo, variaveis)
                                VALUES (%s, %s, %s, %s, %s)
                            """, (
                                nome_template,
                                tipo_template,
                                texto_template,
                                True,
                                ['nome_prestador', 'periodo', 'valor'] if tipo_template == "prestador" else ['nome_montador', 'periodo_relatorio', 'valor_total']
                            ))
                            
                            conn.commit()
                            conn.close()
                            
                            st.success("✅ Template criado com sucesso!")
                            st.balloons()
                            del st.session_state['modo_edicao']
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Erro ao salvar: {e}")
            
            with col_cancelar:
                if st.button("❌ Cancelar", use_container_width=True):
                    del st.session_state['modo_edicao']
                    st.rerun()
        
        elif modo == 'editar':
            # EDITAR TEMPLATE EXISTENTE
            template_id = st.session_state.get('template_editando')
            template_atual = templates_salvos.get(template_id)
            
            if template_atual:
                st.divider()
                st.markdown(f"### ✏️ Editando: `{template_atual['nome']}`")
                
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    texto_editado = st.text_area(
                        "Mensagem",
                        value=template_atual['template'],
                        height=300,
                        key=f"edit_{template_id}"
                    )
                
                with col2:
                    st.markdown("### 📋 Variáveis Disponíveis")
                    
                    if template_atual['tipo'] == "prestador":
                        st.code("{{nome_prestador}}")
                        st.code("{{periodo}}")
                        st.code("{{valor}}")
                        st.code("{{link}}")
                        st.code("{{numero_nf}}")
                        st.code("{{data_recebimento}}")
                    else:
                        st.code("{{nome_montador}}")
                        st.code("{{periodo_relatorio}}")
                        st.code("{{valor_total}}")
                        st.code("{{quantidade_os}}")
                        st.code("{{numero_nf}}")
                        st.code("{{data_recebimento}}")
                
                col_salvar, col_cancelar, col_deletar = st.columns(3)
                
                with col_salvar:
                    if st.button("💾 Salvar", type="primary", use_container_width=True):
                        try:
                            conn = db.get_db_connection()
                            cursor = conn.cursor()
                            
                            cursor.execute("""
                                UPDATE templates_whatsapp
                                SET template = %s
                                WHERE nome = %s
                            """, (texto_editado, template_id))
                            
                            conn.commit()
                            conn.close()
                            
                            st.success("✅ Template atualizado!")
                            st.balloons()
                            del st.session_state['modo_edicao']
                            del st.session_state['template_editando']
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Erro: {e}")
                
                with col_cancelar:
                    if st.button("❌ Cancelar", use_container_width=True):
                        del st.session_state['modo_edicao']
                        del st.session_state['template_editando']
                        st.rerun()
                
                with col_deletar:
                    if st.button("🗑️ Deletar", use_container_width=True):
                        st.session_state['confirmar_delete'] = template_id
                        st.rerun()
                
                # Confirmação de delete
                if st.session_state.get('confirmar_delete') == template_id:
                    st.warning(f"⚠️ Tem certeza que deseja deletar `{template_id}`?")
                    col_sim, col_nao = st.columns(2)
                    
                    with col_sim:
                        if st.button("✅ Sim, deletar", type="primary"):
                            try:
                                conn = db.get_db_connection()
                                cursor = conn.cursor()
                                cursor.execute("UPDATE templates_whatsapp SET ativo = FALSE WHERE nome = %s", (template_id,))
                                conn.commit()
                                conn.close()
                                
                                st.success("✅ Template deletado!")
                                del st.session_state['modo_edicao']
                                del st.session_state['template_editando']
                                del st.session_state['confirmar_delete']
                                st.rerun()
                            except Exception as e:
                                st.error(f"❌ Erro: {e}")
                    
                    with col_nao:
                        if st.button("❌ Não, cancelar"):
                            del st.session_state['confirmar_delete']
                            st.rerun()
        
        else:
            # LISTAR TEMPLATES
            if not templates_salvos:
                st.info("📝 Nenhum template criado ainda. Clique em '➕ Novo Template' para criar.")
            else:
                st.markdown("### 📋 Templates Cadastrados")
                
                # Separar por tipo
                templates_prestador = {k: v for k, v in templates_salvos.items() if v['tipo'] == 'prestador'}
                templates_montador = {k: v for k, v in templates_salvos.items() if v['tipo'] == 'montador'}
                
                # Prestadores
                if templates_prestador:
                    st.markdown("#### 👤 Prestadores")
                    for nome, tpl in templates_prestador.items():
                        with st.expander(f"📄 {nome}"):
                            st.code(tpl['template'][:200] + "..." if len(tpl['template']) > 200 else tpl['template'])
                            
                            col1, col2 = st.columns(2)
                            with col1:
                                if st.button("✏️ Editar", key=f"edit_btn_{nome}"):
                                    st.session_state['modo_edicao'] = 'editar'
                                    st.session_state['template_editando'] = nome
                                    st.rerun()
                            with col2:
                                if st.button("🧪 Testar", key=f"test_btn_{nome}"):
                                    st.session_state['testar_template'] = nome
                                    st.rerun()
                
                # Montadores
                if templates_montador:
                    st.markdown("#### 🔧 Montadores")
                    for nome, tpl in templates_montador.items():
                        with st.expander(f"📄 {nome}"):
                            st.code(tpl['template'][:200] + "..." if len(tpl['template']) > 200 else tpl['template'])
                            
                            col1, col2 = st.columns(2)
                            with col1:
                                if st.button("✏️ Editar", key=f"edit_btn_{nome}"):
                                    st.session_state['modo_edicao'] = 'editar'
                                    st.session_state['template_editando'] = nome
                                    st.rerun()
                            with col2:
                                if st.button("🧪 Testar", key=f"test_btn_{nome}"):
                                    st.session_state['testar_template'] = nome
                                    st.rerun()
        
        # Preview de teste (funciona em qualquer modo)
        if st.session_state.get('testar_template'):
            template_teste = st.session_state.get('testar_template')
            template_dados = templates_salvos.get(template_teste)
            
            if template_dados:
                st.divider()
                st.markdown("### 🧪 Preview do Template")
                
                # Dados de exemplo
                dados_exemplo = {
                    "nome_prestador": "João Silva",
                    "nome_montador": "Pedro Santos",
                    "periodo": "01-31/10/2025",
                    "periodo_relatorio": "Outubro/2025",
                    "valor": "1.500,00",
                    "valor_total": "2.300,00",
                    "numero_nf": "NF-123456",
                    "data_recebimento": "28/10/2025 14:30",
                    "data_vencimento": "07/11/2025",
                    "status": "Aguardando Pagamento",
                    "quantidade_os": "15",
                    "link": "https://exemplo.com/upload/12345"
                }
                
                # Renderizar template
                template_renderizado = template_dados['template']
                for var, valor in dados_exemplo.items():
                    template_renderizado = template_renderizado.replace("{{" + var + "}}", valor)
                
                st.info(template_renderizado)
                
                if st.button("❌ Fechar Preview"):
                    del st.session_state['testar_template']
                    st.rerun()
    
    # ========== TAB TRIGGERS ==========
    with tab_triggers:
        st.subheader("⚡ Gatilhos Automáticos")
        
        st.markdown("""
        Configure quando as mensagens devem ser enviadas automaticamente.
        """)
        
        # Carregar configurações
        try:
            conn = db.get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT evento, template_id, ativo, condicoes
                FROM automacao_whatsapp
                ORDER BY evento
            """)
            triggers = cursor.fetchall()
            conn.close()
        except:
            triggers = []
        
        # Lista de eventos disponíveis
        eventos = {
            "envio_email_prestador": {
                "nome": "📧 Email Enviado - Prestador",
                "descricao": "Quando um email é enviado ao prestador solicitando NF",
                "template_padrao": "prestador_envio_inicial"
            },
            "nf_recebida_prestador": {
                "nome": "📄 NF Anexada - Prestador",
                "descricao": "Quando o prestador anexa a nota fiscal no sistema",
                "template_padrao": "prestador_nf_recebida"
            },
            "pagamento_proximo_prestador": {
                "nome": "⏰ Pagamento Próximo - Prestador",
                "descricao": "X dias antes do vencimento do pagamento",
                "template_padrao": "prestador_pagamento_proximo"
            },
            "envio_email_montador": {
                "nome": "📧 Email Enviado - Montador",
                "descricao": "Quando um email de pagamento é enviado ao montador",
                "template_padrao": "montador_envio_inicial"
            },
            "nf_recebida_montador": {
                "nome": "📄 NF Anexada - Montador",
                "descricao": "Quando o montador anexa a nota fiscal no sistema",
                "template_padrao": "montador_nf_recebida"
            }
        }
        
        # Criar/Editar triggers
        for evento_id, evento_info in eventos.items():
            with st.expander(f"{evento_info['nome']}", expanded=False):
                st.markdown(f"**{evento_info['descricao']}**")
                
                # Buscar configuração atual
                config_atual = None
                for t in triggers:
                    if t[0] == evento_id:
                        config_atual = {
                            'evento': t[0],
                            'template_id': t[1],
                            'ativo': t[2],
                            'condicoes': t[3]
                        }
                        break
                
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    # Checkbox ativo
                    ativo = st.checkbox(
                        "✅ Ativo",
                        value=config_atual['ativo'] if config_atual else False,
                        key=f"ativo_{evento_id}",
                        help="Marque para ativar o envio automático deste gatilho"
                    )
                    
                    # Buscar templates disponíveis do tipo correto
                    try:
                        conn = db.get_db_connection()
                        cursor = conn.cursor()
                        tipo_template = "prestador" if "prestador" in evento_id else "montador"
                        cursor.execute("""
                            SELECT nome FROM templates_whatsapp 
                            WHERE tipo = %s AND ativo = TRUE
                            ORDER BY nome
                        """, (tipo_template,))
                        templates_disponiveis = [row[0] for row in cursor.fetchall()]
                        conn.close()
                    except:
                        templates_disponiveis = [evento_info['template_padrao']]
                    
                    # Se não houver templates, usar o padrão
                    if not templates_disponiveis:
                        templates_disponiveis = [evento_info['template_padrao']]
                    
                    # Selectbox para escolher template
                    template_atual = config_atual['template_id'] if config_atual else evento_info['template_padrao']
                    if template_atual not in templates_disponiveis:
                        templates_disponiveis.append(template_atual)
                    
                    template_selecionado = st.selectbox(
                        "📝 Template",
                        options=templates_disponiveis,
                        index=templates_disponiveis.index(template_atual) if template_atual in templates_disponiveis else 0,
                        key=f"template_{evento_id}",
                        help="Escolha qual template será usado quando este gatilho disparar"
                    )
                    
                    # Condições adicionais
                    if "pagamento_proximo" in evento_id:
                        dias = st.number_input(
                            "⏰ Dias antes do vencimento",
                            min_value=1,
                            max_value=30,
                            value=3,
                            key=f"dias_{evento_id}"
                        )
                
                with col2:
                    st.write("")  # Espaço
                    st.write("")  # Espaço
                    if st.button("💾 Salvar", key=f"save_{evento_id}", use_container_width=True):
                        try:
                            conn = db.get_db_connection()
                            cursor = conn.cursor()
                            
                            condicoes = {}
                            if "pagamento_proximo" in evento_id:
                                condicoes['dias_antes'] = dias
                            
                            cursor.execute("""
                                INSERT INTO automacao_whatsapp 
                                (evento, template_id, ativo, condicoes)
                                VALUES (%s, %s, %s, %s)
                                ON CONFLICT (evento)
                                DO UPDATE SET 
                                    template_id = EXCLUDED.template_id,
                                    ativo = EXCLUDED.ativo,
                                    condicoes = EXCLUDED.condicoes
                            """, (
                                evento_id,
                                template_selecionado,  # ✅ Usar o template selecionado
                                ativo,
                                str(condicoes) if condicoes else None
                            ))
                            
                            conn.commit()
                            conn.close()
                            st.success("✅ Configuração salva!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Erro: {e}")
        
        st.divider()
        
        # Status geral
        st.subheader("📊 Status Geral")
        
        ativos = len([t for t in triggers if t[2]])  # t[2] é o campo 'ativo'
        total = len(eventos)
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Total de Gatilhos", total)
        col2.metric("Ativos", ativos)
        col3.metric("Inativos", total - ativos)
    
    # ========== TAB HISTÓRICO ==========
    with tab_historico:
        st.subheader("📊 Histórico de Automações")
        
        try:
            conn = db.get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT 
                    n.id,
                    n.tipo,
                    n.mensagem,
                    n.status,
                    n.data_envio,
                    p.nome as prestador_nome,
                    m.nome as montador_nome,
                    n.metadata
                FROM notificacoes_whatsapp n
                LEFT JOIN prestadores p ON n.prestador_id = p.id
                LEFT JOIN montadores m ON n.montador_id = m.id
                WHERE n.tipo != 'manual'
                ORDER BY n.data_envio DESC
                LIMIT 50
            """)
            
            historico = cursor.fetchall()
            conn.close()
            
            if not historico:
                st.info("Nenhuma automação executada ainda.")
            else:
                # Filtros
                col1, col2 = st.columns(2)
                with col1:
                    filtro_tipo = st.selectbox(
                        "Filtrar por Tipo",
                        ["Todos", "nota_fiscal", "confirmacao", "lembrete"]
                    )
                with col2:
                    filtro_status = st.selectbox(
                        "Filtrar por Status",
                        ["Todos", "enviado", "erro"]
                    )
                
                # Aplicar filtros
                historico_filtrado = historico
                if filtro_tipo != "Todos":
                    historico_filtrado = [h for h in historico_filtrado if h[1] == filtro_tipo]
                if filtro_status != "Todos":
                    historico_filtrado = [h for h in historico_filtrado if h[3] == filtro_status]
                
                st.caption(f"Mostrando {len(historico_filtrado)} de {len(historico)} registros")
                
                # Exibir histórico
                for h in historico_filtrado:
                    destinatario = h[5] or h[6] or "Desconhecido"
                    
                    with st.expander(
                        f"{'✅' if h[3] == 'enviado' else '❌'} "
                        f"{destinatario} - {h[4].strftime('%d/%m/%Y %H:%M')}"
                    ):
                        col1, col2 = st.columns([2, 1])
                        
                        with col1:
                            st.markdown(f"**Destinatário:** {destinatario}")
                            st.markdown(f"**Tipo:** {h[1]}")
                            st.markdown(f"**Status:** {h[3]}")
                        
                        with col2:
                            st.markdown(f"**Data:** {h[4].strftime('%d/%m/%Y')}")
                            st.markdown(f"**Hora:** {h[4].strftime('%H:%M:%S')}")
                        
                        st.divider()
                        st.markdown("**Mensagem:**")
                        st.text(h[2][:300] + "..." if len(h[2]) > 300 else h[2])
        
        except Exception as e:
            st.error(f"❌ Erro ao carregar histórico: {e}")
