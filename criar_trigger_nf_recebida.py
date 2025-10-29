#!/usr/bin/env python3
"""
Cria trigger no PostgreSQL que dispara WhatsApp automaticamente
quando status do lote muda para 'N.F. RECEBIDA'
"""

import database as db

# SQL para criar função que será chamada pelo trigger
TRIGGER_FUNCTION_SQL = """
CREATE OR REPLACE FUNCTION notificar_whatsapp_nf_recebida()
RETURNS TRIGGER AS $$
BEGIN
    -- Verificar se o status mudou para N.F. RECEBIDA
    IF NEW.status = 'N.F. RECEBIDA' AND (OLD.status IS NULL OR OLD.status != 'N.F. RECEBIDA') THEN
        -- Inserir job na fila para processar
        INSERT INTO whatsapp_queue (lote_id, tipo, data_criacao)
        VALUES (NEW.id, 'nf_recebida_prestador', NOW());
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
"""

# SQL para criar o trigger
TRIGGER_SQL = """
DROP TRIGGER IF EXISTS trigger_nf_recebida ON lotes_servico;

CREATE TRIGGER trigger_nf_recebida
    AFTER UPDATE ON lotes_servico
    FOR EACH ROW
    EXECUTE FUNCTION notificar_whatsapp_nf_recebida();
"""

# SQL para criar tabela de fila
QUEUE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS whatsapp_queue (
    id SERIAL PRIMARY KEY,
    lote_id INTEGER NOT NULL,
    tipo VARCHAR(50) NOT NULL,
    data_criacao TIMESTAMP DEFAULT NOW(),
    processado BOOLEAN DEFAULT FALSE,
    data_processamento TIMESTAMP,
    erro TEXT
);

CREATE INDEX IF NOT EXISTS idx_whatsapp_queue_processado ON whatsapp_queue(processado);
"""

def criar_trigger():
    """Cria trigger e tabela de fila"""
    try:
        conn = db.get_db_connection()
        cur = conn.cursor()
        
        print("\n📋 Criando estrutura de trigger para WhatsApp...")
        print("="*60)
        
        # 1. Criar tabela de fila
        print("\n1️⃣ Criando tabela whatsapp_queue...")
        cur.execute(QUEUE_TABLE_SQL)
        print("   ✅ Tabela criada/verificada")
        
        # 2. Criar função do trigger
        print("\n2️⃣ Criando função notificar_whatsapp_nf_recebida()...")
        cur.execute(TRIGGER_FUNCTION_SQL)
        print("   ✅ Função criada")
        
        # 3. Criar trigger
        print("\n3️⃣ Criando trigger trigger_nf_recebida...")
        cur.execute(TRIGGER_SQL)
        print("   ✅ Trigger criado")
        
        conn.commit()
        conn.close()
        
        print("\n" + "="*60)
        print("✅ TRIGGER CRIADO COM SUCESSO!")
        print("="*60)
        print("""
📌 Como funciona agora:

1. Quando qualquer processo (API, Streamlit, etc) atualizar um lote
   e mudar o status para 'N.F. RECEBIDA', o trigger será disparado

2. O trigger adiciona uma entrada na fila 'whatsapp_queue'

3. Um job processa a fila e envia os WhatsApps pendentes

4. Você pode rodar o job manualmente ou agendar via cron

🔧 Para processar a fila:
   python processar_fila_whatsapp.py

📅 Para agendar (cron - a cada 5 minutos):
   */5 * * * * cd /Users/david/Documents/GitHub/disparador-email && source venv/bin/activate && python processar_fila_whatsapp.py
        """)
        
    except Exception as e:
        print(f"\n❌ Erro ao criar trigger: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    criar_trigger()
