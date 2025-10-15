"""
Script para criar tabelas de integração com Trello
"""

import database as db

def criar_tabelas_trello():
    """Cria as tabelas necessárias para integração com Trello"""
    
    conn = db.get_db_connection()
    cur = conn.cursor()
    
    try:
        print("🔧 Criando tabelas de integração...")
        
        # Tabela de configuração das integrações
        cur.execute("""
            CREATE TABLE IF NOT EXISTS integracoes_config (
                id INTEGER PRIMARY KEY DEFAULT 1,
                
                -- Trello
                trello_api_key TEXT,
                trello_token TEXT,
                trello_board_id TEXT,
                trello_list_id TEXT,
                trello_ativo BOOLEAN DEFAULT FALSE,
                
                -- Futuras integrações podem ser adicionadas aqui
                -- slack_webhook TEXT,
                -- teams_webhook TEXT,
                
                data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                
                CONSTRAINT single_row CHECK (id = 1)
            )
        """)
        print("  ✓ Tabela integracoes_config criada")
        
        # Insere registro padrão se não existir
        cur.execute("""
            INSERT INTO integracoes_config (id) 
            VALUES (1) 
            ON CONFLICT (id) DO NOTHING
        """)
        
        # Tabela para rastrear cards criados
        cur.execute("""
            CREATE TABLE IF NOT EXISTS trello_cards (
                id SERIAL PRIMARY KEY,
                lote_id INTEGER NOT NULL,
                card_id TEXT NOT NULL,
                card_url TEXT NOT NULL,
                data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                
                CONSTRAINT unique_lote_card UNIQUE(lote_id)
            )
        """)
        print("  ✓ Tabela trello_cards criada")
        
        # Índice para buscar cards por lote
        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_trello_cards_lote 
            ON trello_cards(lote_id)
        """)
        print("  ✓ Índice criado")
        
        conn.commit()
        print("\n✅ Tabelas de integração criadas com sucesso!")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Erro ao criar tabelas: {e}")
        conn.rollback()
        return False
    finally:
        cur.close()
        conn.close()


if __name__ == '__main__':
    criar_tabelas_trello()
