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
import time

def processar_uploads_pendentes():
    """Processa lotes aguardando upload de notas fiscais"""
    
    print(f"\n{'='*60}")
    print(f"🔍 JOB DE CONSULTA DE NOTAS FISCAIS")
    print(f"{'='*60}")
    print(f"⏰ Executado em: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    
    try:
        # Buscar lotes com upload pendente
        lotes = db.get_lotes_upload_pendente()
        print(f"\n📋 {len(lotes)} lote(s) aguardando nota fiscal")
        
        if not lotes:
            print("✅ Nenhum lote pendente no momento")
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
            
            print(f"\n{'─'*60}")
            print(f"📦 Lote #{lote_id}")
            print(f"   👤 Prestador: {prestador}")
            print(f"   📅 Período: {periodo}")
            
            # Verificar se tem hash
            if not upload_hash:
                print(f"   ⚠️  Sem hash de upload (lote antigo)")
                continue
            
            print(f"   🔑 Hash: {upload_hash[:20]}...")
            
            # Consultar status na API
            print(f"   🔍 Consultando arquivos...")
            sucesso, dados, erro = client.consultar_e_processar(upload_hash)
            
            if not sucesso:
                print(f"   ❌ Erro ao consultar: {erro}")
                erros += 1
                continue
            
            # Extrair informações
            nota = dados['nota']
            arquivos = dados['arquivos']
            stats = dados['estatisticas']
            
            print(f"   📊 Status: {nota['status_descricao']}")
            print(f"   📁 Arquivos encontrados: {stats['total_arquivos']}")
            
            # Processar arquivos
            if len(arquivos) > 0:
                arquivos_encontrados += 1
                print(f"   📦 Total: {stats['total_tamanho_formatado']}")
                
                # Verificar se já foi processado antes (evitar duplicações)
                status_arquivo_atual = lote.get('status_arquivo', 0)
                ja_processado = status_arquivo_atual == 2  # 2 = Arquivos baixados
                
                if ja_processado:
                    print(f"   ℹ️  Arquivos já foram baixados anteriormente")
                    continue
                
                # Salvar informações no banco
                db.salvar_arquivos_nf(lote_id, arquivos, stats)
                print(f"   ✅ Dados salvos no banco")
                
                # Baixar cada arquivo
                pasta_destino = f"uploads/lote_{lote_id}"
                import os
                os.makedirs(pasta_destino, exist_ok=True)
                
                for arquivo in arquivos:
                    nome_arquivo = arquivo['nome_original']
                    caminho_local = os.path.join(pasta_destino, nome_arquivo)
                    
                    # Verificar se arquivo já existe
                    if os.path.exists(caminho_local):
                        print(f"   ✓ Já existe: {nome_arquivo}")
                        downloads_realizados += 1
                        continue
                    
                    print(f"   ⬇️  Baixando: {nome_arquivo} ({arquivo['tamanho_formatado']})")
                    
                    sucesso_download, mensagem = client.baixar_arquivo(
                        arquivo['link_download'],
                        caminho_local
                    )
                    
                    if sucesso_download:
                        downloads_realizados += 1
                    else:
                        print(f"      ❌ {mensagem}")
                        erros += 1
                
                # Atualizar status do arquivo para "baixado"
                db.atualizar_status_arquivo(lote_id, 2)
                print(f"   ✅ Status atualizado: Arquivos baixados")
                
                # Criar notificação APENAS na primeira vez
                total_arqs = len(arquivos)
                titulo = f"📥 Nota Fiscal Recebida - Lote #{lote_id}"
                mensagem = f"{prestador} enviou {total_arqs} arquivo(s) da nota fiscal ({stats['total_tamanho_formatado']})"
                
                db.criar_notificacao(
                    tipo='nf_recebida',
                    titulo=titulo,
                    mensagem=mensagem,
                    lote_id=lote_id,
                    icone='📥',
                    prioridade=1
                )
                print(f"   🔔 Notificação criada")
            
            elif nota['link_valido']:
                print(f"   ⏳ Aguardando upload do prestador")
                print(f"   📅 Link válido por mais {nota['dias_restantes']} dia(s)")
            
            else:
                print(f"   ⏰ Link expirado")
                db.atualizar_status_api(lote_id, 2)  # Status expirado
            
            # Pequena pausa entre requisições
            time.sleep(0.5)
        
        # Resumo final
        print(f"\n{'='*60}")
        print(f"📊 RESUMO DO PROCESSAMENTO")
        print(f"{'='*60}")
        print(f"📁 Lotes com arquivos: {arquivos_encontrados}")
        print(f"⬇️  Arquivos baixados: {downloads_realizados}")
        print(f"⏳ Ainda pendentes: {len(lotes) - arquivos_encontrados}")
        if erros > 0:
            print(f"❌ Erros encontrados: {erros}")
        print(f"\n⏰ Concluído em: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        print(f"{'='*60}\n")
        
    except Exception as e:
        print(f"\n❌ ERRO CRÍTICO: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    processar_uploads_pendentes()
