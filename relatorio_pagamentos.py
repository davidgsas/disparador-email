"""
Módulo para geração de relatórios de pagamentos
"""

import database as db
from datetime import datetime, date
from typing import Optional, Dict, List
from jinja2 import Environment, FileSystemLoader
import os


def gerar_pdf_relatorio(prestador_id: int, data_inicio: Optional[str] = None, data_fim: Optional[str] = None) -> bytes:
    """
    Gera PDF do relatório de pagamentos
    
    Args:
        prestador_id: ID do prestador
        data_inicio: Data início no formato YYYY-MM-DD (opcional)
        data_fim: Data fim no formato YYYY-MM-DD (opcional)
        
    Returns:
        bytes: Conteúdo do PDF gerado
    """
    # Buscar dados do relatório
    dados = get_relatorio_pagamentos_prestador(prestador_id, data_inicio, data_fim)
    
    if not dados:
        raise ValueError(f"Prestador {prestador_id} não encontrado")
    
    # Configurar Jinja2
    template_dir = os.path.join(os.path.dirname(__file__), 'templates')
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template('relatorio_pagamentos.html')
    
    # Renderizar HTML
    html_content = template.render(**dados)
    
    # Configurar variáveis de ambiente para WeasyPrint
    os.environ['DYLD_LIBRARY_PATH'] = '/opt/homebrew/lib:' + os.environ.get('DYLD_LIBRARY_PATH', '')
    
    # Gerar PDF com WeasyPrint
    from weasyprint import HTML
    pdf_bytes = HTML(string=html_content, base_url=template_dir).write_pdf()
    
    return pdf_bytes

def get_relatorio_pagamentos_prestador(prestador_id: int, data_inicio: Optional[str] = None, data_fim: Optional[str] = None) -> Dict:
    """
    Busca dados de pagamentos de um prestador
    
    Args:
        prestador_id: ID do prestador
        data_inicio: Data início no formato YYYY-MM-DD (opcional)
        data_fim: Data fim no formato YYYY-MM-DD (opcional)
        
    Returns:
        Dict com:
            - prestador: dados do prestador
            - lotes_pagos: lista de lotes pagos
            - lotes_pendentes: lista de lotes não pagos
            - totais: resumo dos totais
    """
    
    conn = db.get_db_connection()
    cur = conn.cursor()
    
    # Buscar dados do prestador
    cur.execute("""
        SELECT id, nome, email, telefone, fornecedor_id
        FROM prestadores
        WHERE id = %s
    """, (prestador_id,))
    
    prestador = cur.fetchone()
    
    if not prestador:
        conn.close()
        return None
    
    prestador_dict = {
        'id': prestador[0],
        'nome': prestador[1],
        'email': prestador[2],
        'telefone': prestador[3],
        'fornecedor_id': prestador[4]
    }
    
    # Query base para lotes
    query_base = """
        SELECT 
            l.id,
            l.periodo,
            l.valor_total,
            l.data_envio,
            l.status,
            l.nota_fiscal_path,
            l.data_pagamento,
            l.data_vencimento_pagamento,
            l.link_upload,
            l.conversation_id,
            l.data_recebimento_nf
        FROM lotes_servico l
        WHERE l.prestador_id = %s
    """
    
    params = [prestador_id]
    
    # Adicionar filtros de data se fornecidos
    if data_inicio:
        query_base += " AND l.data_envio >= %s"
        params.append(data_inicio)
    
    if data_fim:
        query_base += " AND l.data_envio <= %s"
        params.append(data_fim)
    
    query_base += " ORDER BY l.data_envio DESC"
    
    # Buscar todos os lotes
    cur.execute(query_base, params)
    lotes = cur.fetchall()
    
    conn.close()
    
    # Separar lotes pagos e pendentes
    lotes_pagos = []
    lotes_pendentes = []
    
    for lote in lotes:
        lote_dict = {
            'id': lote[0],
            'periodo': lote[1],
            'valor_total': float(lote[2]) if lote[2] else 0.0,
            'data_envio': lote[3],
            'status': lote[4],
            'nota_fiscal_path': lote[5],
            'data_pagamento': lote[6],
            'vencimento': lote[7],
            'link_upload': lote[8],
            'conversation_id': lote[9],
            'data_recebimento_nf': lote[10],
            'tem_nota_fiscal': bool(lote[5]),
            'dias_vencido': None,
            'quantidade_os': 0  # Não temos esse campo, mas vamos adicionar para compatibilidade
        }
        
        # Calcular dias de vencimento se tiver data de vencimento e não estiver pago
        if lote[7] and lote[4] != 'PAGO':
            vencimento_date = lote[7] if isinstance(lote[7], date) else datetime.strptime(str(lote[7]), '%Y-%m-%d').date()
            hoje = date.today()
            dias_diff = (hoje - vencimento_date).days
            if dias_diff > 0:
                lote_dict['dias_vencido'] = dias_diff
        
        # Verificar se foi pago (status = 'PAGO')
        if lote[5] == 'PAGO':
            lotes_pagos.append(lote_dict)
        else:
            lotes_pendentes.append(lote_dict)
    
    # Calcular totais
    total_pago = sum(l['valor_total'] for l in lotes_pagos)
    total_pendente = sum(l['valor_total'] for l in lotes_pendentes)
    total_geral = total_pago + total_pendente
    
    return {
        'prestador': prestador_dict,
        'lotes_pagos': lotes_pagos,
        'lotes_pendentes': lotes_pendentes,
        'totais': {
            'pago': total_pago,
            'pendente': total_pendente,
            'geral': total_geral,
            'quantidade_pagos': len(lotes_pagos),
            'quantidade_pendentes': len(lotes_pendentes),
            'quantidade_total': len(lotes_pagos) + len(lotes_pendentes)
        },
        'data_geracao': datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
        'periodo_filtro': {
            'inicio': data_inicio,
            'fim': data_fim
        }
    }



def get_lista_prestadores_com_lotes() -> List[Dict]:
    """
    Retorna lista de prestadores que têm lotes cadastrados
    """
    conn = db.get_db_connection()
    cur = conn.cursor()
    
    cur.execute("""
        SELECT DISTINCT
            p.id,
            p.nome,
            COUNT(l.id) as total_lotes,
            SUM(CASE WHEN l.status = 'PAGO' THEN l.valor_total ELSE 0 END) as total_pago,
            SUM(CASE WHEN l.status != 'PAGO' THEN l.valor_total ELSE 0 END) as total_pendente
        FROM prestadores p
        INNER JOIN lotes_servico l ON l.prestador_id = p.id
        GROUP BY p.id, p.nome
        ORDER BY p.nome
    """)
    
    prestadores = []
    for row in cur.fetchall():
        prestadores.append({
            'id': row[0],
            'nome': row[1],
            'total_lotes': row[2],
            'total_pago': float(row[3]) if row[3] else 0.0,
            'total_pendente': float(row[4]) if row[4] else 0.0,
            'total_geral': float(row[3] or 0) + float(row[4] or 0)
        })
    
    conn.close()
    return prestadores


def get_os_detalhadas_prestador(prestador_id: int, data_inicio: Optional[str] = None, data_fim: Optional[str] = None) -> List[Dict]:
    """
    Retorna lista detalhada de todas as O.S. de um prestador
    
    Args:
        prestador_id: ID do prestador
        data_inicio: Data início filtro (YYYY-MM-DD)
        data_fim: Data fim filtro (YYYY-MM-DD)
        
    Returns:
        Lista de dicionários com dados detalhados de cada O.S.
    """
    conn = db.get_db_connection()
    cur = conn.cursor()
    
    # Query para buscar O.S. com todos os detalhes do JSONB
    query = """
        SELECT 
            ls.id as lote_id,
            ls.periodo as lote_periodo,
            ls.status as lote_status,
            ls.data_envio as lote_data_envio,
            ls.data_pagamento as lote_data_pagamento,
            ls.data_recebimento_nf as lote_data_recebimento_nf,
            os.os_numero,
            os.detalhes
        FROM lotes_servico ls
        INNER JOIN os_enviadas os ON os.lote_id = ls.id
        WHERE ls.prestador_id = %s
    """
    
    params = [prestador_id]
    
    if data_inicio:
        query += " AND ls.data_envio >= %s"
        params.append(data_inicio)
    
    if data_fim:
        query += " AND ls.data_envio <= %s"
        params.append(data_fim)
    
    query += " ORDER BY ls.id DESC, os.os_numero"
    
    cur.execute(query, params)
    
    os_list = []
    for row in cur.fetchall():
        detalhes = row[7]  # Campo JSONB
        
        # Extrair dados do JSONB
        valor = float(detalhes.get('valor_custo_prestador', 0)) if detalhes.get('valor_custo_prestador') else 0.0
        valor_extra = float(detalhes.get('valor_extra', 0)) if detalhes.get('valor_extra') else 0.0
        
        os_list.append({
            'lote_id': row[0],
            'lote_periodo': row[1],
            'lote_status': row[2],
            'lote_data_envio': row[3],
            'lote_data_pagamento': row[4],
            'lote_data_recebimento_nf': row[5],
            'numero_os': row[6] or detalhes.get('o_s', ''),  # Usar os_numero ou o_s do JSONB
            'nome_cliente': detalhes.get('cliente', ''),
            'localidade': detalhes.get('localidade', ''),
            'modalidade': detalhes.get('modalidade', ''),
            'data_execucao': detalhes.get('data_execucao', ''),
            'valor': valor,
            'valor_extra': valor_extra,
            'valor_total': valor + valor_extra
        })
    
    conn.close()
    return os_list

