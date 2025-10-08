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

        # Migrações para adicionar colunas se não existirem
        cur.execute("ALTER TABLE lotes_servico ADD COLUMN IF NOT EXISTS prestador_id INTEGER REFERENCES prestadores(id);")
        cur.execute("ALTER TABLE envios_montagem ADD COLUMN IF NOT EXISTS montador_id INTEGER REFERENCES montadores(id);")
        cur.execute("ALTER TABLE envios_montagem DROP COLUMN IF EXISTS montador_identificador;")
        
        # Adicionar coluna para múltiplos emails em prestadores
        cur.execute("ALTER TABLE prestadores ADD COLUMN IF NOT EXISTS emails_adicionais TEXT;")
        
        # Adicionar coluna para múltiplos emails em montadores
        cur.execute("ALTER TABLE montadores ADD COLUMN IF NOT EXISTS emails_adicionais TEXT;")


        cur.execute('''CREATE TABLE IF NOT EXISTS lotes_servico (id SERIAL PRIMARY KEY, prestador_id INTEGER REFERENCES prestadores(id), prestador_nome TEXT, periodo TEXT NOT NULL, valor_total REAL NOT NULL, data_envio TIMESTAMP NOT NULL, status TEXT NOT NULL DEFAULT 'Em Aberto', conversation_id TEXT, anexo_path TEXT)''')
        cur.execute('''CREATE TABLE IF NOT EXISTS os_enviadas (id SERIAL PRIMARY KEY, lote_id INTEGER REFERENCES lotes_servico(id) ON DELETE CASCADE, os_numero TEXT NOT NULL UNIQUE, detalhes JSONB)''')
        cur.execute('''CREATE TABLE IF NOT EXISTS envios_montagem (id SERIAL PRIMARY KEY, montador_id INTEGER REFERENCES montadores(id), data_envio TIMESTAMP NOT NULL, status TEXT NOT NULL DEFAULT 'Em Aberto', detalhes JSONB, conversation_id TEXT, anexo_path TEXT)''')
        cur.execute('''CREATE UNIQUE INDEX IF NOT EXISTS idx_unique_montagem ON envios_montagem ((detalhes->>'periodo_relatorio'), montador_id);''')
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
        
        # Nova tabela para tokens únicos de upload de NF
        cur.execute('''CREATE TABLE IF NOT EXISTS upload_tokens (
            id SERIAL PRIMARY KEY,
            token TEXT NOT NULL UNIQUE,
            tipo TEXT NOT NULL, -- 'prestador' ou 'montador'
            entidade_id INTEGER NOT NULL, -- ID do prestador ou montador
            lote_id INTEGER, -- ID do lote (para prestadores) ou envio (para montadores)
            data_criacao TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            data_expiracao TIMESTAMP NOT NULL,
            usado BOOLEAN NOT NULL DEFAULT FALSE,
            data_upload TIMESTAMP,
            arquivo_nome TEXT,
            arquivo_path TEXT
        )''')
        cur.execute('''CREATE INDEX IF NOT EXISTS idx_upload_tokens_token ON upload_tokens (token);''')
        cur.execute('''CREATE INDEX IF NOT EXISTS idx_upload_tokens_entidade ON upload_tokens (tipo, entidade_id);''')

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
            "INSERT INTO envios_montagem (montador_id, data_envio, detalhes, conversation_id) VALUES (%s, %s, %s, %s) RETURNING id",
            (montador_id, now, psycopg2.extras.Json(group_details), conversation_id)
        )
        envio_id = cur.fetchone()[0]
    conn.commit()
    conn.close()
    return envio_id

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

# --- Funções de Upload de Notas Fiscais ---
import uuid
import secrets

def gerar_token_upload(tipo, entidade_id, lote_id=None, dias_expiracao=30):
    """Gera um token único para upload de nota fiscal"""
    conn = get_db_connection()
    token = secrets.token_urlsafe(32)
    data_expiracao = datetime.datetime.now() + datetime.timedelta(days=dias_expiracao)
    
    with conn.cursor() as cur:
        cur.execute(
            """INSERT INTO upload_tokens (token, tipo, entidade_id, lote_id, data_expiracao) 
               VALUES (%s, %s, %s, %s, %s) RETURNING id""",
            (token, tipo, entidade_id, lote_id, data_expiracao)
        )
        token_id = cur.fetchone()[0]
    
    conn.commit()
    conn.close()
    return token, token_id

def validar_token_upload(token):
    """Valida se o token existe e não expirou"""
    conn = get_db_connection()
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        cur.execute(
            """SELECT t.*, 
                      CASE WHEN t.tipo = 'prestador' THEN p.nome ELSE m.nome END as entidade_nome,
                      CASE WHEN t.tipo = 'prestador' THEN p.email ELSE m.email END as entidade_email
               FROM upload_tokens t 
               LEFT JOIN prestadores p ON t.tipo = 'prestador' AND t.entidade_id = p.id
               LEFT JOIN montadores m ON t.tipo = 'montador' AND t.entidade_id = m.id
               WHERE t.token = %s AND t.data_expiracao > NOW() AND t.usado = FALSE""",
            (token,)
        )
        token_info = cur.fetchone()
    conn.close()
    return dict(token_info) if token_info else None

def marcar_token_usado(token, arquivo_nome, arquivo_path):
    """Marca o token como usado após o upload e atualiza status do lote/envio"""
    conn = get_db_connection()
    with conn.cursor() as cur:
        # Primeiro, buscar informações do token
        cur.execute(
            """SELECT tipo, lote_id FROM upload_tokens WHERE token = %s""",
            (token,)
        )
        token_info = cur.fetchone()
        
        if token_info:
            tipo, lote_id = token_info
            
            # Marcar token como usado
            cur.execute(
                """UPDATE upload_tokens 
                   SET usado = TRUE, data_upload = NOW(), arquivo_nome = %s, arquivo_path = %s 
                   WHERE token = %s""",
                (arquivo_nome, arquivo_path, token)
            )
            
            # Atualizar status do lote ou envio para "NF RECEBIDA"
            if tipo == 'prestador' and lote_id:
                cur.execute(
                    """UPDATE lotes_servico 
                       SET status = 'NF RECEBIDA', anexo_path = %s 
                       WHERE id = %s""",
                    (arquivo_path, lote_id)
                )
            elif tipo == 'montador' and lote_id:
                cur.execute(
                    """UPDATE envios_montagem 
                       SET status = 'NF RECEBIDA', anexo_path = %s 
                       WHERE id = %s""",
                    (arquivo_path, lote_id)
                )
    
    conn.commit()
    conn.close()
    
    # Retornar informações para notificação
    return token_info

def get_dados_para_notificacao(tipo, lote_id):
    """Busca dados completos para notificação de upload"""
    conn = get_db_connection()
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        if tipo == 'prestador':
            cur.execute(
                """SELECT l.*, p.nome as prestador_nome, p.email as prestador_email
                   FROM lotes_servico l 
                   JOIN prestadores p ON l.prestador_id = p.id 
                   WHERE l.id = %s""",
                (lote_id,)
            )
        else:  # montador
            cur.execute(
                """SELECT e.*, m.nome as montador_nome, m.email as montador_email,
                          e.detalhes->>'periodo_relatorio' as periodo
                   FROM envios_montagem e 
                   JOIN montadores m ON e.montador_id = m.id 
                   WHERE e.id = %s""",
                (lote_id,)
            )
        
        resultado = cur.fetchone()
    conn.close()
    return dict(resultado) if resultado else None

def get_uploads_por_entidade(tipo, entidade_id):
    """Retorna histórico de uploads de uma entidade"""
    conn = get_db_connection()
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        cur.execute(
            """SELECT * FROM upload_tokens 
               WHERE tipo = %s AND entidade_id = %s AND usado = TRUE 
               ORDER BY data_upload DESC""",
            (tipo, entidade_id)
        )
        uploads = cur.fetchall()
    conn.close()
    return uploads

def get_token_info_completa(token):
    """Retorna informações completas do token incluindo dados do lote/envio"""
    conn = get_db_connection()
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        cur.execute(
            """SELECT t.*, 
                      CASE WHEN t.tipo = 'prestador' THEN p.nome ELSE m.nome END as entidade_nome,
                      CASE WHEN t.tipo = 'prestador' THEN p.email ELSE m.email END as entidade_email,
                      CASE WHEN t.tipo = 'prestador' THEN l.periodo ELSE e.detalhes->>'periodo_relatorio' END as periodo,
                      CASE WHEN t.tipo = 'prestador' THEN l.valor_total ELSE NULL END as valor_total
               FROM upload_tokens t 
               LEFT JOIN prestadores p ON t.tipo = 'prestador' AND t.entidade_id = p.id
               LEFT JOIN montadores m ON t.tipo = 'montador' AND t.entidade_id = m.id
               LEFT JOIN lotes_servico l ON t.tipo = 'prestador' AND t.lote_id = l.id
               LEFT JOIN envios_montagem e ON t.tipo = 'montador' AND t.lote_id = e.id
               WHERE t.token = %s""",
            (token,)
        )
        token_info = cur.fetchone()
    conn.close()
    return dict(token_info) if token_info else None

def get_upload_info_por_lote(tipo, lote_id):
    """Retorna informações de upload por lote/envio"""
    conn = get_db_connection()
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        cur.execute(
            """SELECT * FROM upload_tokens 
               WHERE tipo = %s AND lote_id = %s 
               ORDER BY data_criacao DESC LIMIT 1""",
            (tipo, lote_id)
        )
        upload_info = cur.fetchone()
    conn.close()
    return dict(upload_info) if upload_info else None

def listar_pagamentos_enviados():
    """Lista todos os pagamentos enviados (prestadores e montadores) com status de upload"""
    conn = get_db_connection()
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            # Buscar prestadores
            cur.execute("""
                SELECT 
                    'prestador' as tipo,
                    l.id as lote_id,
                    l.prestador_nome as entidade_nome,
                    p.email as entidade_email,
                    l.periodo,
                    l.valor_total,
                    l.data_envio,
                    l.status,
                    ut.token,
                    ut.usado as upload_feito,
                    ut.data_upload,
                    ut.arquivo_nome,
                    ut.data_expiracao as token_expira
                FROM lotes_servico l
                JOIN prestadores p ON l.prestador_id = p.id
                LEFT JOIN upload_tokens ut ON ut.tipo = 'prestador' AND ut.entidade_id = p.id AND ut.lote_id = l.id
                ORDER BY l.data_envio DESC
            """)
            prestadores = cur.fetchall()
            
            # Buscar montadores
            cur.execute("""
                SELECT 
                    'montador' as tipo,
                    e.id as lote_id,
                    m.nome as entidade_nome,
                    m.email as entidade_email,
                    (e.detalhes->>'periodo_relatorio') as periodo,
                    CAST(e.detalhes->>'total_geral' AS REAL) as valor_total,
                    e.data_envio,
                    e.status,
                    ut.token,
                    ut.usado as upload_feito,
                    ut.data_upload,
                    ut.arquivo_nome,
                    ut.data_expiracao as token_expira
                FROM envios_montagem e
                JOIN montadores m ON e.montador_id = m.id
                LEFT JOIN upload_tokens ut ON ut.tipo = 'montador' AND ut.entidade_id = m.id AND ut.lote_id = e.id
                ORDER BY e.data_envio DESC
            """)
            montadores = cur.fetchall()
            
            # Combinar e ordenar por data
            todos_pagamentos = list(prestadores) + list(montadores)
            todos_pagamentos.sort(key=lambda x: x['data_envio'], reverse=True)
            
            return [dict(p) for p in todos_pagamentos]
            
    finally:
        conn.close()

def editar_pagamento_prestador(lote_id, novo_valor, novo_periodo=None):
    """Edita valor e período de um lote de prestador"""
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            if novo_periodo:
                cur.execute("""
                    UPDATE lotes_servico 
                    SET valor_total = %s, periodo = %s
                    WHERE id = %s
                """, (novo_valor, novo_periodo, lote_id))
            else:
                cur.execute("""
                    UPDATE lotes_servico 
                    SET valor_total = %s
                    WHERE id = %s
                """, (novo_valor, lote_id))
            
            conn.commit()
            return cur.rowcount > 0
    finally:
        conn.close()

def editar_pagamento_montador(envio_id, novo_valor, novo_periodo=None):
    """Edita valor e período de um envio de montador"""
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            # Obter detalhes atuais
            cur.execute("SELECT detalhes FROM envios_montagem WHERE id = %s", (envio_id,))
            resultado = cur.fetchone()
            if not resultado:
                return False
            
            detalhes = resultado[0]
            detalhes['total_geral'] = novo_valor
            
            if novo_periodo:
                detalhes['periodo_relatorio'] = novo_periodo
            
            # Atualizar
            cur.execute("""
                UPDATE envios_montagem 
                SET detalhes = %s
                WHERE id = %s
            """, (json.dumps(detalhes), envio_id))
            
            conn.commit()
            return cur.rowcount > 0
    finally:
        conn.close()

def invalidar_token_antigo(tipo, entidade_id, lote_id):
    """Invalida token antigo para permitir reenvio"""
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                DELETE FROM upload_tokens 
                WHERE tipo = %s AND entidade_id = %s AND lote_id = %s
            """, (tipo, entidade_id, lote_id))
            conn.commit()
            return cur.rowcount > 0
    finally:
        conn.close()

def prestador_info(lote_id):
    """Obter informações do prestador por lote_id"""
    conn = get_db_connection()
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute("""
                SELECT p.id, p.nome, p.email 
                FROM prestadores p
                JOIN lotes_servico l ON p.id = l.prestador_id
                WHERE l.id = %s
            """, (lote_id,))
            resultado = cur.fetchone()
            return dict(resultado) if resultado else None
    finally:
        conn.close()

def montador_info(envio_id):
    """Obter informações do montador por envio_id"""
    conn = get_db_connection()
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute("""
                SELECT m.id, m.nome, m.email 
                FROM montadores m
                JOIN envios_montagem e ON m.id = e.montador_id
                WHERE e.id = %s
            """, (envio_id,))
            resultado = cur.fetchone()
            return dict(resultado) if resultado else None
    finally:
        conn.close()

def get_lote_by_id(lote_id):
    """Obter dados completos de um lote por ID"""
    conn = get_db_connection()
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute("""
                SELECT l.*, p.nome as prestador_nome, p.email as prestador_email
                FROM lotes_servico l
                JOIN prestadores p ON l.prestador_id = p.id
                WHERE l.id = %s
            """, (lote_id,))
            resultado = cur.fetchone()
            return dict(resultado) if resultado else None
    finally:
        conn.close()

def get_envio_by_id(envio_id):
    """Obter dados completos de um envio por ID"""
    conn = get_db_connection()
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute("""
                SELECT e.*, m.nome as montador_nome, m.email as montador_email
                FROM envios_montagem e
                JOIN montadores m ON e.montador_id = m.id
                WHERE e.id = %s
            """, (envio_id,))
            resultado = cur.fetchone()
            return dict(resultado) if resultado else None
    finally:
        conn.close()

def update_os_detalhes(os_id, novos_detalhes):
    """Atualizar detalhes de uma O.S. específica"""
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE os_enviadas 
                SET detalhes = %s
                WHERE id = %s
            """, (json.dumps(novos_detalhes), os_id))
            conn.commit()
            return cur.rowcount > 0
    finally:
        conn.close()

def update_lote_valor_total(lote_id, novo_valor):
    """Atualizar valor total de um lote"""
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE lotes_servico 
                SET valor_total = %s
                WHERE id = %s
            """, (novo_valor, lote_id))
            conn.commit()
            return cur.rowcount > 0
    finally:
        conn.close()

run_migrations()