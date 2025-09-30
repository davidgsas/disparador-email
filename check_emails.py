import os
import base64
from pathlib import Path
import requests
from dotenv import load_dotenv
from msal import PublicClientApplication, SerializableTokenCache
import database as db
import time
import datetime # <--- A LINHA QUE FALTAVA FOI ADICIONADA AQUI

load_dotenv()

# --- Configurações de Autenticação ---
CLIENT_ID = os.getenv("CLIENT_ID")
TENANT_ID = os.getenv("TENANT_ID")
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPES = ["Mail.ReadWrite"]
TOKEN_CACHE_PATH = Path("token_cache.json")

cache = SerializableTokenCache()
if TOKEN_CACHE_PATH.exists():
    cache.deserialize(TOKEN_CACHE_PATH.read_text())

pca = PublicClientApplication(client_id=CLIENT_ID, authority=AUTHORITY, token_cache=cache)

def get_access_token():
    accounts = pca.get_accounts()
    if not accounts:
        print("Nenhuma conta encontrada. Faça login primeiro pelo app principal (streamlit_app.py).")
        return None
    
    result = pca.acquire_token_silent(SCOPES, account=accounts[0])
    if not result or "access_token" not in result:
        print("Não foi possível obter o token silenciosamente. Refaça o login no app principal.")
        return None
    
    return result["access_token"]

def process_replies():
    token = get_access_token()
    if not token:
        return

    headers = {"Authorization": f"Bearer {token}"}
    
    search_url = "https://graph.microsoft.com/v1.0/me/mailFolders/inbox/messages?$filter=isRead eq false and conversationId ne null&$select=id,conversationId,hasAttachments"
    response = requests.get(search_url, headers=headers)
    
    if response.status_code != 200:
        print(f"Erro ao buscar e-mails: {response.status_code} - {response.text}")
        return

    messages = response.json().get('value', [])
    if not messages:
        print("Nenhuma nova resposta encontrada.")
        return

    print(f"Encontradas {len(messages)} novas mensagens. Verificando...")

    for msg in messages:
        conv_id = msg.get('conversationId')
        
        envio_os = db.get_envio_os_by_conversation_id(conv_id)
        envio_montagem = db.get_envio_montagem_by_conversation_id(conv_id)

        target_envio = None
        is_os = False
        if envio_os and envio_os['status'] == 'Em Aberto':
            target_envio = envio_os
            is_os = True
        elif envio_montagem and envio_montagem['status'] == 'Em Aberto':
            target_envio = envio_montagem
        
        if target_envio:
            if msg.get('hasAttachments'):
                attach_url = f"https://graph.microsoft.com/v1.0/me/messages/{msg['id']}/attachments"
                attach_response = requests.get(attach_url, headers=headers)
                
                if attach_response.status_code != 200: continue
                
                attachments = attach_response.json().get('value', [])
                if not attachments: continue

                attachment = attachments[0]
                file_content = base64.b64decode(attachment['contentBytes'])
                
                anexo_dir = Path("anexos_recebidos")
                anexo_dir.mkdir(exist_ok=True)
                
                if is_os:
                    file_path = anexo_dir / f"NF_OS_{target_envio['os']}_{attachment['name']}"
                    db.update_os_attachment(target_envio['id'], str(file_path))
                    print(f"-> N.F. da OS {target_envio['os']} recebida e salva!")
                else:
                    file_path = anexo_dir / f"NF_Montador_{target_envio['montador_identificador']}_{attachment['name']}"
                    db.update_montagem_attachment(target_envio['id'], str(file_path))
                    print(f"-> N.F. do Montador {target_envio['montador_identificador']} recebida e salva!")

                with open(file_path, 'wb') as f:
                    f.write(file_content)

                update_url = f"https://graph.microsoft.com/v1.0/me/messages/{msg['id']}"
                requests.patch(update_url, headers=headers, json={"isRead": True})

if __name__ == "__main__":
    while True:
        print(f"\nVerificando e-mails às {datetime.datetime.now().strftime('%H:%M:%S')}...")
        process_replies()
        print("Aguardando 5 minutos para a próxima verificação...")
        time.sleep(60) # Espera 5 minutos