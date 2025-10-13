import os
import psycopg2
import psycopg2.extras
import datetime
from dotenv import load_dotenv
import json

load_dotenv()

def get_db_connection():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        port=os.getenv("DB_PORT")
    )
    return conn

def run_migrations():
    conn = get_db_connection()
    with conn.cursor() as cur:
        # Garante que as tabelas base existam
        cur.execute('''CREATE TABLE IF NOT EXISTS prestadores (id SERIAL PRIMARY KEY, nome TEXT NOT NULL UNIQUE, email TEXT NOT NULL, fornecedor_id TEXT UNIQUE, regra_envio TEXT, dias_envio TEXT)''')
        cur.execute('''CREATE TABLE IF NOT EXISTS montadores (id SERIAL PRIMARY KEY, nome TEXT NOT NULL, identificador TEXT NOT NULL UNIQUE, email TEXT NOT NULL, percentual_comissao REAL NOT NULL, auxilio_semanal REAL NOT NULL, ativo BOOLEAN NOT NULL DEFAULT TRUE, fornecedor_id TEXT UNIQUE, regra_envio TEXT, dias_envio TEXT)''')
        
        # Criar tabelas principais ANTES de tentar adicionar colunas
        cur.execute('''CREATE TABLE IF NOT EXISTS lotes_servico (id SERIAL PRIMARY KEY, prestador_id INTEGER REFERENCES prestadores(id), prestador_nome TEXT, periodo TEXT NOT NULL, valor_total REAL NOT NULL, data_envio TIMESTAMP NOT NULL, status TEXT NOT NULL DEFAULT 'Em Aberto', conversation_id TEXT, anexo_path TEXT)''')
        cur.execute('''CREATE TABLE IF NOT EXISTS os_enviadas (id SERIAL PRIMARY KEY, lote_id INTEGER REFERENCES lotes_servico(id) ON DELETE CASCADE, os_numero TEXT NOT NULL UNIQUE, detalhes JSONB)''')
        cur.execute('''CREATE TABLE IF NOT EXISTS envios_montagem (id SERIAL PRIMARY KEY, montador_id INTEGER REFERENCES montadores(id), data_envio TIMESTAMP NOT NULL, status TEXT NOT NULL DEFAULT 'Em Aberto', detalhes JSONB, conversation_id TEXT, anexo_path TEXT)''')
        
        # Agora podemos adicionar colunas adicionais se não existirem
        cur.execute("ALTER TABLE prestadores ADD COLUMN IF NOT EXISTS emails_adicionais TEXT;")
        cur.execute("ALTER TABLE montadores ADD COLUMN IF NOT EXISTS emails_adicionais TEXT;")
        
        # Criar índices
        cur.execute('''CREATE UNIQUE INDEX IF NOT EXISTS idx_unique_montagem ON envios_montagem ((detalhes->>'periodo_relatorio'), montador_id);''')
        
        # Tabela de envios ignorados
        cur.execute('''CREATE TABLE IF NOT EXISTS envios_ignorados (id SERIAL PRIMARY KEY, tipo TEXT NOT NULL, entidade_id INTEGER NOT NULL, ano INTEGER NOT NULL, periodo_chave TEXT NOT NULL, data_ignorada TIMESTAMP NOT NULL)''')
        cur.execute('''CREATE UNIQUE INDEX IF NOT EXISTS idx_unique_ignore ON envios_ignorados (tipo, entidade_id, ano, periodo_chave);''')
        
        # Nova tabela para blacklist de boletins (montadores)
        cur.execute('''CREATE TABLE IF NOT EXISTS boletins_blacklist (
            id SERIAL PRIMARY KEY,
            montador_id INTEGER REFERENCES montadores(id) ON DELETE CASCADE,
            boletim TEXT NOT NULL,
            data_adicao TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            motivo TEXT
        )''')
        cur.execute('''CREATE UNIQUE INDEX IF NOT EXISTS idx_unique_boletim_blacklist ON boletins_blacklist (montador_id, boletim);''')
        
        # Nova tabela para blacklist de OS (prestadores)
        cur.execute('''CREATE TABLE IF NOT EXISTS os_blacklist (
            id SERIAL PRIMARY KEY,
            prestador_id INTEGER REFERENCES prestadores(id) ON DELETE CASCADE,
            os_numero TEXT NOT NULL,
            data_adicao TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            motivo TEXT
        )''')
        cur.execute('''CREATE UNIQUE INDEX IF NOT EXISTS idx_unique_os_blacklist ON os_blacklist (prestador_id, os_numero);''')

    conn.commit()
    conn.close()

# --- Funções de Prestadores ---
def add_prestador(nome, email, fornecedor_id, regra_envio, dias_envio, emails_adicionais=None):
    conn = get_db_connection()
    try:
        with conn.cursor() as cur: 
            cur.execute('INSERT INTO prestadores (nome, email, fornecedor_id, regra_envio, dias_envio, emails_adicionais) VALUES (%s, %s, %s, %s, %s, %s)', 
                       (nome, email, fornecedor_id, regra_envio, dias_envio, emails_adicionais))
        conn.commit()
        return True, "Prestador adicionado!"
    except psycopg2.IntegrityError: return False, f"Erro: Fornecedor ID ou Nome já existe."
    finally: conn.close()

def update_prestador(prestador_id, regra_envio, dias_envio, emails_adicionais=None):
    conn = get_db_connection()
    with conn.cursor() as cur:
        if emails_adicionais is not None:
            cur.execute('UPDATE prestadores SET regra_envio = %s, dias_envio = %s, emails_adicionais = %s WHERE id = %s', 
                       (regra_envio, dias_envio, emails_adicionais, prestador_id))
        else:
            cur.execute('UPDATE prestadores SET regra_envio = %s, dias_envio = %s WHERE id = %s', (regra_envio, dias_envio, prestador_id))
    conn.commit()
    conn.close()

def get_all_prestadores():
    conn = get_db_connection()
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        cur.execute('SELECT * FROM prestadores ORDER BY nome ASC')
        prestadores = cur.fetchall()
    conn.close()
    return prestadores

def get_prestador_by_name(name):
    conn = get_db_connection()
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        cur.execute('SELECT * FROM prestadores WHERE nome = %s', (name,))
        prestador = cur.fetchone()
    conn.close()
    return prestador

def delete_prestador(prestador_id):
    conn = get_db_connection()
    with conn.cursor() as cur: cur.execute('DELETE FROM prestadores WHERE id = %s', (prestador_id,))
    conn.commit()
    conn.close()

def get_prestador_emails(prestador_info):
    """Retorna lista de todos os emails do prestador (principal + adicionais)"""
    emails = [prestador_info['email']]  # Email principal
    
    # Adicionar emails adicionais se existirem
    if prestador_info.get('emails_adicionais'):
        emails_extras = [email.strip() for email in prestador_info['emails_adicionais'].split(',') if email.strip()]
        emails.extend(emails_extras)
    
    return emails

def get_montador_emails(montador_info):
    """Retorna lista de todos os emails do montador (principal + adicionais)"""
    emails = [montador_info['email']]  # Email principal
    
    # Adicionar emails adicionais se existirem
    if montador_info.get('emails_adicionais'):
        emails_extras = [email.strip() for email in montador_info['emails_adicionais'].split(',') if email.strip()]
        emails.extend(emails_extras)
    
    return emails

# --- Funções de Lote de Serviço ---
def criar_lote_servico(prestador_id, prestador_nome, periodo, valor_total, items_raw):
    conn = get_db_connection()
    now = datetime.datetime.now()
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO lotes_servico (prestador_id, prestador_nome, periodo, valor_total, data_envio) VALUES (%s, %s, %s, %s, %s) RETURNING id",
            (prestador_id, prestador_nome, periodo, valor_total, now)
        )
        lote_id = cur.fetchone()[0]
        
        for item in items_raw:
            cur.execute(
                "INSERT INTO os_enviadas (lote_id, os_numero, detalhes) VALUES (%s, %s, %s)",
                (lote_id, item.get('o_s'), psycopg2.extras.Json(item))
            )
    conn.commit()
    conn.close()
    return lote_id

def atualizar_lote_com_conversation_id(lote_id, conversation_id):
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute('UPDATE lotes_servico SET conversation_id = %s WHERE id = %s', (conversation_id, lote_id))
    conn.commit()
    conn.close()

def get_all_lotes_servico():
    conn = get_db_connection()
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        cur.execute('SELECT * FROM lotes_servico ORDER BY data_envio DESC')
        lotes = cur.fetchall()
    conn.close()
    return lotes

def get_os_by_lote_id(lote_id):
    conn = get_db_connection()
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        cur.execute('SELECT * FROM os_enviadas WHERE lote_id = %s', (lote_id,))
        os_list = cur.fetchall()
    conn.close()
    return os_list

def check_os_list(os_numbers):
    if not os_numbers: return []
    conn = get_db_connection()
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        cur.execute('SELECT os_numero FROM os_enviadas WHERE os_numero = ANY(%s)', (os_numbers,))
        sent_os = [row['os_numero'] for row in cur.fetchall()]
    conn.close()
    return sent_os

def update_lote_servico_status(lote_id, status):
    conn = get_db_connection()
    with conn.cursor() as cur: cur.execute('UPDATE lotes_servico SET status = %s WHERE id = %s', (status, lote_id))
    conn.commit()
    conn.close()

def update_lote_servico_attachment(lote_id, anexo_path):
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute('UPDATE lotes_servico SET anexo_path = %s, status = %s WHERE id = %s', (anexo_path, 'N.F. RECEBIDA', lote_id))
    conn.commit()
    conn.close()

def delete_lote_servico(lote_id):
    conn = get_db_connection()
    with conn.cursor() as cur: cur.execute('DELETE FROM lotes_servico WHERE id = %s', (lote_id,))
    conn.commit()
    conn.close()

def get_lote_servico_by_conversation_id(conversation_id):
    conn = get_db_connection()
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        cur.execute('SELECT * FROM lotes_servico WHERE conversation_id = %s', (conversation_id,))
        lote = cur.fetchone()
    conn.close()
    return lote

# --- Funções de Montadores ---
def add_montador(nome, identificador, email, percentual_comissao, auxilio_semanal, fornecedor_id, regra_envio, dias_envio, emails_adicionais=None):
    conn = get_db_connection()
    try:
        with conn.cursor() as cur: 
            cur.execute('INSERT INTO montadores (nome, identificador, email, percentual_comissao, auxilio_semanal, fornecedor_id, regra_envio, dias_envio, emails_adicionais) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)', 
                       (nome, identificador, email, percentual_comissao, auxilio_semanal, fornecedor_id, regra_envio, dias_envio, emails_adicionais))
        conn.commit()
        return True, "Montador adicionado!"
    except psycopg2.IntegrityError: return False, f"Erro: Identificador ou Fornecedor ID já existem."
    finally: conn.close()

def update_montador(montador_id, email, percentual_comissao, auxilio_semanal, ativo, regra_envio, dias_envio, fornecedor_id=None, emails_adicionais=None):
    conn = get_db_connection()
    with conn.cursor() as cur:
        if fornecedor_id is not None and emails_adicionais is not None:
            cur.execute('UPDATE montadores SET email = %s, percentual_comissao = %s, auxilio_semanal = %s, ativo = %s, regra_envio = %s, dias_envio = %s, fornecedor_id = %s, emails_adicionais = %s WHERE id = %s', 
                       (email, percentual_comissao, auxilio_semanal, ativo, regra_envio, dias_envio, fornecedor_id, emails_adicionais, montador_id))
        elif fornecedor_id is not None:
            cur.execute('UPDATE montadores SET email = %s, percentual_comissao = %s, auxilio_semanal = %s, ativo = %s, regra_envio = %s, dias_envio = %s, fornecedor_id = %s WHERE id = %s', 
                       (email, percentual_comissao, auxilio_semanal, ativo, regra_envio, dias_envio, fornecedor_id, montador_id))
        elif emails_adicionais is not None:
            cur.execute('UPDATE montadores SET email = %s, percentual_comissao = %s, auxilio_semanal = %s, ativo = %s, regra_envio = %s, dias_envio = %s, emails_adicionais = %s WHERE id = %s', 
                       (email, percentual_comissao, auxilio_semanal, ativo, regra_envio, dias_envio, emails_adicionais, montador_id))
        else:
            cur.execute('UPDATE montadores SET email = %s, percentual_comissao = %s, auxilio_semanal = %s, ativo = %s, regra_envio = %s, dias_envio = %s WHERE id = %s', 
                       (email, percentual_comissao, auxilio_semanal, ativo, regra_envio, dias_envio, montador_id))
    conn.commit()
    conn.close()

def get_all_montadores(apenas_ativos=False):
    conn = get_db_connection()
    query = 'SELECT * FROM montadores ORDER BY nome ASC'
    if apenas_ativos:
        query = 'SELECT * FROM montadores WHERE ativo = TRUE ORDER BY nome ASC'
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        cur.execute(query)
        montadores = cur.fetchall()
    conn.close()
    return montadores

def get_montador_by_id(montador_id):
    conn = get_db_connection()
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        cur.execute('SELECT * FROM montadores WHERE id = %s', (montador_id,))
        montador = cur.fetchone()
    conn.close()
    return montador

def get_montador_by_identificador(identificador):
    conn = get_db_connection()
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        cur.execute('SELECT * FROM montadores WHERE identificador = %s', (identificador,))
        montador = cur.fetchone()
    conn.close()
    return montador

def log_sent_montagem(montador_id, group_details, conversation_id):
    conn = get_db_connection()
    now = datetime.datetime.now()
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO envios_montagem (montador_id, data_envio, detalhes, conversation_id) VALUES (%s, %s, %s, %s)",
            (montador_id, now, psycopg2.extras.Json(group_details), conversation_id)
        )
    conn.commit()
    conn.close()

def get_envio_montagem_by_conversation_id(conversation_id):
    conn = get_db_connection()
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        cur.execute('SELECT * FROM envios_montagem WHERE conversation_id = %s', (conversation_id,))
        envio = cur.fetchone()
    conn.close()
    return envio

def update_montagem_attachment(envio_id, anexo_path):
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute('UPDATE envios_montagem SET anexo_path = %s, status = %s WHERE id = %s', (anexo_path, 'N.F. RECEBIDA', envio_id))
    conn.commit()
    conn.close()

def get_all_sent_montagens():
    conn = get_db_connection()
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        cur.execute('SELECT e.*, m.nome as montador_nome FROM envios_montagem e LEFT JOIN montadores m ON e.montador_id = m.id ORDER BY data_envio DESC')
        history = cur.fetchall()
    conn.close()
    return history

def get_montagens_by_montador_id(montador_id):
    """Retorna histórico de montagens por montador específico"""
    conn = get_db_connection()
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        cur.execute('SELECT e.*, m.nome as montador_nome FROM envios_montagem e LEFT JOIN montadores m ON e.montador_id = m.id WHERE e.montador_id = %s ORDER BY data_envio DESC', (montador_id,))
        history = cur.fetchall()
    conn.close()
    return history

def update_montagem_status(envio_id, status):
    conn = get_db_connection()
    with conn.cursor() as cur: cur.execute('UPDATE envios_montagem SET status = %s WHERE id = %s', (status, envio_id))
    conn.commit()
    conn.close()

def update_montagem_details(envio_id, details):
    conn = get_db_connection()
    with conn.cursor() as cur: cur.execute('UPDATE envios_montagem SET detalhes = %s WHERE id = %s', (json.dumps(details), envio_id))
    conn.commit()
    conn.close()

def delete_envio_montagem(envio_id):
    conn = get_db_connection()
    with conn.cursor() as cur: cur.execute('DELETE FROM envios_montagem WHERE id = %s', (envio_id,))
    conn.commit()
    conn.close()

def check_boletim_list(boletim_ids):
    if not boletim_ids: return []
    conn = get_db_connection()
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        cur.execute("SELECT DISTINCT elem ->> 'boletim' as sent_boletim FROM envios_montagem, jsonb_array_elements(detalhes -> 'items') elem WHERE elem ->> 'boletim' = ANY(%s)", (boletim_ids,))
        sent_boletins = [row['sent_boletim'] for row in cur.fetchall()]
    conn.close()
    return sent_boletins

def get_envios_na_semana(tipo, entidade_id, ano, semana):
    conn = get_db_connection()
    table = "lotes_servico" if tipo == 'prestador' else "envios_montagem"
    id_col = "prestador_id" if tipo == 'prestador' else "montador_id"
    with conn.cursor() as cur:
        cur.execute(f"SELECT COUNT(*) FROM {table} WHERE {id_col} = %s AND EXTRACT(YEAR FROM data_envio) = %s AND EXTRACT(WEEK FROM data_envio) = %s", (entidade_id, ano, semana))
        count = cur.fetchone()[0]
    conn.close()
    return count > 0

def foi_ignorado_na_semana(tipo, entidade_id, ano, semana):
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM envios_ignorados WHERE tipo = %s AND entidade_id = %s AND ano = %s AND periodo_chave = %s", (tipo, entidade_id, ano, f"semana_{semana}"))
        count = cur.fetchone()[0]
    conn.close()
    return count > 0

def ignorar_envio_semanal(tipo, entidade_id, ano, semana):
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute("INSERT INTO envios_ignorados (tipo, entidade_id, ano, periodo_chave, data_ignorada) VALUES (%s, %s, %s, %s, %s) ON CONFLICT (tipo, entidade_id, ano, periodo_chave) DO NOTHING", (tipo, entidade_id, ano, f"semana_{semana}", datetime.datetime.now()))
    conn.commit()
    conn.close()

# --- Funções de Blacklist de Boletins ---
def adicionar_boletim_blacklist(montador_id, boletim, motivo=None):
    """Adiciona um boletim à blacklist de um montador"""
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO boletins_blacklist (montador_id, boletim, motivo) VALUES (%s, %s, %s)",
                (montador_id, boletim, motivo)
            )
        conn.commit()
        return True, "Boletim adicionado à blacklist!"
    except psycopg2.IntegrityError:
        return False, "Este boletim já está na blacklist"
    finally:
        conn.close()

def remover_boletim_blacklist(montador_id, boletim):
    """Remove um boletim da blacklist de um montador"""
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute(
            "DELETE FROM boletins_blacklist WHERE montador_id = %s AND boletim = %s",
            (montador_id, boletim)
        )
    conn.commit()
    conn.close()

def get_boletins_blacklist(montador_id=None):
    """Retorna todos os boletins na blacklist, filtrados por montador se especificado"""
    conn = get_db_connection()
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        if montador_id:
            cur.execute('''
                SELECT b.*, m.nome as montador_nome 
                FROM boletins_blacklist b 
                JOIN montadores m ON b.montador_id = m.id 
                WHERE b.montador_id = %s 
                ORDER BY b.data_adicao DESC
            ''', (montador_id,))
        else:
            cur.execute('''
                SELECT b.*, m.nome as montador_nome 
                FROM boletins_blacklist b 
                JOIN montadores m ON b.montador_id = m.id 
                ORDER BY b.data_adicao DESC
            ''')
        return cur.fetchall()

def check_boletins_blacklist(boletim_ids):
    """Verifica quais boletins estão na blacklist"""
    if not boletim_ids:
        return []
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute(
            "SELECT boletim FROM boletins_blacklist WHERE boletim = ANY(%s)",
            (boletim_ids,)
        )
        blacklisted = [row[0] for row in cur.fetchall()]
    conn.close()
    return blacklisted

# --- Funções de Blacklist de OS (Prestadores) ---
def adicionar_os_blacklist(prestador_id, os_numero, motivo=None):
    """Adiciona uma OS à blacklist de um prestador"""
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO os_blacklist (prestador_id, os_numero, motivo) VALUES (%s, %s, %s)",
                (prestador_id, os_numero, motivo)
            )
        conn.commit()
        return True, "OS adicionada à blacklist!"
    except psycopg2.IntegrityError:
        return False, "Esta OS já está na blacklist"
    finally:
        conn.close()

def remover_os_blacklist(prestador_id, os_numero):
    """Remove uma OS da blacklist de um prestador"""
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute(
            "DELETE FROM os_blacklist WHERE prestador_id = %s AND os_numero = %s",
            (prestador_id, os_numero)
        )
    conn.commit()
    conn.close()

def get_os_blacklist(prestador_id=None):
    """Retorna todas as OS na blacklist, filtradas por prestador se especificado"""
    conn = get_db_connection()
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        if prestador_id:
            cur.execute('''
                SELECT o.*, p.nome as prestador_nome 
                FROM os_blacklist o 
                JOIN prestadores p ON o.prestador_id = p.id 
                WHERE o.prestador_id = %s 
                ORDER BY o.data_adicao DESC
            ''', (prestador_id,))
        else:
            cur.execute('''
                SELECT o.*, p.nome as prestador_nome 
                FROM os_blacklist o 
                JOIN prestadores p ON o.prestador_id = p.id 
                ORDER BY o.data_adicao DESC
            ''')
        return cur.fetchall()

def check_os_blacklist(os_numbers):
    """Verifica quais OS estão na blacklist"""
    if not os_numbers:
        return []
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute(
            "SELECT os_numero FROM os_blacklist WHERE os_numero = ANY(%s)",
            (os_numbers,)
        )
        blacklisted = [row[0] for row in cur.fetchall()]
    conn.close()
    return blacklisted

run_migrations()