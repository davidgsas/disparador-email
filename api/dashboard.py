"""
Módulo Dashboard - Pendências e Resumos
"""

from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import datetime
import database as db

# Configurar router
dashboard_router = APIRouter()
security = HTTPBearer()

# ===== MODELS =====

class PendenciaItem(BaseModel):
    id: int
    nome: str
    tipo: str  # 'prestador' ou 'montador'
    regra_envio: str
    dias_envio: str
    pode_ignorar: bool = True

class ResumoDia(BaseModel):
    total_pendentes: int
    total_enviados_hoje: int
    total_ignorados: int
    total_entidades_ativas: int

class DashboardData(BaseModel):
    prestadores_pendentes: List[PendenciaItem]
    montadores_pendentes: List[PendenciaItem]
    resumo: ResumoDia

class IgnorarEnvioRequest(BaseModel):
    tipo: str  # 'prestador' ou 'montador'
    entidade_id: int

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

# ===== FUNÇÕES AUXILIARES =====

DIAS_SEMANA_MAP = {
    "Monday": "Segunda-feira",
    "Tuesday": "Terça-feira",
    "Wednesday": "Quarta-feira", 
    "Thursday": "Quinta-feira",
    "Friday": "Sexta-feira",
    "Saturday": "Sábado",
    "Sunday": "Domingo"
}

def verificar_pendencias(entidades: List[Dict], tipo: str) -> List[PendenciaItem]:
    """Verificar pendências de hoje para uma lista de entidades"""
    pendentes = []
    hoje = datetime.date.today()
    ano_atual, semana_atual, dia_semana_hoje_num = hoje.isocalendar()
    dia_semana_hoje_en = hoje.strftime('%A')
    dia_do_mes_hoje = hoje.day

    for entidade in entidades:
        regra = entidade.get('regra_envio')
        dias = entidade.get('dias_envio')
        
        if not regra or regra == "Nenhuma" or not dias:
            continue
        
        entidade_id = entidade['id']
        pendente = False
        
        if regra == 'Semanal' and DIAS_SEMANA_MAP.get(dia_semana_hoje_en) == dias:
            # Verificar se não foi enviado nem ignorado nesta semana
            if not db.get_envios_na_semana(tipo, entidade_id, ano_atual, semana_atual) and \
               not db.foi_ignorado_na_semana(tipo, entidade_id, ano_atual, semana_atual):
                pendente = True
                
        elif regra in ['Mensal (Dia Fixo)', 'Quinzenal']:
            try:
                dias_envio_mes = [int(d.strip()) for d in dias.split(',')]
                if dia_do_mes_hoje in dias_envio_mes:
                    # Verificar se não foi enviado hoje (lógica simplificada)
                    pendente = True
            except ValueError:
                continue
        
        if pendente:
            pendentes.append(PendenciaItem(
                id=entidade_id,
                nome=entidade['nome'],
                tipo=tipo,
                regra_envio=regra,
                dias_envio=dias,
                pode_ignorar=regra == 'Semanal'  # Só permite ignorar envios semanais
            ))
            
    return pendentes

# ===== ROTAS =====

@dashboard_router.get("/pendencias", response_model=DashboardData)
async def get_pendencias(user: dict = Depends(get_current_user)):
    """Obter todas as pendências do dashboard"""
    try:
        # Obter prestadores e montadores
        prestadores = db.get_all_prestadores()
        montadores = db.get_all_montadores(apenas_ativos=True)
        
        # Verificar pendências
        prestadores_pendentes = verificar_pendencias(prestadores, 'prestador')
        montadores_pendentes = verificar_pendencias(montadores, 'montador')
        
        # Calcular resumo
        hoje = datetime.date.today()
        
        # Contar envios reais do banco
        total_enviados_hoje = len(db.get_all_lotes_servico()) + len(db.get_all_sent_montagens())
        total_ignorados = 0  # Implementar contador de ignorados se necessário
        
        resumo = ResumoDia(
            total_pendentes=len(prestadores_pendentes) + len(montadores_pendentes),
            total_enviados_hoje=total_enviados_hoje,
            total_ignorados=total_ignorados,
            total_entidades_ativas=len([p for p in prestadores]) + len([m for m in montadores])
        )
        
        return DashboardData(
            prestadores_pendentes=prestadores_pendentes,
            montadores_pendentes=montadores_pendentes,
            resumo=resumo
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao carregar pendências: {str(e)}"
        )

@dashboard_router.post("/ignorar-envio")
async def ignorar_envio(request: IgnorarEnvioRequest, user: dict = Depends(get_current_user)):
    """Ignorar um envio pendente"""
    try:
        if request.tipo not in ['prestador', 'montador']:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Tipo deve ser 'prestador' ou 'montador'"
            )
        
        hoje = datetime.date.today()
        ano, semana, _ = hoje.isocalendar()
        
        # Ignorar envio semanal
        db.ignorar_envio_semanal(request.tipo, request.entidade_id, ano, semana)
        
        return {
            "success": True,
            "message": f"Envio ignorado para esta semana"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao ignorar envio: {str(e)}"
        )

@dashboard_router.get("/resumo", response_model=ResumoDia)
async def get_resumo_dia(user: dict = Depends(get_current_user)):
    """Obter resumo do dia"""
    try:
        # Obter dados básicos
        prestadores = db.get_all_prestadores()
        montadores = db.get_all_montadores(apenas_ativos=True)
        
        # Verificar pendências  
        prestadores_pendentes = verificar_pendencias(prestadores, 'prestador')
        montadores_pendentes = verificar_pendencias(montadores, 'montador')
        
        # TODO: Implementar contadores baseados no banco
        total_enviados_hoje = 0
        total_ignorados = 0
        
        return ResumoDia(
            total_pendentes=len(prestadores_pendentes) + len(montadores_pendentes),
            total_enviados_hoje=total_enviados_hoje,
            total_ignorados=total_ignorados,
            total_entidades_ativas=len(prestadores) + len(montadores)
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao carregar resumo: {str(e)}"
        )
