"""
FastAPI Backend para o Sistema Disparador de Email Novo Mundo
"""

from fastapi import FastAPI, HTTPException, Depends, status, Request, File, UploadFile
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import json
import datetime
from pathlib import Path
from typing import List, Optional, Dict, Any
import uvicorn
import logging
import traceback
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Importar módulos locais
import database as db
from api.auth import auth_router, get_current_user
from api.prestadores import prestadores_router
from api.montadores import montadores_router
from api.dashboard import dashboard_router

# Inicializar FastAPI
app = FastAPI(
    title="Disparador de Email - Novo Mundo",
    description="Sistema de gestão e envio de emails para prestadores e montadores",
    version="2.0.0"
)

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('logs/app.log')
    ]
)
logger = logging.getLogger(__name__)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especificar domínios
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configurar segurança
security = HTTPBearer()

# Servir arquivos estáticos
app.mount("/assets", StaticFiles(directory="frontend/assets"), name="assets")
app.mount("/templates", StaticFiles(directory="templates"), name="templates")

# Incluir routers
app.include_router(auth_router, prefix="/api/auth", tags=["authentication"])
app.include_router(dashboard_router, prefix="/api/dashboard", tags=["dashboard"])
app.include_router(prestadores_router, prefix="/api/prestadores", tags=["prestadores"])
app.include_router(montadores_router, prefix="/api/montadores", tags=["montadores"])

# ===== EXCEPTION HANDLERS =====

from fastapi.exceptions import RequestValidationError

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handler para erros de validação (422)"""
    logger.error(f"🔴 ERRO DE VALIDAÇÃO 422!")
    logger.error(f"🔴 URL: {request.url}")
    logger.error(f"🔴 Method: {request.method}")
    logger.error(f"🔴 Erros: {exc.errors()}")
    logger.error(f"🔴 Body: {exc.body}")
    
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()}
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handler personalizado para HTTPException com logs detalhados"""
    logger.warning(f"⚠️  HTTP Exception: {exc.status_code} - {exc.detail} - Path: {request.url.path}")
    logger.warning(f"⚠️  Query params: {dict(request.query_params)}")
    logger.warning(f"⚠️  Headers: {list(request.headers.keys())}")
    
    # Log extra para 422
    if exc.status_code == 422:
        logger.error(f"🔴 ERRO 422 DETALHADO:")
        logger.error(f"🔴 URL completa: {request.url}")
        logger.error(f"🔴 Method: {request.method}")
        logger.error(f"🔴 Detail type: {type(exc.detail)}")
        logger.error(f"🔴 Detail content: {exc.detail}")
    
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
        headers=exc.headers
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handler para exceções gerais não tratadas"""
    logger.error(f"🔴 EXCEÇÃO NÃO TRATADA!")
    logger.error(f"🔴 Tipo: {type(exc).__name__}")
    logger.error(f"🔴 Mensagem: {str(exc)}")
    logger.error(f"🔴 Path: {request.url.path}")
    logger.error(f"🔴 Traceback:\n{traceback.format_exc()}")
    
    return JSONResponse(
        status_code=500,
        content={"detail": f"Erro interno: {str(exc)}"}
    )

# ===== MIDDLEWARES =====

@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log de todas as requisições"""
    start_time = datetime.datetime.now()
    client_ip = request.client.host if request.client else "unknown"
    
    # Log detalhado da requisição
    logger.info(f"🔄 {request.method} {request.url.path} - IP: {client_ip}")
    logger.debug(f"🔍 Query params: {dict(request.query_params)}")
    logger.debug(f"🔍 Headers: Authorization={'Present' if 'authorization' in request.headers else 'Missing'}")
    
    try:
        response = await call_next(request)
        process_time = datetime.datetime.now() - start_time
        
        # Log mais detalhado baseado no status
        if response.status_code >= 400:
            logger.warning(f"⚠️  {request.method} {request.url.path} - {response.status_code} - {process_time.total_seconds():.3f}s")
        else:
            logger.info(f"✅ {request.method} {request.url.path} - {response.status_code} - {process_time.total_seconds():.3f}s")
        
        return response
    except Exception as e:
        process_time = datetime.datetime.now() - start_time
        logger.error(f"❌ {request.method} {request.url.path} - ERROR: {type(e).__name__}: {str(e)} - {process_time.total_seconds():.3f}s")
        logger.error(f"Stack trace:\n{traceback.format_exc()}")
        raise

@app.get("/")
async def root():
    """Redirecionar para o frontend"""
    return FileResponse("frontend/index.html")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.datetime.now().isoformat(),
        "version": "2.0.0"
    }

# ===== ROTAS DE CONFIGURAÇÃO =====

@app.get("/api/config")
async def get_config(user: dict = Depends(get_current_user)):
    """Obter configurações atuais do usuário"""
    try:
        config_file = Path("config.json")
        if config_file.exists():
            with open(config_file, "r", encoding="utf-8") as f:
                config = json.load(f)
        else:
            config = {}
        
        return {
            "success": True,
            "data": config
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao carregar configurações: {str(e)}"
        )

@app.post("/api/config")
async def save_config(config: dict, user: dict = Depends(get_current_user)):
    """Salvar configurações do usuário"""
    try:
        config_file = Path("config.json")
        with open(config_file, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
        
        return {
            "success": True,
            "message": "Configurações salvas com sucesso"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao salvar configurações: {str(e)}"
        )

# ===== ROTAS DE TEMPLATES =====

@app.get("/api/templates/pdf/{tipo}")
async def get_pdf_template(tipo: str, user: dict = Depends(get_current_user)):
    """Obter template PDF atual"""
    try:
        template_files = {
            "prestadores": "templates/invoice_template.html",
            "montadores": "templates/montador_template.html"
        }
        
        if tipo not in template_files:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tipo de template não encontrado"
            )
        
        template_path = Path(template_files[tipo])
        if not template_path.exists():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Template não encontrado"
            )
        
        with open(template_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        return {
            "success": True,
            "data": {
                "content": content,
                "tipo": tipo
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao carregar template: {str(e)}"
        )

@app.post("/api/templates/pdf/{tipo}")
async def save_pdf_template(tipo: str, template_data: dict, user: dict = Depends(get_current_user)):
    """Salvar template PDF"""
    try:
        template_files = {
            "prestadores": "templates/invoice_template.html",
            "montadores": "templates/montador_template.html"
        }
        
        if tipo not in template_files:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tipo de template não encontrado"
            )
        
        template_path = Path(template_files[tipo])
        content = template_data.get("content", "")
        
        if not content:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Conteúdo do template é obrigatório"
            )
        
        with open(template_path, "w", encoding="utf-8") as f:
            f.write(content)
        
        return {
            "success": True,
            "message": "Template salvo com sucesso"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao salvar template: {str(e)}"
        )

# ===== ROTA DE UPLOAD DE ARQUIVOS =====

@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...), user: dict = Depends(get_current_user)):
    """Upload de arquivos (Excel, anexos, etc.)"""
    try:
        # Validar tipo de arquivo
        allowed_extensions = {".xlsx", ".xls", ".pdf", ".png", ".jpg", ".jpeg"}
        file_extension = Path(file.filename).suffix.lower()
        
        if file_extension not in allowed_extensions:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Tipo de arquivo não permitido"
            )
        
        # Criar diretório de upload se não existir
        upload_dir = Path("uploads")
        upload_dir.mkdir(exist_ok=True)
        
        # Gerar nome único para o arquivo
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{file.filename}"
        file_path = upload_dir / filename
        
        # Salvar arquivo
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        return {
            "success": True,
            "data": {
                "filename": filename,
                "original_filename": file.filename,
                "path": str(file_path),
                "size": len(content),
                "content_type": file.content_type
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro no upload: {str(e)}"
        )

# ===== TRATAMENTO DE ERROS =====

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handler customizado para HTTPException"""
    logger.warning(f"⚠️  HTTP Exception: {exc.status_code} - {exc.detail} - Path: {request.url.path}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": exc.detail,
            "status_code": exc.status_code,
            "path": request.url.path
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handler para exceções gerais"""
    logger.error(f"💥 Erro não tratado: {str(exc)}")
    logger.error(f"Stack trace completo:\n{traceback.format_exc()}")
    logger.error(f"Request path: {request.url.path}")
    logger.error(f"Request method: {request.method}")
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "error": f"Erro interno do servidor: {str(exc)}",
            "status_code": 500,
            "path": request.url.path,
            "method": request.method
        }
    )

# ===== INICIALIZAÇÃO =====

@app.on_event("startup")
async def startup_event():
    """Eventos na inicialização do servidor"""
    print("🚀 Iniciando servidor Disparador de Email...")
    
    # Executar migrações do banco de dados
    try:
        db.run_migrations()
        print("✅ Migrações do banco executadas com sucesso")
    except Exception as e:
        print(f"❌ Erro nas migrações: {e}")
    
    # Criar diretórios necessários
    for directory in ["uploads", "logs"]:
        Path(directory).mkdir(exist_ok=True)
    
    print("✅ Servidor iniciado com sucesso!")

@app.on_event("shutdown")
async def shutdown_event():
    """Eventos no encerramento do servidor"""
    print("🛑 Encerrando servidor...")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_dirs=[".", "api", "templates"],
        log_level="info"
    )
