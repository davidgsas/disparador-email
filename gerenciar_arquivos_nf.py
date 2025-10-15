#!/usr/bin/env python3
"""
Script auxiliar para gerenciar arquivos baixados de notas fiscais

Uso:
    python gerenciar_arquivos_nf.py [comando]

Comandos:
    listar              - Lista todos os lotes com arquivos
    verificar           - Verifica integridade dos arquivos
    estatisticas        - Mostra estatísticas gerais
    lote <id>           - Mostra arquivos de um lote específico
    limpar <dias>       - Remove arquivos mais antigos que X dias
"""

import sys
import os
from pathlib import Path
import json
import datetime

# Adicionar diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent))

import database as db


def listar_lotes_com_arquivos():
    """Lista todos os lotes com arquivos baixados"""
    print("\n" + "="*70)
    print("📁 LOTES COM ARQUIVOS DE NOTAS FISCAIS")
    print("="*70 + "\n")
    
    lotes = db.get_lotes_com_arquivos()
    
    if not lotes:
        print("⚠️  Nenhum lote com arquivos encontrado\n")
        return
    
    for lote in lotes:
        print(f"📦 Lote #{lote['id']} - {lote['prestador_nome']}")
        print(f"   📅 Período: {lote['periodo']}")
        print(f"   💰 Valor: R$ {lote['valor_total']:,.2f}")
        
        if lote['arquivos_nf']:
            try:
                arquivos_data = json.loads(lote['arquivos_nf']) if isinstance(lote['arquivos_nf'], str) else lote['arquivos_nf']
                stats = arquivos_data.get('estatisticas', {})
                
                print(f"   📁 Arquivos: {stats.get('total_arquivos', 0)}")
                print(f"   💾 Tamanho: {stats.get('total_tamanho_formatado', '-')}")
                print(f"   📅 Última consulta: {lote['data_ultima_consulta']}")
                
                # Verificar se arquivos existem localmente
                pasta = Path(f"uploads/lote_{lote['id']}")
                if pasta.exists():
                    arquivos_locais = list(pasta.glob('*'))
                    print(f"   💾 Local: {len(arquivos_locais)} arquivo(s) em {pasta}")
                else:
                    print(f"   ⚠️  Pasta local não encontrada")
            
            except Exception as e:
                print(f"   ❌ Erro ao processar: {e}")
        
        print()
    
    print(f"Total: {len(lotes)} lote(s) com arquivos\n")


def verificar_integridade():
    """Verifica se todos os arquivos registrados existem localmente"""
    print("\n" + "="*70)
    print("🔍 VERIFICAÇÃO DE INTEGRIDADE")
    print("="*70 + "\n")
    
    lotes = db.get_lotes_com_arquivos()
    
    arquivos_ok = 0
    arquivos_faltando = 0
    arquivos_extra = 0
    
    for lote in lotes:
        if not lote['arquivos_nf']:
            continue
        
        try:
            arquivos_data = json.loads(lote['arquivos_nf']) if isinstance(lote['arquivos_nf'], str) else lote['arquivos_nf']
            arquivos_esperados = arquivos_data.get('arquivos', [])
            
            pasta = Path(f"uploads/lote_{lote['id']}")
            
            if not pasta.exists():
                print(f"❌ Lote #{lote['id']}: Pasta não existe ({len(arquivos_esperados)} arquivos faltando)")
                arquivos_faltando += len(arquivos_esperados)
                continue
            
            arquivos_locais = {f.name for f in pasta.glob('*')}
            
            for arq in arquivos_esperados:
                nome = arq['nome_original']
                if nome in arquivos_locais:
                    arquivos_ok += 1
                    arquivos_locais.remove(nome)
                else:
                    print(f"❌ Lote #{lote['id']}: Arquivo faltando: {nome}")
                    arquivos_faltando += 1
            
            # Arquivos extras (não registrados)
            if arquivos_locais:
                print(f"⚠️  Lote #{lote['id']}: {len(arquivos_locais)} arquivo(s) extra(s): {arquivos_locais}")
                arquivos_extra += len(arquivos_locais)
        
        except Exception as e:
            print(f"❌ Lote #{lote['id']}: Erro ao verificar: {e}")
    
    print("\n" + "="*70)
    print("📊 RESULTADO")
    print("="*70)
    print(f"✅ Arquivos OK: {arquivos_ok}")
    print(f"❌ Arquivos faltando: {arquivos_faltando}")
    print(f"⚠️  Arquivos extra: {arquivos_extra}")
    print()


def mostrar_estatisticas():
    """Mostra estatísticas gerais"""
    print("\n" + "="*70)
    print("📊 ESTATÍSTICAS GERAIS")
    print("="*70 + "\n")
    
    lotes = db.get_lotes_com_arquivos()
    
    total_lotes = len(lotes)
    total_arquivos = 0
    total_bytes = 0
    por_prestador = {}
    
    for lote in lotes:
        if not lote['arquivos_nf']:
            continue
        
        try:
            arquivos_data = json.loads(lote['arquivos_nf']) if isinstance(lote['arquivos_nf'], str) else lote['arquivos_nf']
            stats = arquivos_data.get('estatisticas', {})
            
            num_arquivos = stats.get('total_arquivos', 0)
            tamanho = stats.get('total_tamanho', 0)
            
            total_arquivos += num_arquivos
            total_bytes += tamanho
            
            prestador = lote['prestador_nome']
            if prestador not in por_prestador:
                por_prestador[prestador] = {'lotes': 0, 'arquivos': 0}
            
            por_prestador[prestador]['lotes'] += 1
            por_prestador[prestador]['arquivos'] += num_arquivos
        
        except Exception as e:
            pass
    
    # Converter bytes para formato legível
    tamanho_mb = total_bytes / (1024 * 1024)
    tamanho_gb = tamanho_mb / 1024
    
    print(f"📦 Total de lotes com arquivos: {total_lotes}")
    print(f"📁 Total de arquivos: {total_arquivos}")
    
    if tamanho_gb >= 1:
        print(f"💾 Tamanho total: {tamanho_gb:.2f} GB")
    else:
        print(f"💾 Tamanho total: {tamanho_mb:.2f} MB")
    
    # Verificar espaço em disco
    pasta_uploads = Path("uploads")
    if pasta_uploads.exists():
        import shutil
        total, usado, livre = shutil.disk_usage(pasta_uploads)
        print(f"💿 Espaço livre no disco: {livre / (1024**3):.2f} GB")
    
    print("\n" + "─"*70)
    print("📊 Por Prestador:")
    print("─"*70)
    
    for prestador in sorted(por_prestador.keys()):
        info = por_prestador[prestador]
        print(f"{prestador:30s} {info['lotes']:3d} lote(s)  {info['arquivos']:3d} arquivo(s)")
    
    print()


def mostrar_arquivos_lote(lote_id):
    """Mostra detalhes dos arquivos de um lote específico"""
    print(f"\n" + "="*70)
    print(f"📦 ARQUIVOS DO LOTE #{lote_id}")
    print("="*70 + "\n")
    
    lote = db.get_lote_by_id(lote_id)
    
    if not lote:
        print(f"❌ Lote #{lote_id} não encontrado\n")
        return
    
    print(f"👤 Prestador: {lote['prestador_nome']}")
    print(f"📅 Período: {lote['periodo']}")
    print(f"💰 Valor: R$ {lote['valor_total']:,.2f}")
    print(f"📊 Status: {lote.get('status_arquivo', 0)}")
    
    if not lote['arquivos_nf']:
        print(f"\n⚠️  Nenhum arquivo registrado para este lote\n")
        return
    
    try:
        arquivos_data = json.loads(lote['arquivos_nf']) if isinstance(lote['arquivos_nf'], str) else lote['arquivos_nf']
        arquivos = arquivos_data.get('arquivos', [])
        stats = arquivos_data.get('estatisticas', {})
        
        print(f"\n📊 Estatísticas:")
        print(f"   Total de arquivos: {stats.get('total_arquivos', 0)}")
        print(f"   Tamanho total: {stats.get('total_tamanho_formatado', '-')}")
        print(f"   Primeiro upload: {stats.get('primeiro_upload', '-')}")
        print(f"   Último upload: {stats.get('ultimo_upload', '-')}")
        
        print(f"\n📁 Arquivos:")
        print("─"*70)
        
        pasta = Path(f"uploads/lote_{lote_id}")
        
        for i, arq in enumerate(arquivos, 1):
            nome = arq['nome_original']
            caminho = pasta / nome
            existe = "✅" if caminho.exists() else "❌"
            
            print(f"\n{i}. {nome}")
            print(f"   Tipo: {arq.get('tipo_arquivo', '-')}")
            print(f"   Tamanho: {arq.get('tamanho_formatado', '-')}")
            print(f"   Upload: {arq.get('data_upload', '-')}")
            print(f"   Status: {arq.get('status_processamento', '-')}")
            print(f"   Local: {existe} {caminho if caminho.exists() else 'Não encontrado'}")
            print(f"   Download: {arq.get('link_download', '-')}")
    
    except Exception as e:
        print(f"\n❌ Erro ao processar arquivos: {e}\n")
        return
    
    print()


def limpar_arquivos_antigos(dias):
    """Remove arquivos mais antigos que X dias"""
    print(f"\n⚠️  Esta operação irá remover arquivos com mais de {dias} dias!")
    resposta = input("Deseja continuar? (s/N): ")
    
    if resposta.lower() != 's':
        print("Operação cancelada\n")
        return
    
    print("\n🧹 Limpando arquivos antigos...\n")
    
    pasta_uploads = Path("uploads")
    if not pasta_uploads.exists():
        print("❌ Pasta uploads não encontrada\n")
        return
    
    cutoff_date = datetime.datetime.now() - datetime.timedelta(days=dias)
    removidos = 0
    
    for pasta_lote in pasta_uploads.glob("lote_*"):
        if not pasta_lote.is_dir():
            continue
        
        for arquivo in pasta_lote.glob("*"):
            if not arquivo.is_file():
                continue
            
            mtime = datetime.datetime.fromtimestamp(arquivo.stat().st_mtime)
            
            if mtime < cutoff_date:
                print(f"🗑️  Removendo: {arquivo}")
                arquivo.unlink()
                removidos += 1
    
    print(f"\n✅ {removidos} arquivo(s) removido(s)\n")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    comando = sys.argv[1].lower()
    
    try:
        if comando == "listar":
            listar_lotes_com_arquivos()
        
        elif comando == "verificar":
            verificar_integridade()
        
        elif comando == "estatisticas":
            mostrar_estatisticas()
        
        elif comando == "lote":
            if len(sys.argv) < 3:
                print("❌ Uso: python gerenciar_arquivos_nf.py lote <id>")
                sys.exit(1)
            
            lote_id = int(sys.argv[2])
            mostrar_arquivos_lote(lote_id)
        
        elif comando == "limpar":
            if len(sys.argv) < 3:
                print("❌ Uso: python gerenciar_arquivos_nf.py limpar <dias>")
                sys.exit(1)
            
            dias = int(sys.argv[2])
            limpar_arquivos_antigos(dias)
        
        else:
            print(f"❌ Comando desconhecido: {comando}\n")
            print(__doc__)
            sys.exit(1)
    
    except KeyboardInterrupt:
        print("\n\n⚠️  Operação interrompida pelo usuário\n")
        sys.exit(130)
    
    except Exception as e:
        print(f"\n❌ Erro: {e}\n")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
