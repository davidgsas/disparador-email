"""
Exemplo de integração WhatsApp com o sistema de emails
Combina notificações por email e WhatsApp
"""

from whatsapp_client import WhatsAppClient
import database as db
from typing import List, Dict
import time


class NotificacaoIntegrada:
    """Gerencia notificações por Email e WhatsApp"""
    
    def __init__(self):
        self.whatsapp = WhatsAppClient()
    
    def verificar_whatsapp_conectado(self) -> bool:
        """Verifica se o WhatsApp está pronto para uso"""
        return self.whatsapp.is_connected()
    
    def notificar_prestador_nota_fiscal(
        self,
        prestador_id: int,
        periodo: str,
        valor: float,
        email: bool = True,
        whatsapp: bool = True
    ) -> Dict:
        """
        Notifica prestador sobre nota fiscal por email e/ou WhatsApp
        
        Args:
            prestador_id: ID do prestador no banco
            periodo: Período da nota (ex: "01/10/2025 a 31/10/2025")
            valor: Valor da nota fiscal
            email: Se deve enviar email
            whatsapp: Se deve enviar WhatsApp
        
        Returns:
            Dict com status dos envios
        """
        resultado = {
            "prestador_id": prestador_id,
            "email_enviado": False,
            "whatsapp_enviado": False,
            "erros": []
        }
        
        # Buscar dados do prestador no banco
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT nome, email, telefone, link_upload
            FROM prestadores
            WHERE id = ?
        """, (prestador_id,))
        
        prestador = cursor.fetchone()
        if not prestador:
            resultado["erros"].append(f"Prestador {prestador_id} não encontrado")
            return resultado
        
        nome, email_prestador, telefone, link_upload = prestador
        
        # Enviar email (se solicitado e tiver email)
        if email and email_prestador:
            try:
                # Aqui você integraria com seu sistema de email existente
                # import send_email
                # send_email.enviar_nota_fiscal(email_prestador, nome, periodo, valor, link_upload)
                resultado["email_enviado"] = True
            except Exception as e:
                resultado["erros"].append(f"Erro ao enviar email: {str(e)}")
        
        # Enviar WhatsApp (se solicitado e tiver telefone)
        if whatsapp and telefone:
            if not self.verificar_whatsapp_conectado():
                resultado["erros"].append("WhatsApp não está conectado")
            else:
                try:
                    mensagem = f"""
🧾 *Nota Fiscal - Novo Mundo Resolve*

Olá, *{nome}*!

📅 *Período:* {periodo}
💰 *Valor:* R$ {valor:.2f}

Por favor, emita a nota fiscal para:
CNPJ: 01.534.080/0008-02

⚠️ *IMPORTANTE:*
Envie a nota exclusivamente pelo link:
{link_upload}

Notas enviadas por outros meios não serão processadas.

Obrigado! 🙏
                    """.strip()
                    
                    resultado_whats = self.whatsapp.send_message(
                        number=telefone,
                        message=mensagem
                    )
                    
                    if resultado_whats.get("success"):
                        resultado["whatsapp_enviado"] = True
                        
                        # Registrar envio no banco
                        cursor.execute("""
                            INSERT INTO notificacoes_whatsapp 
                            (prestador_id, tipo, mensagem, status, data_envio)
                            VALUES (?, ?, ?, ?, datetime('now'))
                        """, (prestador_id, "nota_fiscal", mensagem, "enviado"))
                        conn.commit()
                    else:
                        resultado["erros"].append(f"Erro WhatsApp: {resultado_whats.get('error')}")
                        
                except Exception as e:
                    resultado["erros"].append(f"Erro ao enviar WhatsApp: {str(e)}")
        
        conn.close()
        return resultado
    
    def notificar_multiplos_prestadores(
        self,
        prestadores: List[Dict],
        email: bool = True,
        whatsapp: bool = True,
        delay_entre_mensagens: int = 3
    ) -> Dict:
        """
        Notifica múltiplos prestadores
        
        Args:
            prestadores: Lista de dicts com dados dos prestadores
                Exemplo: [{"id": 1, "periodo": "01-31/10", "valor": 1500.00}, ...]
            email: Se deve enviar emails
            whatsapp: Se deve enviar WhatsApp
            delay_entre_mensagens: Segundos de espera entre mensagens
        
        Returns:
            Dict com estatísticas dos envios
        """
        resultados = {
            "total": len(prestadores),
            "emails_enviados": 0,
            "whatsapp_enviados": 0,
            "falhas": 0,
            "detalhes": []
        }
        
        for prestador in prestadores:
            resultado = self.notificar_prestador_nota_fiscal(
                prestador_id=prestador["id"],
                periodo=prestador["periodo"],
                valor=prestador["valor"],
                email=email,
                whatsapp=whatsapp
            )
            
            if resultado["email_enviado"]:
                resultados["emails_enviados"] += 1
            
            if resultado["whatsapp_enviado"]:
                resultados["whatsapp_enviados"] += 1
            
            if resultado["erros"]:
                resultados["falhas"] += 1
            
            resultados["detalhes"].append(resultado)
            
            # Delay entre mensagens para evitar bloqueio
            if whatsapp and prestador != prestadores[-1]:
                time.sleep(delay_entre_mensagens)
        
        return resultados
    
    def enviar_lembrete_pendencia(
        self,
        prestador_id: int,
        tipo_pendencia: str,
        detalhes: str
    ) -> bool:
        """Envia lembrete de pendência via WhatsApp"""
        
        if not self.verificar_whatsapp_conectado():
            print("WhatsApp não está conectado!")
            return False
        
        # Buscar dados do prestador
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT nome, telefone
            FROM prestadores
            WHERE id = ?
        """, (prestador_id,))
        
        prestador = cursor.fetchone()
        if not prestador or not prestador[1]:  # Sem telefone
            conn.close()
            return False
        
        nome, telefone = prestador
        
        mensagem = f"""
⚠️ *Lembrete - Novo Mundo Resolve*

Olá, *{nome}*!

Você possui uma pendência:

📋 *Tipo:* {tipo_pendencia}
📝 *Detalhes:* {detalhes}

Por favor, regularize o quanto antes.

Em caso de dúvidas, entre em contato conosco.
        """.strip()
        
        resultado = self.whatsapp.send_message(telefone, mensagem)
        
        if resultado.get("success"):
            # Registrar no banco
            cursor.execute("""
                INSERT INTO notificacoes_whatsapp 
                (prestador_id, tipo, mensagem, status, data_envio)
                VALUES (?, ?, ?, ?, datetime('now'))
            """, (prestador_id, "lembrete", mensagem, "enviado"))
            conn.commit()
        
        conn.close()
        return resultado.get("success", False)
    
    def confirmar_recebimento_nota(
        self,
        prestador_id: int,
        numero_nota: str
    ) -> bool:
        """Confirma recebimento de nota fiscal via WhatsApp"""
        
        if not self.verificar_whatsapp_conectado():
            return False
        
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT nome, telefone
            FROM prestadores
            WHERE id = ?
        """, (prestador_id,))
        
        prestador = cursor.fetchone()
        if not prestador or not prestador[1]:
            conn.close()
            return False
        
        nome, telefone = prestador
        
        mensagem = f"""
✅ *Nota Fiscal Recebida*

Olá, *{nome}*!

Confirmamos o recebimento da nota fiscal:

📄 *Número:* {numero_nota}

Sua nota está sendo processada.

Obrigado! 🙏
        """.strip()
        
        resultado = self.whatsapp.send_message(telefone, mensagem)
        
        if resultado.get("success"):
            cursor.execute("""
                INSERT INTO notificacoes_whatsapp 
                (prestador_id, tipo, mensagem, status, data_envio)
                VALUES (?, ?, ?, ?, datetime('now'))
            """, (prestador_id, "confirmacao", mensagem, "enviado"))
            conn.commit()
        
        conn.close()
        return resultado.get("success", False)


# ========== EXEMPLO DE USO ==========

if __name__ == "__main__":
    notificador = NotificacaoIntegrada()
    
    # Verificar se WhatsApp está conectado
    print("🔍 Verificando WhatsApp...")
    if not notificador.verificar_whatsapp_conectado():
        print("❌ WhatsApp não está conectado!")
        print("📱 Inicie o serviço com: npm start")
        print("📱 Depois acesse: http://localhost:3000/qr")
        exit(1)
    
    print("✅ WhatsApp conectado!")
    
    # Exemplo 1: Notificar um prestador
    print("\n📤 Exemplo 1: Notificar prestador individual")
    resultado = notificador.notificar_prestador_nota_fiscal(
        prestador_id=1,
        periodo="01/10/2025 a 31/10/2025",
        valor=1500.00,
        email=True,
        whatsapp=True
    )
    print(f"Resultado: {resultado}")
    
    # Exemplo 2: Notificar múltiplos prestadores
    print("\n📤 Exemplo 2: Notificar múltiplos prestadores")
    prestadores = [
        {"id": 1, "periodo": "01-31/10", "valor": 1500.00},
        {"id": 2, "periodo": "01-31/10", "valor": 2300.00},
        {"id": 3, "periodo": "01-31/10", "valor": 1800.00}
    ]
    
    resultados = notificador.notificar_multiplos_prestadores(
        prestadores=prestadores,
        email=True,
        whatsapp=True,
        delay_entre_mensagens=3
    )
    
    print(f"\n📊 Estatísticas:")
    print(f"   Total: {resultados['total']}")
    print(f"   Emails enviados: {resultados['emails_enviados']}")
    print(f"   WhatsApp enviados: {resultados['whatsapp_enviados']}")
    print(f"   Falhas: {resultados['falhas']}")
    
    # Exemplo 3: Enviar lembrete
    print("\n📤 Exemplo 3: Enviar lembrete")
    enviado = notificador.enviar_lembrete_pendencia(
        prestador_id=1,
        tipo_pendencia="Nota Fiscal Pendente",
        detalhes="Nota fiscal do período 01-30/09 ainda não foi enviada"
    )
    print(f"Lembrete enviado: {enviado}")
    
    # Exemplo 4: Confirmar recebimento
    print("\n📤 Exemplo 4: Confirmar recebimento")
    confirmado = notificador.confirmar_recebimento_nota(
        prestador_id=1,
        numero_nota="NF-123456"
    )
    print(f"Confirmação enviada: {confirmado}")
