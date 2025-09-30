import psycopg2
import json
from database import get_db_connection

def check_montagem_exists(montador_id, periodo_relatorio):
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id FROM envios_montagem 
                WHERE montador_id = %s 
                AND detalhes->>'periodo_relatorio' = %s
            """, (montador_id, periodo_relatorio))
            result = cur.fetchone()
            return result is not None
    finally:
        conn.close()
