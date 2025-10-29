#!/usr/bin/env python3
"""
Processa fila de WhatsApp pendentes
Envia mensagens para lotes que mudaram de status
"""

import database as db
from whatsapp_triggers import WhatsAppAutomation
import time
from datetime import datetime

def processar_fila():
    """Processa todos os itens pendentes na fila"""
    
    print(f"\n{'='*60}")
    print(f"🔄 PROCESSAMENTO FILA WHATSAPP")
    print(f"{'='*60}")
    print(f"⏰ {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
    
    try:
        conn = db.get_db_connection()
        cur = conn.cursor()
        
        # Buscar itens não processados
        cur.execute("""
            SELECT id, lote_id, tipo, data_criacao
            FROM whatsapp_queue
            WHERE processado = FALSE
            ORDER BY data_criacao ASC
        """)
        
        pendentes = cur.fetchall()
        
        if not pendentes:
            print("✅ Nenhum item pendente na fila")
            conn.close()
            return
        
        print(f"📊 {len(pendentes)} item(ns) na fila para processar\n")
        
        wa = WhatsAppAutomation()
        sucesso = 0
        erros = 0
        
        for item in pendentes:
            queue_id, lote_id, tipo, data_criacao = item
            
            print(f"\n{'─'*60}")
            print(f"📦 Processando lote #{lote_id}")
            print(f"   ID Fila: {queue_id}")
            print(f"   Tipo: {tipo}")
            print(f"   Criado: {data_criacao}")
            
            try:
                # Buscar dados do lote
                lote = db.get_lote_by_id(lote_id)
                
                if not lote:
                    raise Exception(f"Lote {lote_id} não encontrado")
                
                # Extrair número da NF
                import os
                if lote.get('nota_fiscal_path'):
                    numero_nf = os.path.basename(lote['nota_fiscal_path']).replace('.pdf', '').replace('.PDF', '')
                else:
                    numero_nf = f"Lote_{lote_id}"
                
                print(f"   📄 NF: {numero_nf}")
                print(f"   👤 Prestador: {lote['prestador_nome']}")
                print(f"   💰 Valor: R$ {lote['valor_total']:.2f}")
                
                # Enviar WhatsApp
                print(f"   📱 Enviando WhatsApp...")
                resultado = wa.enviar_prestador_nf_recebida(
                    lote['prestador_id'],
                    lote['periodo'],
                    lote['valor_total'],
                    numero_nf,
                    lote_id=lote_id
                )
                
                if resultado.get('success'):
                    print(f"   ✅ WhatsApp enviado com sucesso!")
                    
                    # Marcar como processado
                    cur.execute("""
                        UPDATE whatsapp_queue
                        SET processado = TRUE,
                            data_processamento = NOW()
                        WHERE id = %s
                    """, (queue_id,))
                    
                    sucesso += 1
                else:
                    erro_msg = resultado.get('error', 'Erro desconhecido')
                    print(f"   ⚠️  Erro: {erro_msg}")
                    
                    # Marcar como processado com erro
                    cur.execute("""
                        UPDATE whatsapp_queue
                        SET processado = TRUE,
                            data_processamento = NOW(),
                            erro = %s
                        WHERE id = %s
                    """, (erro_msg, queue_id))
                    
                    erros += 1
                
                conn.commit()
                
            except Exception as e:
                erro_msg = str(e)
                print(f"   ❌ ERRO: {erro_msg}")
                
                # Marcar como processado com erro
                cur.execute("""
                    UPDATE whatsapp_queue
                    SET processado = TRUE,
                        data_processamento = NOW(),
                        erro = %s
                    WHERE id = %s
                """, (erro_msg, queue_id))
                
                conn.commit()
                erros += 1
        
        conn.close()
        
        print(f"\n{'='*60}")
        print(f"📊 RESUMO DO PROCESSAMENTO")
        print(f"{'='*60}")
        print(f"✅ Sucesso: {sucesso}")
        print(f"❌ Erros: {erros}")
        print(f"📋 Total: {len(pendentes)}")
        print(f"⏰ {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
        
    except Exception as e:
        print(f"\n❌ Erro ao processar fila: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    processar_fila()
