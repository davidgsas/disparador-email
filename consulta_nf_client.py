"""
Cliente para consulta de arquivos de notas fiscais na API DV Processamento

Endpoint: POST http://api.link.dev.br/dvprocessamento/consulta-nf/
Autenticação: X-API-Key
"""

import requests
import json
import urllib3
from datetime import datetime
from typing import Optional, Dict, List, Tuple

# Desabilitar warnings de SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class ConsultaNFClient:
    """Cliente para consultar arquivos de notas fiscais enviadas"""
    
    def __init__(self, api_url=None, api_key=None):
        """
        Inicializa o cliente
        
        Args:
            api_url: URL base da API (opcional)
            api_key: Chave de autenticação (opcional)
        """
        self.api_url = api_url or "http://api.link.dev.br/dvprocessamento/consulta-nf/"
        self.api_key = api_key or "DV_API_2025_CTRL_NOTAS_f8e9d2c1b4a6"
        self.verify_ssl = False  # SSL ainda não está ativo
    
    def consultar_nota(self, hash_nota: str) -> Tuple[bool, Optional[Dict], Optional[str]]:
        """
        Consulta dados de uma nota fiscal pelo hash
        
        Args:
            hash_nota: Hash da nota fiscal (32 caracteres)
            
        Returns:
            tuple: (sucesso: bool, dados: dict, erro: str)
        """
        try:
            # Validar hash
            if not hash_nota or len(hash_nota) < 10:
                return False, None, "Hash inválido (mínimo 10 caracteres)"
            
            # Headers
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'User-Agent': 'NovoMundo-DisparadorEmail/1.0',
                'X-API-Key': self.api_key
            }
            
            # Payload
            payload = {
                'hash': hash_nota
            }
            
            print(f"🔍 Consultando nota fiscal com hash: {hash_nota[:20]}...")
            
            # Fazer requisição
            response = requests.post(
                self.api_url,
                json=payload,
                headers=headers,
                timeout=30,
                verify=self.verify_ssl
            )
            
            # Processar resposta
            if response.status_code == 200:
                dados = response.json()
                
                print(f"📥 Resposta da API: {json.dumps(dados, indent=2, ensure_ascii=False)[:500]}...")
                
                if dados.get('success'):
                    # A API retorna os dados direto na raiz, não dentro de "data"
                    # Remover o campo "success" e retornar o resto
                    data = {k: v for k, v in dados.items() if k != 'success'}
                    
                    print(f"✅ Consulta realizada com sucesso")
                    print(f"📊 {data.get('estatisticas', {}).get('total_arquivos', 0)} arquivo(s) encontrado(s)")
                    return True, data, None
                else:
                    erro = dados.get('error', 'Erro desconhecido')
                    return False, None, erro
            
            elif response.status_code == 401:
                return False, None, "API Key inválida"
            
            elif response.status_code == 404:
                return False, None, "Nota fiscal não encontrada"
            
            elif response.status_code == 410:
                return False, None, "Link da nota fiscal expirado"
            
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
    
    def extrair_info_nota(self, dados: Dict) -> Dict:
        """
        Extrai informações principais da nota fiscal
        
        Args:
            dados: Dados completos retornados pela API
            
        Returns:
            dict: Informações principais da nota
        """
        # Validar dados
        if not dados or not isinstance(dados, dict):
            return {}
        
        nota = dados.get('nota_fiscal', {})
        status_info = dados.get('status_info', {})
        
        return {
            'id_controle': nota.get('id_controle'),
            'lote_id': nota.get('lote_id'),
            'nome': nota.get('nome'),
            'email': nota.get('email'),
            'periodo': nota.get('periodo'),
            'valor_total': nota.get('valor_total'),
            'quantidade_os': nota.get('quantidade_os'),
            'status': nota.get('status'),
            'status_descricao': status_info.get('descricao'),
            'validade_link': nota.get('validade_link'),
            'link_valido': status_info.get('link_valido'),
            'dias_restantes': status_info.get('dias_restantes'),
            'data_criacao': nota.get('data_criacao'),
            'data_atualizacao': nota.get('data_atualizacao')
        }
    
    def extrair_arquivos(self, dados: Dict) -> List[Dict]:
        """
        Extrai lista de arquivos da nota fiscal
        
        Args:
            dados: Dados completos retornados pela API
            
        Returns:
            list: Lista de arquivos com suas informações
        """
        # Validar dados
        if not dados or not isinstance(dados, dict):
            return []
        
        arquivos = dados.get('arquivos', [])
        
        return [{
            'id': arq.get('id'),
            'nome_original': arq.get('nome_original'),
            'nome_arquivo': arq.get('nome_arquivo'),
            'tipo_arquivo': arq.get('tipo_arquivo'),
            'tamanho_arquivo': arq.get('tamanho_arquivo'),
            'tamanho_formatado': arq.get('tamanho_formatado'),
            'hash_arquivo': arq.get('hash_arquivo'),
            'caminho_arquivo': arq.get('caminho_arquivo'),
            'link_download': arq.get('link_download'),
            'data_upload': arq.get('data_upload'),
            'status_processamento': arq.get('status_processamento'),
            'observacoes': arq.get('observacoes', '')
        } for arq in arquivos]
    
    def extrair_estatisticas(self, dados: Dict) -> Dict:
        """
        Extrai estatísticas dos arquivos
        
        Args:
            dados: Dados completos retornados pela API
            
        Returns:
            dict: Estatísticas dos arquivos
        """
        # Validar dados
        if not dados or not isinstance(dados, dict):
            return {
                'total_arquivos': 0,
                'total_tamanho': 0,
                'total_tamanho_formatado': '0 B',
                'tipos_arquivo': {},
                'primeiro_upload': None,
                'ultimo_upload': None
            }
        
        stats = dados.get('estatisticas', {})
        
        return {
            'total_arquivos': stats.get('total_arquivos', 0),
            'total_tamanho': stats.get('total_tamanho', 0),
            'total_tamanho_formatado': stats.get('total_tamanho_formatado', '0 B'),
            'tipos_arquivo': stats.get('tipos_arquivo', {}),
            'primeiro_upload': stats.get('primeiro_upload'),
            'ultimo_upload': stats.get('ultimo_upload')
        }
    
    def baixar_arquivo(self, link_download: str, caminho_destino: str) -> Tuple[bool, str]:
        """
        Baixa um arquivo da nota fiscal
        
        Args:
            link_download: URL do arquivo
            caminho_destino: Caminho local para salvar
            
        Returns:
            tuple: (sucesso: bool, mensagem: str)
        """
        try:
            print(f"⬇️  Baixando arquivo de: {link_download}")
            
            # Adicionar headers necessários (mesmos da consulta para evitar Mod_Security)
            headers = {
                'User-Agent': 'NovoMundo-DisparadorEmail/1.0',
                'Accept': '*/*'
            }
            
            response = requests.get(
                link_download, 
                headers=headers,
                stream=True, 
                timeout=60,
                verify=False  # Manter consistente com outras chamadas
            )
            
            if response.status_code == 200:
                # Criar diretório se não existir
                import os
                os.makedirs(os.path.dirname(caminho_destino), exist_ok=True)
                
                # Salvar arquivo
                with open(caminho_destino, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                
                print(f"✅ Arquivo salvo em: {caminho_destino}")
                return True, f"Arquivo baixado com sucesso"
            
            else:
                return False, f"Erro ao baixar: HTTP {response.status_code}"
        
        except Exception as e:
            return False, f"Erro ao baixar arquivo: {str(e)}"
    
    def consultar_e_processar(self, hash_nota: str) -> Tuple[bool, Optional[Dict], Optional[str]]:
        """
        Consulta e processa dados completos de uma nota fiscal
        
        Args:
            hash_nota: Hash da nota fiscal
            
        Returns:
            tuple: (sucesso: bool, dados_processados: dict, erro: str)
        """
        # Consultar
        sucesso, dados, erro = self.consultar_nota(hash_nota)
        
        if not sucesso:
            return False, None, erro
        
        # Processar dados
        processados = {
            'nota': self.extrair_info_nota(dados),
            'arquivos': self.extrair_arquivos(dados),
            'estatisticas': self.extrair_estatisticas(dados),
            'consulta_realizada_em': dados.get('consulta_realizada_em'),
            'hash_consultado': dados.get('hash_consultado')
        }
        
        return True, processados, None


def consultar_nota_fiscal(hash_nota: str) -> Tuple[bool, Optional[Dict], Optional[str]]:
    """
    Função auxiliar para consultar uma nota fiscal
    
    Args:
        hash_nota: Hash da nota fiscal
        
    Returns:
        tuple: (sucesso: bool, dados: dict, erro: str)
    """
    client = ConsultaNFClient()
    return client.consultar_e_processar(hash_nota)


def baixar_arquivos_nota(hash_nota: str, pasta_destino: str = "./downloads") -> Dict:
    """
    Consulta e baixa todos os arquivos de uma nota fiscal
    
    Args:
        hash_nota: Hash da nota fiscal
        pasta_destino: Pasta onde salvar os arquivos
        
    Returns:
        dict: Estatísticas do download
    """
    import os
    
    client = ConsultaNFClient()
    
    # Consultar nota
    sucesso, dados, erro = client.consultar_e_processar(hash_nota)
    
    if not sucesso:
        return {
            'sucesso': False,
            'erro': erro,
            'arquivos_baixados': 0
        }
    
    # Criar pasta para o lote
    lote_id = dados['nota']['lote_id']
    pasta_lote = os.path.join(pasta_destino, f"lote_{lote_id}")
    os.makedirs(pasta_lote, exist_ok=True)
    
    # Baixar cada arquivo
    arquivos_baixados = 0
    arquivos_erro = 0
    
    for arquivo in dados['arquivos']:
        caminho_arquivo = os.path.join(pasta_lote, arquivo['nome_original'])
        sucesso_download, mensagem = client.baixar_arquivo(
            arquivo['link_download'],
            caminho_arquivo
        )
        
        if sucesso_download:
            arquivos_baixados += 1
        else:
            arquivos_erro += 1
            print(f"❌ {mensagem}")
    
    return {
        'sucesso': True,
        'lote_id': lote_id,
        'pasta': pasta_lote,
        'total_arquivos': len(dados['arquivos']),
        'arquivos_baixados': arquivos_baixados,
        'arquivos_erro': arquivos_erro,
        'dados': dados
    }


# Exemplo de uso
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        hash_nota = sys.argv[1]
        
        print(f"\n{'='*70}")
        print(f"🔍 CONSULTA DE NOTA FISCAL")
        print(f"{'='*70}\n")
        
        resultado = baixar_arquivos_nota(hash_nota, "./downloads")
        
        if resultado['sucesso']:
            print(f"\n{'='*70}")
            print(f"📊 RESUMO")
            print(f"{'='*70}")
            print(f"Lote: {resultado['lote_id']}")
            print(f"Total de arquivos: {resultado['total_arquivos']}")
            print(f"Arquivos baixados: {resultado['arquivos_baixados']}")
            if resultado['arquivos_erro'] > 0:
                print(f"Erros: {resultado['arquivos_erro']}")
            print(f"Pasta: {resultado['pasta']}")
            print(f"{'='*70}\n")
        else:
            print(f"\n❌ Erro: {resultado['erro']}\n")
    else:
        print("Uso: python consulta_nf_client.py <hash_nota>")
