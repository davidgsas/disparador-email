"""
Script para testar anexação de arquivo no Trello
"""

import os
import sys
from integracoes.trello_integration import TrelloIntegration

def testar_anexo():
    print("\n" + "="*70)
    print("📎 TESTE DE ANEXAÇÃO DE ARQUIVO NO TRELLO")
    print("="*70)
    
    # Inicializar integração
    trello = TrelloIntegration()
    
    if not trello.is_configured():
        print("❌ Integração Trello não configurada!")
        return False
    
    print("✅ Integração Trello configurada")
    
    # Verificar se existe um arquivo de teste
    arquivo_teste = None
    
    print("\n📂 Listando arquivos disponíveis em uploads/:")
    
    if os.path.exists("uploads"):
        for pasta in sorted(os.listdir("uploads")):
            pasta_path = os.path.join("uploads", pasta)
            if os.path.isdir(pasta_path):
                print(f"\n   📁 {pasta}:")
                for arquivo in os.listdir(pasta_path):
                    arquivo_path = os.path.join(pasta_path, arquivo)
                    if os.path.isfile(arquivo_path):
                        tamanho = os.path.getsize(arquivo_path)
                        print(f"      - {arquivo} ({tamanho} bytes)")
                        if not arquivo_teste and arquivo.endswith('.pdf'):
                            arquivo_teste = arquivo_path
    else:
        print("   ❌ Pasta uploads/ não existe")
    
    if not arquivo_teste or not os.path.isfile(arquivo_teste):
        print("\n❌ Nenhum arquivo PDF disponível para teste")
        return False
    
    print(f"\n📋 Usando arquivo: {arquivo_teste}")
    
    # ID de um card existente no Trello (você precisa ter um card criado)
    # Vamos listar os cards criados no banco
    import database as db
    conn = db.get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT lote_id, card_id, card_url FROM trello_cards ORDER BY data_criacao DESC LIMIT 5")
    cards = cur.fetchall()
    cur.close()
    conn.close()
    
    if not cards:
        print("\n❌ Nenhum card encontrado no banco de dados")
        print("   Crie um card primeiro executando o job_consultar_notas.py")
        return False
    
    print(f"\n📋 Cards encontrados no banco:")
    for lote_id, card_id, card_url in cards:
        print(f"   • Lote #{lote_id}: {card_url} (ID: {card_id})")
    
    # Usar o primeiro card
    lote_id, card_id, card_url = cards[0]
    print(f"\n🎯 Testando anexação no card: {card_url}")
    
    # Testar anexação
    print(f"\n📎 Anexando arquivo: {arquivo_teste}")
    print(f"   Tamanho: {os.path.getsize(arquivo_teste)} bytes")
    
    resultado = trello._anexar_arquivo(card_id, arquivo_teste)
    
    if resultado:
        print(f"\n✅ TESTE PASSOU!")
        print(f"   Verifique o card no Trello: {card_url}")
    else:
        print(f"\n❌ TESTE FALHOU!")
        print(f"   Verifique os logs acima para detalhes do erro")
    
    print("="*70)
    return resultado


if __name__ == '__main__':
    sucesso = testar_anexo()
    sys.exit(0 if sucesso else 1)
