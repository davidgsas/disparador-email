import os
import base64
import datetime
import re
from pathlib import Path
import json
import time

import streamlit as st
import pandas as pd
import requests
from dotenv import load_dotenv
from msal import PublicClientApplication, SerializableTokenCache
from jinja2 import Template
from weasyprint import HTML

import database as db
from templates.variaveis import mostrar_variaveis_disponiveis

# --- Novas Funções de Configuração ---
CONFIG_FILE = Path("config.json")
DIAS_SEMANA_MAP = {
    "Monday": "Segunda-feira",
    "Tuesday": "Terça-feira", 
    "Wednesday": "Quarta-feira",
    "Thursday": "Quinta-feira",
    "Friday": "Sexta-feira",
    "Saturday": "Sábado",
    "Sunday": "Domingo"
}

def load_config():
    """Carrega as configurações salvas do arquivo JSON."""
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {}

def save_config():
    """Salva as configurações atuais da session_state no arquivo JSON."""
    config_data = {
        "prestador_cc": st.session_state.get("prestador_cc", ""),
        "prestador_subject": st.session_state.get("prestador_subject", ""),
        "prestador_body": st.session_state.get("prestador_body", ""),
        "montador_cc": st.session_state.get("montador_cc", ""),
        "montador_subject": st.session_state.get("montador_subject", ""),
        "montador_body": st.session_state.get("montador_body", "")
    }
    with open(CONFIG_FILE, "w") as f:
        json.dump(config_data, f, indent=4)

def convert_plain_text_to_html(text):
    """Converte texto com quebras de linha em HTML simples com <br>."""
    if not text:
        return ""
    # Envolve o texto em parágrafos e substitui quebras de linha por <br>
    return f"<p>{text.replace(chr(10), '<br>')}</p>"

def verificar_pendencias(entidades, tipo):
    pendentes = []
    hoje = datetime.date.today()
    ano_atual, semana_atual, dia_semana_hoje_num = hoje.isocalendar()
    dia_semana_hoje_en = hoje.strftime('%A')
    dia_do_mes_hoje = hoje.day

    for entidade in entidades:
        regra, dias = entidade.get('regra_envio'), entidade.get('dias_envio')
        if not regra or regra == "Nenhuma" or not dias:
            continue
        
        entidade_id = entidade['id']
        pendente = False
        
        if regra == 'Semanal' and DIAS_SEMANA_MAP.get(dia_semana_hoje_en) == dias:
            if not db.get_envios_na_semana(tipo, entidade_id, ano_atual, semana_atual) and not db.foi_ignorado_na_semana(tipo, entidade_id, ano_atual, semana_atual):
                pendente = True
        elif regra in ['Mensal (Dia Fixo)', 'Quinzenal']:
            dias_envio_mes = [int(d.strip()) for d in dias.split(',')]
            if dia_do_mes_hoje in dias_envio_mes:
                # (Lógica simplificada, pode ser melhorada para não mostrar se já foi enviado no dia)
                pendente = True
        
        if pendente:
            pendentes.append(entidade)
            
    return pendentes

st.set_page_config(page_title="Disparador Novo Mundo", layout="wide")
TOKEN_CACHE_PATH = Path("token_cache.json")
cache = SerializableTokenCache()
if TOKEN_CACHE_PATH.exists():
    cache.deserialize(TOKEN_CACHE_PATH.read_text())

load_dotenv()
CLIENT_ID = os.getenv("CLIENT_ID")
TENANT_ID = os.getenv("TENANT_ID")
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPES = ["Mail.Send", "Mail.ReadWrite"]

pca = PublicClientApplication(client_id=CLIENT_ID, authority=AUTHORITY, token_cache=cache)

# --- FLUXO DE LOGIN ---
if "access_token" not in st.session_state:
    accounts = pca.get_accounts()
    if accounts:
        result = pca.acquire_token_silent(SCOPES, account=accounts[0])
        if result and "access_token" in result:
            st.session_state.access_token = result["access_token"]
            st.session_state.user = accounts[0].get("username")

def login_callback():
    flow = pca.initiate_device_flow(scopes=SCOPES)
    st.info(flow["message"])
    auth = pca.acquire_token_by_device_flow(flow)
    if "access_token" in auth:
        st.session_state.access_token = auth["access_token"]
        TOKEN_CACHE_PATH.write_text(cache.serialize())
        me = requests.get("https://graph.microsoft.com/v1.0/me", headers={"Authorization": f"Bearer {auth['access_token']}"}).json()
        st.session_state.user = me.get("userPrincipalName", "")
        st.rerun() # Força o recarregamento da página após o login
    else:
        st.session_state.login_error = auth.get("error_description", "desconhecido")

if "access_token" not in st.session_state:
    st.title("🔐 Login com Office 365")
    st.write("Exclua o arquivo 'token_cache.json' se precisar re-autorizar permissões.")
    st.button("Entrar com Office 365", on_click=login_callback)
    if "login_error" in st.session_state: st.error(f"❌ Falha no login: {st.session_state.login_error}")
    st.stop() # Interrompe a execução aqui se não estiver logado

# --- APLICAÇÃO PRINCIPAL (SÓ EXECUTA SE LOGADO) ---
config = load_config()

st.sidebar.title("MENU")
app_mode = st.sidebar.selectbox("Selecione a Página", ["Dashboard de Pendências", "Serviços (Prestadores)", "Montagem (Montadores)"])
st.sidebar.info(f"**Conectado como:** \n{st.session_state.user}")

if app_mode == "Dashboard de Pendências":
    st.title("🗓️ Dashboard de Pendências de Envio")
    
    st.subheader("Prestadores com Envios Pendentes Oggi")
    pendencias_prestadores = verificar_pendencias(db.get_all_prestadores(), 'prestador')
    if not pendencias_prestadores:
        st.success("Nenhum prestador com pendências para hoje!")
    else:
        for p in pendencias_prestadores:
            cols = st.columns([3, 2, 1])
            cols[0].write(f"**{p['nome']}**")
            cols[1].write(f"Regra: {p['regra_envio']} ({p['dias_envio']})")
            if cols[2].button("Ignorar Envio", key=f"ign_p_{p['id']}"):
                hoje = datetime.date.today()
                ano, semana, _ = hoje.isocalendar()
                if p['regra_envio'] == 'Semanal':
                    db.ignorar_envio_semanal('prestador', p['id'], ano, semana)
                    st.success(f"Envio para {p['nome']} ignorado nesta semana.")
                    st.rerun()
    
    st.subheader("Montadores com Envios Pendentes Oggi")
    pendencias_montadores = verificar_pendencias(db.get_all_montadores(apenas_ativos=True), 'montador')
    if not pendencias_montadores:
        st.success("Nenhum montador com pendências para hoje!")
    else:
        for m in pendencias_montadores:
            cols = st.columns([3, 2, 1])
            cols[0].write(f"**{m['nome']}**")
            cols[1].write(f"Regra: {m['regra_envio']} ({m['dias_envio']})")
            if cols[2].button("Ignorar Envio", key=f"ign_m_{m['id']}"):
                hoje = datetime.date.today()
                ano, semana, _ = hoje.isocalendar()
                if m['regra_envio'] == 'Semanal':
                    db.ignorar_envio_semanal('montador', m['id'], ano, semana)
                    st.success(f"Envio para {m['nome']} ignorado nesta semana.")
                    st.rerun()

elif app_mode == "Serviços (Prestadores)":
    st.sidebar.divider()
    page = st.sidebar.radio("Navegar", ["Enviar Boletins", "Gerenciar Prestadores", "Histórico de Envios", "Editor de PDF (Serviços)"])

    if page == "Enviar Boletins":
        st.title("📤 Envio de Boletins de Serviço")
        input_method = st.tabs(["Lançamento Manual", "Importar via Excel"])
        df_para_envio = None

        with input_method[0]:
            st.header("Adicionar Boletim Manualmente")
            if 'manual_entries' not in st.session_state: 
                st.session_state.manual_entries = []
            
            with st.form("manual_entry_form", clear_on_submit=True):
                prestador_nomes = [p['nome'] for p in db.get_all_prestadores()]
                if not prestador_nomes:
                    st.warning("Nenhum prestador cadastrado.")
                else:
                    nome_prestador = st.selectbox("Prestador", options=prestador_nomes)
                    periodo, o_s, modalidade = st.text_input("Período"), st.text_input("O.S"), st.text_input("Modalidade")
                    data_execucao = st.date_input("Data de Execução")
                    valor, valor_extra = st.number_input("Valor", 0.0, format="%.2f"), st.number_input("Valor Extra", 0.0, format="%.2f")
                    motivo_valor_extra = st.text_input("Motivo Valor Extra")
                    valor_total = valor + valor_extra
                    st.metric("Valor Total", f"R$ {valor_total:.2f}")
                    
                    if st.form_submit_button("Adicionar à Lista"):
                        st.session_state.manual_entries.append({
                            "nome_prestador": nome_prestador, 
                            "periodo": periodo, 
                            "o_s": o_s, 
                            "modalidade": modalidade, 
                            "data_execucao": data_execucao, 
                            "valor_custo_prestador": valor, 
                            "valor_extra": valor_extra, 
                            "motivo_extra": motivo_valor_extra, 
                            "valor_total": valor_total
                        })
                        
            if st.session_state.manual_entries:
                df_para_envio = pd.DataFrame(st.session_state.manual_entries)
                st.subheader("Lista para Envio")
                st.dataframe(df_para_envio)
                if st.button("Limpar Lista"):
                    st.session_state.manual_entries = []
                    st.rerun()

        with input_method[1]:
            uploader = st.file_uploader("Carregue a planilha", type=["xlsx"], label_visibility="collapsed")
            if uploader:
                df = pd.read_excel(uploader)
                df.columns = [re.sub(r"\W+", "_", c.strip()).lower() for c in df.columns]
                required = ["nome_prestador", "periodo", "data_execucao", "o_s"]
                if not all(c in df.columns for c in required): 
                    st.error(f"Excel precisa das colunas: {', '.join(required)}")
                else:
                    for col in ["valor_custo_prestador", "valor_extra", "valor_total"]:
                        if col in df.columns: 
                            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)
                    df_para_envio = df
        
        st.divider()
        st.header("🚀 Disparar E-mails de Serviço")
        if df_para_envio is not None and not df_para_envio.empty:
            df_para_envio['o_s'] = df_para_envio['o_s'].astype(str)
            all_os_numbers = df_para_envio['o_s'].dropna().tolist()
            sent_os = db.check_os_list(all_os_numbers)
            blacklisted_os = db.check_os_blacklist(all_os_numbers)
            
            def get_os_status(row):
                os_numero = row['o_s']
                if os_numero in blacklisted_os:
                    return "Na blacklist"
                elif os_numero in sent_os:
                    return "Já enviado"
                return "Pendente"
            
            df_para_envio['status_envio'] = df_para_envio.apply(get_os_status, axis=1)
            
            st.subheader("Pré-visualização")
            st.dataframe(df_para_envio[['nome_prestador', 'o_s', 'status_envio']])
            
            if sent_os: 
                st.warning(f"{len(sent_os)} O.S. já enviadas serão ignoradas.")
            if blacklisted_os:
                st.warning(f"{len(blacklisted_os)} O.S. na blacklist serão ignoradas.")
            
            df_final = df_para_envio[df_para_envio['status_envio'] == 'Pendente']
            
            if df_final.empty: 
                st.error("Nenhuma O.S. nova para enviar.")
            else:
                st.success(f"Tudo pronto para enviar {len(df_final)} novas O.S.")
                
                st.sidebar.divider()
                st.sidebar.title("⚙️ Configurações de Envio (Serviços)")
                
                default_subject = "Novo Mundo Resolve | Nota Fiscal | Período: {{periodo}} | Prestador: {{nome_prestador}}"
                default_body = "Segue a relação de boletins para emissão da nota fiscal de serviços entre **{{periodo}}**.\n\nObrigado."

                mostrar_variaveis_disponiveis()
                st.text_input("CC", value=config.get("prestador_cc", "projetos.qualidade@novomundo.com.br"), key="prestador_cc", on_change=save_config)
                st.text_input("Assunto", value=config.get("prestador_subject", default_subject), key="prestador_subject", on_change=save_config)
                st.text_area("Corpo do E-mail", value=config.get("prestador_body", default_body), key="prestador_body", on_change=save_config, height=200)
                
                if st.button("▶️ ENVIAR E-MAILS PENDENTES", type="primary"):
                    report = []
                    saudacao = "Bom dia" if datetime.datetime.now().hour < 12 else "Boa tarde" if datetime.datetime.now().hour < 18 else "Boa noite"
                    invoice_tpl = Template(Path("templates/invoice_template.html").read_text(encoding="utf-8"))
                    
                    cc_list = [e.strip() for e in st.session_state.prestador_cc.split(",") if e.strip()]
                    
                    with st.spinner("Enviando e-mails..."):
                        for key, group in df_final.groupby(["nome_prestador", "periodo"]):
                            nome_prestador, periodo = key
                            prestador_info = db.get_prestador_by_name(nome_prestador)
                            if not prestador_info:
                                report.append({"Prestador": nome_prestador, "Status": "❌ Prestador não cadastrado no DB"})
                                continue
                            
                            items_raw = [r.to_dict() for _, r in group.iterrows()]
                            total_geral = float(group["valor_total"].sum())
                            items_fmt = []
                            
                            for item in items_raw:
                                data_exec = item.get('data_execucao')
                                items_fmt.append({
                                    "OS": item.get('o_s'), 
                                    "Modalidade": item.get('modalidade'), 
                                    "Data_execucao": data_exec.strftime('%d/%m/%Y') if hasattr(data_exec, 'strftime') else str(data_exec), 
                                    "Valor": f"{item.get('valor_custo_prestador', 0):.2f}", 
                                    "Valor_extra": f"{item.get('valor_extra', 0):.2f}", 
                                    "Motivo_valor_extra": item.get("motivo_extra", "-"), 
                                    "Valor_total": f"{item.get('valor_total', 0):.2f}"
                                })
                            
                            items_to_log = []
                            for item in items_raw:
                                log_item = {k: (v.isoformat() if isinstance(v, (datetime.date, datetime.datetime)) else (None if pd.isna(v) else v)) for k, v in item.items()}
                                items_to_log.append(log_item)
                            
                            lote_id = db.criar_lote_servico(prestador_info['id'], nome_prestador, periodo, total_geral, items_to_log)
                            
                            ctx = {
                                "nome_prestador": nome_prestador, 
                                "periodo": periodo, 
                                "items": items_fmt, 
                                "total_geral": total_geral, 
                                "saudacao": saudacao, 
                                "lote_id": lote_id
                            }
                            
                            subj_template = Template(st.session_state.prestador_subject)
                            body_template = Template(st.session_state.prestador_body)
                            
                            subj, body_plain = subj_template.render(**ctx), body_template.render(**ctx)
                            body_html = convert_plain_text_to_html(body_plain)
                            html_pdf = invoice_tpl.render(**ctx)
                            pdf_bytes = HTML(string=html_pdf, base_url="templates").write_pdf()

                            # Obter todos os emails do prestador (principal + adicionais)
                            prestador_emails = db.get_prestador_emails(prestador_info)
                            recipients = [{"emailAddress": {"address": email}} for email in prestador_emails]
                            
                            message_data = {
                                "subject": subj, 
                                "body": {"contentType": "HTML", "content": body_html}, 
                                "toRecipients": recipients, 
                                "attachments": [{"@odata.type": "#microsoft.graph.fileAttachment", "name": f"Relatorio_{nome_prestador.replace(' ', '_')}_Lote_{lote_id}.pdf", "contentBytes": base64.b64encode(pdf_bytes).decode()}]
                            }
                            
                            if cc_list:
                                message_data["ccRecipients"] = [{"emailAddress": {"address": cc}} for cc in cc_list]
                            
                            final_payload = { "message": message_data, "saveToSentItems": "true" }

                            resp = requests.post("https://graph.microsoft.com/v1.0/me/sendMail", headers={"Authorization": f"Bearer {st.session_state.access_token}", "Content-Type": "application/json"}, json=final_payload)
                            
                            if resp.status_code == 202:
                                time.sleep(2)
                                headers = {"Authorization": f"Bearer {st.session_state.access_token}"}
                                sent_items_url = "https://graph.microsoft.com/v1.0/me/mailfolders/sentitems/messages?$top=1&$select=conversationId"
                                sent_resp = requests.get(sent_items_url, headers=headers).json()
                                conversation_id = sent_resp['value'][0]['conversationId']
                                db.atualizar_lote_com_conversation_id(lote_id, conversation_id)
                                report.append({"Prestador": nome_prestador, "Status": f"✅ Lote #{lote_id} Enviado"})
                            else:
                                report.append({"Prestador": nome_prestador, "Status": f"❌ Erro {resp.status_code} - {resp.text}"})
                                
                    st.subheader("📋 Relatório de Envio")
                    st.table(pd.DataFrame(report))
                    st.success("Processo concluído!")
                    st.session_state.manual_entries = []

    elif page == "Gerenciar Prestadores":
        st.title("📇 Gerenciar Prestadores de Serviço")
        
        # Seção de Blacklist de OS
        with st.expander("📋 Blacklist de O.S."):
            st.subheader("Adicionar O.S. à Blacklist")
            cols = st.columns([2, 2, 1])
            
            with cols[0]:
                prestadores = {p['nome']: p['id'] for p in db.get_all_prestadores()}
                prestador_selected = st.selectbox("Prestador", options=list(prestadores.keys()))
            
            with cols[1]:
                os_input = st.text_input("Números das O.S. (separados por vírgula)")
            
            with cols[2]:
                motivo = st.text_input("Motivo (opcional)")
            
            if st.button("Adicionar à Blacklist"):
                if os_input and prestador_selected:
                    prestador_id = prestadores[prestador_selected]
                    os_numbers = [o.strip() for o in os_input.split(",")]
                    for os_numero in os_numbers:
                        success, message = db.adicionar_os_blacklist(prestador_id, os_numero, motivo)
                        st.toast(f"O.S. {os_numero}: {message}")
                    st.rerun()
                else:
                    st.warning("Selecione um prestador e insira os números das O.S.")
            
            st.divider()
            st.subheader("O.S. na Blacklist")
            os_blacklist = db.get_os_blacklist()
            
            if not os_blacklist:
                st.info("Nenhuma O.S. na blacklist.")
            else:
                for o in os_blacklist:
                    cols = st.columns([2, 2, 2, 1])
                    cols[0].text(o['prestador_nome'])
                    cols[1].text(f"O.S.: {o['os_numero']}")
                    cols[2].text(f"Motivo: {o['motivo'] or '-'}")
                    if cols[3].button("🗑️", key=f"del_os_blacklist_{o['id']}"):
                        db.remover_os_blacklist(o['prestador_id'], o['os_numero'])
                        st.success(f"O.S. {o['os_numero']} removida da blacklist!")
                        st.rerun()
        
        st.divider()
        
        with st.form("novo_prestador_form", clear_on_submit=True):
            st.subheader("Adicionar Novo Prestador")
            nome = st.text_input("Nome")
            email = st.text_input("E-mail Principal")
            emails_adicionais = st.text_input("E-mails Adicionais (separados por vírgula)", 
                                            help="Digite os emails adicionais separados por vírgula. Ex: email2@empresa.com, email3@empresa.com")
            fornecedor_id = st.text_input("Número do Fornecedor")
            regra_envio = st.selectbox("Regra de Envio", ["Nenhuma", "Semanal", "Mensal (Dia Fixo)", "Quinzenal"], key="p_regra")
            dias_envio = ""
            
            if regra_envio == "Semanal":
                dias_envio = st.selectbox("Dia da Semana", list(DIAS_SEMANA_MAP.values()), key="p_dia_sem")
            elif regra_envio in ["Mensal (Dia Fixo)", "Quinzenal"]:
                dias_envio = st.text_input("Dias do Mês (ex: 5 ou 5,20)", key="p_dia_mes")
            
            if st.form_submit_button("Adicionar"):
                if all([nome, email, fornecedor_id]):
                    success, message = db.add_prestador(nome, email, fornecedor_id, regra_envio, dias_envio, emails_adicionais.strip() if emails_adicionais.strip() else None)
                    st.toast(message)
                else:
                    st.warning("Todos os campos obrigatórios devem ser preenchidos (Nome, E-mail Principal e Número do Fornecedor).")
                    
        st.divider()
        st.subheader("Prestadores Cadastrados")
        
        for p in db.get_all_prestadores():
            with st.expander(f"{p['nome']} - ID: {p['id']}"):
                # Mostrar emails atuais
                st.info(f"**E-mail Principal:** {p['email']}")
                if p.get('emails_adicionais'):
                    emails_extras = [email.strip() for email in p['emails_adicionais'].split(',') if email.strip()]
                    st.info(f"**E-mails Adicionais:** {', '.join(emails_extras)}")
                
                with st.form(key=f"form_p_{p['id']}"):
                    st.text_input("Número do Fornecedor", value=p['fornecedor_id'], disabled=True)
                    
                    # Campo para editar emails adicionais
                    emails_adicionais_edit = st.text_input("E-mails Adicionais (separados por vírgula)", 
                                                         value=p.get('emails_adicionais', '') or '', 
                                                         key=f"p_emails_edit_{p['id']}",
                                                         help="Digite os emails adicionais separados por vírgula")
                    
                    regra_atual = p.get('regra_envio') or "Nenhuma"
                    dias_atuais = p.get('dias_envio') or ""
                    
                    regra_edit = st.selectbox("Regra de Envio", ["Nenhuma", "Semanal", "Mensal (Dia Fixo)", "Quinzenal"], index=["Nenhuma", "Semanal", "Mensal (Dia Fixo)", "Quinzenal"].index(regra_atual), key=f"p_regra_edit_{p['id']}")
                    dias_edit = ""
                    
                    if regra_edit == "Semanal":
                        dias_semana_list = list(DIAS_SEMANA_MAP.values())
                        index_sem = dias_semana_list.index(dias_atuais) if dias_atuais in dias_semana_list else 0
                        dias_edit = st.selectbox("Dia da Semana", dias_semana_list, index=index_sem, key=f"p_dia_sem_edit_{p['id']}")
                    elif regra_edit in ["Mensal (Dia Fixo)", "Quinzenal"]:
                        dias_edit = st.text_input("Dias do Mês", value=dias_atuais, key=f"p_dia_mes_edit_{p['id']}")

                    if st.form_submit_button("Salvar Alterações"):
                        db.update_prestador(p['id'], regra_edit, dias_edit, emails_adicionais_edit.strip() if emails_adicionais_edit.strip() else None)
                        st.success("Dados do prestador atualizados!")
                        st.rerun()

    elif page == "Histórico de Envios":
        st.title("📚 Histórico de Lotes Enviados (Serviços)")
        status_filter = st.selectbox("Filtrar por Status", ["Todos", "Em Aberto", "Pago", "Cancelado", "N.F. RECEBIDA"])
        
        lotes_data = db.get_all_lotes_servico()
        
        if not lotes_data:
            st.info("Nenhum lote de serviço registrado ainda.")
        else:
            for lote in lotes_data:
                if status_filter != "Todos" and lote['status'] != status_filter:
                    continue
                
                with st.container():
                    st.markdown("---")
                    cols = st.columns([1, 2, 1, 1, 1])
                    cols[0].text(f"Lote #{lote['id']}")
                    cols[1].text(lote['prestador_nome'])
                    cols[2].text(f"R$ {lote['valor_total']:.2f}")
                    cols[3].text(lote['data_envio'].strftime('%d/%m/%Y'))
                    cols[4].markdown(f"**{lote['status']}**")

                    with st.expander("Ver O.S. do Lote e Gerenciar"):
                        os_do_lote = db.get_os_by_lote_id(lote['id'])
                        if os_do_lote:
                            df_os = pd.DataFrame([item['detalhes'] for item in os_do_lote])
                            st.dataframe(df_os)
                        else:
                            st.warning("Não há O.S. detalhadas para este lote.")
                        
                        if lote['anexo_path']:
                            with open(lote['anexo_path'], "rb") as file:
                                st.download_button(label="Baixar N.F. Recebida", data=file, file_name=Path(lote['anexo_path']).name)
                        
                        st.markdown("---")
                        sub_cols = st.columns(2)
                        
                        with sub_cols[0]:
                            status_options = ["Em Aberto", "Pago", "Cancelado", "N.F. RECEBIDA"]
                            try: 
                                current_status_index = status_options.index(lote['status'])
                            except ValueError: 
                                current_status_index = 0
                            
                            new_status = st.selectbox("Alterar status do lote:", options=status_options, index=current_status_index, key=f"status_lote_{lote['id']}")
                            if st.button("Salvar Status", key=f"save_lote_{lote['id']}"):
                                db.update_lote_servico_status(lote['id'], new_status)
                                st.success(f"Status do Lote #{lote['id']} atualizado!")
                                st.rerun()
                        
                        with sub_cols[1]:
                            st.write("")
                            st.write("")
                            if st.button("🚨 Excluir Lote", key=f"del_lote_{lote['id']}"):
                                db.delete_lote_servico(lote['id'])
                                st.success(f"Lote #{lote['id']} e todas as suas O.S. foram excluídos!")
                                st.rerun()

    elif page == "Editor de PDF (Serviços)":
        st.title("📄 Editor de Template do PDF (Serviços)")
        template_path = Path("templates/invoice_template.html")
        html_content = template_path.read_text(encoding="utf-8")
        new_html_content = st.text_area("Código HTML", value=html_content, height=600)
        if st.button("Salvar Template"):
            template_path.write_text(new_html_content, encoding="utf-8")
            st.success("Template salvo!")

elif app_mode == "Montagem (Montadores)":
    st.sidebar.divider()
    page = st.sidebar.radio("Navegar", ["Enviar Pagamentos", "Gerenciar Montadores", "Histórico de Montagens"])
    
    if page == "Enviar Pagamentos":
        st.title("💸 Enviar Pagamentos de Montagem")
        input_method = st.tabs(["Lançamento Manual", "Importar via Excel"])
        df_para_envio_montagem = None

        with input_method[0]:
            st.header("Adicionar Montagem Manualmente")
            if 'manual_montagem_entries' not in st.session_state:
                st.session_state.manual_montagem_entries = []
                
            with st.form("manual_montagem_form", clear_on_submit=True):
                montadores = db.get_all_montadores(apenas_ativos=True)
                montador_map = {m['nome']: m['identificador'] for m in montadores}
                
                if not montador_map:
                    st.warning("Nenhum montador ativo cadastrado.")
                else:
                    montador_nome = st.selectbox("Montador", options=montador_map.keys())
                    boletim, data_montagem = st.text_input("Boletim Montagem"), st.date_input("Data da Montagem")
                    valor_venda = st.number_input("Média de Valor Venda (R$)", 0.0, format="%.2f")
                    cliente, produto = st.text_input("Cliente"), st.text_input("Nome do Produto")
                    
                    if st.form_submit_button("Adicionar à Lista"):
                        st.session_state.manual_montagem_entries.append({
                            "identificador_do_montador": montador_map[montador_nome], 
                            "identificador_boletim_montagem": boletim, 
                            "data_da_montagem": data_montagem, 
                            "media_de_valor_venda": valor_venda, 
                            "nome_do_cliente": cliente, 
                            "nome_produto": produto, 
                            "nome_do_montador": montador_nome
                        })
                        
            if st.session_state.manual_montagem_entries:
                df_para_envio_montagem = pd.DataFrame(st.session_state.manual_montagem_entries)
                st.subheader("Lista para Envio")
                st.dataframe(df_para_envio_montagem[['nome_do_montador', 'identificador_boletim_montagem', 'media_de_valor_venda']])
                if st.button("Limpar Lista de Montagem"):
                    st.session_state.manual_montagem_entries = []
                    st.rerun()

        with input_method[1]:
            uploader = st.file_uploader("Carregue o relatório de montagem", type=["xlsx"])
            if uploader:
                df = pd.read_excel(uploader)
                df.columns = [re.sub(r"\W+", "_", c.strip()).lower() for c in df.columns]
                required_cols = ['identificador_do_montador', 'identificador_boletim_montagem', 'data_da_montagem', 'media_de_valor_venda', 'nome_produto']
                if not all(c in df.columns for c in required_cols):
                    st.error(f"Excel precisa das colunas: {', '.join(required_cols)}")
                else: 
                    df_para_envio_montagem = df
        
        st.divider()
        st.header("🚀 Processar e Disparar Pagamentos")
        
        if df_para_envio_montagem is not None and not df_para_envio_montagem.empty:
            df = df_para_envio_montagem
            df['identificador_boletim_montagem'] = df['identificador_boletim_montagem'].astype(str)
            df['identificador_do_montador'] = df['identificador_do_montador'].astype(str)
            df['data_da_montagem'] = pd.to_datetime(df['data_da_montagem'])
            
            all_boletins = df['identificador_boletim_montagem'].unique().tolist()
            sent_boletins = db.check_boletim_list(all_boletins)
            blacklisted_boletins = db.check_boletins_blacklist(all_boletins)
            
            def get_status(row):
                boletim = row['identificador_boletim_montagem']
                if boletim in blacklisted_boletins:
                    return "Na blacklist"
                elif boletim in sent_boletins:
                    return "Já enviado"
                return "Pendente"
            
            df['status_envio'] = df.apply(get_status, axis=1)
            st.dataframe(df[['identificador_do_montador', 'identificador_boletim_montagem', 'status_envio']])
            df_final = df[df['status_envio'] == 'Pendente']

            if df_final.empty:
                st.error("Nenhuma montagem nova para processar.")
            else:
                st.sidebar.divider()
                st.sidebar.title("⚙️ Configurações de E-mail (Montador)")
                
                default_subject_montador = "Relatório de Pagamento de Montagem - Período: {{periodo_relatorio}}"
                default_body_montador = "Olá, {{nome_montador}},\n\nSegue em anexo o seu relatório de pagamento de montagens referente ao período de **{{periodo_relatorio}}**.\n\nQualquer dúvida, estamos à disposição."

                mostrar_variaveis_disponiveis()
                st.text_input("CC (Montadores)", value=config.get("montador_cc", "projetos.qualidade@novomundo.com.br"), key="montador_cc", on_change=save_config)
                st.text_input("Assunto (Montadores)", value=config.get("montador_subject", default_subject_montador), key="montador_subject", on_change=save_config)
                st.text_area("Corpo do E-mail (Montadores)", value=config.get("montador_body", default_body_montador), key="montador_body", on_change=save_config, height=200)
                
                if st.button("▶️ PROCESSAR E ENVIAR E-MAILS", type="primary"):
                    report_summary = []
                    cc_list_montador = [e.strip() for e in st.session_state.montador_cc.split(",") if e.strip()]
                    
                    with st.spinner("Processando e enviando..."):
                        for montador_id_str, group in df_final.groupby('identificador_do_montador'):
                            montador_info = db.get_montador_by_identificador(montador_id_str)
                            if not montador_info:
                                report_summary.append({"Montador ID": montador_id_str, "Status": "❌ Não cadastrado"})
                                continue
                            
                            group['comissao_calculada'] = group['media_de_valor_venda'] * montador_info['percentual_comissao']
                            total_comissao = float(group['comissao_calculada'].sum())
                            semanas_trabalhadas = group['data_da_montagem'].dt.isocalendar().week.nunique()
                            total_auxilio = float(semanas_trabalhadas * montador_info['auxilio_semanal'])
                            total_geral = total_comissao + total_auxilio
                            items_para_pdf = []
                            
                            for _, row in group.iterrows():
                                items_para_pdf.append({
                                    'boletim': row['identificador_boletim_montagem'], 
                                    'data_montagem': row['data_da_montagem'].strftime('%d/%m/%Y'), 
                                    'cliente': row.get('nome_do_cliente', '-'), 
                                    'nome_produto': row.get('nome_produto', '-'), 
                                    'valor_venda': row['media_de_valor_venda'], 
                                    'comissao_calculada': row['comissao_calculada'], 
                                    'comissao_editada': None, 
                                    'adicional': 0.0
                                })
                            
                            periodo_relatorio = f"{group['data_da_montagem'].min().strftime('%d/%m/%Y')} - {group['data_da_montagem'].max().strftime('%d/%m/%Y')}"
                            
                            ctx = {
                                "nome_montador": montador_info['nome'], 
                                "periodo_relatorio": periodo_relatorio, 
                                "percentual_comissao": montador_info['percentual_comissao'] * 100, 
                                "items": items_para_pdf, 
                                "total_comissao": total_comissao, 
                                "total_adicionais": 0, 
                                "total_auxilio": total_auxilio, 
                                "total_geral": total_geral
                            }
                            
                            template = Template(Path("templates/montador_template.html").read_text(encoding="utf-8"))
                            html_pdf = template.render(**ctx)
                            pdf_bytes = HTML(string=html_pdf, base_url="templates").write_pdf()
                            
                            subj_template = Template(st.session_state.montador_subject)
                            body_template = Template(st.session_state.montador_body)

                            subj, body_plain = subj_template.render(**ctx), body_template.render(**ctx)
                            body_html = convert_plain_text_to_html(body_plain)

                            # Obter todos os emails do montador (principal + adicionais)
                            montador_emails = db.get_montador_emails(montador_info)
                            recipients = [{"emailAddress": {"address": email}} for email in montador_emails]

                            message_data = {
                                "subject": subj,
                                "body": {"contentType": "HTML", "content": body_html},
                                "toRecipients": recipients,
                                "attachments": [{"@odata.type": "#microsoft.graph.fileAttachment", "name": f"Relatorio_Montagem_{montador_info['nome']}.pdf", "contentBytes": base64.b64encode(pdf_bytes).decode()}]
                            }
                            
                            if cc_list_montador:
                                message_data["ccRecipients"] = [{"emailAddress": {"address": cc}} for cc in cc_list_montador]
                            
                            final_payload = { "message": message_data, "saveToSentItems": "true" }

                            resp = requests.post("https://graph.microsoft.com/v1.0/me/sendMail", headers={"Authorization": f"Bearer {st.session_state.access_token}", "Content-Type": "application/json"}, json=final_payload)
                            
                            from check_montagem_exists import check_montagem_exists
                            
                            if check_montagem_exists(montador_info['id'], periodo_relatorio):
                                report_summary.append({"Montador": montador_info['nome'], "Status": "❌ Já existe envio para este período"})
                                continue
                                
                            if resp.status_code == 202:
                                time.sleep(2)
                                headers = {"Authorization": f"Bearer {st.session_state.access_token}"}
                                sent_items_url = "https://graph.microsoft.com/v1.0/me/mailfolders/sentitems/messages?$top=1&$select=id,conversationId"
                                sent_resp = requests.get(sent_items_url, headers=headers).json()
                                message_id = sent_resp['value'][0]['id']
                                conversation_id = sent_resp['value'][0]['conversationId']
                                
                                db.log_sent_montagem(montador_info['id'], ctx, conversation_id)
                                report_summary.append({"Montador": montador_info['nome'], "Status": "✅ Enviado"})
                            else:
                                report_summary.append({"Montador": montador_info['nome'], "Status": f"❌ Erro {resp.status_code} - {resp.text}"})
                                
                    st.subheader("📋 Relatório de Envio")
                    st.table(pd.DataFrame(report_summary))
                    st.session_state.manual_montagem_entries = []

    elif page == "Gerenciar Montadores":
        st.title("👷 Gerenciar Montadores")
        
        # Seção de Blacklist
        with st.expander("📋 Blacklist de Boletins"):
            st.subheader("Adicionar Boletins à Blacklist")
            cols = st.columns([2, 2, 1])
            
            with cols[0]:
                montadores = {m['nome']: m['id'] for m in db.get_all_montadores()}
                montador_selected = st.selectbox("Montador", options=list(montadores.keys()))
            
            with cols[1]:
                boletins_input = st.text_input("Números dos Boletins (separados por vírgula)")
            
            with cols[2]:
                motivo = st.text_input("Motivo (opcional)")
            
            if st.button("Adicionar à Blacklist"):
                if boletins_input and montador_selected:
                    montador_id = montadores[montador_selected]
                    boletins = [b.strip() for b in boletins_input.split(",")]
                    for boletim in boletins:
                        success, message = db.adicionar_boletim_blacklist(montador_id, boletim, motivo)
                        st.toast(f"Boletim {boletim}: {message}")
                    st.rerun()
                else:
                    st.warning("Selecione um montador e insira os números dos boletins.")
            
            st.divider()
            st.subheader("Boletins na Blacklist")
            boletins_blacklist = db.get_boletins_blacklist()
            
            if not boletins_blacklist:
                st.info("Nenhum boletim na blacklist.")
            else:
                for b in boletins_blacklist:
                    cols = st.columns([2, 2, 2, 1])
                    cols[0].text(b['montador_nome'])
                    cols[1].text(f"Boletim: {b['boletim']}")
                    cols[2].text(f"Motivo: {b['motivo'] or '-'}")
                    if cols[3].button("🗑️", key=f"del_blacklist_{b['id']}"):
                        db.remover_boletim_blacklist(b['montador_id'], b['boletim'])
                        st.success(f"Boletim {b['boletim']} removido da blacklist!")
                        st.rerun()
        
        st.divider()
        
        with st.form("novo_montador_form", clear_on_submit=True):
            st.subheader("Adicionar Novo Montador")
            nome = st.text_input("Nome Completo")
            identificador = st.text_input("Identificador do Montador (ID único)")
            fornecedor_id = st.text_input("Número do Fornecedor")
            email = st.text_input("E-mail Principal")
            emails_adicionais = st.text_input("E-mails Adicionais (separados por vírgula)", 
                                            help="Digite os emails adicionais separados por vírgula. Ex: email2@empresa.com, email3@empresa.com")
            percentual_comissao = st.number_input("Comissão (%)", 0.0, 100.0, 5.0, 0.1, "%.2f")
            auxilio_semanal = st.number_input("Auxílio Semanal (R$)", 0.0, value=100.0, step=10.0, format="%.2f")
            
            regra_envio = st.selectbox("Regra de Envio", ["Nenhuma", "Semanal", "Mensal (Dia Fixo)", "Quinzenal"], key="m_regra")
            dias_envio = ""
            
            if regra_envio == "Semanal":
                dias_envio = st.selectbox("Dia da Semana", list(DIAS_SEMANA_MAP.values()), key="m_dia_sem")
            elif regra_envio in ["Mensal (Dia Fixo)", "Quinzenal"]:
                dias_envio = st.text_input("Dias do Mês (ex: 5 ou 5,20)", key="m_dia_mes")

            if st.form_submit_button("Adicionar"):
                if all([nome, identificador, email, fornecedor_id]):
                    success, message = db.add_montador(nome, identificador, email, percentual_comissao / 100.0, auxilio_semanal, fornecedor_id, regra_envio, dias_envio, emails_adicionais.strip() if emails_adicionais.strip() else None)
                    st.toast(message)
                else:
                    st.warning("Todos os campos obrigatórios devem ser preenchidos (Nome, Identificador, E-mail Principal e Número do Fornecedor).")
                    
        st.divider()
        st.subheader("Montadores Cadastrados")
        
        for m in db.get_all_montadores():
            with st.expander(f"{m['nome']} ({'Ativo' if m['ativo'] else 'Inativo'}) - ID: {m['id']}"):
                # Informações básicas do montador
                st.info(f"**ID do Montador:** {m['id']} | **Identificador:** {m['identificador']}")
                
                # Mostrar emails atuais
                st.info(f"**E-mail Principal:** {m['email']}")
                if m.get('emails_adicionais'):
                    emails_extras = [email.strip() for email in m['emails_adicionais'].split(',') if email.strip()]
                    st.info(f"**E-mails Adicionais:** {', '.join(emails_extras)}")
                
                with st.form(key=f"form_montador_{m['id']}"):
                    # Permitir edição do número do fornecedor
                    fornecedor_id = st.text_input("Número do Fornecedor", value=m['fornecedor_id'], key=f"fornecedor_{m['id']}")
                    email = st.text_input("E-mail Principal", value=m['email'], key=f"email_{m['id']}")
                    
                    # Campo para editar emails adicionais
                    emails_adicionais_edit = st.text_input("E-mails Adicionais (separados por vírgula)", 
                                                         value=m.get('emails_adicionais', '') or '', 
                                                         key=f"m_emails_edit_{m['id']}",
                                                         help="Digite os emails adicionais separados por vírgula")
                    
                    comissao = st.number_input("Comissão (%)", value=m['percentual_comissao'] * 100, key=f"com_{m['id']}")
                    auxilio = st.number_input("Auxílio Semanal (R$)", value=m['auxilio_semanal'], key=f"aux_{m['id']}")
                    ativo = st.toggle("Ativo", value=m['ativo'], key=f"ativo_{m['id']}")
                    
                    regra_atual = m.get('regra_envio') or "Nenhuma"
                    dias_atuais = m.get('dias_envio') or ""
                    
                    regra_edit = st.selectbox("Regra de Envio", ["Nenhuma", "Semanal", "Mensal (Dia Fixo)", "Quinzenal"], index=["Nenhuma", "Semanal", "Mensal (Dia Fixo)", "Quinzenal"].index(regra_atual), key=f"m_regra_edit_{m['id']}")
                    dias_edit = ""
                    
                    if regra_edit == "Semanal":
                        dias_semana_list = list(DIAS_SEMANA_MAP.values())
                        index_sem = dias_semana_list.index(dias_atuais) if dias_atuais in dias_semana_list else 0
                        dias_edit = st.selectbox("Dia da Semana", dias_semana_list, index=index_sem, key=f"m_dia_sem_edit_{m['id']}")
                    elif regra_edit in ["Mensal (Dia Fixo)", "Quinzenal"]:
                        dias_edit = st.text_input("Dias do Mês", value=dias_atuais, key=f"m_dia_mes_edit_{m['id']}")

                    if st.form_submit_button("Salvar Alterações"):
                        db.update_montador(m['id'], email, comissao / 100.0, auxilio, ativo, regra_edit, dias_edit, fornecedor_id, emails_adicionais_edit.strip() if emails_adicionais_edit.strip() else None)
                        st.success(f"Dados de {m['nome']} atualizados!")
                        st.rerun()
                
                # Histórico de montagens do montador
                st.divider()
                st.subheader(f"📋 Histórico de Montagens - {m['nome']}")
                
                historico_montador = db.get_montagens_by_montador_id(m['id'])
                
                if not historico_montador:
                    st.info("Nenhuma montagem enviada ainda para este montador.")
                else:
                    st.write(f"**Total de envios:** {len(historico_montador)}")
                    
                    # Mostrar resumo dos últimos envios
                    for idx, envio in enumerate(historico_montador[:3]):  # Mostra apenas os 3 mais recentes
                        details = envio.get('detalhes', {})
                        cols = st.columns([2, 2, 1, 1])
                        
                        cols[0].text(f"📅 {envio['data_envio'].strftime('%d/%m/%Y')}")
                        cols[1].text(f"Período: {details.get('periodo_relatorio', 'N/A')}")
                        cols[2].text(f"R$ {details.get('total_geral', 0):.2f}")
                        cols[3].markdown(f"**{envio['status']}**")
                    
                    if len(historico_montador) > 3:
                        st.write(f"... e mais {len(historico_montador) - 3} envios anteriores.")
                    
                    # Botão para ver histórico completo
                    if st.button(f"Ver Histórico Completo", key=f"hist_{m['id']}"):
                        st.session_state[f"show_full_history_{m['id']}"] = True
                    
                    # Mostrar histórico completo se solicitado
                    if st.session_state.get(f"show_full_history_{m['id']}", False):
                        st.markdown("#### Histórico Completo")
                        
                        for envio in historico_montador:
                            details = envio.get('detalhes', {})
                            
                            with st.container():
                                st.markdown("---")
                                cols = st.columns([2, 2, 1, 1, 1])
                                cols[0].text(f"📅 {envio['data_envio'].strftime('%d/%m/%Y')}")
                                cols[1].text(f"Período: {details.get('periodo_relatorio', 'N/A')}")
                                cols[2].text(f"R$ {details.get('total_geral', 0):.2f}")
                                cols[3].markdown(f"**{envio['status']}**")
                                
                                # Mostrar detalhes dos boletins
                                if details and 'items' in details:
                                    # Usar checkbox para controlar a visualização
                                    show_boletins = st.checkbox(f"👁️ Ver {len(details['items'])} boletins", key=f"show_boletins_{envio['id']}")
                                    
                                    if show_boletins:
                                        df_boletins = pd.DataFrame(details['items'])
                                        st.dataframe(df_boletins[['boletim', 'data_montagem', 'valor_venda', 'comissao_calculada']])
                        
                        if st.button(f"Ocultar Histórico", key=f"hide_hist_{m['id']}"):
                            st.session_state[f"show_full_history_{m['id']}"] = False
                            st.rerun()

    elif page == "Histórico de Montagens":
        st.title("📚 Histórico e Status de Pagamentos (Montagem)")
        status_filter = st.selectbox("Filtrar por Status", ["Todos", "Em Aberto", "Pago", "Cancelado", "N.F. RECEBIDA"])
        
        history_data = db.get_all_sent_montagens()

        if not history_data:
            st.info("Nenhum pagamento de montador registrado ainda.")
        else:
            for item in history_data:
                details = item['detalhes']
                if status_filter != "Todos" and item['status'] != status_filter:
                    continue

                montador_info = db.get_montador_by_id(item['montador_id'])
                
                with st.container():
                    st.markdown("---")
                    cols = st.columns([2, 2, 1, 1, 1])
                    cols[0].text(montador_info['nome'] if montador_info else "Montador não encontrado")
                    
                    if details:
                        cols[1].text(f"Período: {details.get('periodo_relatorio', 'N/A')}")
                        cols[2].text(f"R$ {details.get('total_geral', 0):.2f}")
                    else:
                        cols[1].text("Período: N/A"), cols[2].text("R$ N/A")

                    cols[3].text(item['data_envio'].strftime('%d/%m/%Y'))
                    cols[4].markdown(f"**{item['status']}**")

                    with st.expander("Ver Detalhes e Gerenciar"):
                        if details:
                            df_items = pd.DataFrame(details.get('items', []))
                            if 'comissao_editada' not in df_items.columns: 
                                df_items['comissao_editada'] = None
                            if 'adicional' not in df_items.columns: 
                                df_items['adicional'] = 0.0
                            
                            st.markdown("##### Editar Boletins")
                            edited_df = st.data_editor(df_items, key=f"editor_{item['id']}", disabled=['boletim', 'data_montagem', 'cliente', 'nome_produto', 'valor_venda', 'comissao_calculada'])
                            
                            if st.button("Salvar Alterações nos Boletins", key=f"save_details_{item['id']}"):
                                new_details = details.copy()
                                new_details['items'] = edited_df.to_dict('records')
                                
                                total_comissao_final = sum(row.get('comissao_editada') if pd.notna(row.get('comissao_editada')) and row.get('comissao_editada') is not None else row.get('comissao_calculada', 0) for row in new_details['items'])
                                total_adicionais = sum(row.get('adicional', 0) for row in new_details['items'])
                                new_details['total_comissao'] = total_comissao_final
                                new_details['total_adicionais'] = total_adicionais
                                new_details['total_geral'] = total_comissao_final + total_adicionais + new_details.get('total_auxilio', 0)
                                
                                db.update_montagem_details(item['id'], new_details)
                                st.success("Detalhes do pagamento atualizados!")
                                st.rerun()

                        else: 
                            st.warning("Não há detalhes salvos.")
                        
                        if item['anexo_path']:
                            with open(item['anexo_path'], "rb") as file:
                                st.download_button(label="Baixar N.F. Recebida", data=file, file_name=Path(item['anexo_path']).name)

                        st.markdown("---")
                        sub_cols = st.columns(2)
                        
                        with sub_cols[0]:
                            status_options = ["Em Aberto", "Pago", "Cancelado", "N.F. RECEBIDA"]
                            try: 
                                current_status_index = status_options.index(item['status'])
                            except ValueError: 
                                current_status_index = 0
                                
                            new_status = st.selectbox("Alterar status:", options=status_options, index=current_status_index, key=f"status_mont_{item['id']}")
                            if st.button("Salvar Status", key=f"save_status_mont_{item['id']}"):
                                db.update_montagem_status(item['id'], new_status)
                                st.success(f"Status atualizado!")
                                st.rerun()
                                
                        with sub_cols[1]:
                            st.write("")
                            st.write("")
                            if st.button("🚨 Excluir Pagamento", key=f"del_mont_{item['id']}"):
                                db.delete_envio_montagem(item['id'])
                                st.success("Pagamento excluído!")
                                st.rerun()
