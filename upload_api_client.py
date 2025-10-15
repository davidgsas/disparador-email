"""
Módulo de integração com API de Upload de Notas Fiscais
Gerencia criação de links, consulta de status e download de arquivos
"""

import requests
import json
import os
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class UploadAPIClient:
    """Cliente para API de Upload de Notas Fiscais"""
    
    def __init__(self):
        self.base_url = os.getenv("UPLOAD_API_URL", "https://api-upload.exemplo.com")
        self.api_key = os.getenv("UPLOAD_API_KEY", "")
        self.timeout = 30
        
    def _get_headers(self):
        """Retorna headers padrão para requisições"""
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
    
    def criar_link_upload(self, lote_id, prestador_info, lote_info):
        """
        Cria um link único para upload de nota fiscal
        
        Args:
            lote_id (int): ID do lote de serviço
            prestador_info (dict): Informações do prestador
            lote_info (dict): Informações do lote
            
        Returns:
            tuple: (success, data_or_error)
        """
        try:
            payload = {
                "lote_id": lote_id,
                "prestador": {
                    "id": prestador_info.get('id'),
                    "nome": prestador_info.get('nome'),
                    "email": prestador_info.get('email')
                },
                "lote_info": {
                    "periodo": lote_info.get('periodo'),
                    "valor_total": float(lote_info.get('valor_total', 0)),
                    "quantidade_os": lote_info.get('quantidade_os', 0),
                    "data_envio": lote_info.get('data_envio', datetime.now().isoformat())
                },
                "metadata": {
                    "sistema": "disparador-email",
                    "versao": "1.0",
                    "empresa": "Novo Mundo"
                }
            }
            
            response = requests.post(
                f"{self.base_url}/api/upload/create",
                headers=self._get_headers(),
                json=payload,
                timeout=self.timeout
            )
            
            if response.status_code == 201:
                data = response.json()
                if data.get('success'):
                    return True, data.get('data')
                else:
                    return False, data.get('error', {}).get('message', 'Erro desconhecido')
            else:
                return False, f"Erro HTTP {response.status_code}: {response.text}"
                
        except requests.exceptions.RequestException as e:
            return False, f"Erro de conexão: {str(e)}"
        except Exception as e:
            return False, f"Erro: {str(e)}"
    
    def consultar_status(self, token):
        """
        Consulta o status do upload
        
        Args:
            token (str): Token único do upload
            
        Returns:
            tuple: (success, data_or_error)
        """
        try:
            response = requests.get(
                f"{self.base_url}/api/upload/status/{token}",
                headers=self._get_headers(),
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    return True, data.get('data')
                else:
                    return False, data.get('error', {}).get('message', 'Erro desconhecido')
            else:
                return False, f"Erro HTTP {response.status_code}"
                
        except requests.exceptions.RequestException as e:
            return False, f"Erro de conexão: {str(e)}"
        except Exception as e:
            return False, f"Erro: {str(e)}"
    
    def download_arquivo(self, token, save_path):
        """
        Faz download do arquivo enviado
        
        Args:
            token (str): Token único do upload
            save_path (str): Caminho onde salvar o arquivo
            
        Returns:
            tuple: (success, message_or_error)
        """
        try:
            response = requests.get(
                f"{self.base_url}/api/upload/download/{token}",
                headers=self._get_headers(),
                timeout=self.timeout,
                stream=True
            )
            
            if response.status_code == 200:
                # Criar diretório se não existir
                Path(save_path).parent.mkdir(parents=True, exist_ok=True)
                
                # Salvar arquivo
                with open(save_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                
                file_size = Path(save_path).stat().st_size
                return True, f"Arquivo baixado com sucesso ({file_size} bytes)"
            
            elif response.status_code == 404:
                return False, "Arquivo não encontrado ou token inválido"
            else:
                return False, f"Erro HTTP {response.status_code}"
                
        except requests.exceptions.RequestException as e:
            return False, f"Erro de conexão: {str(e)}"
        except Exception as e:
            return False, f"Erro: {str(e)}"
    
    def verificar_conexao(self):
        """
        Verifica se a API está acessível
        
        Returns:
            bool: True se API está online
        """
        try:
            response = requests.get(
                f"{self.base_url}/api/health",
                timeout=5
            )
            return response.status_code == 200
        except:
            return False


# Instância global do cliente
upload_api = UploadAPIClient()
