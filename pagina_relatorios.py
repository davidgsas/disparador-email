"""
Página de Relatórios de Pagamentos no Streamlit
"""

import streamlit as st
import relatorio_pagamentos as rp
from datetime import datetime, date
import io
import pandas as pd

def mostrar_pagina_relatorios():
    """Exibe a página de relatórios de pagamentos"""
    
    st.title("Relatórios de Pagamentos")
    st.markdown("---")
    
    # Tipo de relatório
    tipo_relatorio = st.radio(
        "Tipo de Relatório",
        ["Sintético (Resumo)", "Analítico (Detalhado)"],
        horizontal=True,
        help="Sintético: apenas totais e resumo | Analítico: todos os lotes detalhados"
    )
    
    st.markdown("---")
    
    try:
        # Buscar prestadores com lotes
        try:
            prestadores = rp.get_lista_prestadores_com_lotes()
        except Exception as e:
            st.error(f"Erro ao buscar prestadores: {str(e)}")
            import traceback
            st.code(traceback.format_exc())
            return
        
        if not prestadores:
            st.warning("Nenhum prestador com lotes cadastrados encontrado.")
            st.info("Verifique se há lotes cadastrados no sistema.")
            return
        
        st.success(f"{len(prestadores)} prestadores encontrados com lotes")
        
        # Criar tabs
        tab_gerar, tab_os, tab_lista = st.tabs(["Gerar Relatório", "Relatório de O.S.", "Visão Geral"])
        
        with tab_gerar:
            st.subheader("Gerar Relatório por Prestador")
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                # Criar dicionário de prestadores para o selectbox
                prestadores_dict = {f"{p['nome']} (ID: {p['id']})": p['id'] for p in prestadores}
                
                prestador_selecionado = st.selectbox(
                    "Selecione o Prestador",
                    options=list(prestadores_dict.keys()),
                    help="Escolha o prestador para gerar o relatório"
                )
                
                prestador_id = prestadores_dict[prestador_selecionado]
                prestador_info = next(p for p in prestadores if p['id'] == prestador_id)
            
            with col2:
                st.info(f"**Total de Lotes:** {prestador_info['total_lotes']}")
            
            # Filtro de data
            st.subheader("Período (opcional)")
            
            col_data1, col_data2, col_data3 = st.columns([2, 2, 1])
            
            with col_data1:
                usar_filtro_data = st.checkbox("Filtrar por período", value=False)
            
            data_inicio = None
            data_fim = None
            
            if usar_filtro_data:
                with col_data2:
                    data_inicio = st.date_input(
                        "Data Início",
                        value=None,
                        help="Data inicial para filtrar os lotes"
                    )
                
                with col_data3:
                    data_fim = st.date_input(
                        "Data Fim",
                        value=date.today(),
                        help="Data final para filtrar os lotes"
                    )
            
            st.markdown("---")
            
            # Botões de ação
            col_btn1, col_btn2 = st.columns(2)
            
            with col_btn1:
                if st.button("Visualizar Dados", type="primary", use_container_width=True):
                    with st.spinner("Carregando dados..."):
                        try:
                            # Converter datas apenas se existirem
                            dt_inicio = data_inicio.strftime('%Y-%m-%d') if data_inicio else None
                            dt_fim = data_fim.strftime('%Y-%m-%d') if data_fim else None
                            
                            dados = rp.get_relatorio_pagamentos_prestador(
                                prestador_id,
                                dt_inicio,
                                dt_fim
                            )
                            
                            if dados:
                                st.session_state.dados_relatorio = dados
                                st.session_state.prestador_id_relatorio = prestador_id
                                st.session_state.tipo_relatorio = tipo_relatorio
                                st.rerun()
                        except Exception as e:
                            st.error(f"Erro ao buscar dados: {str(e)}")
                            import traceback
                            st.code(traceback.format_exc())
            
            with col_btn2:
                if st.button("Baixar PDF", type="secondary", use_container_width=True):
                    with st.spinner("Gerando PDF..."):
                        try:
                            # Converter datas apenas se existirem
                            dt_inicio = data_inicio.strftime('%Y-%m-%d') if data_inicio else None
                            dt_fim = data_fim.strftime('%Y-%m-%d') if data_fim else None
                            
                            pdf_bytes = rp.gerar_pdf_relatorio(
                                prestador_id,
                                dt_inicio,
                                dt_fim
                            )
                            
                            # Nome do arquivo
                            prestador_nome = prestador_info['nome'].replace(' ', '_')[:50]
                            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                            tipo_str = "Sintetico" if "Sintético" in tipo_relatorio else "Analitico"
                            filename = f"Relatorio_{tipo_str}_{prestador_nome}_{timestamp}.pdf"
                            
                            st.download_button(
                                label="Clique para baixar o PDF",
                                data=pdf_bytes,
                                file_name=filename,
                                mime="application/pdf",
                                type="primary",
                                use_container_width=True
                            )
                            
                            st.success("PDF gerado com sucesso!")
                            
                        except Exception as e:
                            st.error(f"Erro ao gerar PDF: {str(e)}")
                            import traceback
                            st.code(traceback.format_exc())
            
            # Exibir dados se existirem na session_state
            if 'dados_relatorio' in st.session_state and st.session_state.get('prestador_id_relatorio') == prestador_id:
                st.markdown("---")
                
                # Verificar tipo de relatório salvo
                tipo_salvo = st.session_state.get('tipo_relatorio', 'Sintético (Resumo)')
                
                if "Sintético" in tipo_salvo:
                    st.subheader("Resumo Sintético - Totais")
                else:
                    st.subheader("Relatório Analítico - Detalhado")
                
                dados = st.session_state.dados_relatorio
                
                # Métricas principais (sempre exibir)
                col_m1, col_m2, col_m3 = st.columns(3)
                
                with col_m1:
                    st.metric(
                        "Total Pago",
                        f"R$ {dados['totais']['pago']:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'),
                        f"{dados['totais']['quantidade_pagos']} lote(s)",
                        delta_color="normal"
                    )
                
                with col_m2:
                    st.metric(
                        "Total Pendente",
                        f"R$ {dados['totais']['pendente']:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'),
                        f"{dados['totais']['quantidade_pendentes']} lote(s)",
                        delta_color="inverse"
                    )
                
                with col_m3:
                    st.metric(
                        "Total Geral",
                        f"R$ {dados['totais']['geral']:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'),
                        f"{dados['totais']['quantidade_total']} lote(s)"
                    )
                
                # RELATÓRIO SINTÉTICO - Apenas totais por status
                if "Sintético" in tipo_salvo:
                    st.markdown("---")
                    st.markdown("### Resumo por Status")
                    
                    col_s1, col_s2 = st.columns(2)
                    
                    with col_s1:
                        st.success("**Lotes Pagos**")
                        st.write(f"Quantidade: **{dados['totais']['quantidade_pagos']}** lotes")
                        st.write(f"Valor Total: **R$ {dados['totais']['pago']:,.2f}**".replace(',', 'X').replace('.', ',').replace('X', '.'))
                    
                    with col_s2:
                        st.warning("**Lotes Pendentes**")
                        st.write(f"Quantidade: **{dados['totais']['quantidade_pendentes']}** lotes")
                        st.write(f"Valor Total: **R$ {dados['totais']['pendente']:,.2f}**".replace(',', 'X').replace('.', ',').replace('X', '.'))
                    
                    st.info("Para ver os detalhes de cada lote, selecione 'Analítico (Detalhado)' e visualize novamente.")
                
                # RELATÓRIO ANALÍTICO - Tabelas detalhadas
                else:
                    # Tabelas
                    if dados['lotes_pagos']:
                        st.markdown("### Lotes Pagos")
                        df_pagos = pd.DataFrame(dados['lotes_pagos'])
                        
                        # Formatar colunas
                        df_pagos['valor_fmt'] = df_pagos['valor_total'].apply(lambda x: f"R$ {x:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
                        df_pagos['data_envio_fmt'] = pd.to_datetime(df_pagos['data_envio']).dt.strftime('%d/%m/%Y')
                        df_pagos['data_pagamento_fmt'] = pd.to_datetime(df_pagos['data_pagamento']).dt.strftime('%d/%m/%Y')
                        df_pagos['vencimento_fmt'] = pd.to_datetime(df_pagos['vencimento']).dt.strftime('%d/%m/%Y')
                        df_pagos['nf'] = df_pagos['nota_fiscal_path'].apply(lambda x: 'Sim' if x else 'Não')
                        
                        st.dataframe(
                            df_pagos[['id', 'periodo', 'valor_fmt', 'data_envio_fmt', 'data_pagamento_fmt', 'vencimento_fmt', 'nf', 'status']].rename(columns={
                                'id': 'Lote #',
                                'periodo': 'Período',
                                'valor_fmt': 'Valor',
                                'data_envio_fmt': 'Data Envio',
                                'data_pagamento_fmt': 'Data Pagto',
                                'vencimento_fmt': 'Vencimento',
                                'nf': 'NF',
                                'status': 'Status'
                            }),
                            use_container_width=True,
                            hide_index=True
                        )
                    else:
                        st.info("Nenhum lote pago encontrado.")
                    
                    if dados['lotes_pendentes']:
                        st.markdown("### Lotes Pendentes")
                        df_pendentes = pd.DataFrame(dados['lotes_pendentes'])
                        
                        # Formatar colunas
                        df_pendentes['valor_fmt'] = df_pendentes['valor_total'].apply(lambda x: f"R$ {x:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
                        df_pendentes['data_envio_fmt'] = pd.to_datetime(df_pendentes['data_envio']).dt.strftime('%d/%m/%Y')
                        df_pendentes['vencimento_fmt'] = pd.to_datetime(df_pendentes['vencimento']).dt.strftime('%d/%m/%Y')
                        df_pendentes['nf'] = df_pendentes['nota_fiscal_path'].apply(lambda x: 'Sim' if x else 'Não')
                        df_pendentes['situacao'] = df_pendentes['dias_vencido'].apply(lambda x: f'{x}d vencido' if x else 'OK')
                        
                        st.dataframe(
                            df_pendentes[['id', 'periodo', 'valor_fmt', 'data_envio_fmt', 'vencimento_fmt', 'situacao', 'nf', 'status']].rename(columns={
                                'id': 'Lote #',
                                'periodo': 'Período',
                                'valor_fmt': 'Valor',
                                'data_envio_fmt': 'Data Envio',
                                'vencimento_fmt': 'Vencimento',
                                'situacao': 'Situação',
                                'nf': 'NF',
                                'status': 'Status'
                            }),
                            use_container_width=True,
                            hide_index=True
                        )
                    else:
                        st.info("Nenhum lote pendente encontrado.")
        
        with tab_os:
            st.subheader("Relatório Detalhado de Ordens de Serviço")
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                # Criar dicionário de prestadores para o selectbox
                prestadores_dict = {f"{p['nome']} (ID: {p['id']})": p['id'] for p in prestadores}
                
                prestador_selecionado_os = st.selectbox(
                    "Selecione o Prestador",
                    options=list(prestadores_dict.keys()),
                    help="Escolha o prestador para ver as O.S.",
                    key="select_prestador_os"
                )
                
                prestador_id_os = prestadores_dict[prestador_selecionado_os]
                prestador_info_os = next(p for p in prestadores if p['id'] == prestador_id_os)
            
            with col2:
                st.info(f"**Total de Lotes:** {prestador_info_os['total_lotes']}")
            
            # Filtro de data
            st.subheader("Período (opcional)")
            
            col_data1, col_data2, col_data3 = st.columns([2, 2, 1])
            
            with col_data1:
                usar_filtro_data_os = st.checkbox("Filtrar por período", value=False, key="filtro_data_os")
            
            data_inicio_os = None
            data_fim_os = None
            
            if usar_filtro_data_os:
                with col_data2:
                    data_inicio_os = st.date_input(
                        "Data Início",
                        value=None,
                        help="Data inicial para filtrar",
                        key="data_inicio_os"
                    )
                
                with col_data3:
                    data_fim_os = st.date_input(
                        "Data Fim",
                        value=date.today(),
                        help="Data final para filtrar",
                        key="data_fim_os"
                    )
            
            st.markdown("---")
            
            # Botão para carregar O.S.
            if st.button("Carregar Ordens de Serviço", type="primary", use_container_width=True):
                with st.spinner("Buscando O.S..."):
                    try:
                        dt_inicio = data_inicio_os.strftime('%Y-%m-%d') if data_inicio_os else None
                        dt_fim = data_fim_os.strftime('%Y-%m-%d') if data_fim_os else None
                        
                        os_list = rp.get_os_detalhadas_prestador(prestador_id_os, dt_inicio, dt_fim)
                        
                        if os_list:
                            st.session_state.os_list = os_list
                            st.session_state.prestador_id_os = prestador_id_os
                            st.rerun()
                        else:
                            st.warning("Nenhuma O.S. encontrada para este prestador.")
                    except Exception as e:
                        st.error(f"Erro ao buscar O.S.: {str(e)}")
                        import traceback
                        st.code(traceback.format_exc())
            
            # Exibir O.S. se existirem
            if 'os_list' in st.session_state and st.session_state.get('prestador_id_os') == prestador_id_os:
                st.markdown("---")
                st.subheader("Ordens de Serviço Detalhadas")
                
                os_list = st.session_state.os_list
                
                if os_list:
                    # Criar DataFrame
                    df_os = pd.DataFrame(os_list)
                    
                    # Formatar valores
                    df_os['valor_fmt'] = df_os['valor'].apply(lambda x: f"R$ {x:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
                    df_os['valor_extra_fmt'] = df_os['valor_extra'].apply(lambda x: f"R$ {x:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.') if x > 0 else '-')
                    df_os['valor_total_fmt'] = df_os['valor_total'].apply(lambda x: f"R$ {x:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
                    df_os['data_execucao_fmt'] = pd.to_datetime(df_os['data_execucao']).dt.strftime('%d/%m/%Y')
                    df_os['lote_data_envio_fmt'] = pd.to_datetime(df_os['lote_data_envio']).dt.strftime('%d/%m/%Y')
                    df_os['lote_data_recebimento_nf_fmt'] = df_os['lote_data_recebimento_nf'].apply(
                        lambda x: pd.to_datetime(x).strftime('%d/%m/%Y') if pd.notna(x) else '-'
                    )
                    df_os['status_pago'] = df_os['lote_status'].apply(lambda x: 'Sim' if x == 'PAGO' else 'Não')
                    
                    # Métricas
                    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
                    
                    with col_m1:
                        st.metric("Total de O.S.", len(df_os))
                    
                    with col_m2:
                        total_valor = df_os['valor_total'].sum()
                        st.metric("Valor Total", f"R$ {total_valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
                    
                    with col_m3:
                        os_pagas = df_os[df_os['lote_status'] == 'PAGO']
                        st.metric("O.S. Pagas", len(os_pagas))
                    
                    with col_m4:
                        os_pendentes = df_os[df_os['lote_status'] != 'PAGO']
                        st.metric("O.S. Pendentes", len(os_pendentes))
                    
                    st.markdown("---")
                    
                    # Filtros adicionais
                    col_f1, col_f2 = st.columns(2)
                    
                    with col_f1:
                        filtro_status = st.multiselect(
                            "Filtrar por Status",
                            options=['PAGO', 'N.F. RECEBIDA', 'Em Aberto'],
                            default=['PAGO', 'N.F. RECEBIDA', 'Em Aberto'],
                            key="filtro_status_os"
                        )
                    
                    with col_f2:
                        filtro_lote = st.multiselect(
                            "Filtrar por Lote",
                            options=sorted(df_os['lote_id'].unique()),
                            default=sorted(df_os['lote_id'].unique()),
                            key="filtro_lote_os"
                        )
                    
                    # Aplicar filtros
                    df_filtrado = df_os[
                        (df_os['lote_status'].isin(filtro_status)) &
                        (df_os['lote_id'].isin(filtro_lote))
                    ]
                    
                    # Tabela completa
                    st.dataframe(
                        df_filtrado[[
                            'numero_os', 'nome_cliente', 'localidade', 'modalidade',
                            'data_execucao_fmt', 'lote_id', 'lote_periodo',
                            'valor_fmt', 'valor_extra_fmt', 'valor_total_fmt',
                            'lote_data_envio_fmt', 'lote_data_recebimento_nf_fmt', 'status_pago'
                        ]].rename(columns={
                            'numero_os': 'O.S.',
                            'nome_cliente': 'Cliente',
                            'localidade': 'Localidade',
                            'modalidade': 'Modalidade',
                            'data_execucao_fmt': 'Data Execução',
                            'lote_id': 'Lote #',
                            'lote_periodo': 'Período',
                            'valor_fmt': 'Valor',
                            'valor_extra_fmt': 'Valor Extra',
                            'valor_total_fmt': 'Valor Total',
                            'lote_data_envio_fmt': 'Data Enviado',
                            'lote_data_recebimento_nf_fmt': 'Data Recebido NF',
                            'status_pago': 'Pago'
                        }),
                        use_container_width=True,
                        hide_index=True,
                        height=500
                    )
                    
                    # Botão para download Excel
                    st.markdown("---")
                    
                    # Criar arquivo Excel para download
                    output = io.BytesIO()
                    with pd.ExcelWriter(output, engine='openpyxl') as writer:
                        df_filtrado[[
                            'numero_os', 'nome_cliente', 'localidade', 'modalidade',
                            'data_execucao_fmt', 'lote_id', 'lote_periodo',
                            'valor', 'valor_extra', 'valor_total',
                            'lote_data_envio_fmt', 'lote_data_recebimento_nf_fmt', 'lote_status', 'status_pago'
                        ]].rename(columns={
                            'numero_os': 'O.S.',
                            'nome_cliente': 'Cliente',
                            'localidade': 'Localidade',
                            'modalidade': 'Modalidade',
                            'data_execucao_fmt': 'Data Execução',
                            'lote_id': 'Lote',
                            'lote_periodo': 'Período',
                            'valor': 'Valor',
                            'valor_extra': 'Valor Extra',
                            'valor_total': 'Valor Total',
                            'lote_data_envio_fmt': 'Data Enviado',
                            'lote_data_recebimento_nf_fmt': 'Data Recebido NF',
                            'lote_status': 'Status',
                            'status_pago': 'Pago'
                        }).to_excel(writer, sheet_name='OS_Detalhadas', index=False)
                    
                    excel_data = output.getvalue()
                    
                    prestador_nome = prestador_info_os['nome'].replace(' ', '_')[:50]
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    
                    st.download_button(
                        label="Baixar Excel - Relatório de O.S.",
                        data=excel_data,
                        file_name=f"OS_Detalhadas_{prestador_nome}_{timestamp}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True
                    )
                else:
                    st.info("Nenhuma O.S. encontrada.")
        
        with tab_lista:
            st.subheader("Visão Geral de Todos os Prestadores")
            
            # Criar DataFrame
            df = pd.DataFrame(prestadores)
            
            # Calcular total geral
            df['total_geral'] = df['total_pago'] + df['total_pendente']
            
            # Formatar valores
            df['total_pago_fmt'] = df['total_pago'].apply(lambda x: f"R$ {x:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
            df['total_pendente_fmt'] = df['total_pendente'].apply(lambda x: f"R$ {x:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
            df['total_geral_fmt'] = df['total_geral'].apply(lambda x: f"R$ {x:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
            
            # Exibir tabela
            st.dataframe(
                df[['id', 'nome', 'total_lotes', 'total_pago_fmt', 'total_pendente_fmt', 'total_geral_fmt']].rename(columns={
                    'id': 'ID',
                    'nome': 'Nome do Prestador',
                    'total_lotes': 'Qtd Lotes',
                    'total_pago_fmt': 'Total Pago',
                    'total_pendente_fmt': 'Total Pendente',
                    'total_geral_fmt': 'Total Geral'
                }),
                use_container_width=True,
                hide_index=True
            )
            
            # Totais gerais
            st.markdown("---")
            st.subheader("Totais Gerais (Todos os Prestadores)")
            
            total_pago_geral = df['total_pago'].sum()
            total_pendente_geral = df['total_pendente'].sum()
            total_geral_geral = df['total_geral'].sum()
            
            col_t1, col_t2, col_t3 = st.columns(3)
            
            with col_t1:
                st.metric(
                    "Total Pago",
                    f"R$ {total_pago_geral:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
                )
            
            with col_t2:
                st.metric(
                    "Total Pendente",
                    f"R$ {total_pendente_geral:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
                )
            
            with col_t3:
                st.metric(
                    "Total Geral",
                    f"R$ {total_geral_geral:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
                )
    
    except Exception as e:
        st.error(f"ERRO CRÍTICO: {str(e)}")
        import traceback
        st.code(traceback.format_exc())
