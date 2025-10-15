#!/usr/bin/env python3
"""
Script de teste para consultar arquivos de nota fiscal

Uso:
    python testar_consulta_nf.py <hash>
    
Exemplo:
    python testar_consulta_nf.py 03de0449e11849318f7d67e08377f150
"""

import sys
from consulta_nf_client import ConsultaNFClient

def testar_consulta(hash_nota):
    """Testa consulta de arquivos de nota fiscal"""
    
    print("\n" + "="*70)
    print("🧪 TESTE DE CONSULTA DE NOTA FISCAL")
    print("="*70 + "\n")
    
    # Criar cliente
    client = ConsultaNFClient()
    
    # Consultar
    print(f"📋 Hash: {hash_nota}")
    print(f"🔍 Consultando API...\n")
    
    sucesso, dados, erro = client.consultar_e_processar(hash_nota)
    
    if not sucesso:
        print(f"❌ Erro: {erro}\n")
        return False
    
    # Exibir dados da nota
    nota = dados['nota']
    arquivos = dados['arquivos']
    stats = dados['estatisticas']
    
    print("="*70)
    print("📄 DADOS DA NOTA FISCAL")
    print("="*70)
    print(f"ID Controle: {nota['id_controle']}")
    print(f"Lote ID: {nota['lote_id']}")
    print(f"Prestador: {nota['nome']}")
    print(f"Email: {nota['email']}")
    print(f"Período: {nota['periodo']}")
    print(f"Valor Total: R$ {nota['valor_total']:,.2f}")
    print(f"Quantidade OS: {nota['quantidade_os']}")
    print(f"Status: {nota['status_descricao']}")
    print(f"Validade: {nota['validade_link']}")
    print(f"Link Válido: {'✅ Sim' if nota['link_valido'] else '❌ Não'}")
    print(f"Dias Restantes: {nota['dias_restantes']}")
    
    # Exibir estatísticas
    print("\n" + "="*70)
    print("📊 ESTATÍSTICAS DOS ARQUIVOS")
    print("="*70)
    print(f"Total de Arquivos: {stats['total_arquivos']}")
    print(f"Tamanho Total: {stats['total_tamanho_formatado']}")
    
    if stats['tipos_arquivo']:
        print(f"Tipos de Arquivo:")
        for tipo, qtd in stats['tipos_arquivo'].items():
            print(f"  - {tipo}: {qtd}")
    
    if stats['primeiro_upload']:
        print(f"Primeiro Upload: {stats['primeiro_upload']}")
    if stats['ultimo_upload']:
        print(f"Último Upload: {stats['ultimo_upload']}")
    
    # Listar arquivos
    if len(arquivos) > 0:
        print("\n" + "="*70)
        print("📁 ARQUIVOS RECEBIDOS")
        print("="*70)
        
        for i, arq in enumerate(arquivos, 1):
            print(f"\n{i}. {arq['nome_original']}")
            print(f"   Tipo: {arq['tipo_arquivo']}")
            print(f"   Tamanho: {arq['tamanho_formatado']}")
            print(f"   Upload: {arq['data_upload']}")
            print(f"   Status: {arq['status_processamento']}")
            print(f"   Link: {arq['link_download']}")
            if arq['observacoes']:
                print(f"   Obs: {arq['observacoes']}")
    else:
        print("\n⚠️  Nenhum arquivo foi enviado ainda")
    
    print("\n" + "="*70)
    print(f"✅ Consulta realizada em: {dados['consulta_realizada_em']}")
    print("="*70 + "\n")
    
    return True


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("\n❌ Erro: Hash não fornecido")
        print("\nUso:")
        print("  python testar_consulta_nf.py <hash>\n")
        print("Exemplo:")
        print("  python testar_consulta_nf.py 03de0449e11849318f7d67e08377f150\n")
        sys.exit(1)
    
    hash_nota = sys.argv[1]
    
    try:
        sucesso = testar_consulta(hash_nota)
        sys.exit(0 if sucesso else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Teste interrompido pelo usuário\n")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}\n")
        import traceback
        traceback.print_exc()
        sys.exit(1)
