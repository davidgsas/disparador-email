import warnings
from urllib3.exceptions import NotOpenSSLWarning
# Suprimir alerta de LibreSSL x OpenSSL do urllib3
warnings.filterwarnings("ignore", category=NotOpenSSLWarning)

import os
import base64
import datetime
import re
from pathlib import Path

import streamlit as st
import pandas as pd
import requests
from dotenv import load_dotenv
from msal import PublicClientApplication, SerializableTokenCache
from jinja2 import Template
from weasyprint import HTML

# 1) Configuração da página e cache de token
st.set_page_config(page_title="Disparador Novo Mundo", layout="wide")
TOKEN_CACHE_PATH = Path("token_cache.json")
cache = SerializableTokenCache()
if TOKEN_CACHE_PATH.exists():
    cache.deserialize(TOKEN_CACHE_PATH.read_text())

# 2) Carregar credenciais do .env
load_dotenv()
CLIENT_ID = os.getenv("CLIENT_ID")
TENANT_ID = os.getenv("TENANT_ID")
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPES = ["Mail.Send"]

# 3) Instanciar MSAL
pca = PublicClientApplication(
    client_id=CLIENT_ID,
    authority=AUTHORITY,
    token_cache=cache
)

# 4) Tentativa de login silencioso
if "access_token" not in st.session_state:
    accounts = pca.get_accounts()
    if accounts:
        result = pca.acquire_token_silent(SCOPES, account=accounts[0])
        if result and "access_token" in result:
            st.session_state.access_token = result["access_token"]
            st.session_state.user = accounts[0].get("username")

# 5) Device Code Flow
def do_login():
    flow = pca.initiate_device_flow(scopes=SCOPES)
    st.info(flow["message"])
    return pca.acquire_token_by_device_flow(flow)

def login_callback():
    auth = do_login()
    if "access_token" in auth:
        st.session_state.access_token = auth["access_token"]
        TOKEN_CACHE_PATH.write_text(cache.serialize())
        me = requests.get(
            "https://graph.microsoft.com/v1.0/me",
            headers={"Authorization": f"Bearer {auth['access_token']}"}
        ).json()
        st.session_state.user = me.get("userPrincipalName", "")
        TOKEN_CACHE_PATH.write_text(cache.serialize())
    else:
        st.session_state.login_error = auth.get("error_description") or auth.get("error") or "desconhecido"

# 6) UI de login
if "access_token" not in st.session_state:
    st.title("🔐 Login com Office 365")
    st.write("Clique em Entrar e conclua o login no navegador (2FA).")
    st.button("Entrar com Office 365", on_click=login_callback)
    if "login_error" in st.session_state:
        st.error(f"❌ Falha no login: {st.session_state.login_error}")
    st.stop()

# 7) Sidebar de configurações
st.sidebar.title("⚙️ Configurações")
st.sidebar.markdown(f"**Conectado como:**  \n{st.session_state.user}")

# CC padrão ajustado
default_cc = "projetos.qualidade@novomundo.com.br, centralclientes01@novomundo.com.br"
cc_input = st.sidebar.text_input("CC (separe por vírgula)", value=default_cc)
cc_list = [e.strip() for e in cc_input.split(",") if e.strip()]

st.sidebar.markdown("---")
st.sidebar.markdown("**✉️ Assunto**")
default_subject = (
    "Novo Mundo Resolve | Nota Fiscal Eletrônica de Prestação de Serviços"
    " | Período: {{Periodo}} | Prestador: {{Nome_prestador}}"
)
if "subject" not in st.session_state:
    st.session_state.subject = default_subject
st.session_state.subject = st.sidebar.text_input("Assunto", value=st.session_state.subject)

st.sidebar.markdown("---")
st.sidebar.markdown("**✏️ Corpo de e-mail (HTML)**")
default_body = """
<p>{{saudacao}},</p>

<p>Espero que estejam tendo um ótimo dia. A seguir, envio a relação de boletins finalizados,
para que possam emitir a nota fiscal referente aos serviços prestados entre
<strong>{{Periodo}}</strong>.</p>

<p>Gostaria de lembrá-los que os cortes para pagamentos serão realizados nos dias 04
e 22 de cada mês, resultando em dois pagamentos mensais. Além disso, o prazo para o
crédito é de até 10 dias ÚTEIS após o envio da nota fiscal.</p>

<p>Por gentileza, envie a nota fiscal em até 1 dia útil após o recebimento deste e-mail.
Caso contrário, as ordens de serviço (OS) serão incluídas no próximo fechamento.</p>

<p>Lembrando que a nota fiscal deve ser emitida no CNPJ 01.534.080/0008-02.</p>

<p>Informamos que o encaminhamento de notas fiscais deve ser feito exclusivamente por meio
deste e-mail. Não serão considerados e-mails enviados separadamente (avulsos) com a nota
fiscal em anexo.</p>

<p>Para garantir o correto recebimento e processamento, responda diretamente a este e-mail
utilizando a opção 'Responder a todos', mantendo todos os contatos que constam na mensagem
original.</p>

<p>O envio por outros canais ou a alteração dos destinatários poderá causar desencontros de
informação e resultar em atrasos no prazo de pagamento.</p>

<p>Agradecemos sua atenção e colaboração.</p>
"""
if "body" not in st.session_state:
    st.session_state.body = default_body
st.session_state.body = st.sidebar.text_area(
    label="Corpo do e-mail",
    value=st.session_state.body,
    height=300,
    label_visibility="collapsed"
)

st.sidebar.markdown("---")
st.sidebar.markdown("**📌 Variáveis**")
cols = st.sidebar.columns(2)

# 8) Upload e preview da planilha
st.title("📤 Envio de Boletins")
uploader = st.file_uploader("Carregue o arquivo .xlsx", type=["xlsx"])
if not uploader:
    st.info("Aguardando upload do .xlsx...")
    st.stop()

# 9) Ler, normalizar colunas e converter números
df = pd.read_excel(uploader)
df.columns = [re.sub(r"\W+", "_", c.strip()) for c in df.columns]
for col in ["Valor", "Valor_extra", "Valor_total"]:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)
st.dataframe(df)

for i, var in enumerate(list(df.columns) + ["saudacao"]):
    if cols[i % 2].button(var):
        st.session_state.body += f" {{{{{var}}}}}"

invoice_tpl = Template(open("templates/invoice_template.html", encoding="utf-8").read())

if "confirming" not in st.session_state:
    st.session_state.confirming = False

if not st.session_state.confirming:
    if st.button("▶️ Enviar e-mails", key="start_send"):
        st.session_state.confirming = True
else:
    st.warning("🔔 Tem certeza que deseja enviar todos os e-mails agora?")
    c1, c2 = st.columns(2)
    if c1.button("Sim", key="confirm_yes"):
        report = []
        hour = datetime.datetime.now().hour
        if 6 <= hour < 12:
            saudacao = "Bom dia"
        elif 12 <= hour < 18:
            saudacao = "Boa tarde"
        else:
            saudacao = "Boa noite"

        for (prestador, periodo), group in df.groupby(["nome_prestador", "Periodo"]):
            total_geral = group["Valor_total"].sum()
            items = []
            for _, r in group.iterrows():
                data = r.get("Data_execucao")
                if hasattr(data, "strftime"):
                    data = data.strftime("%d/%m/%Y")
                motivo = str(r.get("Motivo_valor_extra") or "").strip().lower()
                items.append({
                    "OS": r.get("O_S"),
                    "Modalidade": r.get("Modalidade"),
                    "Data_execucao": data,
                    "Valor": f"{r.Valor:.2f}",
                    "Valor_extra": f"{r.Valor_extra:.2f}",
                    "Motivo_valor_extra": "-" if motivo in ["", "nan", "none"] else r.get("Motivo_valor_extra"),
                    "Valor_total": f"{r.Valor_total:.2f}"
                })
            ctx = {
                "Nome_prestador": prestador,
                "Periodo": periodo,
                "items": items,
                "total_geral": f"{total_geral:.2f}",
                "saudacao": saudacao
            }
            subject = Template(st.session_state.subject).render(**ctx)
            body_html = Template(st.session_state.body).render(**ctx)
            html = invoice_tpl.render(**ctx)
            pdf_bytes = HTML(string=html, base_url="templates").write_pdf()
            email_to = group["E_mail"].iloc[0]
            resp = requests.post(
                "https://graph.microsoft.com/v1.0/me/sendMail",
                headers={
                    "Authorization": f"Bearer {st.session_state.access_token}",
                    "Content-Type": "application/json"
                },
                json={
                    "message": {
                        "subject": subject,
                        "body": {"contentType": "HTML", "content": body_html},
                        "toRecipients": [{"emailAddress": {"address": email_to}}],
                        "ccRecipients": [{"emailAddress": {"address": cc}} for cc in cc_list],
                        "attachments": [{
                            "@odata.type": "#microsoft.graph.fileAttachment",
                            "name": f"Relatorio_{prestador}_{periodo}.pdf",
                            "contentBytes": base64.b64encode(pdf_bytes).decode()
                        }]
                    }
                }
            )
            status = resp.status_code
            report.append({
                "Prestador": prestador,
                "Período": periodo,
                "Status": "✅" if status == 202 else f"❌ Erro {status}"
            })

        st.subheader("📋 Relatório de Envio")
        st.table(report)
        st.success("Envio concluído com sucesso!")
        st.session_state.confirming = False

    if c2.button("Não", key="confirm_no"):
        st.info("Envio cancelado.")
        st.session_state.confirming = False
