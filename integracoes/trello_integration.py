"""
Integração com Trello
Cria cards automaticamente quando arquivos são baixados
"""

import requests
import json
from datetime import datetime
from typing import Optional, Dict, Any
import database as db


class TrelloIntegration:
    """
    Cliente para integração com a API do Trello
    
    Funcionalidades:
    - Criar cards quando arquivos são baixados
    - Anexar informações do lote ao card
    - Adicionar labels personalizadas
    - Criar checklists automáticas
    """
    
    def __init__(self):
        """Inicializa a integração com as credenciais do banco"""
        self.config = self._load_config()
        self.api_key = self.config.get('trello_api_key')
        self.token = self.config.get('trello_token')
        self.board_id = self.config.get('trello_board_id')
        self.list_id = self.config.get('trello_list_id')
        self.base_url = 'https://api.trello.com/1'
        
    def _load_config(self) -> Dict[str, Any]:
        """Carrega configurações do Trello do banco de dados"""
        conn = db.get_db_connection()
        cur = conn.cursor()
        
        try:
            cur.execute("""
                SELECT 
                    trello_api_key, 
                    trello_token, 
                    trello_board_id, 
                    trello_list_id,
                    trello_ativo
                FROM integracoes_config 
                WHERE id = 1
            """)
            
            result = cur.fetchone()
            
            if result:
                return {
                    'trello_api_key': result[0],
                    'trello_token': result[1],
                    'trello_board_id': result[2],
                    'trello_list_id': result[3],
                    'trello_ativo': result[4]
                }
            else:
                # Retorna configuração vazia se não existir
                return {
                    'trello_api_key': None,
                    'trello_token': None,
                    'trello_board_id': None,
                    'trello_list_id': None,
                    'trello_ativo': False
                }
        except Exception as e:
            print(f"❌ Erro ao carregar config Trello: {e}")
            return {}
        finally:
            cur.close()
            conn.close()
    
    def is_configured(self) -> bool:
        """Verifica se a integração está configurada"""
        return all([
            self.api_key,
            self.token,
            self.board_id,
            self.list_id,
            self.config.get('trello_ativo', False)
        ])
    
    def criar_card_download(
        self, 
        lote_id: int,
        prestador_nome: str,
        montador_nome: str,
        arquivos_baixados: list,
        nota_fiscal: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Cria um card no Trello quando arquivos são baixados
        
        Args:
            lote_id: ID do lote
            prestador_nome: Nome do prestador
            montador_nome: Nome do montador
            arquivos_baixados: Lista de nomes dos arquivos baixados
            nota_fiscal: Número da nota fiscal (opcional)
            
        Returns:
            Dados do card criado ou None se falhar
        """
        
        if not self.is_configured():
            print("⚠️  Integração Trello não configurada. Card não será criado.")
            return None
        
        try:
            # Monta o título do card
            titulo = f"📦 Lote #{lote_id} - {prestador_nome}"
            
            # Monta a descrição do card
            descricao = self._montar_descricao(
                lote_id, 
                prestador_nome, 
                montador_nome, 
                arquivos_baixados, 
                nota_fiscal
            )
            
            # Cria o card via API
            url = f"{self.base_url}/cards"
            
            params = {
                'key': self.api_key,
                'token': self.token,
                'idList': self.list_id,
                'name': titulo,
                'desc': descricao,
                'pos': 'top'  # Coloca no topo da lista
            }
            
            response = requests.post(url, params=params)
            response.raise_for_status()
            
            card_data = response.json()
            card_id = card_data['id']
            card_url = card_data['shortUrl']
            
            print(f"✅ Card Trello criado: {card_url}")
            
            # Adiciona label (se configurado)
            self._adicionar_label(card_id, 'green')
            
            # Cria checklist automática
            self._criar_checklist(card_id, arquivos_baixados)
            
            # Salva no banco que o card foi criado
            self._salvar_card_criado(lote_id, card_id, card_url)
            
            return card_data
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Erro ao criar card no Trello: {e}")
            return None
        except Exception as e:
            print(f"❌ Erro inesperado ao criar card: {e}")
            return None
    
    def _montar_descricao(
        self, 
        lote_id: int, 
        prestador_nome: str, 
        montador_nome: str, 
        arquivos_baixados: list,
        nota_fiscal: Optional[str]
    ) -> str:
        """Monta a descrição formatada do card"""
        
        data_hora = datetime.now().strftime("%d/%m/%Y às %H:%M")
        
        descricao = f"""## 📋 Informações do Lote

**Lote:** #{lote_id}
**Prestador:** {prestador_nome}
**Montador:** {montador_nome}
**Data/Hora:** {data_hora}
"""
        
        if nota_fiscal:
            descricao += f"**Nota Fiscal:** {nota_fiscal}\n"
        
        descricao += f"\n## 📎 Arquivos Baixados ({len(arquivos_baixados)})\n\n"
        
        for i, arquivo in enumerate(arquivos_baixados, 1):
            descricao += f"{i}. `{arquivo}`\n"
        
        descricao += """
---
*Card criado automaticamente pelo Sistema de Disparador de Emails*
"""
        
        return descricao
    
    def _adicionar_label(self, card_id: str, cor: str = 'green'):
        """Adiciona uma label colorida ao card"""
        try:
            # Primeiro, busca as labels disponíveis no board
            url = f"{self.base_url}/boards/{self.board_id}/labels"
            params = {
                'key': self.api_key,
                'token': self.token
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            labels = response.json()
            
            # Encontra a label da cor desejada
            label_id = None
            for label in labels:
                if label['color'] == cor:
                    label_id = label['id']
                    break
            
            if label_id:
                # Adiciona a label ao card
                url = f"{self.base_url}/cards/{card_id}/idLabels"
                params['value'] = label_id
                
                response = requests.post(url, params=params)
                response.raise_for_status()
                
        except Exception as e:
            print(f"⚠️  Não foi possível adicionar label: {e}")
    
    def _criar_checklist(self, card_id: str, arquivos: list):
        """Cria uma checklist no card com os arquivos baixados"""
        try:
            # Cria a checklist
            url = f"{self.base_url}/checklists"
            params = {
                'key': self.api_key,
                'token': self.token,
                'idCard': card_id,
                'name': 'Arquivos para Processar'
            }
            
            response = requests.post(url, params=params)
            response.raise_for_status()
            
            checklist_data = response.json()
            checklist_id = checklist_data['id']
            
            # Adiciona cada arquivo como item da checklist
            for arquivo in arquivos:
                url = f"{self.base_url}/checklists/{checklist_id}/checkItems"
                params = {
                    'key': self.api_key,
                    'token': self.token,
                    'name': arquivo
                }
                
                requests.post(url, params=params)
            
        except Exception as e:
            print(f"⚠️  Não foi possível criar checklist: {e}")
    
    def _salvar_card_criado(self, lote_id: int, card_id: str, card_url: str):
        """Salva no banco que o card foi criado para este lote"""
        conn = db.get_db_connection()
        cur = conn.cursor()
        
        try:
            cur.execute("""
                INSERT INTO trello_cards 
                (lote_id, card_id, card_url, data_criacao)
                VALUES (%s, %s, %s, NOW())
            """, (lote_id, card_id, card_url))
            
            conn.commit()
            
        except Exception as e:
            print(f"⚠️  Erro ao salvar card no banco: {e}")
            conn.rollback()
        finally:
            cur.close()
            conn.close()
    
    def listar_boards(self) -> list:
        """Lista todos os boards do usuário (útil para configuração)"""
        if not self.api_key or not self.token:
            raise ValueError("API Key e Token não configurados")
        
        try:
            url = f"{self.base_url}/members/me/boards"
            params = {
                'key': self.api_key,
                'token': self.token
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            return response.json()
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                raise ValueError("API Key ou Token inválidos. Gere novas credenciais em https://trello.com/power-ups/admin")
            else:
                raise ValueError(f"Erro HTTP {e.response.status_code}: {e.response.text[:100]}")
        except Exception as e:
            raise ValueError(f"Erro ao conectar com Trello: {str(e)}")
    
    def listar_listas(self, board_id: str) -> list:
        """Lista todas as listas de um board (útil para configuração)"""
        if not self.api_key or not self.token:
            return []
        
        try:
            url = f"{self.base_url}/boards/{board_id}/lists"
            params = {
                'key': self.api_key,
                'token': self.token
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            return response.json()
        except Exception as e:
            print(f"❌ Erro ao listar listas: {e}")
            return []
