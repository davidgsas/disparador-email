"""
Cliente para API DV Processamento
Envia dados de lotes de serviço para geração de links de upload de NF
"""

import requests
import json
from datetime import datetime
from dotenv import load_dotenv
import os
import urllib3

# Suprimir avisos de SSL enquanto certificado não está ativo
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

load_dotenv()

# Configurações da API
# NOTA: Certificado SSL ainda não está ativo, usando HTTP temporariamente
API_URL = "http://api.link.dev.br/dvprocessamento/"  # HTTP (sem SSL por enquanto)
API_KEY = "DV_API_2025_CTRL_NOTAS_f8e9d2c1b4a6"

# Quando certificado SSL estiver ativo, alterar para:
# API_URL = "https://api.link.dev.br/dvprocessamento/"

class APIUploadClient:
    """Cliente para comunicação com a API de upload de notas fiscais"""
    
    def __init__(self, api_url=None, api_key=None, verify_ssl=False):
        """
        Inicializa o cliente da API
        
        Args:
            api_url: URL do endpoint (opcional, usa padrão se não fornecido)
            api_key: Chave de autenticação (opcional, usa padrão se não fornecido)
            verify_ssl: Se deve verificar certificado SSL (False por padrão até certificado estar ativo)
        """
        self.api_url = api_url or API_URL
        self.api_key = api_key or API_KEY
        self.verify_ssl = verify_ssl
        
    def preparar_payload(self, lote):
        """
        Prepara o payload JSON para envio à API
        
        Mapeamento:
        - NOME_EMPRESA (prestador_nome) -> nome
        - EMAIL_CONTATO (usar email do prestador) -> email
        - PERIODO_REF (periodo) -> periodo (formato MM/YYYY)
        - VALOR_TOTAL (valor_total) -> valor_total
        - QTD_OS (contar OS) -> quantidade_os
        - DATA_ENVIO (data_envio) -> data_envio (ISO format)
        - LOTE_ID (id) -> lote_id
        
        Args:
            lote: Dicionário com dados do lote do banco local
            
        Returns:
            dict: Payload formatado para a API
        """
        # Importar aqui para evitar import circular
        from database import get_os_by_lote_id, get_prestador_by_name
        
        # Obter informações do prestador para pegar o email
        prestador = get_prestador_by_name(lote['prestador_nome'])
        email_contato = prestador['email'] if prestador else "sem-email@novomundo.com.br"
        
        # Contar quantidade de OS deste lote
        os_list = get_os_by_lote_id(lote['id'])
        quantidade_os = len(os_list)
        
        # Formatar data_envio para ISO 8601 (YYYY-MM-DDTHH:MM:SS)
        print(f"📅 Data envio original: '{lote['data_envio']}' (tipo: {type(lote['data_envio'])})")
        
        try:
            if isinstance(lote['data_envio'], str):
                # Tentar parsear a string para datetime
                data_obj = datetime.fromisoformat(lote['data_envio'].replace('Z', '+00:00'))
            else:
                data_obj = lote['data_envio']
            
            # Formatar para ISO sem microsegundos e sem timezone
            data_envio_iso = data_obj.strftime("%Y-%m-%dT%H:%M:%S")
        except Exception as e:
            print(f"⚠️ Erro ao processar data_envio: {e}")
            # Usar data/hora atual como fallback
            data_envio_iso = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
            print(f"⚠️ Usando data atual como fallback: {data_envio_iso}")
        
        print(f"📅 Data envio formatada: '{data_envio_iso}'")
        
        # Normalizar período para formato MM/AAAA (ano com 4 dígitos)
        periodo_original = lote['periodo']
        print(f"📅 Período original: '{periodo_original}' (tipo: {type(periodo_original)})")
        
        # Extrair mês/ano do período (pode estar como "DD/MM/YYYY - DD/MM/YYYY" ou "MM/YYYY")
        periodo_str = str(periodo_original).strip()
        
        # Se contém " - " ou " – ", é um intervalo de datas, pegar a primeira data
        if ' - ' in periodo_str or ' – ' in periodo_str:
            periodo_str = periodo_str.split(' - ')[0].split(' – ')[0].strip()
        
        # Tentar extrair mês e ano
        try:
            # Se está no formato DD/MM/YYYY, extrair MM/YYYY
            if '/' in periodo_str:
                partes = periodo_str.split('/')
                if len(partes) == 3:  # DD/MM/YYYY
                    mes = partes[1].strip().zfill(2)
                    ano = partes[2].strip()
                elif len(partes) == 2:  # MM/YYYY ou MM/YY
                    mes = partes[0].strip().zfill(2)
                    ano = partes[1].strip()
                    # Se ano tem 2 dígitos, converter para 4
                    if len(ano) == 2:
                        ano = '20' + ano
                else:
                    raise ValueError(f"Formato de período não reconhecido: {periodo_original}")
                
                periodo = f"{mes}/{ano}"
            else:
                # Se não tem barra, não é um formato de data válido
                raise ValueError(f"Período não contém data válida: {periodo_original}")
        except Exception as e:
            print(f"⚠️ Erro ao processar período: {e}")
            # Usar data atual como fallback
            agora = datetime.now()
            periodo = agora.strftime("%m/%Y")
            print(f"⚠️ Usando período atual como fallback: {periodo}")
        
        print(f"📅 Período formatado: '{periodo}'")
        
        payload = {
            "nome": lote['prestador_nome'],
            "email": email_contato,
            "periodo": periodo,  # Formato MM/AAAA garantido
            "valor_total": float(lote['valor_total']),
            "quantidade_os": quantidade_os,
            "data_envio": data_envio_iso,
            "lote_id": lote['id']
        }
        
        return payload
    
    def enviar_lote(self, lote):
        """
        Envia um lote para a API e retorna a resposta
        
        Args:
            lote: Dicionário com dados do lote
            
        Returns:
            tuple: (sucesso: bool, resposta: dict, erro: str)
        """
        try:
            # Preparar payload
            payload = self.preparar_payload(lote)
            
            # Configurar headers com User-Agent para evitar bloqueio do Mod_Security
            headers = {
                "Content-Type": "application/json; charset=utf-8",
                "Accept": "application/json",
                "User-Agent": "NovoMundo-DisparadorEmail/1.0",
                "X-API-Key": self.api_key
            }
            
            # Fazer requisição POST
            # verify=False porque certificado SSL ainda não está ativo
            response = requests.post(
                self.api_url,
                json=payload,
                headers=headers,
                timeout=30,
                verify=self.verify_ssl  # False por padrão até certificado estar ativo
            )
            
            # Verificar status code
            # 200 OK ou 201 Created são sucessos
            if response.status_code in [200, 201]:
                resposta_json = response.json()
                
                # Verificar se o campo success existe e é True
                if resposta_json.get('success'):
                    print(f"✅ API retornou sucesso (HTTP {response.status_code})")
                    print(f"📦 Resposta: {resposta_json}")
                    return True, resposta_json, None
                else:
                    erro_msg = resposta_json.get('message', 'Erro desconhecido')
                    return False, resposta_json, f"API retornou erro: {erro_msg}"
            
            elif response.status_code == 409:
                # Conflito - lote duplicado
                return False, None, "Lote já foi enviado anteriormente (duplicado)"
            
            else:
                return False, None, f"Erro HTTP {response.status_code}: {response.text}"
        
        except requests.exceptions.Timeout:
            return False, None, "Timeout ao conectar com a API"
        
        except requests.exceptions.ConnectionError:
            return False, None, "Erro de conexão com a API"
        
        except json.JSONDecodeError:
            return False, None, "Resposta da API não é um JSON válido"
        
        except Exception as e:
            return False, None, f"Erro inesperado: {str(e)}"
    
    def processar_resposta(self, resposta):
        """
        Processa a resposta da API e extrai os campos relevantes
        
        Resposta esperada:
        {
          "success": true,
          "id_controle": 1,
          "lote_id": 99999,
          "link": "https://api.link.com.br/dvprocessamento/envio-nf/...",
          "hash": "03de0449e11849318f7d67e08377f150",
          "validade_link": "2025-11-12",
          "status": 0,
          "message": "Registro criado com sucesso"
        }
        
        Args:
            resposta: Dicionário com a resposta da API
            
        Returns:
            dict: Campos extraídos e formatados
        """
        return {
            'id_controle': resposta.get('id_controle'),
            'link': resposta.get('link'),
            'hash': resposta.get('hash'),
            'validade_link': resposta.get('validade_link'),
            'status': resposta.get('status', 0),
            'message': resposta.get('message', '')
        }
    
    def enviar_e_salvar(self, lote_id):
        """
        Envia um lote para a API e salva a resposta no banco
        
        Args:
            lote_id: ID do lote a ser enviado
            
        Returns:
            tuple: (sucesso: bool, mensagem: str, dados: dict)
        """
        from database import get_db_connection, salvar_resposta_api, verificar_lote_duplicado
        import psycopg2.extras
        
        # Buscar dados do lote
        conn = get_db_connection()
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute('SELECT * FROM lotes_servico WHERE id = %s', (lote_id,))
            lote = cur.fetchone()
        conn.close()
        
        if not lote:
            return False, "Lote não encontrado", None
        
        # Verificar se já foi enviado
        if verificar_lote_duplicado(lote['id'], lote['periodo']):
            return False, "Este lote já foi enviado para a API anteriormente", None
        
        # Enviar para API
        sucesso, resposta, erro = self.enviar_lote(lote)
        
        if not sucesso:
            return False, erro or "Erro ao enviar para API", None
        
        # Processar resposta
        dados = self.processar_resposta(resposta)
        
        # Salvar no banco
        salvar_resposta_api(
            lote_id=lote['id'],
            id_controle=dados['id_controle'],
            link=dados['link'],
            validade_link=dados['validade_link'],
            status_api=dados['status'],
            message=dados['message'],
            upload_hash=dados.get('hash')
        )
        
        return True, dados['message'], dados


def enviar_lote_para_api(lote_id, api_url=None, api_key=None):
    """
    Função auxiliar para enviar um lote específico
    
    Args:
        lote_id: ID do lote
        api_url: URL da API (opcional)
        api_key: Chave da API (opcional)
        
    Returns:
        tuple: (sucesso: bool, mensagem: str, dados: dict)
    """
    client = APIUploadClient(api_url, api_key)
    return client.enviar_e_salvar(lote_id)


def enviar_lotes_pendentes():
    """
    Envia todos os lotes que ainda não foram enviados para a API
    
    Returns:
        dict: Estatísticas do processamento
    """
    from database import get_lotes_para_enviar_api
    
    lotes = get_lotes_para_enviar_api()
    
    stats = {
        'total': len(lotes),
        'sucesso': 0,
        'erro': 0,
        'detalhes': []
    }
    
    client = APIUploadClient()
    
    for lote in lotes:
        sucesso, mensagem, dados = client.enviar_e_salvar(lote['id'])
        
        if sucesso:
            stats['sucesso'] += 1
            stats['detalhes'].append({
                'lote_id': lote['id'],
                'status': 'sucesso',
                'mensagem': mensagem,
                'link': dados.get('link') if dados else None
            })
        else:
            stats['erro'] += 1
            stats['detalhes'].append({
                'lote_id': lote['id'],
                'status': 'erro',
                'mensagem': mensagem
            })
    
    return stats


if __name__ == "__main__":
    # Teste da API
    print("🔍 Buscando lotes pendentes...")
    stats = enviar_lotes_pendentes()
    
    print(f"\n📊 Resultado:")
    print(f"   Total: {stats['total']}")
    print(f"   ✅ Sucesso: {stats['sucesso']}")
    print(f"   ❌ Erro: {stats['erro']}")
    
    if stats['detalhes']:
        print(f"\n📝 Detalhes:")
        for det in stats['detalhes']:
            emoji = "✅" if det['status'] == 'sucesso' else "❌"
            print(f"   {emoji} Lote {det['lote_id']}: {det['mensagem']}")
            if det.get('link'):
                print(f"      🔗 Link: {det['link']}")
