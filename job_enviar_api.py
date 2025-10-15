#!/usr/bin/env python3
"""
Job Automático: Enviar Lotes/Envios para API DV Processamento
Executa periodicamente para enviar lotes de prestadores e envios de montadores pendentes à API externa
"""

import sys
import logging
from datetime import datetime
from api_upload_client import enviar_lotes_pendentes

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/job_enviar_api.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)


def executar_job():
    """
    Executa o job de envio de lotes para a API
    """
    logger.info("=" * 70)
    logger.info("🚀 Iniciando job de envio para API DV Processamento")
    logger.info("=" * 70)
    
    try:
        # Enviar lotes pendentes
        stats = enviar_lotes_pendentes()
        
        # Log dos resultados
        logger.info(f"📊 Processamento concluído:")
        logger.info(f"   📦 Total geral: {stats['total']}")
        
        # Estatísticas de Prestadores
        logger.info(f"\n   📦 Lotes de Prestadores:")
        logger.info(f"      Total: {stats['lotes']['total']}")
        logger.info(f"      ✅ Sucesso: {stats['lotes']['sucesso']}")
        logger.info(f"      ❌ Erro: {stats['lotes']['erro']}")
        
        # Estatísticas de Montadores
        logger.info(f"\n   🔧 Envios de Montadores:")
        logger.info(f"      Total: {stats['montagens']['total']}")
        logger.info(f"      ✅ Sucesso: {stats['montagens']['sucesso']}")
        logger.info(f"      ❌ Erro: {stats['montagens']['erro']}")
        
        # Detalhar lotes de prestadores processados
        if stats['lotes']['detalhes']:
            logger.info("\n📝 Detalhes dos lotes de prestadores:")
            for detalhe in stats['lotes']['detalhes']:
                item_id = detalhe['id']
                nome = detalhe['nome']
                status = detalhe['status']
                mensagem = detalhe['mensagem']
                
                if status == 'sucesso':
                    link = detalhe.get('link', 'N/A')
                    logger.info(f"   ✅ Lote #{item_id} ({nome}): {mensagem}")
                    logger.info(f"      🔗 Link: {link}")
                else:
                    logger.error(f"   ❌ Lote #{item_id} ({nome}): {mensagem}")
        
        # Detalhar envios de montadores processados
        if stats['montagens']['detalhes']:
            logger.info("\n🔧 Detalhes dos envios de montadores:")
            for detalhe in stats['montagens']['detalhes']:
                item_id = detalhe['id']
                nome = detalhe['nome']
                status = detalhe['status']
                mensagem = detalhe['mensagem']
                
                if status == 'sucesso':
                    link = detalhe.get('link', 'N/A')
                    logger.info(f"   ✅ Envio #{item_id} ({nome}): {mensagem}")
                    logger.info(f"      🔗 Link: {link}")
                else:
                    logger.error(f"   ❌ Envio #{item_id} ({nome}): {mensagem}")
        
        logger.info("\n" + "=" * 70)
        logger.info("✅ Job finalizado com sucesso")
        logger.info("=" * 70 + "\n")
        
        return stats
        
    except Exception as e:
        logger.error(f"❌ Erro crítico ao executar job: {str(e)}", exc_info=True)
        return {
            'total': 0,
            'lotes': {'total': 0, 'sucesso': 0, 'erro': 1, 'detalhes': []},
            'montagens': {'total': 0, 'sucesso': 0, 'erro': 0, 'detalhes': []},
        }


if __name__ == "__main__":
    # Criar diretório de logs se não existir
    import os
    os.makedirs('logs', exist_ok=True)
    
    # Executar job
    resultado = executar_job()
    
    # Exit code baseado no resultado
    total_erros = resultado['lotes']['erro'] + resultado['montagens']['erro']
    sys.exit(0 if total_erros == 0 else 1)
