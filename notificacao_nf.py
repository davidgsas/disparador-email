import os
import json
import datetime
import requests
from pathlib import Path
from jinja2 import Template
from msal import PublicClientApplication, SerializableTokenCache
from dotenv import load_dotenv

CONFIG_FILE = Path("config.json")
TOKEN_CACHE_FILE = Path("token_cache.json")

def load_config():
    """Carrega as configurações do arquivo JSON."""
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def get_cached_access_token():
    """Tenta obter um access token válido usando MSAL (mesmo método do sistema principal)."""
    try:
        # Carregar variáveis de ambiente
        load_dotenv()
        CLIENT_ID = os.getenv("CLIENT_ID")
        TENANT_ID = os.getenv("TENANT_ID")
        
        if not CLIENT_ID or not TENANT_ID:
            print(f"[LOG] Credenciais não configuradas - CLIENT_ID ou TENANT_ID ausentes")
            return None
        
        # Configurar MSAL como no sistema principal
        AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
        SCOPES = ["Mail.Send", "Mail.ReadWrite"]
        
        # Configurar cache
        cache = SerializableTokenCache()
        if TOKEN_CACHE_FILE.exists():
            cache.deserialize(TOKEN_CACHE_FILE.read_text())
        
        # Criar aplicação MSAL
        pca = PublicClientApplication(client_id=CLIENT_ID, authority=AUTHORITY, token_cache=cache)
        
        # Tentar obter token silenciosamente (mesma lógica do sistema principal)
        accounts = pca.get_accounts()
        if accounts:
            print(f"[LOG] Encontradas {len(accounts)} contas no cache")
            result = pca.acquire_token_silent(SCOPES, account=accounts[0])
            if result and "access_token" in result:
                print(f"[LOG] ✅ Token obtido com sucesso via MSAL")
                return result["access_token"]
            else:
                print(f"[LOG] ❌ Falha ao obter token via MSAL: {result.get('error', 'Erro desconhecido')}")
        else:
            print(f"[LOG] ❌ Nenhuma conta encontrada no cache MSAL")
        
        print(f"[LOG] 💡 Para reativar emails automáticos, faça login no sistema principal")
        return None
        
    except Exception as e:
        print(f"[LOG] Erro ao obter token via MSAL: {e}")
        return None

def enviar_notificacao_nf_upload(token_info, dados_lote, arquivo_nome, access_token=None, arquivo_path=None):
    """
    Envia notificação automática quando nota fiscal é recebida
    
    Args:
        token_info: Tupla (tipo, lote_id)
        dados_lote: Dados do lote/envio
        arquivo_nome: Nome do arquivo enviado
        access_token: Token de acesso Microsoft Graph (opcional)
        arquivo_path: Caminho completo do arquivo da nota fiscal (opcional)
    """
    try:
        # Carregar configurações de notificação
        config = load_config()
        notif_config = config.get("notificacao_nf", {})
        
        print(f"[LOG] Configuração carregada: {notif_config}")
        
        # Verificar se notificações estão ativas
        if not notif_config.get("ativo", False):
            print(f"[LOG] Notificações desativadas: ativo = {notif_config.get('ativo', False)}")
            return {"success": True, "message": "Notificações desativadas"}
        
        # Verificar se há emails configurados
        emails_str = notif_config.get("emails", "").strip()
        if not emails_str:
            print(f"[LOG] Nenhum email configurado: emails = '{emails_str}'")
            return {"success": False, "message": "Nenhum email configurado"}
        
        print(f"[LOG] Emails encontrados: {emails_str}")
        print(f"[LOG] Access token disponível: {'SIM' if access_token else 'NÃO'}")
        
        # Preparar variáveis para o template
        tipo, lote_id = token_info
        
        vars_template = {
            "lote_id": str(lote_id),
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
            detalhes = dados_lote.get('detalhes', {})
            if isinstance(detalhes, str):
                import json
                detalhes = json.loads(detalhes)
            
            vars_template.update({
                "prestador_nome": dados_lote.get('montador_nome', 'N/A'),  # Usar nome do montador
                "periodo": dados_lote.get('periodo', detalhes.get('periodo_relatorio', 'N/A')),
                "valor_total": f"{detalhes.get('total_geral', 0):,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
            })
        
        # Renderizar templates
        assunto_template = Template(notif_config.get("assunto", "🚨 NOTA FISCAL RECEBIDA - {{prestador_nome}} - Lote {{lote_id}}"))
        corpo_template = Template(notif_config.get("corpo", "Nova nota fiscal recebida de {{prestador_nome}}."))
        
        assunto_final = assunto_template.render(**vars_template)
        corpo_final = corpo_template.render(**vars_template)
        
        # Preparar lista de emails
        emails_list = [email.strip() for email in emails_str.split(",") if email.strip()]
        recipients = [{"emailAddress": {"address": email}} for email in emails_list]
        
        # Configurar prioridade
        prioridade = notif_config.get("prioridade", "Alta")
        importance = "high" if prioridade in ["Alta", "Urgente"] else "normal"
        
        # Preparar anexo se arquivo existe
        attachments = []
        if arquivo_path and os.path.exists(arquivo_path):
            print(f"[LOG] Preparando anexo: {arquivo_path}")
            try:
                import base64
                with open(arquivo_path, "rb") as f:
                    file_content = f.read()
                
                # Codificar arquivo em base64
                encoded_content = base64.b64encode(file_content).decode('utf-8')
                
                # Determinar tipo MIME
                import mimetypes
                mime_type, _ = mimetypes.guess_type(arquivo_path)
                if not mime_type:
                    mime_type = "application/octet-stream"
                
                attachment = {
                    "@odata.type": "#microsoft.graph.fileAttachment",
                    "name": arquivo_nome,
                    "contentType": mime_type,
                    "contentBytes": encoded_content
                }
                attachments.append(attachment)
                print(f"[LOG] Anexo preparado: {arquivo_nome} ({len(file_content)} bytes, {mime_type})")
                
            except Exception as e:
                print(f"[LOG] Erro ao preparar anexo: {e}")
        else:
            print(f"[LOG] Sem anexo - arquivo_path: {arquivo_path}")
        
        # Montar payload do email (estrutura correta para Microsoft Graph)
        message_data = {
            "message": {
                "subject": assunto_final,
                "body": {
                    "contentType": "Text",
                    "content": corpo_final
                },
                "toRecipients": recipients,
                "importance": importance
            }
        }
        
        # Adicionar anexos se houver
        if attachments:
            message_data["message"]["attachments"] = attachments
        
        print(f"[LOG] Template renderizado - Assunto: {assunto_final}")
        print(f"[LOG] Destinatários preparados: {emails_list}")
        print(f"[LOG] Prioridade definida: {importance}")
        
        # Se não tiver access_token, retornar os dados para debug
        if not access_token:
            print(f"[LOG] Sem access_token - retornando preview")
            preview_data = {
                "para": emails_list,
                "assunto": assunto_final,
                "corpo": corpo_final,
                "prioridade": importance
            }
            
            # Adicionar info sobre anexo se houver
            if attachments:
                preview_data["anexo"] = f"{arquivo_nome} ({len(attachments[0]['contentBytes'])} caracteres base64)"
            
            return {
                "success": False, 
                "message": "Token de acesso não disponível - Preview gerado",
                "preview": preview_data
            }
        
        print(f"[LOG] Tentando enviar email via Microsoft Graph API...")
        print(f"[LOG] Payload preparado: {len(str(message_data))} caracteres")
        
        # Enviar via Microsoft Graph API
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        print(f"[LOG] Fazendo request para Microsoft Graph...")
        
        try:
            response = requests.post(
                "https://graph.microsoft.com/v1.0/me/sendMail",
                headers=headers,
                json=message_data,
                timeout=30
            )
            
            print(f"[LOG] Response status: {response.status_code}")
            print(f"[LOG] Response headers: {dict(response.headers)}")
            print(f"[LOG] Response text: {response.text[:500]}...")
            
            if response.status_code == 202:
                print(f"[LOG] EMAIL ENVIADO COM SUCESSO!")
                return {
                    "success": True, 
                    "message": f"✅ Email enviado com sucesso para {len(emails_list)} destinatário(s)",
                    "emails": emails_list,
                    "response_code": response.status_code
                }
            else:
                print(f"[LOG] ERRO no envio - Status: {response.status_code}")
                return {
                    "success": False,
                    "message": f"❌ Erro HTTP {response.status_code}: {response.text[:200]}",
                    "response_code": response.status_code,
                    "response_text": response.text
                }
                
        except requests.exceptions.RequestException as e:
            print(f"[LOG] ERRO de conexão: {str(e)}")
            return {
                "success": False,
                "message": f"❌ Erro de conexão: {str(e)}",
                "error_type": "connection_error"
            }
        
    except Exception as e:
        return {
            "success": False,
            "message": f"Erro ao enviar notificação: {str(e)}",
            "error": str(e)
        }

def preview_notificacao(tipo="prestador", lote_id="123", arquivo_nome="nota_fiscal_teste.pdf", arquivo_path=None):
    """Gera preview da notificação para teste"""
    try:
        # Dados simulados para preview
        dados_simulados = {
            "prestador_nome": "Prestador Teste Ltda",
            "periodo": "01/10/2025 - 31/10/2025",
            "valor_total": 1234.56
        }
        
        if tipo == "montador":
            dados_simulados.update({
                "montador_nome": "Montador Teste",
                "detalhes": {
                    "periodo_relatorio": "01/10/2025 - 31/10/2025",
                    "total_geral": 987.65
                }
            })
        
        # Debug: verificar se config existe
        config = load_config()
        if "notificacao_nf" not in config:
            return {
                "success": False,
                "message": "Configuração de notificação não encontrada. Salve as configurações primeiro.",
                "debug": "config_missing"
            }
        
        resultado = enviar_notificacao_nf_upload(
            (tipo, lote_id),
            dados_simulados,
            arquivo_nome,
            access_token=None,  # Forçar preview
            arquivo_path=arquivo_path  # Incluir caminho do arquivo para anexo
        )
        
        return resultado
        
    except Exception as e:
        return {
            "success": False,
            "message": f"Erro no preview: {str(e)}",
            "error": str(e),
            "debug": "preview_exception"
        }
