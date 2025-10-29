"""
Funções para envio automático de WhatsApp
Chamadas quando eventos acontecem no sistema
"""

import requests
import database as db
from datetime import datetime
import json


class WhatsAppAutomation:
    """Gerencia envio automático de WhatsApp"""
    
    def __init__(self, base_url="http://localhost:3000"):
        self.base_url = base_url
    
    def _is_connected(self):
        """Verifica se WhatsApp está conectado"""
        try:
            print(f"🟡 Verificando conexão WhatsApp em {self.base_url}...")
            response = requests.get(f"{self.base_url}/status", timeout=2)
            data = response.json()
            conectado = data.get("status") == "connected"
            print(f"🟡 Status WhatsApp: {data.get('status')} - Conectado: {conectado}")
            return conectado
        except Exception as e:
            print(f"🔴 Erro ao verificar conexão: {e}")
            return False
    
    def _send_message(self, number, message):
        """Envia mensagem via WhatsApp"""
        try:
            print(f"🟡 Enviando mensagem para {number}...")
            response = requests.post(
                f"{self.base_url}/send",
                json={"number": number, "message": message},
                timeout=30
            )
            resultado = response.json()
            print(f"🟡 Resposta do servidor: {resultado}")
            return resultado
        except Exception as e:
            print(f"🔴 Erro ao enviar mensagem: {e}")
            return {"success": False, "error": str(e)}
    
    def _get_template(self, evento):
        """Busca template configurado para o evento"""
        try:
            print(f"🟡 Buscando template para evento: {evento}")
            conn = db.get_db_connection()
            cursor = conn.cursor()
            
            # Primeiro buscar qual template está configurado para este evento
            cursor.execute("""
                SELECT template_id
                FROM automacao_whatsapp
                WHERE evento = %s AND ativo = TRUE
                LIMIT 1
            """, (evento,))
            
            automacao = cursor.fetchone()
            print(f"🟡 Automação encontrada: {automacao}")
            
            if not automacao:
                print(f"🔴 Nenhuma automação ativa encontrada para evento: {evento}")
                conn.close()
                return None
            
            template_nome = automacao[0]
            print(f"🟡 Template configurado: {template_nome}")
            
            # Agora buscar o template pelo nome
            cursor.execute("""
                SELECT template
                FROM templates_whatsapp
                WHERE nome = %s AND ativo = TRUE
                LIMIT 1
            """, (template_nome,))
            
            template_result = cursor.fetchone()
            conn.close()
            
            print(f"🟡 Template encontrado no banco: {template_result}")
            
            if template_result and template_result[0]:
                print(f"🟡 ✅ Template OK: {template_result[0][:100]}...")
                return template_result[0]
            
            print(f"🔴 Template '{template_nome}' não encontrado na tabela templates_whatsapp")
            return None
            
        except Exception as e:
            print(f"🔴 Erro ao buscar template: {e}")
            import traceback
            print(f"🔴 Traceback: {traceback.format_exc()}")
            return None
    
    def _render_template(self, template, dados):
        """Renderiza template com dados"""
        for chave, valor in dados.items():
            template = template.replace("{{" + chave + "}}", str(valor))
        return template
    
    def _registrar_envio(self, prestador_id=None, montador_id=None, lote_id=None, montagem_id=None, tipo="", mensagem="", status="enviado", erro=None):
        """Registra envio no banco"""
        try:
            conn = db.get_db_connection()
            cursor = conn.cursor()
            
            # Montar metadata com IDs relevantes
            metadata = {}
            if lote_id:
                metadata['lote_id'] = str(lote_id)
            if montagem_id:
                metadata['montagem_id'] = str(montagem_id)
            
            import json
            metadata_json = json.dumps(metadata) if metadata else None
            
            cursor.execute("""
                INSERT INTO notificacoes_whatsapp 
                (prestador_id, montador_id, tipo, mensagem, status, erro, metadata)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (prestador_id, montador_id, tipo, mensagem, status, erro, metadata_json))
            
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Erro ao registrar envio: {e}")
    
    def enviar_prestador_email_enviado(self, prestador_id, periodo, valor, link):
        """
        Trigger: Quando email é enviado ao prestador
        """
        print(f"\n🟢 [WhatsApp] enviar_prestador_email_enviado iniciado")
        print(f"🟢 Params: prestador_id={prestador_id}, periodo={periodo}, valor={valor}, link={link[:50] if link else 'vazio'}...")
        
        if not self._is_connected():
            print(f"🔴 WhatsApp não conectado!")
            return {"success": False, "error": "WhatsApp não conectado"}
        
        print(f"🟢 WhatsApp conectado OK")
        
        # Buscar template
        template = self._get_template("envio_email_prestador")
        if not template:
            print(f"🔴 Template 'envio_email_prestador' não encontrado!")
            return {"success": False, "error": "Template não configurado"}
        
        print(f"🟢 Template encontrado: {template[:100]}...")
        
        # Buscar dados do prestador
        try:
            print(f"🟢 Buscando dados do prestador ID {prestador_id}...")
            conn = db.get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT nome, telefone FROM prestadores WHERE id = %s", (prestador_id,))
            prestador = cursor.fetchone()
            conn.close()
            
            print(f"🟢 Prestador encontrado: {prestador}")
            
            if not prestador or not prestador[1]:
                print(f"🔴 Prestador sem telefone!")
                return {"success": False, "error": "Prestador sem telefone"}
            
            nome, telefone = prestador
            print(f"🟢 Enviando para: {nome} - {telefone}")
            
            # Renderizar template
            dados = {
                "nome_prestador": nome,
                "periodo": periodo,
                "valor": f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
                "link": link
            }
            
            print(f"🟢 Renderizando template com dados: {dados}")
            mensagem = self._render_template(template, dados)
            print(f"🟢 Mensagem renderizada: {mensagem[:200]}...")
            
            # Enviar
            print(f"🟢 Chamando _send_message...")
            resultado = self._send_message(telefone, mensagem)
            print(f"🟢 Resultado do envio: {resultado}")
            
            # Registrar
            status = "enviado" if resultado.get("success") else "erro"
            erro = resultado.get("error") if not resultado.get("success") else None
            
            print(f"🟢 Registrando envio com status: {status}")
            self._registrar_envio(
                prestador_id=prestador_id,
                tipo="envio_email",
                mensagem=mensagem,
                status=status,
                erro=erro
            )
            
            print(f"🟢 Retornando resultado: {resultado}")
            return resultado
            
        except Exception as e:
            print(f"🔴 EXCEPTION em enviar_prestador_email_enviado: {e}")
            import traceback
            print(f"🔴 Traceback: {traceback.format_exc()}")
            return {"success": False, "error": str(e)}
    
    def enviar_prestador_nf_recebida(self, prestador_id, periodo, valor, numero_nf, lote_id=None):
        """
        Trigger: Quando prestador anexa nota fiscal
        """
        if not self._is_connected():
            return {"success": False, "error": "WhatsApp não conectado"}
        
        template = self._get_template("nf_recebida_prestador")
        if not template:
            return {"success": False, "error": "Template não configurado"}
        
        try:
            conn = db.get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT nome, telefone FROM prestadores WHERE id = %s", (prestador_id,))
            prestador = cursor.fetchone()
            conn.close()
            
            if not prestador or not prestador[1]:
                return {"success": False, "error": "Prestador sem telefone"}
            
            nome, telefone = prestador
            
            dados = {
                "nome_prestador": nome,
                "periodo": periodo,
                "valor": f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
                "numero_nf": numero_nf,
                "data_recebimento": datetime.now().strftime("%d/%m/%Y %H:%M")
            }
            
            mensagem = self._render_template(template, dados)
            resultado = self._send_message(telefone, mensagem)
            
            status = "enviado" if resultado.get("success") else "erro"
            erro = resultado.get("error") if not resultado.get("success") else None
            
            self._registrar_envio(
                prestador_id=prestador_id,
                lote_id=lote_id,
                tipo="confirmacao",
                mensagem=mensagem,
                status=status,
                erro=erro
            )
            
            return resultado
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def enviar_montador_email_enviado(self, montador_id, periodo, valor_total, quantidade_os):
        """
        Trigger: Quando email é enviado ao montador
        """
        if not self._is_connected():
            return {"success": False, "error": "WhatsApp não conectado"}
        
        template = self._get_template("envio_email_montador")
        if not template:
            return {"success": False, "error": "Template não configurado"}
        
        try:
            conn = db.get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT nome, telefone FROM montadores WHERE id = %s", (montador_id,))
            montador = cursor.fetchone()
            conn.close()
            
            if not montador or not montador[1]:
                return {"success": False, "error": "Montador sem telefone"}
            
            nome, telefone = montador
            
            dados = {
                "nome_montador": nome,
                "periodo_relatorio": periodo,
                "valor_total": f"{valor_total:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
                "quantidade_os": quantidade_os
            }
            
            mensagem = self._render_template(template, dados)
            resultado = self._send_message(telefone, mensagem)
            
            status = "enviado" if resultado.get("success") else "erro"
            erro = resultado.get("error") if not resultado.get("success") else None
            
            self._registrar_envio(
                montador_id=montador_id,
                tipo="envio_email",
                mensagem=mensagem,
                status=status,
                erro=erro
            )
            
            return resultado
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def enviar_montador_nf_recebida(self, montador_id, periodo, valor_total, numero_nf):
        """
        Trigger: Quando montador anexa nota fiscal
        """
        if not self._is_connected():
            return {"success": False, "error": "WhatsApp não conectado"}
        
        template = self._get_template("nf_recebida_montador")
        if not template:
            return {"success": False, "error": "Template não configurado"}
        
        try:
            conn = db.get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT nome, telefone FROM montadores WHERE id = %s", (montador_id,))
            montador = cursor.fetchone()
            conn.close()
            
            if not montador or not montador[1]:
                return {"success": False, "error": "Montador sem telefone"}
            
            nome, telefone = montador
            
            dados = {
                "nome_montador": nome,
                "periodo_relatorio": periodo,
                "valor_total": f"{valor_total:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
                "numero_nf": numero_nf,
                "data_recebimento": datetime.now().strftime("%d/%m/%Y %H:%M")
            }
            
            mensagem = self._render_template(template, dados)
            resultado = self._send_message(telefone, mensagem)
            
            status = "enviado" if resultado.get("success") else "erro"
            erro = resultado.get("error") if not resultado.get("success") else None
            
            self._registrar_envio(
                montador_id=montador_id,
                tipo="confirmacao",
                mensagem=mensagem,
                status=status,
                erro=erro
            )
            
            return resultado
            
        except Exception as e:
            return {"success": False, "error": str(e)}


# Instância global para uso fácil
whatsapp_automation = WhatsAppAutomation()
