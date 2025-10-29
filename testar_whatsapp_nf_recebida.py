"""
Script para testar o envio de WhatsApp quando NF é recebida
Simula o recebimento de uma nota fiscal
"""

import database as db
from whatsapp_triggers import WhatsAppAutomation
import os

print("🧪 TESTE: Envio de WhatsApp quando NF é recebida\n")
print("=" * 60)

# Escolher um lote para testar
print("\n📋 Lotes disponíveis:\n")
conn = db.get_db_connection()
cursor = conn.cursor()
cursor.execute("""
    SELECT l.id, p.nome, l.periodo, l.valor_total, p.telefone, l.nota_fiscal_path
    FROM lotes_servico l
    LEFT JOIN prestadores p ON l.prestador_id = p.id
    ORDER BY l.id DESC
    LIMIT 10
""")
lotes = cursor.fetchall()
conn.close()

if not lotes:
    print("❌ Nenhum lote encontrado!")
    exit(1)

for lote in lotes:
    lote_id, nome, periodo, valor_total, telefone, nf_path = lote
    nf_status = "✅ SIM" if nf_path else "❌ NÃO"
    tel_status = "✅" if telefone else "❌"
    print(f"  #{lote_id:3} | {nome:30} | {periodo:15} | Tel: {tel_status} | NF: {nf_status}")

print("\n" + "=" * 60)
lote_escolhido = input("\n Digite o ID do lote para testar (ou Enter para sair): ").strip()

if not lote_escolhido:
    print("❌ Cancelado")
    exit(0)

try:
    lote_id = int(lote_escolhido)
except:
    print("❌ ID inválido!")
    exit(1)

# Buscar dados do lote
lote = db.get_lote_by_id(lote_id)

if not lote:
    print(f"❌ Lote #{lote_id} não encontrado!")
    exit(1)

print(f"\n✅ Lote encontrado:")
print(f"   Período: {lote.get('periodo', 'N/A')}")
print(f"   Valor: R$ {lote.get('valor_total', 0):,.2f}")
print(f"   Prestador ID: {lote.get('prestador_id', 'N/A')}")

# Verificar telefone do prestador
conn = db.get_db_connection()
cursor = conn.cursor()
cursor.execute("SELECT nome, telefone FROM prestadores WHERE id = %s", (lote['prestador_id'],))
prestador = cursor.fetchone()
conn.close()

if not prestador:
    print(f"\n❌ Prestador não encontrado!")
    exit(1)

nome_prest, telefone = prestador
print(f"\n📱 Telefone: {telefone if telefone else '❌ NÃO CADASTRADO'}")

if not telefone:
    print("\n⚠️  AVISO: Prestador não tem telefone cadastrado!")
    print("   O WhatsApp não será enviado.")
    resposta = input("\n   Deseja continuar mesmo assim? (s/N): ").strip().lower()
    if resposta != 's':
        print("❌ Cancelado")
        exit(0)

# Criar arquivo fake se não existir
arquivo_fake = f"uploads/lote_{lote_id}/nota_fake_teste.pdf"
os.makedirs(os.path.dirname(arquivo_fake), exist_ok=True)

if not os.path.exists(arquivo_fake):
    with open(arquivo_fake, 'w') as f:
        f.write("ARQUIVO DE TESTE - NÃO É UMA NF REAL")
    print(f"\n📄 Arquivo de teste criado: {arquivo_fake}")

# Confirmar
print("\n" + "=" * 60)
print("🚀 PRONTO PARA TESTAR!")
print("=" * 60)
print("\nEste script irá:")
print("  1. Chamar db.salvar_nota_fiscal() com o arquivo fake")
print("  2. Isso atualizará o status no banco")
print("  3. Disparará o envio de WhatsApp automaticamente")
print("  4. Você verá os logs detalhados do processo")

resposta = input("\n▶️  Deseja continuar? (s/N): ").strip().lower()

if resposta != 's':
    print("❌ Teste cancelado")
    exit(0)

# EXECUTAR TESTE
print("\n" + "=" * 60)
print("🚀 EXECUTANDO TESTE...")
print("=" * 60)

try:
    print(f"\n📞 Chamando db.salvar_nota_fiscal({lote_id}, '{arquivo_fake}')...\n")
    db.salvar_nota_fiscal(lote_id, arquivo_fake)
    
    print("\n" + "=" * 60)
    print("✅ TESTE CONCLUÍDO!")
    print("=" * 60)
    print("\nVerifique acima os logs do WhatsApp.")
    print("\nSe você viu mensagens como:")
    print("  🟢 [NF Recebida] ...")
    print("  🟡 Status WhatsApp: connected")
    print("  🟢 Template encontrado")
    print("  🟡 Enviando mensagem...")
    print("\nSignifica que o sistema está funcionando!")
    
    print("\n📊 Para verificar no histórico:")
    print("  1. Abra o Streamlit")
    print("  2. Vá em: 🤖 Automação WhatsApp > Histórico")
    print("  3. Busque pelo prestador ou data atual")
    
except Exception as e:
    print(f"\n❌ ERRO: {e}")
    import traceback
    print(traceback.format_exc())
