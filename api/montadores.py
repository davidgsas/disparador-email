"""
Módulo Montadores - Gestão e Envio de Pagamentos
"""

from fastapi import APIRouter, HTTPException, status, Depends, UploadFile, File
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import pandas as pd
import io
import database as db

# Configurar router
montadores_router = APIRouter()
security = HTTPBearer()

# ===== MODELS =====

class MontadorCreate(BaseModel):
    nome: str
    identificador: str
    email: str
    emails_adicionais: Optional[str] = None
    percentual_comissao: float
    auxilio_semanal: float
    fornecedor_id: str
    regra_envio: str = "Nenhuma"
    dias_envio: Optional[str] = None

class MontadorUpdate(BaseModel):
    email: str
    emails_adicionais: Optional[str] = None
    percentual_comissao: float
    auxilio_semanal: float
    ativo: bool
    regra_envio: str
    dias_envio: Optional[str] = None
    fornecedor_id: Optional[str] = None

class MontadorResponse(BaseModel):
    id: int
    nome: str
    identificador: str
    email: str
    emails_adicionais: Optional[str]
    percentual_comissao: float
    auxilio_semanal: float
    ativo: bool
    fornecedor_id: str
    regra_envio: Optional[str]
    dias_envio: Optional[str]

class MontagemManual(BaseModel):
    identificador_do_montador: str
    identificador_boletim_montagem: str
    data_da_montagem: str
    media_de_valor_venda: float
    nome_do_cliente: str
    nome_produto: str

class ConfiguracaoEmailMontador(BaseModel):
    montador_cc: str
    montador_subject: str
    montador_body: str

class BlacklistBoletim(BaseModel):
    montador_id: int
    boletim: str
    motivo: Optional[str] = None

# ===== DEPENDENCY =====

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verificar token e retornar usuário atual"""
    token = credentials.credentials
    
    try:
        import requests
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get("https://graph.microsoft.com/v1.0/me", headers=headers)
        
        if response.status_code == 200:
            user_data = response.json()
            return {
                "id": user_data.get("id", ""),
                "name": user_data.get("displayName", ""),
                "email": user_data.get("userPrincipalName", "")
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido ou expirado"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Erro ao verificar token"
        )

# ===== ROTAS PRINCIPAIS =====

@montadores_router.get("/")
async def listar_montadores(user: dict = Depends(get_current_user)):
    """Listar todos os montadores"""
    try:
        montadores = db.get_all_montadores()
        return {"success": True, "data": montadores}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao listar montadores: {str(e)}"
        )

@montadores_router.get("/pending")
async def get_montadores_pendentes(user: dict = Depends(get_current_user)):
    """Buscar montadores com pendências"""
    try:
        import datetime
        
        montadores = db.get_all_montadores()
        
        # Filtrar apenas montadores com montagens de hoje
        hoje = datetime.date.today()
        montadores_hoje = []
        
        for montador in montadores:
            # Buscar montagens do montador
            montagens = db.get_montagens_by_montador(montador.get('codigo'))
            montagens_hoje = [m for m in montagens if m.get('data_montagem') == hoje]
            
            if montagens_hoje:
                montador_dict = {
                    "codigo": montador.get('codigo'),
                    "nome": montador.get('nome'),
                    "email": montador.get('email'),
                    "telefone": montador.get('telefone', ''),
                    "valor": sum(m.get('valor', 0) for m in montagens_hoje),
                    "quantidade_montagens": len(montagens_hoje)
                }
                montadores_hoje.append(montador_dict)
        
        return montadores_hoje
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar montadores pendentes: {str(e)}"
        )

@montadores_router.post("/", response_model=dict)
async def criar_montador(montador: MontadorCreate, user: dict = Depends(get_current_user)):
    """Criar novo montador"""
    try:
        success, message = db.add_montador(
            montador.nome,
            montador.identificador,
            montador.email,
            montador.percentual_comissao / 100.0,  # Converter percentual
            montador.auxilio_semanal,
            montador.fornecedor_id,
            montador.regra_envio,
            montador.dias_envio,
            montador.emails_adicionais
        )
        
        if success:
            return {"success": True, "message": message}
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=message
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao criar montador: {str(e)}"
        )

@montadores_router.put("/{montador_id}")
async def atualizar_montador(
    montador_id: int, 
    montador: MontadorUpdate, 
    user: dict = Depends(get_current_user)
):
    """Atualizar montador existente"""
    try:
        db.update_montador(
            montador_id,
            montador.email,
            montador.percentual_comissao / 100.0,  # Converter percentual
            montador.auxilio_semanal,
            montador.ativo,
            montador.regra_envio,
            montador.dias_envio,
            montador.fornecedor_id,
            montador.emails_adicionais
        )
        
        return {"success": True, "message": "Montador atualizado com sucesso"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao atualizar montador: {str(e)}"
        )

@montadores_router.get("/{montador_id}")
async def obter_montador(montador_id: int, user: dict = Depends(get_current_user)):
    """Obter detalhes de um montador específico"""
    try:
        montador = db.get_montador_by_id(montador_id)
        if not montador:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Montador não encontrado"
            )
        
        return {"success": True, "data": dict(montador)}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao obter montador: {str(e)}"
        )

# ===== ROTAS DE ENVIO =====

@montadores_router.post("/enviar-pagamentos")
async def enviar_pagamentos(
    montagens: List[MontagemManual], 
    config: ConfiguracaoEmailMontador,
    user: dict = Depends(get_current_user)
):
    """Enviar pagamentos de montagem"""
    try:
        # TODO: Implementar lógica completa de envio
        # Por enquanto, apenas validação básica
        
        if not montagens:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Lista de montagens não pode estar vazia"
            )
        
        # Validar dados das montagens
        for montagem in montagens:
            if not all([
                montagem.identificador_do_montador, 
                montagem.identificador_boletim_montagem,
                montagem.data_da_montagem,
                montagem.media_de_valor_venda > 0
            ]):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Campos obrigatórios faltando na montagem"
                )
        
        # Verificar boletins já enviados
        boletim_ids = [m.identificador_boletim_montagem for m in montagens]
        sent_boletins = db.check_boletim_list(boletim_ids)
        blacklisted_boletins = db.check_boletins_blacklist(boletim_ids)
        
        # Filtrar apenas boletins novos
        montagens_validas = [
            m for m in montagens 
            if m.identificador_boletim_montagem not in sent_boletins and 
               m.identificador_boletim_montagem not in blacklisted_boletins
        ]
        
        if not montagens_validas:
            return {
                "success": False,
                "message": "Nenhuma montagem nova para processar",
                "sent_boletins": sent_boletins,
                "blacklisted_boletins": blacklisted_boletins
            }
        
        # TODO: Implementar envio real de emails
        
        return {
            "success": True,
            "message": f"{len(montagens_validas)} montagens processadas com sucesso",
            "sent_count": len(montagens_validas),
            "skipped_sent": len(sent_boletins),
            "skipped_blacklist": len(blacklisted_boletins)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao enviar pagamentos: {str(e)}"
        )

@montadores_router.post("/upload-excel")
async def upload_excel_montadores(
    file: UploadFile = File(...), 
    user: dict = Depends(get_current_user)
):
    """Upload e processamento de Excel de montadores"""
    try:
        # Validar tipo de arquivo
        if not file.filename.endswith(('.xlsx', '.xls')):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Arquivo deve ser Excel (.xlsx ou .xls)"
            )
        
        # Ler arquivo Excel
        content = await file.read()
        df = pd.read_excel(io.BytesIO(content))
        
        # Normalizar nomes das colunas
        df.columns = [col.strip().lower().replace(' ', '_') for col in df.columns]
        
        # Verificar colunas obrigatórias
        required_cols = [
            'identificador_do_montador', 
            'identificador_boletim_montagem',
            'data_da_montagem', 
            'media_de_valor_venda', 
            'nome_produto'
        ]
        missing_cols = [col for col in required_cols if col not in df.columns]
        
        if missing_cols:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Colunas obrigatórias faltando: {', '.join(missing_cols)}"
            )
        
        # Converter dados
        data = df.to_dict('records')
        
        return {
            "success": True,
            "message": f"Excel processado com sucesso. {len(data)} registros encontrados.",
            "data": data,
            "columns": list(df.columns)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao processar Excel: {str(e)}"
        )

# ===== ROTAS DE HISTÓRICO =====

@montadores_router.get("/historico")
async def obter_historico(user: dict = Depends(get_current_user)):
    """Obter histórico de montagens enviadas"""
    try:
        historico = db.get_all_sent_montagens()
        
        return {
            "success": True,
            "data": [dict(item) for item in historico]
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao carregar histórico: {str(e)}"
        )

@montadores_router.get("/{montador_id}/historico")
async def obter_historico_montador(montador_id: int, user: dict = Depends(get_current_user)):
    """Obter histórico de um montador específico"""
    try:
        historico = db.get_montagens_by_montador_id(montador_id)
        
        return {
            "success": True,
            "data": [dict(item) for item in historico]
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao carregar histórico do montador: {str(e)}"
        )

@montadores_router.put("/historico/{envio_id}/status")
async def atualizar_status_envio(
    envio_id: int, 
    status_data: dict, 
    user: dict = Depends(get_current_user)
):
    """Atualizar status de um envio de montagem"""
    try:
        novo_status = status_data.get('status')
        if not novo_status:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Status é obrigatório"
            )
        
        db.update_montagem_status(envio_id, novo_status)
        
        return {
            "success": True,
            "message": "Status atualizado com sucesso"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao atualizar status: {str(e)}"
        )

@montadores_router.put("/historico/{envio_id}/detalhes")
async def atualizar_detalhes_envio(
    envio_id: int, 
    detalhes: dict, 
    user: dict = Depends(get_current_user)
):
    """Atualizar detalhes de um envio de montagem"""
    try:
        db.update_montagem_details(envio_id, detalhes)
        
        return {
            "success": True,
            "message": "Detalhes atualizados com sucesso"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao atualizar detalhes: {str(e)}"
        )

@montadores_router.delete("/historico/{envio_id}")
async def deletar_envio(envio_id: int, user: dict = Depends(get_current_user)):
    """Deletar envio de montagem"""
    try:
        db.delete_envio_montagem(envio_id)
        return {"success": True, "message": "Envio removido com sucesso"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao remover envio: {str(e)}"
        )

# ===== ROTAS DE BLACKLIST =====

@montadores_router.get("/blacklist")
async def obter_blacklist(user: dict = Depends(get_current_user)):
    """Obter lista completa da blacklist de boletins"""
    try:
        blacklist = db.get_boletins_blacklist()
        return {
            "success": True,
            "data": [dict(item) for item in blacklist]
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao carregar blacklist: {str(e)}"
        )

@montadores_router.post("/blacklist")
async def adicionar_blacklist(item: BlacklistBoletim, user: dict = Depends(get_current_user)):
    """Adicionar boletim à blacklist"""
    try:
        success, message = db.adicionar_boletim_blacklist(
            item.montador_id,
            item.boletim,
            item.motivo
        )
        
        if success:
            return {"success": True, "message": message}
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=message
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao adicionar à blacklist: {str(e)}"
        )

@montadores_router.delete("/blacklist/{montador_id}/{boletim}")
async def remover_blacklist(
    montador_id: int, 
    boletim: str, 
    user: dict = Depends(get_current_user)
):
    """Remover boletim da blacklist"""
    try:
        db.remover_boletim_blacklist(montador_id, boletim)
        return {"success": True, "message": "Boletim removido da blacklist"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao remover da blacklist: {str(e)}"
        )
