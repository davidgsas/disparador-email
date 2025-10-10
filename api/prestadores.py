"""
Módulo Prestadores - Gestão e Envio de Boletins
Sistema completo baseado na documentação oficial
"""

from fastapi import APIRouter, HTTPException, status, Depends, UploadFile, File, Query
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import pandas as pd
import io
import json
import os
import base64
import datetime
import re
import time
import logging
import requests
from pathlib import Path
from jinja2 import Template
from weasyprint import HTML
import shutil
from itertools import groupby

import database as db

# Importar função de autenticação do módulo auth
from api.auth import get_current_user

# Configurar logging
logger = logging.getLogger(__name__)

# Configurar router
prestadores_router = APIRouter()
security = HTTPBearer()

# ===== CONSTANTS =====

DIAS_SEMANA_MAP = {
    0: "Segunda-feira",
    1: "Terça-feira", 
    2: "Quarta-feira",
    3: "Quinta-feira",
    4: "Sexta-feira",
    5: "Sábado",
    6: "Domingo"
}

STATUS_OPTIONS = ["Em Aberto", "Pago", "Cancelado", "N.F. RECEBIDA"]

# ===== MODELS =====

class PrestadorCreate(BaseModel):
    nome: str
    email: str
    emails_adicionais: Optional[str] = None
    fornecedor_id: Optional[str] = None
    regra_envio: str = "Nenhuma"
    dias_envio: Optional[str] = None

class PrestadorUpdate(BaseModel):
    nome: str
    email: str
    fornecedor_id: Optional[str] = None
    regra_envio: str
    dias_envio: Optional[str] = None
    emails_adicionais: Optional[str] = None

class PrestadorResponse(BaseModel):
    id: int
    nome: str
    email: str
    emails_adicionais: Optional[str]
    fornecedor_id: Optional[str]
    regra_envio: Optional[str]
    dias_envio: Optional[str]

class BoletimManual(BaseModel):
    nome_prestador: str
    periodo: str
    o_s: str
    modalidade: str
    data_execucao: str
    valor_custo_prestador: float
    valor_extra: float = 0.0
    motivo_extra: Optional[str] = None

class EnvioBoletins(BaseModel):
    boletins: List[BoletimManual]
    configuracao: Dict[str, str]  # prestador_cc, prestador_subject, prestador_body

class ConfiguracaoEmail(BaseModel):
    prestador_cc: str
    prestador_subject: str
    prestador_body: str

class BlacklistOS(BaseModel):
    prestador_id: int
    os_numero: str
    motivo: Optional[str] = None

class LoteStatusUpdate(BaseModel):
    status: str

class TemplateUpdate(BaseModel):
    content: str

# ===== HELPER FUNCTIONS =====

def convert_plain_text_to_html(text):
    """Converte texto simples para HTML"""
    html = text.replace('\n', '<br>')
    html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html)
    return html

def get_saudacao():
    """Retorna saudação baseada no horário"""
    hora = datetime.datetime.now().hour
    if hora < 12:
        return "Bom dia"
    elif hora < 18:
        return "Boa tarde"
    else:
        return "Boa noite"

def validate_excel_columns(df, required_cols):
    """Valida se as colunas obrigatórias estão presentes no Excel"""
    missing_cols = [col for col in required_cols if col not in df.columns]
    return missing_cols

def normalize_column_names(df):
    """Normaliza nomes das colunas do DataFrame"""
    df.columns = [re.sub(r"\W+", "_", c.strip()).lower() for c in df.columns]
    return df

def save_config_to_file(config_data):
    """Salva configurações no arquivo config.json"""
    try:
        config_path = Path("config.json")
        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                existing_config = json.load(f)
        else:
            existing_config = {}
        
        existing_config.update(config_data)
        
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(existing_config, f, ensure_ascii=False, indent=2)
        
        return True
    except Exception as e:
        logger.error(f"Erro ao salvar configuração: {str(e)}")
        return False

def load_config_from_file():
    """Carrega configurações do arquivo config.json"""
    try:
        config_path = Path("config.json")
        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    except Exception as e:
        logger.error(f"Erro ao carregar configuração: {str(e)}")
        return {}

# ===== DEPENDENCY =====

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verificar token e retornar usuário atual"""
    token = credentials.credentials
    
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get("https://graph.microsoft.com/v1.0/me", headers=headers, timeout=10)
        
        if response.status_code == 200:
            user_data = response.json()
            return {
                "id": user_data.get("id", ""),
                "name": user_data.get("displayName", ""),
                "email": user_data.get("userPrincipalName", ""),
                "token": token
            }
        else:
            logger.warning(f"❌ Token inválido - Status: {response.status_code}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido ou expirado"
            )
    except requests.RequestException as e:
        logger.error(f"❌ Erro na requisição Graph API: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Erro ao verificar token"
        )
    except Exception as e:
        logger.error(f"❌ Erro inesperado na autenticação: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno na autenticação"
        )

# ===== ROTAS DE GESTÃO =====

@prestadores_router.get("/", response_model=List[PrestadorResponse])
async def listar_prestadores(user: dict = Depends(get_current_user)):
    """Listar todos os prestadores cadastrados"""
    try:
        logger.info(f"👤 {user['name']} solicitou lista de prestadores")
        prestadores = db.get_all_prestadores()
        
        result = []
        for prestador in prestadores:
            result.append(PrestadorResponse(
                id=prestador['id'],
                nome=prestador['nome'],
                email=prestador['email'],
                emails_adicionais=prestador.get('emails_adicionais'),
                fornecedor_id=prestador['fornecedor_id'],
                regra_envio=prestador.get('regra_envio', 'Nenhuma'),
                dias_envio=prestador.get('dias_envio')
            ))
        
        logger.info(f"✅ Retornados {len(result)} prestadores")
        return result
        
    except Exception as e:
        logger.error(f"❌ Erro ao listar prestadores: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao listar prestadores: {str(e)}"
        )

@prestadores_router.get("/pending")
async def get_prestadores_pendentes(user: dict = Depends(get_current_user)):
    """Buscar prestadores com pendências hoje (baseado nas regras de envio)"""
    try:
        logger.info(f"👤 {user['name']} solicitou prestadores pendentes")
        
        prestadores = db.get_all_prestadores()
        hoje = datetime.date.today()
        pendentes = []
        
        for prestador in prestadores:
            # Verificar se tem pendência baseado na regra de envio
            tem_pendencia = verificar_pendencia_prestador(prestador, hoje)
            
            if tem_pendencia:
                # Buscar valor estimado baseado em lotes recentes
                lotes_recentes = db.get_lotes_servico_by_prestador(prestador['fornecedor_id'])
                valor_estimado = sum(l.get('valor_total', 0) for l in lotes_recentes[-5:]) / max(len(lotes_recentes[-5:]), 1)
                
                pendente = {
                    "id": prestador['id'],
                    "codigo": prestador['fornecedor_id'],
                    "nome": prestador['nome'],
                    "email": prestador['email'],
                    "regra_envio": prestador.get('regra_envio', 'Nenhuma'),
                    "dias_envio": prestador.get('dias_envio', ''),
                    "valor_estimado": round(valor_estimado, 2),
                    "pode_ignorar": True
                }
                pendentes.append(pendente)
        
        logger.info(f"📋 Encontrados {len(pendentes)} prestadores pendentes")
        return {"success": True, "data": pendentes}
        
    except Exception as e:
        logger.error(f"❌ Erro ao buscar prestadores pendentes: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar prestadores pendentes: {str(e)}"
        )

def verificar_pendencia_prestador(prestador, data_ref):
    """Verifica se um prestador tem pendência na data de referência"""
    regra = prestador.get('regra_envio', 'Nenhuma')
    dias_envio = prestador.get('dias_envio', '')
    
    if regra == 'Nenhuma':
        return False
    
    # TODO: Implementar lógica completa de regras de envio
    # Por enquanto, considerar apenas regra semanal simples
    if regra == 'Semanal' and dias_envio:
        dia_semana_nome = DIAS_SEMANA_MAP.get(data_ref.weekday())
        return dia_semana_nome == dias_envio
    
    return False

@prestadores_router.post("/", response_model=dict)
async def criar_prestador(prestador: PrestadorCreate, user: dict = Depends(get_current_user)):
    """Criar novo prestador"""
    try:
        logger.info(f"👤 {user['name']} criando prestador: {prestador.nome}")
        
        # Validar campos obrigatórios
        if not all([prestador.nome, prestador.email, prestador.fornecedor_id]):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Todos os campos obrigatórios devem ser preenchidos (Nome, E-mail Principal e Número do Fornecedor)"
            )
        
        # Validar regra de envio
        if prestador.regra_envio not in ["Nenhuma", "Semanal", "Mensal (Dia Fixo)", "Quinzenal"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Regra de envio inválida"
            )
        
        # Validar dias de envio se necessário - conforme documentação é opcional
        if prestador.regra_envio == "Semanal" and prestador.dias_envio:
            # Aceitar tanto nomes dos dias quanto números (mais flexible) 
            dias_validos = list(DIAS_SEMANA_MAP.values()) + [str(i) for i in range(7)]
            if prestador.dias_envio not in dias_validos:
                logger.warning(f"⚠️ Dia enviado: '{prestador.dias_envio}', dias válidos: {dias_validos}")
                # Não bloquear, apenas fazer log - conforme documentação é opcional
        
        success, message = db.add_prestador(
            prestador.nome,
            prestador.email,
            prestador.fornecedor_id,
            prestador.regra_envio,
            prestador.dias_envio,
            prestador.emails_adicionais
        )
        
        if success:
            logger.info(f"✅ Prestador {prestador.nome} criado com sucesso")
            return {"success": True, "message": message}
        else:
            logger.warning(f"⚠️ Falha ao criar prestador {prestador.nome}: {message}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=message
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Erro ao criar prestador: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao criar prestador: {str(e)}"
        )

@prestadores_router.put("/{prestador_id}")
async def atualizar_prestador(
    prestador_id: int, 
    prestador: PrestadorUpdate, 
    user: dict = Depends(get_current_user)
):
    """Atualizar prestador existente"""
    try:
        logger.info(f"👤 {user['name']} atualizando prestador ID: {prestador_id}")
        
        # Validar campos obrigatórios
        if not all([prestador.nome, prestador.email]):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Nome e email são obrigatórios"
            )
        
        # Validar regra de envio
        if prestador.regra_envio not in ["Nenhuma", "Semanal", "Mensal (Dia Fixo)", "Quinzenal"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Regra de envio inválida"
            )
        
        # Validar dias de envio se necessário - conforme documentação é opcional
        if prestador.regra_envio == "Semanal" and prestador.dias_envio:
            # Aceitar tanto nomes dos dias quanto números (mais flexible)
            dias_validos = list(DIAS_SEMANA_MAP.values()) + [str(i) for i in range(7)]
            if prestador.dias_envio not in dias_validos:
                logger.warning(f"⚠️ Dia enviado no update: '{prestador.dias_envio}', dias válidos: {dias_validos}")
                # Não bloquear, apenas fazer log - conforme documentação é opcional
        
        db.update_prestador_completo(
            prestador_id,
            prestador.nome,
            prestador.email,
            prestador.fornecedor_id,
            prestador.regra_envio,
            prestador.dias_envio,
            prestador.emails_adicionais
        )
        
        logger.info(f"✅ Prestador ID {prestador_id} atualizado com sucesso")
        return {"success": True, "message": "Prestador atualizado com sucesso"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Erro ao atualizar prestador ID {prestador_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao atualizar prestador: {str(e)}"
        )

@prestadores_router.delete("/{prestador_id}")
async def deletar_prestador(prestador_id: int, user: dict = Depends(get_current_user)):
    """Deletar prestador"""
    try:
        logger.info(f"👤 {user['name']} deletando prestador ID: {prestador_id}")
        
        # Verificar se existem lotes associados
        # TODO: Implementar verificação de dependências se necessário
        
        db.delete_prestador(prestador_id)
        
        logger.info(f"✅ Prestador ID {prestador_id} removido com sucesso")
        return {"success": True, "message": "Prestador removido com sucesso"}
        
    except Exception as e:
        logger.error(f"❌ Erro ao remover prestador ID {prestador_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao remover prestador: {str(e)}"
        )

# ===== ROTAS DE ENVIO =====

@prestadores_router.post("/enviar-boletins")
async def enviar_boletins(
    dados_envio: EnvioBoletins,
    user: dict = Depends(get_current_user)
):
    """Enviar boletins de serviço - Funcionalidade completa como no Streamlit"""
    try:
        logger.info(f"👤 {user['name']} iniciando envio de boletins")
        boletins = dados_envio.boletins
        configuracao = dados_envio.configuracao
        
        if not boletins:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Lista de boletins não pode estar vazia"
            )
        
        # Salvar configurações
        save_config_to_file({
            "prestador_cc": configuracao.get("prestador_cc", ""),
            "prestador_subject": configuracao.get("prestador_subject", ""),
            "prestador_body": configuracao.get("prestador_body", "")
        })
        
        # Validar dados dos boletins
        for i, boletim in enumerate(boletins):
            if not all([boletim.nome_prestador, boletim.periodo, boletim.o_s]):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Boletim {i+1}: Campos obrigatórios faltando (Nome Prestador, Período, O.S.)"
                )
        
        # Verificar O.S. já enviadas e na blacklist
        os_numbers = [str(b.o_s) for b in boletins]
        sent_os = db.check_os_list(os_numbers)
        blacklisted_os = db.check_os_blacklist(os_numbers)
        
        logger.info(f"📋 Verificação: {len(sent_os)} O.S. já enviadas, {len(blacklisted_os)} na blacklist")
        
        # Filtrar apenas O.S. válidas
        boletins_validos = []
        for boletim in boletins:
            if str(boletim.o_s) not in sent_os and str(boletim.o_s) not in blacklisted_os:
                boletins_validos.append(boletim)
        
        if not boletins_validos:
            return {
                "success": False,
                "message": "Nenhuma O.S. nova para enviar",
                "data": {
                    "total_enviados": 0,
                    "total_ignorados": len(boletins),
                    "sent_os": sent_os,
                    "blacklisted_os": blacklisted_os,
                    "relatorio": []
                }
            }
        
        logger.info(f"📤 Preparando envio de {len(boletins_validos)} boletins válidos")
        
        # Processar envios
        relatorio = await processar_envio_boletins(boletins_validos, configuracao, user['token'])
        
        # Contar sucessos e falhas
        sucessos = sum(1 for r in relatorio if "✅" in r.get("status", ""))
        falhas = len(relatorio) - sucessos
        
        logger.info(f"📊 Resultado: {sucessos} sucessos, {falhas} falhas")
        
        return {
            "success": True,
            "message": f"Processamento concluído: {sucessos} enviados, {falhas} falhas",
            "data": {
                "total_enviados": sucessos,
                "total_falhas": falhas,
                "total_ignorados": len(sent_os) + len(blacklisted_os),
                "sent_os": sent_os,
                "blacklisted_os": blacklisted_os,
                "relatorio": relatorio
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Erro no envio de boletins: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao enviar boletins: {str(e)}"
        )

async def processar_envio_boletins(boletins_validos, configuracao, access_token):
    """Processa o envio de boletins agrupados por prestador e período"""
    relatorio = []
    saudacao = get_saudacao()
    
    # Carregar template de PDF
    template_path = Path("templates/invoice_template.html")
    if not template_path.exists():
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Template de PDF não encontrado"
        )
    
    invoice_template = Template(template_path.read_text(encoding="utf-8"))
    
    # Processar configurações de email
    cc_list = [e.strip() for e in configuracao.get("prestador_cc", "").split(",") if e.strip()]
    subject_template = Template(configuracao.get("prestador_subject", "Relatório de Serviços"))
    body_template = Template(configuracao.get("prestador_body", "Segue relatório em anexo."))
    
    # Agrupar boletins por prestador e período
    from itertools import groupby
    
    # Converter para dicionários para groupby
    boletins_dict = []
    for b in boletins_validos:
        boletim_dict = {
            "nome_prestador": b.nome_prestador,
            "periodo": b.periodo,
            "o_s": str(b.o_s),
            "modalidade": b.modalidade,
            "data_execucao": b.data_execucao,
            "valor_custo_prestador": b.valor_custo_prestador,
            "valor_extra": b.valor_extra,
            "motivo_extra": b.motivo_extra or "",
            "valor_total": b.valor_custo_prestador + b.valor_extra
        }
        boletins_dict.append(boletim_dict)
    
    # Agrupar por prestador e período
    boletins_dict.sort(key=lambda x: (x["nome_prestador"], x["periodo"]))
    
    for (nome_prestador, periodo), group in groupby(boletins_dict, key=lambda x: (x["nome_prestador"], x["periodo"])):
        try:
            logger.info(f"📤 Processando: {nome_prestador} - {periodo}")
            
            # Obter dados do prestador
            prestador_info = db.get_prestador_by_name(nome_prestador)
            if not prestador_info:
                relatorio.append({
                    "prestador": nome_prestador,
                    "periodo": periodo,
                    "status": "❌ Prestador não cadastrado no banco"
                })
                continue
            
            # Converter group para lista
            items = list(group)
            total_geral = sum(item["valor_total"] for item in items)
            
            # Formatar itens para o PDF
            items_formatted = []
            for item in items:
                data_exec = item["data_execucao"]
                if isinstance(data_exec, str):
                    try:
                        data_exec = datetime.datetime.strptime(data_exec, "%Y-%m-%d").date()
                    except:
                        pass
                
                items_formatted.append({
                    "OS": item["o_s"],
                    "Modalidade": item["modalidade"],
                    "Data_execucao": data_exec.strftime('%d/%m/%Y') if hasattr(data_exec, 'strftime') else str(data_exec),
                    "Valor": f"{item['valor_custo_prestador']:.2f}",
                    "Valor_extra": f"{item['valor_extra']:.2f}",
                    "Motivo_valor_extra": item["motivo_extra"] or "-",
                    "Valor_total": f"{item['valor_total']:.2f}"
                })
            
            # Salvar lote no banco
            items_to_log = []
            for item in items:
                log_item = {}
                for k, v in item.items():
                    if isinstance(v, datetime.date):
                        log_item[k] = v.isoformat()
                    elif v is None or (isinstance(v, float) and pd.isna(v)):
                        log_item[k] = None
                    else:
                        log_item[k] = v
                items_to_log.append(log_item)
            
            lote_id = db.criar_lote_servico(prestador_info['id'], nome_prestador, periodo, total_geral, items_to_log)
            
            # Preparar contexto para templates
            context = {
                "nome_prestador": nome_prestador,
                "periodo": periodo,
                "items": items_formatted,
                "total_geral": total_geral,
                "saudacao": saudacao,
                "lote_id": lote_id
            }
            
            # Gerar assunto e corpo do email
            subject = subject_template.render(**context)
            body_plain = body_template.render(**context)
            body_html = convert_plain_text_to_html(body_plain)
            
            # Gerar PDF
            html_pdf = invoice_template.render(**context)
            pdf_bytes = HTML(string=html_pdf, base_url="templates").write_pdf()
            
            # Obter emails do prestador
            prestador_emails = db.get_prestador_emails(prestador_info)
            recipients = [{"emailAddress": {"address": email}} for email in prestador_emails]
            
            # Preparar mensagem para Microsoft Graph
            message_data = {
                "subject": subject,
                "body": {"contentType": "HTML", "content": body_html},
                "toRecipients": recipients,
                "attachments": [{
                    "@odata.type": "#microsoft.graph.fileAttachment",
                    "name": f"Relatorio_{nome_prestador.replace(' ', '_')}_Lote_{lote_id}.pdf",
                    "contentBytes": base64.b64encode(pdf_bytes).decode()
                }]
            }
            
            if cc_list:
                message_data["ccRecipients"] = [{"emailAddress": {"address": cc}} for cc in cc_list]
            
            # Enviar email via Microsoft Graph API
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
            
            payload = {"message": message_data, "saveToSentItems": "true"}
            
            response = requests.post(
                "https://graph.microsoft.com/v1.0/me/sendMail",
                headers=headers,
                json=payload
            )
            
            if response.status_code == 202:
                # Aguardar e obter conversation ID
                time.sleep(2)
                sent_items_url = "https://graph.microsoft.com/v1.0/me/mailfolders/sentitems/messages?$top=1&$select=conversationId"
                sent_resp = requests.get(sent_items_url, headers=headers)
                
                if sent_resp.status_code == 200:
                    sent_data = sent_resp.json()
                    if sent_data.get('value'):
                        conversation_id = sent_data['value'][0]['conversationId']
                        db.atualizar_lote_com_conversation_id(lote_id, conversation_id)
                
                relatorio.append({
                    "prestador": nome_prestador,
                    "periodo": periodo,
                    "lote_id": lote_id,
                    "valor_total": total_geral,
                    "quantidade_os": len(items),
                    "status": f"✅ Lote #{lote_id} enviado com sucesso"
                })
                
                logger.info(f"✅ {nome_prestador} - Lote #{lote_id} enviado")
                
            else:
                error_msg = f"❌ Erro {response.status_code}"
                try:
                    error_detail = response.json()
                    error_msg += f" - {error_detail.get('error', {}).get('message', 'Erro desconhecido')}"
                except:
                    error_msg += f" - {response.text[:100]}"
                
                relatorio.append({
                    "prestador": nome_prestador,
                    "periodo": periodo,
                    "lote_id": lote_id,
                    "status": error_msg
                })
                
                logger.error(f"❌ {nome_prestador} - {error_msg}")
                
        except Exception as e:
            relatorio.append({
                "prestador": nome_prestador,
                "periodo": periodo,
                "status": f"❌ Erro: {str(e)}"
            })
            logger.error(f"❌ Erro ao processar {nome_prestador}: {str(e)}")
    
        return relatorio

# ===== ROTAS DE CONFIGURAÇÃO =====

@prestadores_router.get("/config")
async def obter_configuracoes(user: dict = Depends(get_current_user)):
    """Obter configurações salvas de email"""
    try:
        logger.info(f"� [CONFIG] Início da requisição")
        logger.info(f"🟢 [CONFIG] User autenticado: {user.get('name', 'N/A')}")
        
        logger.info(f"🟢 [CONFIG] Carregando config do arquivo")
        config = load_config_from_file()
        logger.info(f"🟢 [CONFIG] Config carregado: {list(config.keys()) if config else 'None'}")
        
        # Valores padrão
        defaults = {
            "prestador_cc": "projetos.qualidade@novomundo.com.br",
            "prestador_subject": "Novo Mundo Resolve | Nota Fiscal | Período: {{periodo}} | Prestador: {{nome_prestador}}",
            "prestador_body": "Segue a relação de boletins para emissão da nota fiscal de serviços entre **{{periodo}}**.\n\nObrigado."
        }
        
        # Mesclar com defaults
        logger.info(f"🟢 [CONFIG] Mesclando com defaults")
        final_config = {}
        for key, default_value in defaults.items():
            final_config[key] = config.get(key, default_value)
        
        logger.info(f"🟢 [CONFIG] Config final preparado: {list(final_config.keys())}")
        
        response_data = {
            "success": True,
            "data": final_config,
            "variaveis_disponiveis": {
                "prestadores": [
                    "{{nome_prestador}} - Nome do prestador",
                    "{{periodo}} - Período do serviço",
                    "{{saudacao}} - Saudação baseada no horário",
                    "{{lote_id}} - ID do lote gerado"
                ]
            }
        }
        
        logger.info(f"🟢 [CONFIG] Retornando resposta com {len(response_data['data'])} configs")
        return response_data
        
    except Exception as e:
        logger.error(f"❌ Erro ao carregar configurações: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao carregar configurações: {str(e)}"
        )

@prestadores_router.post("/config")
async def salvar_configuracoes(
    config: ConfiguracaoEmail,
    user: dict = Depends(get_current_user)
):
    """Salvar configurações de email"""
    try:
        logger.info(f"👤 {user['name']} salvando configurações de email")
        
        config_data = {
            "prestador_cc": config.prestador_cc,
            "prestador_subject": config.prestador_subject,
            "prestador_body": config.prestador_body
        }
        
        success = save_config_to_file(config_data)
        
        if success:
            logger.info("✅ Configurações salvas com sucesso")
            return {
                "success": True,
                "message": "Configurações salvas com sucesso"
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao salvar configurações"
            )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Erro ao salvar configurações: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao salvar configurações: {str(e)}"
        )

# ===== ROTAS DE TEMPLATES =====

@prestadores_router.get("/template")
async def obter_template_pdf(user: dict = Depends(get_current_user)):
    """Obter conteúdo do template de PDF"""
    try:
        logger.info(f"👤 {user['name']} solicitou template de PDF")
        
        template_path = Path("templates/invoice_template.html")
        
        if not template_path.exists():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Template não encontrado"
            )
        
        content = template_path.read_text(encoding="utf-8")
        
        return {
            "success": True,
            "data": {
                "content": content,
                "path": str(template_path),
                "size": len(content)
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Erro ao carregar template: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao carregar template: {str(e)}"
        )

@prestadores_router.post("/template")
async def salvar_template_pdf(
    template_data: TemplateUpdate,
    user: dict = Depends(get_current_user)
):
    """Salvar template de PDF"""
    try:
        logger.info(f"👤 {user['name']} salvando template de PDF")
        
        template_path = Path("templates/invoice_template.html")
        
        # Backup do template atual
        if template_path.exists():
            backup_path = Path(f"templates/invoice_template_backup_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.html")
            import shutil
            shutil.copy2(template_path, backup_path)
            logger.info(f"📋 Backup criado: {backup_path}")
        
        # Salvar novo template
        template_path.write_text(template_data.content, encoding="utf-8")
        
        logger.info("✅ Template salvo com sucesso")
        
        return {
            "success": True,
            "message": "Template salvo com sucesso",
            "data": {
                "size": len(template_data.content),
                "backup_created": True
            }
        }
        
    except Exception as e:
        logger.error(f"❌ Erro ao salvar template: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao salvar template: {str(e)}"
        )

@prestadores_router.post("/template/preview")
async def preview_template_pdf(
    template_data: TemplateUpdate,
    user: dict = Depends(get_current_user)
):
    """Gerar preview do template de PDF"""
    try:
        logger.info(f"👤 {user['name']} gerando preview do template")
        
        # Dados de exemplo para preview
        context_exemplo = {
            "nome_prestador": "Prestador Exemplo Ltda",
            "periodo": "Janeiro/2024",
            "items": [
                {
                    "OS": "12345",
                    "Modalidade": "Instalação",
                    "Data_execucao": "15/01/2024",
                    "Valor": "150.00",
                    "Valor_extra": "25.00",
                    "Motivo_valor_extra": "Taxa de urgência",
                    "Valor_total": "175.00"
                },
                {
                    "OS": "12346", 
                    "Modalidade": "Manutenção",
                    "Data_execucao": "16/01/2024",
                    "Valor": "200.00",
                    "Valor_extra": "0.00",
                    "Motivo_valor_extra": "-",
                    "Valor_total": "200.00"
                }
            ],
            "total_geral": 375.00,
            "saudacao": "Bom dia",
            "lote_id": 999
        }
        
        # Renderizar template
        template = Template(template_data.content)
        html_rendered = template.render(**context_exemplo)
        
        return {
            "success": True,
            "data": {
                "html_preview": html_rendered,
                "context_exemplo": context_exemplo
            },
            "message": "Preview gerado com sucesso"
        }
        
    except Exception as e:
        logger.error(f"❌ Erro ao gerar preview: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao gerar preview: {str(e)}"
        )

# ===== ROTAS AUXILIARES =====

@prestadores_router.get("/regras-envio")
async def obter_regras_envio(user: dict = Depends(get_current_user)):
    """Obter opções de regras de envio disponíveis"""
    try:
        return {
            "success": True,
            "data": {
                "regras": ["Nenhuma", "Semanal", "Mensal (Dia Fixo)", "Quinzenal"],
                "dias_semana": list(DIAS_SEMANA_MAP.values()),
                "status_lotes": STATUS_OPTIONS
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao carregar regras: {str(e)}"
        )

@prestadores_router.post("/validar-os")
async def validar_os_numeros(
    dados: Dict[str, List[str]],
    user: dict = Depends(get_current_user)
):
    """Validar lista de números de O.S."""
    try:
        os_numbers = dados.get('os_numbers', [])
        
        if not os_numbers:
            return {
                "success": True,
                "data": {
                    "total": 0,
                    "validas": [],
                    "ja_enviadas": [],
                    "na_blacklist": [],
                    "duplicadas": []
                }
            }
        
        # Verificar duplicatas na própria lista
        seen = set()
        duplicadas = []
        for os_num in os_numbers:
            if os_num in seen:
                duplicadas.append(os_num)
            seen.add(os_num)
        
        # Verificar O.S. já enviadas
        ja_enviadas = db.check_os_list(os_numbers)
        
        # Verificar blacklist
        na_blacklist = db.check_os_blacklist(os_numbers)
        
        # O.S. válidas
        validas = [
            os_num for os_num in os_numbers 
            if os_num not in ja_enviadas and os_num not in na_blacklist
        ]
        
        return {
            "success": True,
            "data": {
                "total": len(os_numbers),
                "validas": validas,
                "ja_enviadas": ja_enviadas,
                "na_blacklist": na_blacklist,
                "duplicadas": list(set(duplicadas)),
                "resumo": {
                    "total_validas": len(validas),
                    "total_ja_enviadas": len(ja_enviadas),
                    "total_blacklist": len(na_blacklist),
                    "total_duplicadas": len(set(duplicadas))
                }
            }
        }
        
    except Exception as e:
        logger.error(f"❌ Erro na validação de O.S.: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro na validação: {str(e)}"
        )@prestadores_router.post("/upload-excel")
async def upload_excel_prestadores(
    file: UploadFile = File(...), 
    user: dict = Depends(get_current_user)
):
    """Upload e processamento de Excel de prestadores - Exatamente como no Streamlit"""
    try:
        logger.info(f"👤 {user['name']} fazendo upload de Excel: {file.filename}")
        
        # Validar tipo de arquivo
        if not file.filename.endswith(('.xlsx', '.xls')):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Arquivo deve ser Excel (.xlsx ou .xls)"
            )
        
        # Ler arquivo Excel
        content = await file.read()
        df = pd.read_excel(io.BytesIO(content))
        
        logger.info(f"📊 Excel carregado: {len(df)} linhas, {len(df.columns)} colunas")
        
        # Normalizar nomes das colunas (exatamente como no streamlit)
        df = normalize_column_names(df)
        logger.info(f"📋 Colunas normalizadas: {list(df.columns)}")
        
        # Verificar colunas obrigatórias
        required_cols = ['nome_prestador', 'periodo', 'data_execucao', 'o_s']
        missing_cols = validate_excel_columns(df, required_cols)
        
        if missing_cols:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Excel precisa das colunas: {', '.join(required_cols)}. Faltando: {', '.join(missing_cols)}"
            )
        
        # Processar e limpar dados
        for col in ["valor_custo_prestador", "valor_extra", "valor_total"]:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)
        
        # Calcular valor total se não existir
        if 'valor_total' not in df.columns:
            df['valor_total'] = df.get('valor_custo_prestador', 0) + df.get('valor_extra', 0)
        
        # Adicionar campos padrão se não existirem
        if 'modalidade' not in df.columns:
            df['modalidade'] = 'Serviço'
        if 'valor_extra' not in df.columns:
            df['valor_extra'] = 0
        if 'motivo_extra' not in df.columns:
            df['motivo_extra'] = ''
        
        # Converter para lista de dicionários
        data = df.to_dict('records')
        
        # Limpar dados None/NaN
        for record in data:
            for key, value in record.items():
                if pd.isna(value):
                    record[key] = None if key in ['motivo_extra'] else (0 if 'valor' in key else '')
        
        # Verificar O.S. já enviadas e na blacklist
        os_numbers = [str(record['o_s']) for record in data if record.get('o_s')]
        sent_os = db.check_os_list(os_numbers)
        blacklisted_os = db.check_os_blacklist(os_numbers)
        
        # Adicionar status a cada registro
        for record in data:
            os_numero = str(record.get('o_s', ''))
            if os_numero in blacklisted_os:
                record['status_envio'] = 'Na blacklist'
            elif os_numero in sent_os:
                record['status_envio'] = 'Já enviado'
            else:
                record['status_envio'] = 'Pendente'
        
        # Contar por status
        total_registros = len(data)
        pendentes = sum(1 for r in data if r.get('status_envio') == 'Pendente')
        ja_enviados = sum(1 for r in data if r.get('status_envio') == 'Já enviado')
        blacklist = sum(1 for r in data if r.get('status_envio') == 'Na blacklist')
        
        logger.info(f"📊 Processamento: {pendentes} pendentes, {ja_enviados} já enviados, {blacklist} na blacklist")
        
        return {
            "success": True,
            "message": f"Excel processado com sucesso: {total_registros} registros, {pendentes} pendentes para envio",
            "data": {
                "registros": data,
                "resumo": {
                    "total_registros": total_registros,
                    "pendentes": pendentes,
                    "ja_enviados": ja_enviados,
                    "na_blacklist": blacklist,
                    "colunas_encontradas": list(df.columns),
                    "sent_os": sent_os,
                    "blacklisted_os": blacklisted_os
                }
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Erro ao processar Excel: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao processar Excel: {str(e)}"
        )

# ===== ROTAS DE HISTÓRICO =====

@prestadores_router.get("/historico")
async def obter_historico(
    status_filter: Optional[str] = None,
    user: dict = Depends(get_current_user)
):
    """Obter histórico completo de lotes enviados com filtros"""
    try:
        logger.info(f"👤 {user['name']} solicitou histórico de lotes (filtro: {status_filter})")
        
        lotes = db.get_all_lotes_servico()
        
        # Aplicar filtro de status se especificado
        if status_filter and status_filter != "Todos":
            lotes = [lote for lote in lotes if lote.get('status') == status_filter]
        
        # Enriquecer dados dos lotes
        lotes_enriquecidos = []
        for lote in lotes:
            lote_dict = dict(lote)
            
            # Buscar O.S. do lote
            os_list = db.get_os_by_lote_id(lote['id'])
            lote_dict['os_detalhes'] = [dict(os_item) for os_item in os_list]
            lote_dict['quantidade_os'] = len(os_list)
            
            # Formatar data
            if lote_dict.get('data_envio'):
                lote_dict['data_envio_formatada'] = lote_dict['data_envio'].strftime('%d/%m/%Y %H:%M')
            
            # Status de anexo
            lote_dict['tem_anexo'] = bool(lote_dict.get('anexo_path'))
            
            lotes_enriquecidos.append(lote_dict)
        
        logger.info(f"📋 Retornados {len(lotes_enriquecidos)} lotes")
        
        return {
            "success": True,
            "data": {
                "lotes": lotes_enriquecidos,
                "total": len(lotes_enriquecidos),
                "status_options": STATUS_OPTIONS
            }
        }
        
    except Exception as e:
        logger.error(f"❌ Erro ao carregar histórico: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao carregar histórico: {str(e)}"
        )

@prestadores_router.get("/historico/{lote_id}/os")
async def obter_os_do_lote(lote_id: int, user: dict = Depends(get_current_user)):
    """Obter todas as O.S. de um lote específico"""
    try:
        logger.info(f"👤 {user['name']} solicitou O.S. do lote {lote_id}")
        
        os_list = db.get_os_by_lote_id(lote_id)
        
        if not os_list:
            return {
                "success": True,
                "data": [],
                "message": "Nenhuma O.S. encontrada para este lote"
            }
        
        # Extrair detalhes das O.S.
        os_detalhadas = []
        for os_item in os_list:
            detalhes = os_item.get('detalhes', {})
            if isinstance(detalhes, str):
                import json
                try:
                    detalhes = json.loads(detalhes)
                except:
                    detalhes = {}
            
            os_detalhadas.append({
                "id": os_item['id'],
                "os_numero": os_item['os_numero'],
                "detalhes": detalhes
            })
        
        return {
            "success": True,
            "data": os_detalhadas
        }
        
    except Exception as e:
        logger.error(f"❌ Erro ao buscar O.S. do lote {lote_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar O.S. do lote: {str(e)}"
        )

@prestadores_router.put("/historico/{lote_id}/status")
async def atualizar_status_lote(
    lote_id: int, 
    status_update: LoteStatusUpdate,
    user: dict = Depends(get_current_user)
):
    """Atualizar status de um lote"""
    try:
        logger.info(f"👤 {user['name']} atualizando status do lote {lote_id} para: {status_update.status}")
        
        if status_update.status not in STATUS_OPTIONS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Status inválido. Opções: {', '.join(STATUS_OPTIONS)}"
            )
        
        db.update_lote_servico_status(lote_id, status_update.status)
        
        logger.info(f"✅ Status do lote {lote_id} atualizado para: {status_update.status}")
        
        return {
            "success": True,
            "message": f"Status do Lote #{lote_id} atualizado para '{status_update.status}'"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Erro ao atualizar status do lote {lote_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao atualizar status: {str(e)}"
        )

@prestadores_router.post("/historico/{lote_id}/anexo")
async def upload_anexo_lote(
    lote_id: int,
    file: UploadFile = File(...),
    user: dict = Depends(get_current_user)
):
    """Upload de anexo (N.F.) para um lote"""
    try:
        logger.info(f"👤 {user['name']} fazendo upload de anexo para lote {lote_id}: {file.filename}")
        
        # Validar tipo de arquivo
        allowed_extensions = ['.pdf', '.jpg', '.jpeg', '.png', '.doc', '.docx']
        file_extension = Path(file.filename).suffix.lower()
        
        if file_extension not in allowed_extensions:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Tipo de arquivo não permitido. Permitidos: {', '.join(allowed_extensions)}"
            )
        
        # Criar diretório de anexos se não existir
        anexos_dir = Path("anexos/lotes")
        anexos_dir.mkdir(parents=True, exist_ok=True)
        
        # Gerar nome único para o arquivo
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        nome_arquivo = f"lote_{lote_id}_{timestamp}{file_extension}"
        caminho_arquivo = anexos_dir / nome_arquivo
        
        # Salvar arquivo
        content = await file.read()
        with open(caminho_arquivo, "wb") as f:
            f.write(content)
        
        # Atualizar banco de dados
        db.update_lote_servico_attachment(lote_id, str(caminho_arquivo))
        
        logger.info(f"✅ Anexo salvo: {caminho_arquivo}")
        
        return {
            "success": True,
            "message": "Anexo carregado com sucesso",
            "data": {
                "filename": nome_arquivo,
                "path": str(caminho_arquivo),
                "size": len(content)
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Erro no upload do anexo para lote {lote_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro no upload do anexo: {str(e)}"
        )

@prestadores_router.get("/historico/{lote_id}/anexo")
async def download_anexo_lote(lote_id: int, user: dict = Depends(get_current_user)):
    """Download do anexo de um lote"""
    try:
        logger.info(f"👤 {user['name']} solicitou download do anexo do lote {lote_id}")
        
        # Buscar informações do lote 
        lotes = db.get_all_lotes_servico()
        lote = next((l for l in lotes if l['id'] == lote_id), None)
        
        if not lote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Lote não encontrado"
            )
        
        if not lote.get('anexo_path'):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Nenhum anexo encontrado para este lote"
            )
        
        arquivo_path = Path(lote['anexo_path'])
        
        if not arquivo_path.exists():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Arquivo do anexo não encontrado no sistema"
            )
        
        # Retornar informações do arquivo para download no frontend
        return {
            "success": True,
            "data": {
                "filename": arquivo_path.name,
                "path": str(arquivo_path),
                "exists": True
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Erro no download do anexo do lote {lote_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro no download do anexo: {str(e)}"
        )

@prestadores_router.delete("/historico/{lote_id}")
async def deletar_lote(lote_id: int, user: dict = Depends(get_current_user)):
    """Deletar lote de serviço e todas as suas O.S."""
    try:
        logger.info(f"👤 {user['name']} deletando lote {lote_id}")
        
        # Verificar se o lote existe
        lotes = db.get_all_lotes_servico()
        lote = next((l for l in lotes if l['id'] == lote_id), None)
        
        if not lote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Lote não encontrado"
            )
        
        # Deletar anexo se existir
        if lote.get('anexo_path'):
            try:
                arquivo_path = Path(lote['anexo_path'])
                if arquivo_path.exists():
                    arquivo_path.unlink()
                    logger.info(f"🗑️ Anexo deletado: {arquivo_path}")
            except Exception as e:
                logger.warning(f"⚠️ Erro ao deletar anexo: {str(e)}")
        
        # Deletar lote (cascata deleta as O.S. automaticamente)
        db.delete_lote_servico(lote_id)
        
        logger.info(f"✅ Lote #{lote_id} deletado com sucesso")
        
        return {
            "success": True,
            "message": f"Lote #{lote_id} e todas as suas O.S. foram excluídos com sucesso"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Erro ao deletar lote {lote_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao remover lote: {str(e)}"
        )

# ===== ROTAS DE BLACKLIST =====

@prestadores_router.get("/blacklist-test-simples")
async def test_endpoint():
    """Endpoint de teste super simples"""
    return {"success": True, "message": "Funcionou!", "data": []}

@prestadores_router.get("/blacklist")
async def obter_blacklist_fixed(user: dict = Depends(get_current_user)):
    """Obter lista completa da blacklist de O.S."""
    try:
        logger.info(f"� [BLACKLIST] Início da requisição")
        logger.info(f"🔵 [BLACKLIST] User autenticado: {user.get('name', 'N/A')} (ID: {user.get('oid', 'N/A')})")
        
        logger.info(f"🔵 [BLACKLIST] Chamando db.get_os_blacklist(None)")
        blacklist = db.get_os_blacklist(None)
        logger.info(f"� [BLACKLIST] Retorno do DB: {len(blacklist) if blacklist else 0} itens")
        logger.info(f"🔵 [BLACKLIST] Tipo do retorno: {type(blacklist)}")
        
        # Enriquecer dados
        logger.info(f"🔵 [BLACKLIST] Iniciando enriquecimento dos dados")
        blacklist_enriquecida = []
        for idx, item in enumerate(blacklist):
            try:
                item_dict = dict(item)
                logger.debug(f"🔵 [BLACKLIST] Item {idx}: {item_dict.keys()}")
                
                # Formatar data de adição
                if item_dict.get('data_adicao'):
                    item_dict['data_adicao_formatada'] = item_dict['data_adicao'].strftime('%d/%m/%Y %H:%M')
                
                blacklist_enriquecida.append(item_dict)
            except Exception as item_error:
                logger.error(f"🔴 [BLACKLIST] Erro ao processar item {idx}: {str(item_error)}")
        
        logger.info(f"🔵 [BLACKLIST] Enriquecimento concluído: {len(blacklist_enriquecida)} itens processados")
        
        response_data = {
            "success": True,
            "data": blacklist_enriquecida,
            "total": len(blacklist_enriquecida)
        }
        logger.info(f"🔵 [BLACKLIST] Retornando resposta: success={response_data['success']}, total={response_data['total']}")
        
        return response_data
        
    except Exception as e:
        import traceback
        logger.error(f"🔴 [BLACKLIST] ❌ ERRO CRÍTICO!")
        logger.error(f"🔴 [BLACKLIST] Tipo do erro: {type(e).__name__}")
        logger.error(f"🔴 [BLACKLIST] Mensagem: {str(e)}")
        logger.error(f"🔴 [BLACKLIST] Traceback completo:\n{traceback.format_exc()}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao carregar blacklist: {str(e)}"
        )


@prestadores_router.post("/blacklist")
async def adicionar_blacklist(item: BlacklistOS, user: dict = Depends(get_current_user)):
    """Adicionar O.S. à blacklist"""
    try:
        logger.info(f"👤 {user['name']} adicionando O.S. {item.os_numero} à blacklist (prestador: {item.prestador_id})")
        
        # Validar se o prestador existe
        prestadores = db.get_all_prestadores()
        prestador = next((p for p in prestadores if p['id'] == item.prestador_id), None)
        
        if not prestador:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Prestador não encontrado"
            )
        
        success, message = db.adicionar_os_blacklist(
            item.prestador_id,
            item.os_numero,
            item.motivo
        )
        
        if success:
            logger.info(f"✅ O.S. {item.os_numero} adicionada à blacklist")
            return {"success": True, "message": message}
        else:
            logger.warning(f"⚠️ Falha ao adicionar O.S. {item.os_numero} à blacklist: {message}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=message
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Erro ao adicionar à blacklist: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao adicionar à blacklist: {str(e)}"
        )

@prestadores_router.post("/blacklist/batch")
async def adicionar_blacklist_lote(
    dados: Dict[str, Any],
    user: dict = Depends(get_current_user)
):
    """Adicionar múltiplas O.S. à blacklist de uma vez"""
    try:
        prestador_id = dados.get('prestador_id')
        os_numbers = dados.get('os_numbers', [])
        motivo = dados.get('motivo', '')
        
        logger.info(f"👤 {user['name']} adicionando {len(os_numbers)} O.S. à blacklist (prestador: {prestador_id})")
        
        if not prestador_id or not os_numbers:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Prestador ID e lista de O.S. são obrigatórios"
            )
        
        # Validar se o prestador existe
        prestadores = db.get_all_prestadores()
        prestador = next((p for p in prestadores if p['id'] == prestador_id), None)
        
        if not prestador:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Prestador não encontrado"
            )
        
        # Processar cada O.S.
        resultados = []
        sucessos = 0
        falhas = 0
        
        for os_numero in os_numbers:
            os_numero = str(os_numero).strip()
            if not os_numero:
                continue
                
            success, message = db.adicionar_os_blacklist(prestador_id, os_numero, motivo)
            
            resultado = {
                "os_numero": os_numero,
                "success": success,
                "message": message
            }
            resultados.append(resultado)
            
            if success:
                sucessos += 1
            else:
                falhas += 1
        
        logger.info(f"📊 Resultado batch blacklist: {sucessos} sucessos, {falhas} falhas")
        
        return {
            "success": True,
            "message": f"Processamento concluído: {sucessos} adicionadas, {falhas} falhas",
            "data": {
                "resultados": resultados,
                "total_processadas": len(resultados),
                "sucessos": sucessos,
                "falhas": falhas
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Erro no batch de blacklist: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao processar lote de blacklist: {str(e)}"
        )

@prestadores_router.delete("/blacklist/{prestador_id}/{os_numero}")
async def remover_blacklist(
    prestador_id: int, 
    os_numero: str, 
    user: dict = Depends(get_current_user)
):
    """Remover O.S. da blacklist"""
    try:
        logger.info(f"👤 {user['name']} removendo O.S. {os_numero} da blacklist (prestador: {prestador_id})")
        
        # Verificar se existe na blacklist
        blacklist = db.get_os_blacklist(prestador_id)
        item_exists = any(item['os_numero'] == os_numero for item in blacklist)
        
        if not item_exists:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="O.S. não encontrada na blacklist"
            )
        
        db.remover_os_blacklist(prestador_id, os_numero)
        
        logger.info(f"✅ O.S. {os_numero} removida da blacklist")
        
        return {
            "success": True,
            "message": f"O.S. {os_numero} removida da blacklist com sucesso"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Erro ao remover da blacklist: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao remover da blacklist: {str(e)}"
        )

@prestadores_router.get("/blacklist/check")
async def verificar_os_blacklist(
    os_numbers: str,  # Números separados por vírgula
    user: dict = Depends(get_current_user)
):
    """Verificar quais O.S. estão na blacklist"""
    try:
        # Converter string para lista
        os_list = [os.strip() for os in os_numbers.split(',') if os.strip()]
        
        if not os_list:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Lista de O.S. não pode estar vazia"
            )
        
        logger.info(f"👤 {user['name']} verificando {len(os_list)} O.S. na blacklist")
        
        # Verificar blacklist
        blacklisted = db.check_os_blacklist(os_list)
        
        # Preparar resposta
        resultado = []
        for os_numero in os_list:
            resultado.append({
                "os_numero": os_numero,
                "na_blacklist": os_numero in blacklisted
            })
        
        total_blacklist = len(blacklisted) 
        
        return {
            "success": True,
            "data": {
                "verificacao": resultado,
                "total_verificadas": len(os_list),
                "total_na_blacklist": total_blacklist,
                "blacklisted_os": blacklisted
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Erro ao verificar blacklist: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao verificar blacklist: {str(e)}"
        )

# ===== ROTAS GENÉRICAS (DEVEM FICAR POR ÚLTIMO) =====
# Estas rotas usam path parameters dinâmicos e devem vir depois de todas as rotas específicas

@prestadores_router.get("/{prestador_id}", response_model=PrestadorResponse)
async def obter_prestador(prestador_id: int, user: dict = Depends(get_current_user)):
    """Obter dados de um prestador específico por ID"""
    try:
        logger.info(f"👤 {user['name']} solicitou dados do prestador {prestador_id}")
        
        prestadores = db.get_all_prestadores()
        prestador = next((p for p in prestadores if p['id'] == prestador_id), None)
        
        if not prestador:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Prestador não encontrado"
            )
        
        result = PrestadorResponse(
            id=prestador['id'],
            nome=prestador['nome'],
            email=prestador['email'],
            emails_adicionais=prestador.get('emails_adicionais'),
            fornecedor_id=prestador['fornecedor_id'],
            regra_envio=prestador.get('regra_envio', 'Nenhuma'),
            dias_envio=prestador.get('dias_envio')
        )
        
        logger.info(f"✅ Dados do prestador {prestador_id} retornados")
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Erro ao buscar prestador {prestador_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar prestador: {str(e)}"
        )
