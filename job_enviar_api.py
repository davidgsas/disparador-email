#!/usr/bin/env python3
"""
Job Automático: Enviar Lotes para API DV Processamento
Executa periodicamente para enviar lotes pendentes à API externa
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
        logger.info(f"   📦 Total de lotes: {stats['total']}")
        logger.info(f"   ✅ Enviados com sucesso: {stats['sucesso']}")
        logger.info(f"   ❌ Erros: {stats['erro']}")
        
        # Detalhar cada lote processado
        if stats['detalhes']:
            logger.info("\n📝 Detalhes dos envios:")
            for detalhe in stats['detalhes']:
                lote_id = detalhe['lote_id']
                status = detalhe['status']
                mensagem = detalhe['mensagem']
                
                if status == 'sucesso':
                    link = detalhe.get('link', 'N/A')
                    logger.info(f"   ✅ Lote #{lote_id}: {mensagem}")
                    logger.info(f"      🔗 Link gerado: {link}")
                else:
                    logger.error(f"   ❌ Lote #{lote_id}: {mensagem}")
        
        logger.info("\n" + "=" * 70)
        logger.info("✅ Job finalizado com sucesso")
        logger.info("=" * 70 + "\n")
        
        return stats
        
    except Exception as e:
        logger.error(f"❌ Erro crítico ao executar job: {str(e)}", exc_info=True)
        return {
            'total': 0,
            'sucesso': 0,
            'erro': 1,
            'detalhes': [{'status': 'erro', 'mensagem': str(e)}]
        }


if __name__ == "__main__":
    # Criar diretório de logs se não existir
    import os
    os.makedirs('logs', exist_ok=True)
    
    # Executar job
    resultado = executar_job()
    
    # Exit code baseado no resultado
    sys.exit(0 if resultado['erro'] == 0 else 1)
