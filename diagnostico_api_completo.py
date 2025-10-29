#!/usr/bin/env python3
"""
Diagnóstico completo da integração API de upload de NF
"""

import database as db
from consulta_nf_client import ConsultaNFClient

print("\n" + "="*70)
print("🔍 DIAGNÓSTICO COMPLETO - API DE UPLOAD DE NOTAS FISCAIS")
print("="*70)

# 1. Verificar lotes em aberto com link
conn = db.get_db_connection()
cur = conn.cursor()

cur.execute('''
    SELECT id, prestador_nome, periodo, valor_total, upload_hash, link_upload, status
    FROM lotes_servico 
    WHERE status = 'Em Aberto' AND upload_hash IS NOT NULL
    ORDER BY id DESC 
    LIMIT 5
''')
lotes_abertos = cur.fetchall()

print(f"\n📋 LOTES EM ABERTO COM LINK: {len(lotes_abertos)}")
print("-"*70)

for lote in lotes_abertos:
    print(f"\n  Lote #{lote[0]} - {lote[1]}")
    print(f"  Período: {lote[2]}")
    print(f"  Valor: R$ {lote[3]:.2f}")
    print(f"  Hash: {lote[4][:30]}...")
    print(f"  Link: {lote[5][:60]}...")
    
    # Testar consulta na API
    print(f"\n  🔍 Consultando API...")
    client = ConsultaNFClient()
    success, data, error = client.consultar_nota(lote[4])
    
    if success:
        arquivos = data.get('arquivos', [])
        print(f"  ✅ API respondeu OK")
        print(f"  📊 Arquivos encontrados: {len(arquivos)}")
        if arquivos:
            for i, arq in enumerate(arquivos, 1):
                print(f"     {i}. {arq}")
        else:
            print(f"  ⚠️  Nenhum arquivo anexado ainda")
            print(f"  💡 AÇÃO: Envie o link para o prestador anexar a NF")
            print(f"  🔗 Link: {lote[5]}")
    else:
        print(f"  ❌ Erro na API: {error}")
    
    print("-"*70)

# 2. Verificar lotes com NF recebida
cur.execute('''
    SELECT id, prestador_nome, periodo, nota_fiscal_path, status
    FROM lotes_servico 
    WHERE status = 'N.F. RECEBIDA'
    ORDER BY id DESC 
    LIMIT 3
''')
lotes_recebidos = cur.fetchall()

print(f"\n📦 LOTES COM NF RECEBIDA: {len(lotes_recebidos)}")
print("-"*70)

for lote in lotes_recebidos:
    print(f"\n  Lote #{lote[0]} - {lote[1]}")
    print(f"  Período: {lote[2]}")
    print(f"  Arquivo: {lote[3]}")
    
    # Verificar se WhatsApp foi enviado
    cur.execute('''
        SELECT COUNT(*) 
        FROM notificacoes_whatsapp 
        WHERE metadata->>'lote_id' = %s
    ''', (str(lote[0]),))
    
    whatsapp_count = cur.fetchone()[0]
    
    if whatsapp_count > 0:
        print(f"  📱 WhatsApp: ✅ {whatsapp_count} mensagem(ns) enviada(s)")
    else:
        print(f"  📱 WhatsApp: ❌ Nenhuma mensagem registrada")
        print(f"  ⚠️  NF foi anexada mas WhatsApp NÃO foi disparado!")

conn.close()

print("\n" + "="*70)
print("📊 RESUMO DO DIAGNÓSTICO:")
print("="*70)
print(f"""
1. Lotes em aberto esperando NF: {len(lotes_abertos)}
   → Todos estão com link ativo, mas API retorna 0 arquivos
   → Isso significa que NENHUM arquivo foi anexado ainda
   → OU a API não está recebendo/armazenando os uploads

2. Lotes com NF recebida: {len(lotes_recebidos)}
   → Verificar se WhatsApp foi disparado para cada um

💡 PRÓXIMOS PASSOS:
   
   A) Para testar se a API aceita uploads:
      1. Escolha um lote em aberto acima
      2. Acesse o link no navegador
      3. Anexe um arquivo PDF
      4. Execute: python job_consultar_notas.py
      5. Veja se o arquivo aparece na consulta
   
   B) Para testar o WhatsApp localmente:
      1. Execute: python testar_anexo_novo.py <lote_id>
      2. Isso simula o anexo e deve disparar o WhatsApp
      3. Verifique se recebeu a mensagem no celular
""")
