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
import psycopg2
import psycopg2.extras

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
    try:
        # Carregar configurações existentes para preservar notificacao_nf
        existing_config = load_config()
        
        config_data = {
            "prestador_cc": st.session_state.get("prestador_cc", ""),
            "prestador_subject": st.session_state.get("prestador_subject", ""),
            "prestador_body": st.session_state.get("prestador_body", ""),
            "montador_cc": st.session_state.get("montador_cc", ""),
            "montador_subject": st.session_state.get("montador_subject", ""),
            "montador_body": st.session_state.get("montador_body", "")
        }
        
        # Preservar configurações de notificação existentes
        if "notificacao_nf" in existing_config:
            config_data["notificacao_nf"] = existing_config["notificacao_nf"]
        
        # Garantir que o diretório existe
        CONFIG_FILE.parent.mkdir(exist_ok=True)
        
        # Salvar com backup
        backup_file = CONFIG_FILE.with_suffix('.json.bak')
        if CONFIG_FILE.exists():
            import shutil
            shutil.copy2(CONFIG_FILE, backup_file)
        
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config_data, f, indent=4, ensure_ascii=False)
            
        # Salvar timestamp do último salvamento
        st.session_state['last_save_time'] = datetime.datetime.now()
            
    except Exception as e:
        st.error(f"❌ Erro ao salvar configurações: {e}")
        # Tentar restaurar backup se houver erro
        if 'backup_file' in locals() and backup_file.exists():
            import shutil
            shutil.copy2(backup_file, CONFIG_FILE)

def auto_save_config():
    """Função callback para salvar automaticamente quando qualquer campo for alterado."""
    save_config()

def enviar_notificacao_nf(token_info, dados_lote, arquivo_nome):
    """Envia notificação automática quando nota fiscal é recebida"""
    try:
        # Carregar configurações de notificação
        config = load_config()
        notif_config = config.get("notificacao_nf", {})
        
        # Verificar se notificações estão ativas
        if not notif_config.get("ativo", False):
            return True  # Sucesso silencioso se desativado
        
        # Verificar se há emails configurados
        emails_str = notif_config.get("emails", "").strip()
        if not emails_str:
            return False
        
        # Preparar variáveis para o template
        tipo, lote_id = token_info
        
        vars_template = {
            "lote_id": lote_id,
            "data_upload": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "arquivo_nome": arquivo_nome,
            "sistema_url": os.getenv('UPLOAD_BASE_URL', 'http://localhost:8501')
        }
        
        if tipo == 'prestador':
            vars_template.update({
                "prestador_nome": dados_lote.get('prestador_nome', 'N/A'),
                "periodo": dados_lote.get('periodo', 'N/A'),
                "valor_total": f"{dados_lote.get('valor_total', 0):,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
            })
        else:  # montador
            vars_template.update({
                "prestador_nome": dados_lote.get('montador_nome', 'N/A'),  # Usar mesmo campo
                "periodo": dados_lote.get('periodo', 'N/A'),
                "valor_total": f"{dados_lote.get('detalhes', {}).get('total_geral', 0):,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
            })
        
        # Renderizar templates
        assunto_template = Template(notif_config.get("assunto", "Nota Fiscal Recebida"))
        corpo_template = Template(notif_config.get("corpo", "Nova nota fiscal recebida."))
        
        assunto_final = assunto_template.render(**vars_template)
        corpo_final = corpo_template.render(**vars_template)
        
        # Preparar lista de emails
        emails_list = [email.strip() for email in emails_str.split(",") if email.strip()]
        recipients = [{"emailAddress": {"address": email}} for email in emails_list]
        
        # Configurar prioridade
        prioridade = notif_config.get("prioridade", "Alta")
        importance = "high" if prioridade in ["Alta", "Urgente"] else "normal"
        
        # Montar payload do email
        message_data = {
            "subject": assunto_final,
            "body": {
                "contentType": "Text",
                "content": corpo_final
            },
            "toRecipients": recipients,
            "importance": importance
        }
        
        # Enviar via Microsoft Graph API (usando token da sessão)
        if 'access_token' in st.session_state:
            headers = {
                "Authorization": f"Bearer {st.session_state.access_token}",
                "Content-Type": "application/json"
            }
            
            response = requests.post(
                "https://graph.microsoft.com/v1.0/me/sendMail",
                headers=headers,
                json=message_data,
                timeout=30
            )
            
            return response.status_code == 202
        
        return False
        
    except Exception as e:
        print(f"Erro ao enviar notificação: {e}")
        return False

def init_config():
    """Inicializa as configurações no session_state APENAS se não existirem."""
    config = load_config()
    
    # Valores padrão mais robustos
    defaults = {
        "prestador_cc": "projetos.qualidade@novomundo.com.br",
        "prestador_subject": "Novo Mundo Resolve | Nota Fiscal Eletrônica de Prestação de Serviços | Período: {{periodo}} | Prestador: {{nome_prestador}}",
        "prestador_body": "Olá, {{nome_prestador}}.\n\nEspero que esteja tudo bem.\n\nSegue em anexo a relação de boletins finalizados para emissão da nota fiscal referente aos serviços prestados no período de {{periodo}}.\n\nInformamos que nosso sistema foi atualizado. Agora, a nota fiscal deve ser enviada exclusivamente pelo link abaixo, o que garante mais agilidade no processamento e pagamento.\nSomente as notas fiscais enviadas por esse novo sistema serão consideradas para pagamento.\n\n{{link_upload_nf}}\n\nA nota fiscal deve ser emitida com o mesmo valor indicado neste relatório e enviada em até 2 dias úteis após o recebimento deste e-mail.\nNotas enviadas após esse prazo serão incluídas no próximo fechamento.\n\nLembrando que a nota fiscal deve ser emitida para o CNPJ 01.534.080/0008-02.",
        "montador_cc": "projetos.qualidade@novomundo.com.br",
        "montador_subject": "Relatório de Pagamento de Montagem - Período: {{periodo_relatorio}}",
        "montador_body": "Olá, {{nome_montador}},\n\nSegue em anexo o seu relatório de pagamento de montagens referente ao período de **{{periodo_relatorio}}**.\n\nPara enviar a nota fiscal, utilize o link: {{link_upload_nf}}\n\nQualquer dúvida, estamos à disposição.\n\nAtenciosamente,\nEquipe Novo Mundo"
    }
    
    # Verificar se já foi inicializado E se os campos não estão vazios
    already_initialized = st.session_state.get('config_initialized', False)
    fields_empty = any(not st.session_state.get(key, "").strip() for key in defaults.keys())
    
    # Só pular inicialização se já foi inicializado E os campos não estão vazios
    if already_initialized and not fields_empty:
        return
    
    # Inicializar/reinicializar com valores salvos ou padrões
    for key, default_value in defaults.items():
        saved_value = config.get(key, "")
        # Se tem valor salvo no arquivo e não está vazio, usar ele
        if saved_value and saved_value.strip():
            st.session_state[key] = saved_value
        else:
            # Senão usar padrão (só se campo estiver vazio)
            if not st.session_state.get(key, "").strip():
                st.session_state[key] = default_value
    
    # Marcar como inicializado
    st.session_state['config_initialized'] = True

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

# Inicializar configurações no session_state
init_config()

st.sidebar.title("MENU")
app_mode = st.sidebar.selectbox("Selecione a Página", ["Dashboard de Pendências", "Serviços (Prestadores)", "Montagem (Montadores)", "Gerenciar Uploads NF"])
st.sidebar.info(f"**Conectado como:** \n{st.session_state.user}")

# Botão de reset de configurações na sidebar
st.sidebar.markdown("---")
if st.sidebar.button("🔄 Resetar Configurações", help="Recarrega configurações do arquivo ou usa padrões"):
    # Limpar flag de inicialização para forçar reload
    if 'config_initialized' in st.session_state:
        del st.session_state['config_initialized']
    
    # Forçar reinicialização
    init_config()
    st.sidebar.success("✅ Configurações resetadas!")
    st.rerun()

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
                
                # Indicador de salvamento
                col1, col2 = st.columns([3, 1])
                with col2:
                    if 'last_save_time' in st.session_state:
                        st.success(f"✅ Salvo em {st.session_state.last_save_time.strftime('%H:%M:%S')}")
                    else:
                        st.info("💾 Salvamento automático ativo")
                
                st.text_input("CC", key="prestador_cc", on_change=auto_save_config, 
                             help="Os emails serão salvos automaticamente conforme você digita")
                st.text_input("Assunto", key="prestador_subject", on_change=auto_save_config,
                             help="Use variáveis como {{nome_prestador}} e {{periodo}}")
                st.text_area("Corpo do E-mail", key="prestador_body", on_change=auto_save_config, height=200,
                           help="Use variáveis como {{nome_prestador}} e {{periodo}}. Salvamento automático ativo.")
                
                # Botão de salvamento manual
                col_save1, col_save2 = st.columns(2)
                with col_save1:
                    if st.button("💾 Salvar Configurações", help="Força o salvamento das configurações", key="save_prestador_config"):
                        save_config()
                        st.success("✅ Configurações salvas manualmente!")
                
                with col_save2:
                    if st.button("🔍 Debug Config", help="Ver estado atual das configurações", key="debug_prestador_config"):
                        st.write("**📋 Session State Atual:**")
                        st.json({
                            "prestador_cc": st.session_state.get("prestador_cc", "NÃO DEFINIDO"),
                            "prestador_subject": st.session_state.get("prestador_subject", "NÃO DEFINIDO"),
                            "prestador_body": st.session_state.get("prestador_body", "NÃO DEFINIDO")[:100] + "..."
                        })
                        
                        st.write("**💾 Config.json Atual:**")
                        config_atual = load_config()
                        st.json({
                            "prestador_cc": config_atual.get("prestador_cc", "NÃO DEFINIDO"),
                            "prestador_subject": config_atual.get("prestador_subject", "NÃO DEFINIDO"),
                            "prestador_body": config_atual.get("prestador_body", "NÃO DEFINIDO")[:100] + "..."
                        })
                        
                        st.write("**🔄 Config Initialized:**")
                        st.code(f"config_initialized = {st.session_state.get('config_initialized', False)}")
                        
                        if st.button("🔄 Recarregar do Arquivo", key="reload_prestador"):
                            config = load_config()
                            st.session_state.prestador_cc = config.get("prestador_cc", "")
                            st.session_state.prestador_subject = config.get("prestador_subject", "")
                            st.session_state.prestador_body = config.get("prestador_body", "")
                            st.success("✅ Configurações recarregadas do arquivo!")
                            st.rerun()
                
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
                            
                            # Gerar token único para upload de nota fiscal
                            token_upload, _ = db.gerar_token_upload('prestador', prestador_info['id'], lote_id)
                            # Usar URL configurável - padrão local para desenvolvimento
                            import os
                            base_url = os.getenv('UPLOAD_BASE_URL', 'http://localhost:8502')
                            link_upload_nf = f"{base_url}/?token={token_upload}"
                            
                            ctx = {
                                "nome_prestador": nome_prestador, 
                                "periodo": periodo, 
                                "items": items_fmt, 
                                "total_geral": total_geral, 
                                "saudacao": saudacao, 
                                "lote_id": lote_id,
                                "link_upload_nf": link_upload_nf
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
                        # Informações de Upload
                        upload_info = db.get_upload_info_por_lote('prestador', lote['id'])
                        
                        if upload_info:
                            st.markdown("### 📄 Status do Upload de Nota Fiscal")
                            col1, col2, col3 = st.columns(3)
                            
                            with col1:
                                if upload_info['usado']:
                                    st.success("✅ NF Recebida")
                                    st.write(f"**Upload em:** {upload_info['data_upload'].strftime('%d/%m/%Y %H:%M')}")
                                else:
                                    if upload_info['data_expiracao'] > datetime.datetime.now():
                                        st.warning("⏳ Aguardando NF")
                                    else:
                                        st.error("❌ Link Expirado")
                            
                            with col2:
                                st.write(f"**Token gerado:** {upload_info['data_criacao'].strftime('%d/%m/%Y %H:%M')}")
                                st.write(f"**Expira em:** {upload_info['data_expiracao'].strftime('%d/%m/%Y %H:%M')}")
                            
                            with col3:
                                if upload_info['usado'] and upload_info['arquivo_path'] and os.path.exists(upload_info['arquivo_path']):
                                    with open(upload_info['arquivo_path'], "rb") as file:
                                        st.download_button(
                                            label="📥 Baixar Nota Fiscal",
                                            data=file.read(),
                                            file_name=upload_info['arquivo_nome'],
                                            mime="application/octet-stream",
                                            key=f"download_nf_prestador_{lote['id']}",
                                            use_container_width=True
                                        )
                                else:
                                    if not upload_info['usado']:
                                        st.code(f"Link: {os.getenv('UPLOAD_BASE_URL', 'http://localhost:8502')}/?token={upload_info['token']}")
                        else:
                            st.info("ℹ️ Este lote não possui sistema de upload (anterior à implementação)")
                        
                        st.markdown("---")
                        
                        # O.S. do Lote
                        st.markdown("### 📋 Ordens de Serviço")
                        os_do_lote = db.get_os_by_lote_id(lote['id'])
                        if os_do_lote:
                            df_os = pd.DataFrame([item['detalhes'] for item in os_do_lote])
                            st.dataframe(df_os)
                        else:
                            st.warning("Não há O.S. detalhadas para este lote.")
                        
                        # Download antigo (manter compatibilidade)
                        if lote['anexo_path'] and os.path.exists(lote['anexo_path']):
                            st.markdown("### 📎 Anexo Antigo")
                            with open(lote['anexo_path'], "rb") as file:
                                st.download_button(
                                    label="📥 Baixar Anexo Legado", 
                                    data=file.read(), 
                                    file_name=Path(lote['anexo_path']).name,
                                    key=f"legacy_download_prestador_{lote['id']}"
                                )
                        
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
                
                # Indicador de salvamento
                col1, col2 = st.columns([3, 1])
                with col2:
                    if 'last_save_time' in st.session_state:
                        st.success(f"✅ Salvo em {st.session_state.last_save_time.strftime('%H:%M:%S')}")
                    else:
                        st.info("💾 Salvamento automático ativo")
                
                st.text_input("CC (Montadores)", key="montador_cc", on_change=auto_save_config,
                             help="Os emails serão salvos automaticamente conforme você digita")
                st.text_input("Assunto (Montadores)", key="montador_subject", on_change=auto_save_config,
                             help="Use variáveis como {{nome_montador}} e {{periodo_relatorio}}")
                st.text_area("Corpo do E-mail (Montadores)", key="montador_body", on_change=auto_save_config, height=200,
                           help="Use variáveis como {{nome_montador}} e {{periodo_relatorio}}. Salvamento automático ativo.")
                
                # Botão de salvamento manual
                col_save_mont1, col_save_mont2 = st.columns(2)
                with col_save_mont1:
                    if st.button("💾 Salvar Configurações", help="Força o salvamento das configurações", key="save_montador_config"):
                        save_config()
                        st.success("✅ Configurações salvas manualmente!")
                
                with col_save_mont2:
                    if st.button("🔍 Debug Config", help="Ver estado atual das configurações", key="debug_montador_config"):
                        st.write("**📋 Session State Atual:**")
                        st.json({
                            "montador_cc": st.session_state.get("montador_cc", "NÃO DEFINIDO"),
                            "montador_subject": st.session_state.get("montador_subject", "NÃO DEFINIDO"),
                            "montador_body": st.session_state.get("montador_body", "NÃO DEFINIDO")[:100] + "..."
                        })
                        
                        st.write("**💾 Config.json Atual:**")
                        config_atual = load_config()
                        st.json({
                            "montador_cc": config_atual.get("montador_cc", "NÃO DEFINIDO"),
                            "montador_subject": config_atual.get("montador_subject", "NÃO DEFINIDO"),
                            "montador_body": config_atual.get("montador_body", "NÃO DEFINIDO")[:100] + "..."
                        })
                        
                        if st.button("🔄 Recarregar do Arquivo", key="reload_montador"):
                            config = load_config()
                            st.session_state.montador_cc = config.get("montador_cc", "")
                            st.session_state.montador_subject = config.get("montador_subject", "")
                            st.session_state.montador_body = config.get("montador_body", "")
                            st.success("✅ Configurações recarregadas do arquivo!")
                            st.rerun()
                
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
                            
                            # Gerar token único para upload de nota fiscal (será associado ao envio após criação)
                            token_upload, _ = db.gerar_token_upload('montador', montador_info['id'])
                            # Usar URL configurável - padrão local para desenvolvimento
                            import os
                            base_url = os.getenv('UPLOAD_BASE_URL', 'http://localhost:8502')
                            link_upload_nf = f"{base_url}/?token={token_upload}"
                            
                            ctx = {
                                "nome_montador": montador_info['nome'], 
                                "periodo_relatorio": periodo_relatorio, 
                                "percentual_comissao": montador_info['percentual_comissao'] * 100, 
                                "items": items_para_pdf, 
                                "total_comissao": total_comissao, 
                                "total_adicionais": 0, 
                                "total_auxilio": total_auxilio, 
                                "total_geral": total_geral,
                                "link_upload_nf": link_upload_nf
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
                                
                                envio_id = db.log_sent_montagem(montador_info['id'], ctx, conversation_id)
                                
                                # Atualizar o token para associar ao envio criado
                                conn = db.get_db_connection()
                                with conn.cursor() as cur:
                                    cur.execute("UPDATE upload_tokens SET lote_id = %s WHERE token = %s", (envio_id, token_upload))
                                conn.commit()
                                conn.close()
                                
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
                        # Informações de Upload
                        upload_info = db.get_upload_info_por_lote('montador', item['id'])
                        
                        if upload_info:
                            st.markdown("### 📄 Status do Upload de Nota Fiscal")
                            col1, col2, col3 = st.columns(3)
                            
                            with col1:
                                if upload_info['usado']:
                                    st.success("✅ NF Recebida")
                                    st.write(f"**Upload em:** {upload_info['data_upload'].strftime('%d/%m/%Y %H:%M')}")
                                else:
                                    if upload_info['data_expiracao'] > datetime.datetime.now():
                                        st.warning("⏳ Aguardando NF")
                                    else:
                                        st.error("❌ Link Expirado")
                            
                            with col2:
                                st.write(f"**Token gerado:** {upload_info['data_criacao'].strftime('%d/%m/%Y %H:%M')}")
                                st.write(f"**Expira em:** {upload_info['data_expiracao'].strftime('%d/%m/%Y %H:%M')}")
                            
                            with col3:
                                if upload_info['usado'] and upload_info['arquivo_path'] and os.path.exists(upload_info['arquivo_path']):
                                    with open(upload_info['arquivo_path'], "rb") as file:
                                        st.download_button(
                                            label="📥 Baixar Nota Fiscal",
                                            data=file.read(),
                                            file_name=upload_info['arquivo_nome'],
                                            mime="application/octet-stream",
                                            key=f"download_nf_mont_{item['id']}",
                                            use_container_width=True
                                        )
                                else:
                                    if not upload_info['usado']:
                                        st.code(f"Link: {os.getenv('UPLOAD_BASE_URL', 'http://localhost:8502')}/?token={upload_info['token']}")
                        else:
                            st.info("ℹ️ Este envio não possui sistema de upload (anterior à implementação)")
                        
                        st.markdown("---")
                        
                        # Detalhes dos Boletins
                        if details:
                            st.markdown("### 📋 Detalhes dos Boletins")
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
                                st.download_button(
                                    label="Baixar N.F. Recebida", 
                                    data=file, 
                                    file_name=Path(item['anexo_path']).name,
                                    key=f"download_nf_lote_{item['id']}"
                                )

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

elif app_mode == "Gerenciar Uploads NF":
    st.header("📄 Gerenciamento de Uploads de Notas Fiscais")
    
    # Estatísticas gerais
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        # Total de tokens gerados
        conn = db.get_db_connection()
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM upload_tokens")
            total_tokens = cur.fetchone()[0]
        conn.close()
        st.metric("🔗 Total de Tokens", total_tokens)
    
    with col2:
        # Tokens usados
        conn = db.get_db_connection()
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM upload_tokens WHERE usado = TRUE")
            tokens_usados = cur.fetchone()[0]
        conn.close()
        st.metric("✅ Tokens Usados", tokens_usados)
    
    with col3:
        # Tokens pendentes
        conn = db.get_db_connection()
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM upload_tokens WHERE usado = FALSE AND data_expiracao > NOW()")
            tokens_pendentes = cur.fetchone()[0]
        conn.close()
        st.metric("⏳ Tokens Pendentes", tokens_pendentes)
    
    with col4:
        # Tokens expirados
        conn = db.get_db_connection()
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM upload_tokens WHERE usado = FALSE AND data_expiracao <= NOW()")
            tokens_expirados = cur.fetchone()[0]
        conn.close()
        st.metric("❌ Tokens Expirados", tokens_expirados)
    
    st.markdown("---")
    
    # Tabs para diferentes visualizações
    tab1, tab2, tab3 = st.tabs(["📋 Tokens Recentes", "✅ Uploads Realizados", "⚙️ Configurações"])
    
    with tab1:
        st.subheader("🔗 Tokens Gerados Recentemente")
        
        conn = db.get_db_connection()
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute("""
                SELECT t.*, 
                       CASE WHEN t.tipo = 'prestador' THEN p.nome ELSE m.nome END as entidade_nome,
                       CASE WHEN t.tipo = 'prestador' THEN p.email ELSE m.email END as entidade_email
                FROM upload_tokens t 
                LEFT JOIN prestadores p ON t.tipo = 'prestador' AND t.entidade_id = p.id
                LEFT JOIN montadores m ON t.tipo = 'montador' AND t.entidade_id = m.id
                ORDER BY t.data_criacao DESC
                LIMIT 50
            """)
            tokens = cur.fetchall()
        conn.close()
        
        if tokens:
            for token in tokens:
                status_icon = "✅" if token['usado'] else ("❌" if token['data_expiracao'] < datetime.datetime.now() else "⏳")
                status_text = "Usado" if token['usado'] else ("Expirado" if token['data_expiracao'] < datetime.datetime.now() else "Pendente")
                
                with st.expander(f"{status_icon} {token['entidade_nome']} ({token['tipo'].title()}) - {status_text}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Email:** {token['entidade_email']}")
                        st.write(f"**Criado:** {token['data_criacao'].strftime('%d/%m/%Y %H:%M')}")
                        st.write(f"**Expira:** {token['data_expiracao'].strftime('%d/%m/%Y %H:%M')}")
                    with col2:
                        if token['usado']:
                            st.write(f"**Upload:** {token['data_upload'].strftime('%d/%m/%Y %H:%M')}")
                            st.write(f"**Arquivo:** {token['arquivo_nome']}")
                        else:
                            st.write("**Link de Upload:**")
                            st.code(f"https://uploadnf.novomundo.com.br/?token={token['token']}")
        else:
            st.info("Nenhum token encontrado.")
    
    with tab2:
        st.subheader("📁 Uploads Realizados")
        
        conn = db.get_db_connection()
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute("""
                SELECT t.*, 
                       CASE WHEN t.tipo = 'prestador' THEN p.nome ELSE m.nome END as entidade_nome,
                       CASE WHEN t.tipo = 'prestador' THEN p.email ELSE m.email END as entidade_email,
                       CASE WHEN t.tipo = 'prestador' THEN l.periodo ELSE e.detalhes->>'periodo_relatorio' END as periodo
                FROM upload_tokens t 
                LEFT JOIN prestadores p ON t.tipo = 'prestador' AND t.entidade_id = p.id
                LEFT JOIN montadores m ON t.tipo = 'montador' AND t.entidade_id = m.id
                LEFT JOIN lotes_servico l ON t.tipo = 'prestador' AND t.lote_id = l.id
                LEFT JOIN envios_montagem e ON t.tipo = 'montador' AND t.lote_id = e.id
                WHERE t.usado = TRUE
                ORDER BY t.data_upload DESC
                LIMIT 100
            """)
            uploads = cur.fetchall()
        conn.close()
        
        if uploads:
            for upload in uploads:
                with st.expander(f"📄 {upload['entidade_nome']} - {upload['arquivo_nome']} ({upload['data_upload'].strftime('%d/%m/%Y %H:%M')})"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Tipo:** {upload['tipo'].title()}")
                        st.write(f"**Email:** {upload['entidade_email']}")
                        st.write(f"**Período:** {upload['periodo']}")
                    with col2:
                        st.write(f"**Arquivo:** {upload['arquivo_nome']}")
                        st.write(f"**Caminho:** {upload['arquivo_path']}")
                        
                        # Botão para baixar arquivo (se existir)
                        if upload['arquivo_path'] and os.path.exists(upload['arquivo_path']):
                            with open(upload['arquivo_path'], "rb") as file:
                                st.download_button(
                                    label="📥 Baixar Arquivo",
                                    data=file.read(),
                                    file_name=upload['arquivo_nome'],
                                    mime="application/octet-stream",
                                    key=f"download_upload_{upload['id']}"
                                )
        else:
            st.info("Nenhum upload realizado ainda.")
    
    with tab3:
        st.subheader("⚙️ Configurações do Sistema")
        
        st.markdown("### 🌐 Configuração da URL Base")
        
        # Carregar URL atual das variáveis de ambiente ou usar padrão local
        import os
        current_url = os.getenv('UPLOAD_BASE_URL', 'http://localhost:8502')
        
        new_url = st.text_input("URL Base para Links de Upload", value=current_url, 
                               help="Para desenvolvimento local: http://localhost:8502")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("💾 Salvar URL (Sessão)"):
                os.environ['UPLOAD_BASE_URL'] = new_url
                st.success("✅ URL salva para esta sessão!")
                
        with col2:
            if st.button("🔄 Restaurar Padrão Local"):
                os.environ['UPLOAD_BASE_URL'] = 'http://localhost:8502'
                st.success("✅ URL restaurada para localhost:8502!")
                st.rerun()
        
        st.markdown("---")
        
        st.markdown("### 📧 Notificações de Upload de NF")
        st.markdown("Configure emails automáticos quando uma nota fiscal for enviada")
        
        # Carregar configurações de notificação existentes
        notif_config = load_config().get("notificacao_nf", {})
        
        # Verificar se configuração existe
        if not notif_config:
            st.warning("⚠️ **Configurações de notificação não encontradas!**")
            st.info("👆 Configure os campos abaixo e clique em **'💾 Salvar Configurações de Notificação'** antes de testar.")
        else:
            st.success("✅ Configurações de notificação carregadas")
        
        # Configuração de emails destinatários
        emails_notif = st.text_area(
            "📬 Emails para Notificação",
            value=notif_config.get("emails", ""),
            help="Emails separados por vírgula. Ex: admin@empresa.com, financeiro@empresa.com",
            key="notif_emails",
            height=68
        )
        
        # Configuração do assunto
        assunto_notif = st.text_input(
            "📋 Assunto do Email",
            value=notif_config.get("assunto", "🚨 NOTA FISCAL RECEBIDA - {{prestador_nome}} - Lote {{lote_id}}"),
            help="Use variáveis: {{prestador_nome}}, {{lote_id}}, {{data_upload}}, {{periodo}}, {{valor_total}}",
            key="notif_assunto"
        )
        
        # Configuração do corpo do email
        corpo_notif = st.text_area(
            "📝 Corpo do Email",
            value=notif_config.get("corpo", """🎉 NOVA NOTA FISCAL RECEBIDA!

📋 **Detalhes do Upload:**
• **Prestador:** {{prestador_nome}}
• **Lote:** #{{lote_id}}
• **Período:** {{periodo}}
• **Valor Total:** R$ {{valor_total}}
• **Data/Hora:** {{data_upload}}
• **Arquivo:** {{arquivo_nome}}

⚡ **Ação Necessária:**
A nota fiscal foi recebida e está disponível para download no sistema.

🔗 **Acesso Rápido:**
Acesse o painel de uploads para fazer o download: {{sistema_url}}

---
Este é um email automático do sistema de gestão de notas fiscais."""),
            help="Use variáveis disponíveis para personalizar a mensagem",
            key="notif_corpo",
            height=200
        )
        
        # Configuração de prioridade
        col1, col2 = st.columns(2)
        with col1:
            prioridade_notif = st.selectbox(
                "⚡ Prioridade do Email",
                options=["Normal", "Alta", "Urgente"],
                index=["Normal", "Alta", "Urgente"].index(notif_config.get("prioridade", "Alta")),
                key="notif_prioridade"
            )
        
        with col2:
            ativar_notif = st.checkbox(
                "✅ Ativar Notificações",
                value=notif_config.get("ativo", True),
                help="Marque para enviar emails automáticos quando NF for recebida",
                key="notif_ativo"
            )
        
        # Botões de ação
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("💾 Salvar Configurações de Notificação", type="primary"):
                # Salvar configurações
                config = load_config()
                config["notificacao_nf"] = {
                    "emails": st.session_state.notif_emails,
                    "assunto": st.session_state.notif_assunto,
                    "corpo": st.session_state.notif_corpo,
                    "prioridade": st.session_state.notif_prioridade,
                    "ativo": st.session_state.notif_ativo
                }
                
                # Salvar no arquivo
                try:
                    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                        json.dump(config, f, indent=4, ensure_ascii=False)
                    st.success("✅ Configurações de notificação salvas!")
                except Exception as e:
                    st.error(f"❌ Erro ao salvar: {e}")
        
        with col2:
            if st.button("🧪 Testar Notificação"):
                if st.session_state.notif_emails.strip():
                    try:
                        # Salvar configurações temporariamente para teste
                        config = load_config()
                        config["notificacao_nf"] = {
                            "emails": st.session_state.notif_emails,
                            "assunto": st.session_state.notif_assunto,
                            "corpo": st.session_state.notif_corpo,
                            "prioridade": st.session_state.notif_prioridade,
                            "ativo": True  # Forçar ativo para teste
                        }
                        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                            json.dump(config, f, indent=4, ensure_ascii=False)
                        
                        st.success("✅ Configurações salvas!")
                        
                        # Teste com logs detalhados
                        st.info("🔍 **Iniciando teste da notificação...**")
                        
                        # Log 1: Verificar configurações
                        st.write("**📋 Passo 1: Verificando configurações...**")
                        config_debug = load_config()
                        notif_debug = config_debug.get("notificacao_nf", {})
                        
                        if notif_debug:
                            st.success(f"✅ Configuração encontrada:")
                            col_cfg1, col_cfg2 = st.columns(2)
                            with col_cfg1:
                                st.code(f"Emails: {notif_debug.get('emails', 'NÃO DEFINIDO')}")
                                st.code(f"Ativo: {notif_debug.get('ativo', False)}")
                            with col_cfg2:
                                st.code(f"Prioridade: {notif_debug.get('prioridade', 'NÃO DEFINIDO')}")
                                st.code(f"Assunto: {notif_debug.get('assunto', 'NÃO DEFINIDO')[:50]}...")
                        else:
                            st.error("❌ Nenhuma configuração de notificação encontrada!")
                            st.stop()
                        
                        # Log 2: Status do login
                        st.write("**🔑 Passo 2: Verificando status de login...**")
                        if 'access_token' in st.session_state and st.session_state.access_token:
                            st.success("✅ Usuário logado - Pode enviar emails reais")
                            token_status = "DISPONÍVEL"
                        else:
                            st.warning("⚠️ Usuário não logado - Apenas preview")
                            token_status = "NÃO DISPONÍVEL"
                        
                        # Log 3: Teste de importação
                        st.write("**📦 Passo 3: Importando módulo de notificação...**")
                        try:
                            import sys
                            import os
                            current_dir = os.path.dirname(os.path.abspath(__file__))
                            if current_dir not in sys.path:
                                sys.path.append(current_dir)
                            
                            from notificacao_nf import enviar_notificacao_nf_upload
                            st.success("✅ Módulo importado com sucesso")
                        except Exception as e:
                            st.error(f"❌ Erro na importação: {e}")
                            st.stop()
                        
                        # Log 4: Executar teste
                        st.write("**🧪 Passo 4: Executando teste...**")
                        
                        dados_teste = {
                            "prestador_nome": "EMPRESA TESTE REAL LTDA",
                            "periodo": "01/10/2025 - 31/10/2025",
                            "valor_total": 1234.56
                        }
                        
                        st.code(f"Dados de teste: {dados_teste}")
                        
                        # Executar com token se disponível, senão sem token
                        access_token = st.session_state.get('access_token') if token_status == "DISPONÍVEL" else None
                        
                        with st.spinner("Executando notificação..."):
                            resultado = enviar_notificacao_nf_upload(
                                ("prestador", "TESTE123"),
                                dados_teste,
                                "NF_TESTE_COMPLETO.pdf",
                                access_token,
                                None  # Sem anexo no teste
                            )
                            
                        # Log 5: Mostrar resultado completo
                        st.write("**📊 Passo 5: Resultado da execução:**")
                        st.json(resultado)
                        
                        # Log 6: Interpretação do resultado
                        st.write("**🔍 Passo 6: Análise do resultado:**")
                        
                        if resultado.get("success"):
                            st.success(f"🎉 **SUCESSO!** {resultado['message']}")
                            if "emails" in resultado:
                                st.balloons()
                                st.info(f"� **EMAIL ENVIADO PARA:** {', '.join(resultado['emails'])}")
                            
                        elif "preview" in resultado:
                            st.info("📧 **PREVIEW GERADO** (sem envio real)")
                            preview = resultado["preview"]
                            
                            st.write("**Preview do email:**")
                            col_p1, col_p2 = st.columns(2)
                            with col_p1:
                                st.code(f"Para: {', '.join(preview['para'])}")
                                st.code(f"Prioridade: {preview['prioridade'].upper()}")
                            with col_p2:
                                st.code(f"Assunto: {preview['assunto']}")
                            
                            st.text_area("**Corpo completo:**", preview['corpo'], height=300, disabled=True)
                            
                            if token_status == "NÃO DISPONÍVEL":
                                st.info("💡 **Para enviar email real:** Faça login na página principal primeiro")
                        else:
                            st.error(f"❌ **ERRO:** {resultado.get('message', 'Erro desconhecido')}")
                            if "error" in resultado:
                                st.code(f"Detalhes do erro: {resultado['error']}")
                        
                        # Log 7: Teste de envio real (se logado)
                        if token_status == "DISPONÍVEL" and not resultado.get("success"):
                            st.write("**🚀 Passo 7: Opção de envio real:**")
                            st.warning("⚠️ O teste acima foi apenas preview. Clique abaixo para tentar envio real:")
                            
                            if st.button("📧 FORÇAR ENVIO REAL", type="secondary", key="forcar_envio_real"):
                                st.write("**Executando envio forçado...**")
                                with st.spinner("Enviando email real..."):
                                    resultado_forcado = enviar_notificacao_nf_upload(
                                        ("prestador", "FORÇADO123"),
                                        dados_teste,
                                        "NF_TESTE_FORCADO.pdf",
                                        st.session_state.access_token,
                                        None  # Sem anexo no teste forçado
                                    )
                                
                                st.write("**Resultado do envio forçado:**")
                                st.json(resultado_forcado)
                                
                                if resultado_forcado.get("success"):
                                    st.success("🎉 EMAIL ENVIADO COM SUCESSO!")
                                    st.balloons()
                                else:
                                    st.error("❌ Falha no envio forçado")
                        
                        st.markdown("---")
                        st.info("📝 **Log completo exibido acima - Verifique cada passo**")
                                
                    except Exception as e:
                        st.error(f"❌ Erro ao salvar configurações: {e}")
                        st.code(str(e))
                else:
                    st.warning("⚠️ Configure os emails destinatários primeiro!")
        
        with col3:
            if st.button("🔍 Debug Config", help="Verificar configurações salvas"):
                config = load_config()
                notif_config = config.get("notificacao_nf", {})
                
                st.json({
                    "config_existe": "notificacao_nf" in config,
                    "emails": notif_config.get("emails", "NÃO DEFINIDO"),
                    "assunto": notif_config.get("assunto", "NÃO DEFINIDO"),
                    "ativo": notif_config.get("ativo", False),
                    "prioridade": notif_config.get("prioridade", "NÃO DEFINIDO")
                })
        
        st.markdown("**📚 Variáveis Disponíveis:**")
        with st.expander("Ver todas as variáveis", expanded=False):
            st.code("""
{{prestador_nome}} - Nome do prestador
{{lote_id}} - ID do lote/envio  
{{periodo}} - Período do lote
{{valor_total}} - Valor total formatado
{{data_upload}} - Data/hora do upload
{{arquivo_nome}} - Nome do arquivo NF
{{sistema_url}} - URL do sistema
{{valor_total}}
{{data_upload}}
{{arquivo_nome}}
{{sistema_url}}
            """)
        
        st.markdown("---")
        
        st.markdown("### 🧹 Limpeza de Tokens")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🗑️ Limpar Tokens Expirados"):
                conn = db.get_db_connection()
                with conn.cursor() as cur:
                    cur.execute("DELETE FROM upload_tokens WHERE usado = FALSE AND data_expiracao <= NOW()")
                    deleted_count = cur.rowcount
                conn.commit()
                conn.close()
                st.success(f"✅ {deleted_count} tokens expirados removidos!")
        
        with col2:
            if st.button("📊 Gerar Relatório CSV"):
                conn = db.get_db_connection()
                with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
                    cur.execute("""
                        SELECT t.token, t.tipo, 
                               CASE WHEN t.tipo = 'prestador' THEN p.nome ELSE m.nome END as entidade_nome,
                               t.data_criacao, t.data_expiracao, t.usado, t.data_upload, t.arquivo_nome
                        FROM upload_tokens t 
                        LEFT JOIN prestadores p ON t.tipo = 'prestador' AND t.entidade_id = p.id
                        LEFT JOIN montadores m ON t.tipo = 'montador' AND t.entidade_id = m.id
                        ORDER BY t.data_criacao DESC
                    """)
                    data = cur.fetchall()
                conn.close()
                
                if data:
                    df = pd.DataFrame(data)
                    csv = df.to_csv(index=False)
                    st.download_button(
                        label="📥 Baixar Relatório CSV",
                        data=csv,
                        file_name=f"relatorio_uploads_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv",
                        key="download_relatorio_csv"
                    )
                else:
                    st.info("Nenhum dado para gerar relatório.")
        
        st.markdown("### ℹ️ Informações do Sistema")
        st.info("""
        **Como funciona o sistema de upload:**
        
        1. 📧 Quando um email é enviado, um token único é gerado automaticamente
        2. 🔗 O link com o token é incluído no email para o prestador/montador
        3. 📄 O destinatário acessa o link e faz upload da nota fiscal
        4. ✅ O arquivo é salvo de forma segura e o token é marcado como usado
        5. 📊 Você pode acompanhar todos os uploads através desta interface
        
        **Configuração do servidor de upload:**
        Execute o comando: `./start_upload_server.sh` para iniciar o servidor de upload na porta 8502.
        """)
        
        st.markdown("### 🚀 Servidor de Upload")
        if st.button("▶️ Instruções para Iniciar Servidor"):
            st.code("""
# 1. Via terminal, execute:
./start_upload_server.sh

# 2. O servidor rodará em:
http://localhost:8502

# 3. Configure seu proxy/DNS para apontar:
https://uploadnf.novomundo.com.br -> http://localhost:8502
            """)
            
            st.warning("⚠️ **Importante:** Configure seu servidor web (nginx/apache) para fazer proxy da URL pública para a porta 8502.")
