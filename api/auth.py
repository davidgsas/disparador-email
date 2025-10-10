"""
Módulo de Autenticação - Office 365 Integration
"""

from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import os
import requests
import json
from typing import Optional, Dict, Any
from msal import PublicClientApplication, SerializableTokenCache
from pathlib import Path
import datetime
import logging
import traceback
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Configurar logging
logger = logging.getLogger(__name__)

# Configurar router
auth_router = APIRouter()
security = HTTPBearer()

# Configurações do Azure AD
CLIENT_ID = os.getenv("CLIENT_ID")
TENANT_ID = os.getenv("TENANT_ID")
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPES = ["Mail.Send", "Mail.ReadWrite", "User.Read"]

# Log das configurações (sem expor dados sensíveis)
logger.info(f"🔧 Azure AD Config: CLIENT_ID={'***' if CLIENT_ID else 'NOT_SET'}, TENANT_ID={'***' if TENANT_ID else 'NOT_SET'}")

# Cache de token
TOKEN_CACHE_PATH = Path("token_cache.json")

# ===== MODELS =====

class LoginResponse(BaseModel):
    success: bool
    message: str
    device_code: Optional[str] = None
    user_code: Optional[str] = None
    verification_uri: Optional[str] = None
    expires_in: Optional[int] = None
    interval: Optional[int] = None

class TokenResponse(BaseModel):
    success: bool
    access_token: Optional[str] = None
    user: Optional[Dict[str, Any]] = None
    message: str

class UserInfo(BaseModel):
    id: str
    name: str
    email: str

# ===== FUNÇÕES AUXILIARES =====

def get_msal_app():
    """Obter instância do MSAL Public Client Application"""
    cache = SerializableTokenCache()
    if TOKEN_CACHE_PATH.exists():
        cache.deserialize(TOKEN_CACHE_PATH.read_text())
    
    return PublicClientApplication(
        client_id=CLIENT_ID,
        authority=AUTHORITY,
        token_cache=cache
    )

def save_token_cache(app):
    """Salvar cache de token"""
    TOKEN_CACHE_PATH.write_text(app.token_cache.serialize())

def get_user_info(access_token: str) -> Dict[str, Any]:
    """Obter informações do usuário a partir do token (síncrona)"""
    try:
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get("https://graph.microsoft.com/v1.0/me", headers=headers)
        
        if response.status_code != 200:
            raise Exception(f"Erro ao obter dados do usuário: {response.status_code}")
        
        user_data = response.json()
        
        return {
            "id": user_data.get("id", ""),
            "name": user_data.get("displayName", ""),
            "email": user_data.get("userPrincipalName", "")
        }
        
    except Exception as e:
        raise Exception(f"Erro ao obter informações do usuário: {str(e)}")

# ===== ROTAS DE AUTENTICAÇÃO =====

@auth_router.post("/login")
async def initiate_device_flow():
    """Iniciar fluxo de Device Code"""
    logger.info("🔐 Iniciando device flow para login...")
    
    try:
        app = get_msal_app()
        logger.info("📱 Criando device flow com MSAL...")
        
        device_flow = app.initiate_device_flow(scopes=SCOPES)
        logger.info(f"📱 Device flow criado com sucesso. User code: {device_flow.get('user_code', 'N/A')}")
        
        if "user_code" not in device_flow:
            logger.error("❌ Device flow não contém user_code")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Falha ao iniciar device flow"
            )
        
        # Salvar device flow no cache temporário
        cache_file = Path("token_cache.json")
        cache_data = {}
        if cache_file.exists():
            with open(cache_file, 'r') as f:
                cache_data = json.load(f)
        
        cache_data['device_flow'] = device_flow
        
        with open(cache_file, 'w') as f:
            json.dump(cache_data, f, default=str)
        
        logger.info("💾 Device flow salvo no cache")
        
        response_data = {
            "success": True,
            "data": {
                "user_code": device_flow["user_code"],
                "device_code": device_flow["device_code"],
                "verification_uri": device_flow["verification_uri"],
                "expires_in": device_flow["expires_in"],
                "interval": device_flow["interval"],
                "message": device_flow["message"]
            }
        }
        
        logger.info(f"✅ Device flow iniciado com sucesso: {response_data['data']['user_code']}")
        return response_data
        
    except Exception as e:
        logger.error(f"❌ Erro ao iniciar device flow: {str(e)}")
        logger.error(f"Stack trace: {traceback.format_exc()}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao iniciar login: {str(e)}"
        )

@auth_router.post("/verify")
async def complete_login(verification_data: dict):
    """Completar login com device code"""
    logger.info("🔍 Iniciando verificação do device code...")
    
    try:
        # Carregar device flow do cache
        cache_file = Path("token_cache.json")
        if not cache_file.exists():
            logger.error("❌ Cache file não encontrado")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Device flow não encontrado. Inicie o login novamente."
            )
        
        with open(cache_file, 'r') as f:
            cache_data = json.load(f)
        
        device_flow = cache_data.get('device_flow')
        if not device_flow:
            logger.error("❌ Device flow não encontrado no cache")
            
            # Verificar se já temos um token válido
            if 'token_info' in cache_data:
                logger.info("ℹ️ Token já existe no cache, device flow foi consumido")
                return {
                    "success": False,
                    "error": "Login já foi concluído anteriormente. Recarregue a página.",
                    "pending": False
                }
            
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Device flow expirado. Inicie o login novamente."
            )
        
        logger.info("📱 Verificando token com MSAL...")
        app = get_msal_app()
        result = app.acquire_token_by_device_flow(device_flow)
        
        logger.info(f"📱 Resultado MSAL: {list(result.keys()) if result else 'None'}")
        
        if "access_token" in result:
            logger.info("✅ Token adquirido com sucesso!")
            
            # Login bem-sucedido
            token_info = {
                "access_token": result["access_token"],
                "token_type": result.get("token_type", "Bearer"),
                "expires_in": result.get("expires_in", 3600),
                "scope": result.get("scope", ""),
                "refresh_token": result.get("refresh_token", "")
            }
            
            # Salvar token no cache e limpar device flow usado
            cache_data['token_info'] = token_info
            cache_data['expires_at'] = (datetime.datetime.now() + datetime.timedelta(seconds=token_info["expires_in"])).isoformat()
            
            # Limpar device flow usado para evitar reutilização
            if 'device_flow' in cache_data:
                del cache_data['device_flow']
                logger.info("🧹 Device flow removido do cache (já usado)")
            
            with open(cache_file, 'w') as f:
                json.dump(cache_data, f, default=str)
            
            logger.info("💾 Token salvo no cache")
            
            # Buscar informações do usuário
            logger.info("👤 Buscando informações do usuário...")
            user_info = get_user_info(result["access_token"])
            logger.info(f"👤 Usuário: {user_info.get('name', 'N/A')} ({user_info.get('email', 'N/A')})")
            
            return {
                "success": True,
                "data": {
                    "access_token": result["access_token"],
                    "user": user_info,
                    "expires_in": result.get("expires_in", 3600)
                }
            }
        else:
            error_code = result.get("error", "unknown")
            error_msg = result.get("error_description", "Falha na autenticação")
            
            logger.warning(f"⚠️  Erro MSAL: {error_code} - {error_msg}")
            
            if "authorization_pending" in error_code:
                error_msg = "Aguardando autorização do usuário"
            elif "authorization_declined" in error_code:
                error_msg = "Autorização recusada pelo usuário"
            elif "expired_token" in error_code:
                error_msg = "Código expirado. Inicie o login novamente."
            
            return {
                "success": False,
                "error": error_msg,
                "pending": "authorization_pending" in error_code,
                "error_code": error_code
            }
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Erro ao verificar login: {str(e)}")
        logger.error(f"Stack trace: {traceback.format_exc()}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao verificar login: {str(e)}"
        )

@auth_router.post("/refresh")
async def refresh_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Refresh do token de acesso"""
    try:
        app = get_msal_app()
        accounts = app.get_accounts()
        
        if not accounts:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Nenhuma conta encontrada"
            )
        
        result = app.acquire_token_silent(SCOPES, account=accounts[0])
        
        if result and "access_token" in result:
            save_token_cache(app)
            user_info = get_user_info(result["access_token"])
            
            return TokenResponse(
                success=True,
                access_token=result["access_token"],
                user=user_info,
                message="Token renovado com sucesso"
            )
        
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Não foi possível renovar o token"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao renovar token: {str(e)}"
        )

@auth_router.post("/logout")
async def logout():
    """Fazer logout do usuário"""
    try:
        # Limpar cache de token se existir
        if TOKEN_CACHE_PATH.exists():
            TOKEN_CACHE_PATH.unlink()
        
        return {
            "success": True,
            "message": "Logout realizado com sucesso"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro no logout: {str(e)}"
        )

# ===== DEPENDENCY FUNCTION =====

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verificar token OAuth e retornar usuário atual - Usado como dependência em outros endpoints"""
    token = credentials.credentials
    logger.info(f"🔐 [AUTH] Verificando token: {token[:20]}...")
    
    try:
        # Verificar se o token é válido fazendo uma chamada para a Microsoft Graph API
        headers = {"Authorization": f"Bearer {token}"}
        logger.info("🔐 [AUTH] Fazendo chamada para Microsoft Graph API...")
        
        response = requests.get("https://graph.microsoft.com/v1.0/me", headers=headers, timeout=10)
        logger.info(f"🔐 [AUTH] Resposta Graph API: {response.status_code}")
        
        if response.status_code == 200:
            user_data = response.json()
            user_info = {
                "id": user_data.get("id", ""),
                "oid": user_data.get("id", ""),
                "name": user_data.get("displayName", ""),
                "email": user_data.get("userPrincipalName", "")
            }
            logger.info(f"✅ Usuário autenticado: {user_info['name']} ({user_info['email']})")
            return user_info
        else:
            logger.warning(f"❌ Token inválido - Status: {response.status_code}")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authenticated",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except requests.RequestException as e:
        logger.error(f"❌ Erro na requisição Graph API: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Erro ao verificar token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        logger.error(f"❌ Erro inesperado na autenticação: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno na autenticação"
        )

@auth_router.get("/me", response_model=UserInfo)
async def get_current_user_info(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Obter informações do usuário atual""" 
    try:
        token = credentials.credentials
        user_info = await get_user_info(token)
        
        return UserInfo(**user_info)
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token inválido: {str(e)}"
        )

async def verify_token(token: str) -> Dict[str, Any]:
    """Verificar se o token é válido e retornar dados do usuário"""
    try:
        user_info = get_user_info(token)
        return user_info
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido"
        )
