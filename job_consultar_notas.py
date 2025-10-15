"""
Job para consultar status de uploads de notas fiscais
Executar periodicamente via cron (recomendado: a cada hora)

Uso:
    python job_consultar_notas.py
"""

import sys
from pathlib import Path
import datetime

# Adicionar o diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent))

import database as db
from consulta_nf_client import ConsultaNFClient
from integracoes.trello_integration import TrelloIntegration
import time
import logging

# Configurar logger para este job
logger = logging.getLogger('JobConsultaNotas')

# Configurar logger do TrelloIntegration para exibir no console
trello_logger = logging.getLogger('TrelloIntegration')
trello_logger.setLevel(logging.INFO)
if not trello_logger.hasHandlers():
    handler = logging.StreamHandler()
    formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s')
    handler.setFormatter(formatter)
    trello_logger.addHandler(handler)

def processar_uploads_pendentes():
    """Processa lotes aguardando upload de notas fiscais"""
    
    logger.info("="*60)
    logger.info("🔍 JOB DE CONSULTA DE NOTAS FISCAIS")
    logger.info("="*60)
    logger.info(f"⏰ Executado em: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    
    try:
        # Buscar lotes com upload pendente
        lotes = db.get_lotes_upload_pendente()
        logger.info(f"📋 {len(lotes)} lote(s) aguardando nota fiscal")
        
        if not lotes:
            logger.info("✅ Nenhum lote pendente no momento")
            return
        
        # Criar cliente de consulta
        client = ConsultaNFClient()
        
        arquivos_encontrados = 0
        downloads_realizados = 0
        erros = 0
        
        for lote in lotes:
            lote_id = lote['id']
            upload_hash = lote.get('upload_hash')
            prestador = lote['prestador_nome']
            periodo = lote['periodo']
            
            logger.info(f"\n{'─'*60}")
            logger.info(f"📦 Lote #{lote_id}")
            logger.info(f"   👤 Prestador: {prestador}")
            logger.info(f"   📅 Período: {periodo}")
            
            # Verificar se tem hash
            if not upload_hash:
                logger.info(f"   ⚠️  Sem hash de upload (lote antigo)")
                continue
            
            logger.info(f"   🔑 Hash: {upload_hash[:20]}...")
            
            # Consultar status na API
            logger.info(f"   🔍 Consultando arquivos...")
            sucesso, dados, erro = client.consultar_e_processar(upload_hash)
            
            if not sucesso:
                logger.info(f"   ❌ Erro ao consultar: {erro}")
                erros += 1
                continue
            
            # Extrair informações
            nota = dados['nota']
            arquivos = dados['arquivos']
            stats = dados['estatisticas']
            
            logger.info(f"   📊 Status: {nota['status_descricao']}")
            logger.info(f"   📁 Arquivos encontrados: {stats['total_arquivos']}")
            
            # Processar arquivos
            if len(arquivos) > 0:
                arquivos_encontrados += 1
                logger.info(f"   📦 Total: {stats['total_tamanho_formatado']}")
                
                # Verificar se já foi processado antes (evitar duplicações)
                status_arquivo_atual = lote.get('status_arquivo', 0)
                ja_processado = status_arquivo_atual == 2  # 2 = Arquivos baixados
                
                if ja_processado:
                    logger.info(f"   ℹ️  Arquivos já foram baixados anteriormente")
                    continue
                
                # Verificar se já existe notificação para este lote (dupla proteção)
                conn_check = db.get_db_connection()
                cur_check = conn_check.cursor()
                cur_check.execute("SELECT COUNT(*) FROM notificacoes WHERE lote_id = %s", (lote_id,))
                ja_tem_notificacao = cur_check.fetchone()[0] > 0
                cur_check.close()
                conn_check.close()
                
                if ja_tem_notificacao:
                    logger.info(f"   ℹ️  Notificação já existe para este lote")
                    # Continua o processamento mas não cria notificação
                
                # Salvar informações no banco
                db.salvar_arquivos_nf(lote_id, arquivos, stats)
                logger.info(f"   ✅ Dados salvos no banco")
                
                # Baixar cada arquivo
                pasta_destino = f"uploads/lote_{lote_id}"
                import os
                os.makedirs(pasta_destino, exist_ok=True)
                
                for arquivo in arquivos:
                    nome_arquivo = arquivo['nome_original']
                    caminho_local = os.path.join(pasta_destino, nome_arquivo)
                    
                    # Verificar se arquivo já existe
                    if os.path.exists(caminho_local):
                        logger.info(f"   ✓ Já existe: {nome_arquivo}")
                        downloads_realizados += 1
                        continue
                    
                    logger.info(f"   ⬇️  Baixando: {nome_arquivo} ({arquivo['tamanho_formatado']})")
                    
                    sucesso_download, mensagem = client.baixar_arquivo(
                        arquivo['link_download'],
                        caminho_local
                    )
                    
                    if sucesso_download:
                        downloads_realizados += 1
                    else:
                        logger.info(f"      ❌ {mensagem}")
                        erros += 1
                
                # Atualizar status do arquivo para "baixado"
                db.atualizar_status_arquivo(lote_id, 2)
                logger.info(f"   ✅ Status atualizado: Arquivos baixados")
                
                # Criar notificação APENAS se não existir
                if not ja_tem_notificacao:
                    total_arqs = len(arquivos)
                    titulo = f"📥 Nota Fiscal Recebida - Lote #{lote_id}"
                    mensagem_notif = f"{prestador} enviou {total_arqs} arquivo(s) da nota fiscal ({stats['total_tamanho_formatado']})"
                    
                    db.criar_notificacao(
                        tipo='nf_recebida',
                        titulo=titulo,
                        mensagem=mensagem_notif,
                        lote_id=lote_id,
                        icone='📥',
                        prioridade=1
                    )
                    logger.info(f"   🔔 Notificação criada")
                
                # 🎯 INTEGRAÇÃO TRELLO: Criar card automaticamente (apenas se não existir)
                if not ja_tem_notificacao:
                    try:
                        trello = TrelloIntegration()
                        if trello.is_configured():
                            logger.info(f"   📋 Criando card no Trello...")
                            logger.info(f"   🔍 DEBUG: Iniciando preparação dos dados do card... [VERSÃO: 01:25]")
                            
                            # Obter nome do montador
                            montador_nome = lote.get('montador_nome', 'N/A')
                            logger.info(f"   🔍 DEBUG: Montador = {montador_nome}")
                            
                            # Obter número da nota fiscal (se disponível)
                            nota_fiscal = None
                            if nota.get('numero_nota'):
                                nota_fiscal = nota['numero_nota']
                            
                            # Lista de nomes dos arquivos baixados
                            arquivos_baixados = [arq['nome_original'] for arq in arquivos]
                            logger.info(f"   🔍 DEBUG: arquivos_baixados = {arquivos_baixados}")
                            # Caminhos reais dos arquivos baixados
                            arquivos_para_anexar = [os.path.join(pasta_destino, arq['nome_original']) for arq in arquivos]
                            logger.info(f"   🔍 DEBUG: arquivos_para_anexar = {arquivos_para_anexar}")
                            
                            # Log detalhado dos arquivos para anexar
                            logger.info(f"   📎 Arquivos para anexar no Trello:")
                            for caminho in arquivos_para_anexar:
                                existe = os.path.isfile(caminho)
                                logger.info(f"      {'✅' if existe else '❌'} {caminho}")
                            
                            logger.info(f"   🎯 DEBUG: Chamando criar_card_download com {len(arquivos_para_anexar)} arquivos...")
                            
                            # Criar card
                            card_result = trello.criar_card_download(
                                lote_id=lote_id,
                                prestador_nome=prestador,
                                montador_nome=montador_nome,
                                arquivos_baixados=arquivos_baixados,
                                nota_fiscal=nota_fiscal,
                                arquivos_para_anexar=arquivos_para_anexar
                            )
                            
                            if card_result:
                                logger.info(f"   ✅ Card Trello criado: {card_result['shortUrl']}")
                            else:
                                logger.info(f"   ⚠️  Não foi possível criar card no Trello")
                        else:
                            logger.info(f"   ℹ️  Integração Trello não configurada")
                    except Exception as e:
                        logger.info(f"   ⚠️  Erro ao criar card Trello: {e}")
                        # Não interrompe o fluxo se houver erro no Trello
            
            elif nota['link_valido']:
                logger.info(f"   ⏳ Aguardando upload do prestador")
                logger.info(f"   📅 Link válido por mais {nota['dias_restantes']} dia(s)")
            
            else:
                logger.info(f"   ⏰ Link expirado")
                db.atualizar_status_api(lote_id, 2)  # Status expirado
            
            # Pequena pausa entre requisições
            time.sleep(0.5)
        
        # Resumo final
        logger.info(f"\n{'='*60}")
        logger.info(f"📊 RESUMO DO PROCESSAMENTO")
        logger.info(f"{'='*60}")
        logger.info(f"📁 Lotes com arquivos: {arquivos_encontrados}")
        logger.info(f"⬇️  Arquivos baixados: {downloads_realizados}")
        logger.info(f"⏳ Ainda pendentes: {len(lotes) - arquivos_encontrados}")
        if erros > 0:
            logger.info(f"❌ Erros encontrados: {erros}")
        logger.info(f"\n⏰ Concluído em: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        logger.info(f"{'='*60}\n")
        
    except Exception as e:
        logger.info(f"\n❌ ERRO CRÍTICO: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    processar_uploads_pendentes()
