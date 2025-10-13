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
from upload_api_client import upload_api
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
        
        downloads_realizados = 0
        erros = 0
        
        for lote in lotes:
            lote_id = lote['id']
            token = lote['upload_token']
            prestador = lote['prestador_nome']
            periodo = lote['periodo']
            
            print(f"\n{'─'*60}")
            print(f"📦 Lote #{lote_id}")
            print(f"   👤 Prestador: {prestador}")
            print(f"   📅 Período: {periodo}")
            print(f"   🎫 Token: {token[:20]}...")
            
            # Consultar status na API
            print(f"   🔍 Consultando status...")
            success, result = upload_api.consultar_status(token)
            
            if not success:
                print(f"   ❌ Erro ao consultar: {result}")
                erros += 1
                continue
            
            status = result.get('status')
            print(f"   📊 Status: {status}")
            
            # Processar de acordo com o status
            if status == 'completed' and result.get('file_available'):
                print(f"   ✅ Arquivo disponível para download!")
                
                # Obter informações do arquivo
                file_info = result.get('file_info', {})
                filename = file_info.get('filename', f'nota_fiscal_lote_{lote_id}.pdf')
                filesize = file_info.get('size', 0)
                
                print(f"   📄 Arquivo: {filename}")
                print(f"   📊 Tamanho: {filesize / 1024:.2f} KB")
                
                # Fazer download
                save_path = f"uploads/nota_fiscal_lote_{lote_id}.pdf"
                print(f"   ⬇️  Baixando arquivo...")
                
                success_download, message = upload_api.download_arquivo(token, save_path)
                
                if success_download:
                    print(f"   ✅ {message}")
                    print(f"   💾 Salvo em: {save_path}")
                    
                    # Atualizar banco de dados
                    db.salvar_nota_fiscal(lote_id, save_path)
                    print(f"   ✅ Banco de dados atualizado")
                    
                    downloads_realizados += 1
                else:
                    print(f"   ❌ Erro no download: {message}")
                    erros += 1
            
            elif status == 'expired':
                print(f"   ⏰ Link expirado (30 dias)")
                db.atualizar_status_upload(lote_id, 'expired')
                print(f"   ℹ️  Status atualizado no banco")
            
            elif status == 'pending':
                print(f"   ⏳ Aguardando upload do prestador")
            
            else:
                print(f"   ⚠️  Status desconhecido: {status}")
            
            # Pequena pausa entre requisições
            time.sleep(0.5)
        
        # Resumo final
        print(f"\n{'='*60}")
        print(f"📊 RESUMO DO PROCESSAMENTO")
        print(f"{'='*60}")
        print(f"✅ Downloads realizados: {downloads_realizados}")
        print(f"⏳ Ainda pendentes: {len(lotes) - downloads_realizados - erros}")
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
