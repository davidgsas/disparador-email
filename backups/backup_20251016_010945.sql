--
-- PostgreSQL database dump
--

\restrict jyDJGisTo1AjQYfsoyIbueakhpi81cUdGaaCrgkvI2QBa5o1apRCfLy5KBSX0lZ

-- Dumped from database version 15.14 (Homebrew)
-- Dumped by pg_dump version 15.14 (Homebrew)

-- Started on 2025-10-16 01:09:46 -03

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 227 (class 1259 OID 16501)
-- Name: boletins_blacklist; Type: TABLE; Schema: public; Owner: davidgabriel
--

CREATE TABLE public.boletins_blacklist (
    id integer NOT NULL,
    montador_id integer,
    boletim text NOT NULL,
    data_adicao timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    motivo text
);


ALTER TABLE public.boletins_blacklist OWNER TO davidgabriel;

--
-- TOC entry 226 (class 1259 OID 16500)
-- Name: boletins_blacklist_id_seq; Type: SEQUENCE; Schema: public; Owner: davidgabriel
--

CREATE SEQUENCE public.boletins_blacklist_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.boletins_blacklist_id_seq OWNER TO davidgabriel;

--
-- TOC entry 3960 (class 0 OID 0)
-- Dependencies: 226
-- Name: boletins_blacklist_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: davidgabriel
--

ALTER SEQUENCE public.boletins_blacklist_id_seq OWNED BY public.boletins_blacklist.id;


--
-- TOC entry 225 (class 1259 OID 16491)
-- Name: envios_ignorados; Type: TABLE; Schema: public; Owner: davidgabriel
--

CREATE TABLE public.envios_ignorados (
    id integer NOT NULL,
    tipo text NOT NULL,
    entidade_id integer NOT NULL,
    ano integer NOT NULL,
    periodo_chave text NOT NULL,
    data_ignorada timestamp without time zone NOT NULL
);


ALTER TABLE public.envios_ignorados OWNER TO davidgabriel;

--
-- TOC entry 224 (class 1259 OID 16490)
-- Name: envios_ignorados_id_seq; Type: SEQUENCE; Schema: public; Owner: davidgabriel
--

CREATE SEQUENCE public.envios_ignorados_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.envios_ignorados_id_seq OWNER TO davidgabriel;

--
-- TOC entry 3961 (class 0 OID 0)
-- Dependencies: 224
-- Name: envios_ignorados_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: davidgabriel
--

ALTER SEQUENCE public.envios_ignorados_id_seq OWNED BY public.envios_ignorados.id;


--
-- TOC entry 223 (class 1259 OID 16475)
-- Name: envios_montagem; Type: TABLE; Schema: public; Owner: davidgabriel
--

CREATE TABLE public.envios_montagem (
    id integer NOT NULL,
    montador_id integer,
    data_envio timestamp without time zone NOT NULL,
    status text DEFAULT 'Em Aberto'::text NOT NULL,
    detalhes jsonb,
    conversation_id text,
    anexo_path text,
    id_controle integer,
    link_upload text,
    validade_link date,
    status_api integer DEFAULT 0,
    data_envio_api timestamp without time zone,
    nota_fiscal_path text,
    api_message text,
    upload_hash text,
    status_arquivo integer DEFAULT 0,
    data_ultima_consulta timestamp without time zone,
    quantidade_os integer,
    montador_nome text,
    periodo text,
    valor_total numeric(10,2)
);


ALTER TABLE public.envios_montagem OWNER TO davidgabriel;

--
-- TOC entry 222 (class 1259 OID 16474)
-- Name: envios_montagem_id_seq; Type: SEQUENCE; Schema: public; Owner: davidgabriel
--

CREATE SEQUENCE public.envios_montagem_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.envios_montagem_id_seq OWNER TO davidgabriel;

--
-- TOC entry 3962 (class 0 OID 0)
-- Dependencies: 222
-- Name: envios_montagem_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: davidgabriel
--

ALTER SEQUENCE public.envios_montagem_id_seq OWNED BY public.envios_montagem.id;


--
-- TOC entry 234 (class 1259 OID 16576)
-- Name: integracoes_config; Type: TABLE; Schema: public; Owner: davidgabriel
--

CREATE TABLE public.integracoes_config (
    id integer DEFAULT 1 NOT NULL,
    trello_api_key text,
    trello_token text,
    trello_board_id text,
    trello_list_id text,
    trello_ativo boolean DEFAULT false,
    data_atualizacao timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT single_row CHECK ((id = 1))
);


ALTER TABLE public.integracoes_config OWNER TO davidgabriel;

--
-- TOC entry 233 (class 1259 OID 16560)
-- Name: jobs_config; Type: TABLE; Schema: public; Owner: davidgabriel
--

CREATE TABLE public.jobs_config (
    id integer NOT NULL,
    nome character varying(100) NOT NULL,
    descricao text,
    ativo boolean DEFAULT true,
    intervalo_minutos integer DEFAULT 60,
    ultima_execucao timestamp without time zone,
    proxima_execucao timestamp without time zone,
    total_execucoes integer DEFAULT 0,
    total_erros integer DEFAULT 0,
    ultima_mensagem text,
    data_criacao timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.jobs_config OWNER TO davidgabriel;

--
-- TOC entry 3963 (class 0 OID 0)
-- Dependencies: 233
-- Name: TABLE jobs_config; Type: COMMENT; Schema: public; Owner: davidgabriel
--

COMMENT ON TABLE public.jobs_config IS 'Configurações dos jobs automáticos';


--
-- TOC entry 232 (class 1259 OID 16559)
-- Name: jobs_config_id_seq; Type: SEQUENCE; Schema: public; Owner: davidgabriel
--

CREATE SEQUENCE public.jobs_config_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.jobs_config_id_seq OWNER TO davidgabriel;

--
-- TOC entry 3964 (class 0 OID 0)
-- Dependencies: 232
-- Name: jobs_config_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: davidgabriel
--

ALTER SEQUENCE public.jobs_config_id_seq OWNED BY public.jobs_config.id;


--
-- TOC entry 219 (class 1259 OID 16444)
-- Name: lotes_servico; Type: TABLE; Schema: public; Owner: davidgabriel
--

CREATE TABLE public.lotes_servico (
    id integer NOT NULL,
    prestador_id integer,
    prestador_nome text,
    periodo text NOT NULL,
    valor_total real NOT NULL,
    data_envio timestamp without time zone NOT NULL,
    status text DEFAULT 'Em Aberto'::text NOT NULL,
    conversation_id text,
    anexo_path text,
    upload_token text,
    upload_url text,
    upload_status text DEFAULT 'pending'::text,
    nota_fiscal_path text,
    id_controle integer,
    link_upload text,
    validade_link date,
    status_api integer DEFAULT 0,
    data_envio_api timestamp without time zone,
    api_message text,
    upload_hash character varying(255),
    arquivos_nf jsonb,
    data_ultima_consulta timestamp without time zone,
    status_arquivo integer DEFAULT 0
);


ALTER TABLE public.lotes_servico OWNER TO davidgabriel;

--
-- TOC entry 3965 (class 0 OID 0)
-- Dependencies: 219
-- Name: COLUMN lotes_servico.arquivos_nf; Type: COMMENT; Schema: public; Owner: davidgabriel
--

COMMENT ON COLUMN public.lotes_servico.arquivos_nf IS 'Dados dos arquivos recebidos (JSON)';


--
-- TOC entry 3966 (class 0 OID 0)
-- Dependencies: 219
-- Name: COLUMN lotes_servico.data_ultima_consulta; Type: COMMENT; Schema: public; Owner: davidgabriel
--

COMMENT ON COLUMN public.lotes_servico.data_ultima_consulta IS 'Data da última consulta à API';


--
-- TOC entry 3967 (class 0 OID 0)
-- Dependencies: 219
-- Name: COLUMN lotes_servico.status_arquivo; Type: COMMENT; Schema: public; Owner: davidgabriel
--

COMMENT ON COLUMN public.lotes_servico.status_arquivo IS '0=Aguardando, 1=Recebido, 2=Baixado';


--
-- TOC entry 218 (class 1259 OID 16443)
-- Name: lotes_servico_id_seq; Type: SEQUENCE; Schema: public; Owner: davidgabriel
--

CREATE SEQUENCE public.lotes_servico_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.lotes_servico_id_seq OWNER TO davidgabriel;

--
-- TOC entry 3968 (class 0 OID 0)
-- Dependencies: 218
-- Name: lotes_servico_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: davidgabriel
--

ALTER SEQUENCE public.lotes_servico_id_seq OWNED BY public.lotes_servico.id;


--
-- TOC entry 217 (class 1259 OID 16430)
-- Name: montadores; Type: TABLE; Schema: public; Owner: davidgabriel
--

CREATE TABLE public.montadores (
    id integer NOT NULL,
    nome text NOT NULL,
    identificador text NOT NULL,
    email text NOT NULL,
    percentual_comissao real NOT NULL,
    auxilio_semanal real NOT NULL,
    ativo boolean DEFAULT true NOT NULL,
    fornecedor_id text,
    regra_envio text,
    dias_envio text,
    emails_adicionais text
);


ALTER TABLE public.montadores OWNER TO davidgabriel;

--
-- TOC entry 216 (class 1259 OID 16429)
-- Name: montadores_id_seq; Type: SEQUENCE; Schema: public; Owner: davidgabriel
--

CREATE SEQUENCE public.montadores_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.montadores_id_seq OWNER TO davidgabriel;

--
-- TOC entry 3969 (class 0 OID 0)
-- Dependencies: 216
-- Name: montadores_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: davidgabriel
--

ALTER SEQUENCE public.montadores_id_seq OWNED BY public.montadores.id;


--
-- TOC entry 231 (class 1259 OID 16538)
-- Name: notificacoes; Type: TABLE; Schema: public; Owner: davidgabriel
--

CREATE TABLE public.notificacoes (
    id integer NOT NULL,
    tipo character varying(50) NOT NULL,
    titulo text NOT NULL,
    mensagem text NOT NULL,
    lote_id integer,
    lida boolean DEFAULT false,
    data_criacao timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    data_leitura timestamp without time zone,
    icone character varying(10) DEFAULT '🔔'::character varying,
    prioridade integer DEFAULT 0
);


ALTER TABLE public.notificacoes OWNER TO davidgabriel;

--
-- TOC entry 3970 (class 0 OID 0)
-- Dependencies: 231
-- Name: TABLE notificacoes; Type: COMMENT; Schema: public; Owner: davidgabriel
--

COMMENT ON TABLE public.notificacoes IS 'Notificações do sistema';


--
-- TOC entry 3971 (class 0 OID 0)
-- Dependencies: 231
-- Name: COLUMN notificacoes.tipo; Type: COMMENT; Schema: public; Owner: davidgabriel
--

COMMENT ON COLUMN public.notificacoes.tipo IS 'Tipo: nf_recebida, nf_baixada, link_gerado, etc';


--
-- TOC entry 3972 (class 0 OID 0)
-- Dependencies: 231
-- Name: COLUMN notificacoes.prioridade; Type: COMMENT; Schema: public; Owner: davidgabriel
--

COMMENT ON COLUMN public.notificacoes.prioridade IS '0=Normal, 1=Importante, 2=Urgente';


--
-- TOC entry 230 (class 1259 OID 16537)
-- Name: notificacoes_id_seq; Type: SEQUENCE; Schema: public; Owner: davidgabriel
--

CREATE SEQUENCE public.notificacoes_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.notificacoes_id_seq OWNER TO davidgabriel;

--
-- TOC entry 3973 (class 0 OID 0)
-- Dependencies: 230
-- Name: notificacoes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: davidgabriel
--

ALTER SEQUENCE public.notificacoes_id_seq OWNED BY public.notificacoes.id;


--
-- TOC entry 229 (class 1259 OID 16517)
-- Name: os_blacklist; Type: TABLE; Schema: public; Owner: davidgabriel
--

CREATE TABLE public.os_blacklist (
    id integer NOT NULL,
    prestador_id integer,
    os_numero text NOT NULL,
    data_adicao timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    motivo text
);


ALTER TABLE public.os_blacklist OWNER TO davidgabriel;

--
-- TOC entry 228 (class 1259 OID 16516)
-- Name: os_blacklist_id_seq; Type: SEQUENCE; Schema: public; Owner: davidgabriel
--

CREATE SEQUENCE public.os_blacklist_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.os_blacklist_id_seq OWNER TO davidgabriel;

--
-- TOC entry 3974 (class 0 OID 0)
-- Dependencies: 228
-- Name: os_blacklist_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: davidgabriel
--

ALTER SEQUENCE public.os_blacklist_id_seq OWNED BY public.os_blacklist.id;


--
-- TOC entry 221 (class 1259 OID 16459)
-- Name: os_enviadas; Type: TABLE; Schema: public; Owner: davidgabriel
--

CREATE TABLE public.os_enviadas (
    id integer NOT NULL,
    lote_id integer,
    os_numero text NOT NULL,
    detalhes jsonb
);


ALTER TABLE public.os_enviadas OWNER TO davidgabriel;

--
-- TOC entry 220 (class 1259 OID 16458)
-- Name: os_enviadas_id_seq; Type: SEQUENCE; Schema: public; Owner: davidgabriel
--

CREATE SEQUENCE public.os_enviadas_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.os_enviadas_id_seq OWNER TO davidgabriel;

--
-- TOC entry 3975 (class 0 OID 0)
-- Dependencies: 220
-- Name: os_enviadas_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: davidgabriel
--

ALTER SEQUENCE public.os_enviadas_id_seq OWNED BY public.os_enviadas.id;


--
-- TOC entry 215 (class 1259 OID 16417)
-- Name: prestadores; Type: TABLE; Schema: public; Owner: davidgabriel
--

CREATE TABLE public.prestadores (
    id integer NOT NULL,
    nome text NOT NULL,
    email text NOT NULL,
    fornecedor_id text,
    regra_envio text,
    dias_envio text,
    emails_adicionais text
);


ALTER TABLE public.prestadores OWNER TO davidgabriel;

--
-- TOC entry 214 (class 1259 OID 16416)
-- Name: prestadores_id_seq; Type: SEQUENCE; Schema: public; Owner: davidgabriel
--

CREATE SEQUENCE public.prestadores_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.prestadores_id_seq OWNER TO davidgabriel;

--
-- TOC entry 3976 (class 0 OID 0)
-- Dependencies: 214
-- Name: prestadores_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: davidgabriel
--

ALTER SEQUENCE public.prestadores_id_seq OWNED BY public.prestadores.id;


--
-- TOC entry 236 (class 1259 OID 16588)
-- Name: trello_cards; Type: TABLE; Schema: public; Owner: davidgabriel
--

CREATE TABLE public.trello_cards (
    id integer NOT NULL,
    lote_id integer NOT NULL,
    card_id text NOT NULL,
    card_url text NOT NULL,
    data_criacao timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.trello_cards OWNER TO davidgabriel;

--
-- TOC entry 235 (class 1259 OID 16587)
-- Name: trello_cards_id_seq; Type: SEQUENCE; Schema: public; Owner: davidgabriel
--

CREATE SEQUENCE public.trello_cards_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.trello_cards_id_seq OWNER TO davidgabriel;

--
-- TOC entry 3977 (class 0 OID 0)
-- Dependencies: 235
-- Name: trello_cards_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: davidgabriel
--

ALTER SEQUENCE public.trello_cards_id_seq OWNED BY public.trello_cards.id;


--
-- TOC entry 3712 (class 2604 OID 16504)
-- Name: boletins_blacklist id; Type: DEFAULT; Schema: public; Owner: davidgabriel
--

ALTER TABLE ONLY public.boletins_blacklist ALTER COLUMN id SET DEFAULT nextval('public.boletins_blacklist_id_seq'::regclass);


--
-- TOC entry 3711 (class 2604 OID 16494)
-- Name: envios_ignorados id; Type: DEFAULT; Schema: public; Owner: davidgabriel
--

ALTER TABLE ONLY public.envios_ignorados ALTER COLUMN id SET DEFAULT nextval('public.envios_ignorados_id_seq'::regclass);


--
-- TOC entry 3707 (class 2604 OID 16478)
-- Name: envios_montagem id; Type: DEFAULT; Schema: public; Owner: davidgabriel
--

ALTER TABLE ONLY public.envios_montagem ALTER COLUMN id SET DEFAULT nextval('public.envios_montagem_id_seq'::regclass);


--
-- TOC entry 3721 (class 2604 OID 16563)
-- Name: jobs_config id; Type: DEFAULT; Schema: public; Owner: davidgabriel
--

ALTER TABLE ONLY public.jobs_config ALTER COLUMN id SET DEFAULT nextval('public.jobs_config_id_seq'::regclass);


--
-- TOC entry 3701 (class 2604 OID 16447)
-- Name: lotes_servico id; Type: DEFAULT; Schema: public; Owner: davidgabriel
--

ALTER TABLE ONLY public.lotes_servico ALTER COLUMN id SET DEFAULT nextval('public.lotes_servico_id_seq'::regclass);


--
-- TOC entry 3699 (class 2604 OID 16433)
-- Name: montadores id; Type: DEFAULT; Schema: public; Owner: davidgabriel
--

ALTER TABLE ONLY public.montadores ALTER COLUMN id SET DEFAULT nextval('public.montadores_id_seq'::regclass);


--
-- TOC entry 3716 (class 2604 OID 16541)
-- Name: notificacoes id; Type: DEFAULT; Schema: public; Owner: davidgabriel
--

ALTER TABLE ONLY public.notificacoes ALTER COLUMN id SET DEFAULT nextval('public.notificacoes_id_seq'::regclass);


--
-- TOC entry 3714 (class 2604 OID 16520)
-- Name: os_blacklist id; Type: DEFAULT; Schema: public; Owner: davidgabriel
--

ALTER TABLE ONLY public.os_blacklist ALTER COLUMN id SET DEFAULT nextval('public.os_blacklist_id_seq'::regclass);


--
-- TOC entry 3706 (class 2604 OID 16462)
-- Name: os_enviadas id; Type: DEFAULT; Schema: public; Owner: davidgabriel
--

ALTER TABLE ONLY public.os_enviadas ALTER COLUMN id SET DEFAULT nextval('public.os_enviadas_id_seq'::regclass);


--
-- TOC entry 3698 (class 2604 OID 16420)
-- Name: prestadores id; Type: DEFAULT; Schema: public; Owner: davidgabriel
--

ALTER TABLE ONLY public.prestadores ALTER COLUMN id SET DEFAULT nextval('public.prestadores_id_seq'::regclass);


--
-- TOC entry 3731 (class 2604 OID 16591)
-- Name: trello_cards id; Type: DEFAULT; Schema: public; Owner: davidgabriel
--

ALTER TABLE ONLY public.trello_cards ALTER COLUMN id SET DEFAULT nextval('public.trello_cards_id_seq'::regclass);


--
-- TOC entry 3945 (class 0 OID 16501)
-- Dependencies: 227
-- Data for Name: boletins_blacklist; Type: TABLE DATA; Schema: public; Owner: davidgabriel
--

COPY public.boletins_blacklist (id, montador_id, boletim, data_adicao, motivo) FROM stdin;
\.


--
-- TOC entry 3943 (class 0 OID 16491)
-- Dependencies: 225
-- Data for Name: envios_ignorados; Type: TABLE DATA; Schema: public; Owner: davidgabriel
--

COPY public.envios_ignorados (id, tipo, entidade_id, ano, periodo_chave, data_ignorada) FROM stdin;
\.


--
-- TOC entry 3941 (class 0 OID 16475)
-- Dependencies: 223
-- Data for Name: envios_montagem; Type: TABLE DATA; Schema: public; Owner: davidgabriel
--

COPY public.envios_montagem (id, montador_id, data_envio, status, detalhes, conversation_id, anexo_path, id_controle, link_upload, validade_link, status_api, data_envio_api, nota_fiscal_path, api_message, upload_hash, status_arquivo, data_ultima_consulta, quantidade_os, montador_nome, periodo, valor_total) FROM stdin;
3	1	2025-10-15 13:52:40.464677	N.F RECEBIDA	{"items": [{"boletim": "010101", "cliente": "david", "adicional": 0.0, "valor_venda": 100.0, "nome_produto": "mesa", "data_montagem": "15/10/2025", "comissao_editada": null, "comissao_calculada": 5.0}], "total_geral": 105.0, "nome_montador": "DAVID DIAS", "total_auxilio": 100.0, "total_comissao": 5.0, "total_adicionais": 0, "periodo_relatorio": "15/10/2025 - 15/10/2025", "percentual_comissao": 5.0}	AAQkADhmM2FmNmY0LTFiMjAtNGZmYi05ODQ5LTYyMGZhNTZiOTkyNQAQADR7detXlypJkKBw-wjTYKE=	\N	47	https://api.link.dev.br/dvprocessamento/envio-nf/692df756402d907ae25d85a23041de20	2025-11-14	1	2025-10-15 13:52:49.782149	uploads/montagem_3/nota fiscal novo mundo.pdf	\N	692df756402d907ae25d85a23041de20	2	\N	1	DAVID DIAS	10/2025	105.00
5	1	2025-10-15 15:54:49.421186	N.F RECEBIDA	{"items": [{"boletim": "765231", "cliente": "david dias", "adicional": 0.0, "valor_venda": 120.0, "nome_produto": "mesa verde", "data_montagem": "13/11/2025", "comissao_editada": null, "comissao_calculada": 6.0}], "total_geral": 106.0, "nome_montador": "DAVID DIAS", "total_auxilio": 100.0, "total_comissao": 6.0, "total_adicionais": 0, "periodo_relatorio": "13/11/2025 - 13/11/2025", "percentual_comissao": 5.0}	AAQkADhmM2FmNmY0LTFiMjAtNGZmYi05ODQ5LTYyMGZhNTZiOTkyNQAQAJw78a-7O2RMtWNS3qLFS1o=	\N	49	https://api.link.dev.br/dvprocessamento/envio-nf/c68659619a126d1970f9c4e53cb40ad8	2025-11-14	1	2025-10-15 15:55:06.427834	uploads/montagem_5/NOTA FISCAL DE PRESTAÇÃO DE SERVIÇO Nº 011.pdf	\N	c68659619a126d1970f9c4e53cb40ad8	2	\N	1	DAVID DIAS	11/2025	106.00
7	1	2025-10-15 17:02:40.346258	N.F RECEBIDA	{"items": [{"boletim": "982832", "cliente": "neymar", "adicional": 0.0, "valor_venda": 150.0, "nome_produto": "mesa", "data_montagem": "12/10/2025", "comissao_editada": null, "comissao_calculada": 7.5}], "total_geral": 107.5, "nome_montador": "DAVID DIAS", "total_auxilio": 100.0, "total_comissao": 7.5, "total_adicionais": 0, "periodo_relatorio": "12/10/2025 - 12/10/2025", "percentual_comissao": 5.0}	AAQkADhmM2FmNmY0LTFiMjAtNGZmYi05ODQ5LTYyMGZhNTZiOTkyNQAQAOavdzlM5C5Fs46oAHPS-70=	\N	52	https://api.link.dev.br/dvprocessamento/envio-nf/db8798edb0b799646fc32c5b60b1fedd	2025-11-14	1	2025-10-15 17:02:42.006592	uploads/montagem_7/Relatorio_Potencia_Ferragista_E_Ar_Condicionado_Ltda_Lote_48.pdf	\N	db8798edb0b799646fc32c5b60b1fedd	2	\N	1	DAVID DIAS	10/2025	107.50
6	1	2025-10-15 16:38:57.694697	N.F RECEBIDA	{"items": [{"boletim": "872323", "cliente": "daniel", "adicional": 0.0, "valor_venda": 1200.0, "nome_produto": "mesa", "data_montagem": "29/10/2025", "comissao_editada": null, "comissao_calculada": 60.0}], "total_geral": 160.0, "nome_montador": "DAVID DIAS", "total_auxilio": 100.0, "total_comissao": 60.0, "total_adicionais": 0, "periodo_relatorio": "29/10/2025 - 29/10/2025", "percentual_comissao": 5.0}	AAQkADhmM2FmNmY0LTFiMjAtNGZmYi05ODQ5LTYyMGZhNTZiOTkyNQAQAGKHb9OvGbtOgMR4VgB3WSc=	\N	51	https://api.link.dev.br/dvprocessamento/envio-nf/87e48819a6aeaa5de5380dc7eb7a7a9a	2025-11-14	1	2025-10-15 16:45:32.684913	uploads/montagem_6/Relatorio_Potencia_Ferragista_E_Ar_Condicionado_Ltda_Lote_48.pdf	\N	87e48819a6aeaa5de5380dc7eb7a7a9a	2	2025-10-15 16:47:36.725981	1	DAVID DIAS	10/2025	160.00
8	1	2025-10-15 17:21:27.554973	N.F RECEBIDA	{"items": [{"boletim": "6441195232323", "cliente": "JOSE CLAUDI ANDRADE LIMA", "adicional": 0.0, "valor_venda": 1899.0, "nome_produto": "G ROUPA SUPREME 6P4G FEIJO/OFF W ESP/PES", "data_montagem": "08/10/2025", "comissao_editada": null, "comissao_calculada": 94.95}, {"boletim": "6441195232324", "cliente": "KALYSON FAGUNDES SILVA", "adicional": 0.0, "valor_venda": 1499.0, "nome_produto": "G ROUPA MASTER NEW 8.4 C/PÉS JAT/AREIA", "data_montagem": "03/10/2025", "comissao_editada": null, "comissao_calculada": 74.95}, {"boletim": "6441195232325", "cliente": "GESICA RAYANE", "adicional": 0.0, "valor_venda": 1889.02, "nome_produto": "G ROUPA ROMANUS LUX 2PTS 4 GAV FRE/OFF", "data_montagem": "13/10/2025", "comissao_editada": null, "comissao_calculada": 94.45100000000001}, {"boletim": "6441195232326", "cliente": "MARESIA TERENCIO PEREIRA DE SOUZA", "adicional": 0.0, "valor_venda": 1889.0, "nome_produto": "G ROUPA ROMANUS LUX 2PTS 4 GAV FRE/OFF", "data_montagem": "09/10/2025", "comissao_editada": null, "comissao_calculada": 94.45}, {"boletim": "6441195232327", "cliente": "FELIPE EDUARDO ALVES VITORINO", "adicional": 0.0, "valor_venda": 729.0, "nome_produto": "G. ROUPAS SERENO 2P 2GAV FREIJO/OFFWHITE", "data_montagem": "08/10/2025", "comissao_editada": null, "comissao_calculada": 36.45}, {"boletim": "6441195232328", "cliente": "FELIPE EDUARDO ALVES VITORINO", "adicional": 0.0, "valor_venda": 729.0, "nome_produto": "G. ROUPAS SERENO 2P 2GAV FREIJO/OFFWHITE", "data_montagem": "08/10/2025", "comissao_editada": null, "comissao_calculada": 36.45}, {"boletim": "6441195232329", "cliente": "CIRLENE ALVES DE LIMA", "adicional": 0.0, "valor_venda": 399.0, "nome_produto": "GABINETE EVOLUTION 2P MDP FREI/OFFWHITE", "data_montagem": "13/10/2025", "comissao_editada": null, "comissao_calculada": 19.950000000000003}, {"boletim": "6441195232330", "cliente": "CARLOS APARECIDO BORGES DE OLIVEIRA", "adicional": 0.0, "valor_venda": 899.0, "nome_produto": "G ROUPA ADVANTAGE 6PTS 4GAV CAPUCC WOOD", "data_montagem": "14/10/2025", "comissao_editada": null, "comissao_calculada": 44.95}, {"boletim": "6441195232331", "cliente": "NOVO MUNDO S.A.", "adicional": 0.0, "valor_venda": 1864.79, "nome_produto": "G. ROUPA MESTRE 6P 4G MDF FR/OFFWHITE", "data_montagem": "13/10/2025", "comissao_editada": null, "comissao_calculada": 93.2395}, {"boletim": "6441195232332", "cliente": "CIRLENE ALVES DE LIMA", "adicional": 0.0, "valor_venda": 399.0, "nome_produto": "GABINETE EVOLUTION 2P MDP FREI/OFFWHITE", "data_montagem": "13/10/2025", "comissao_editada": null, "comissao_calculada": 19.950000000000003}], "total_geral": 909.7905000000001, "nome_montador": "DAVID DIAS", "total_auxilio": 300.0, "total_comissao": 609.7905000000001, "total_adicionais": 0, "periodo_relatorio": "03/10/2025 - 14/10/2025", "percentual_comissao": 5.0}	AAQkADhmM2FmNmY0LTFiMjAtNGZmYi05ODQ5LTYyMGZhNTZiOTkyNQAQAEqehlOFgNRIhFyDO8Hm29Y=	\N	53	https://api.link.dev.br/dvprocessamento/envio-nf/3e5b3d19bbbbbfe8ccec6be223304944	2025-11-14	1	2025-10-15 17:21:28.912219	uploads/montagem_8/Relatorio_Potencia_Ferragista_E_Ar_Condicionado_Ltda_Lote_40.pdf	\N	3e5b3d19bbbbbfe8ccec6be223304944	2	2025-10-15 17:22:36.933328	10	DAVID DIAS	10/2025	909.79
9	2	2025-10-15 17:28:07.459508	N.F RECEBIDA	{"items": [{"boletim": "6441195", "cliente": "JOSE CLAUDI ANDRADE LIMA", "adicional": 0.0, "valor_venda": 1899.0, "nome_produto": "G ROUPA SUPREME 6P4G FEIJO/OFF W ESP/PES", "data_montagem": "08/10/2025", "comissao_editada": null, "comissao_calculada": 151.92000000000002}, {"boletim": "6441611", "cliente": "KALYSON FAGUNDES SILVA", "adicional": 0.0, "valor_venda": 1499.0, "nome_produto": "G ROUPA MASTER NEW 8.4 C/PÉS JAT/AREIA", "data_montagem": "03/10/2025", "comissao_editada": null, "comissao_calculada": 119.92}, {"boletim": "6442242", "cliente": "GESICA RAYANE", "adicional": 0.0, "valor_venda": 1889.02, "nome_produto": "G ROUPA ROMANUS LUX 2PTS 4 GAV FRE/OFF", "data_montagem": "13/10/2025", "comissao_editada": null, "comissao_calculada": 151.1216}, {"boletim": "6442268", "cliente": "MARESIA TERENCIO PEREIRA DE SOUZA", "adicional": 0.0, "valor_venda": 1889.0, "nome_produto": "G ROUPA ROMANUS LUX 2PTS 4 GAV FRE/OFF", "data_montagem": "09/10/2025", "comissao_editada": null, "comissao_calculada": 151.12}, {"boletim": "6442417", "cliente": "FELIPE EDUARDO ALVES VITORINO", "adicional": 0.0, "valor_venda": 729.0, "nome_produto": "G. ROUPAS SERENO 2P 2GAV FREIJO/OFFWHITE", "data_montagem": "08/10/2025", "comissao_editada": null, "comissao_calculada": 58.32}, {"boletim": "6442419", "cliente": "FELIPE EDUARDO ALVES VITORINO", "adicional": 0.0, "valor_venda": 729.0, "nome_produto": "G. ROUPAS SERENO 2P 2GAV FREIJO/OFFWHITE", "data_montagem": "08/10/2025", "comissao_editada": null, "comissao_calculada": 58.32}, {"boletim": "6442720", "cliente": "CIRLENE ALVES DE LIMA", "adicional": 0.0, "valor_venda": 399.0, "nome_produto": "GABINETE EVOLUTION 2P MDP FREI/OFFWHITE", "data_montagem": "13/10/2025", "comissao_editada": null, "comissao_calculada": 31.92}, {"boletim": "6442771", "cliente": "CARLOS APARECIDO BORGES DE OLIVEIRA", "adicional": 0.0, "valor_venda": 899.0, "nome_produto": "G ROUPA ADVANTAGE 6PTS 4GAV CAPUCC WOOD", "data_montagem": "14/10/2025", "comissao_editada": null, "comissao_calculada": 71.92}, {"boletim": "6443224", "cliente": "NOVO MUNDO S.A.", "adicional": 0.0, "valor_venda": 1864.79, "nome_produto": "G. ROUPA MESTRE 6P 4G MDF FR/OFFWHITE", "data_montagem": "13/10/2025", "comissao_editada": null, "comissao_calculada": 149.1832}, {"boletim": "6443920", "cliente": "CIRLENE ALVES DE LIMA", "adicional": 0.0, "valor_venda": 399.0, "nome_produto": "GABINETE EVOLUTION 2P MDP FREI/OFFWHITE", "data_montagem": "13/10/2025", "comissao_editada": null, "comissao_calculada": 31.92}], "total_geral": 1125.6648, "nome_montador": "JOSIMAR SOUZA DE RESENDE 02082283143", "total_auxilio": 150.0, "total_comissao": 975.6647999999999, "total_adicionais": 0, "periodo_relatorio": "03/10/2025 - 14/10/2025", "percentual_comissao": 8.0}	AAQkADhmM2FmNmY0LTFiMjAtNGZmYi05ODQ5LTYyMGZhNTZiOTkyNQAQAGgade2o_idIhCDDAZWcZmc=	\N	54	https://api.link.dev.br/dvprocessamento/envio-nf/458a668f8f21d1bf633b10b7a05271fb	2025-11-14	1	2025-10-15 17:28:08.611674	uploads/montagem_9/52131032219518162000144000000000006525100160719918.pdf	\N	458a668f8f21d1bf633b10b7a05271fb	2	2025-10-15 18:09:36.422598	10	JOSIMAR SOUZA DE RESENDE 02082283143	10/2025	1125.66
10	1	2025-10-15 18:11:02.842801	N.F RECEBIDA	{"items": [{"boletim": "876346324", "cliente": "david", "adicional": 0.0, "valor_venda": 111.0, "nome_produto": "cadeira", "data_montagem": "06/11/2025", "comissao_editada": null, "comissao_calculada": 5.550000000000001}], "total_geral": 105.55, "nome_montador": "DAVID DIAS", "total_auxilio": 100.0, "total_comissao": 5.550000000000001, "total_adicionais": 0, "periodo_relatorio": "06/11/2025 - 06/11/2025", "percentual_comissao": 5.0}	AAQkADhmM2FmNmY0LTFiMjAtNGZmYi05ODQ5LTYyMGZhNTZiOTkyNQAQAJd0TTJPnM1IqeHDMcu2iGo=	\N	55	https://api.link.dev.br/dvprocessamento/envio-nf/b0087511c94d1d50cd35b4ab7178233c	2025-11-14	1	2025-10-15 18:11:04.224427	uploads/montagem_10/Relatorio_Potencia_Ferragista_E_Ar_Condicionado_Ltda_Lote_40.pdf	\N	b0087511c94d1d50cd35b4ab7178233c	2	2025-10-15 18:11:59.267752	1	DAVID DIAS	11/2025	105.55
11	1	2025-10-15 19:56:42.304537	N.F RECEBIDA	{"items": [{"boletim": "75521", "cliente": "david", "adicional": 0.0, "valor_venda": 120.0, "nome_produto": "mesa", "data_montagem": "19/11/2025", "comissao_editada": null, "comissao_calculada": 6.0}], "total_geral": 106.0, "nome_montador": "DAVID DIAS", "total_auxilio": 100.0, "total_comissao": 6.0, "total_adicionais": 0, "periodo_relatorio": "19/11/2025 - 19/11/2025", "percentual_comissao": 5.0}	AAQkADhmM2FmNmY0LTFiMjAtNGZmYi05ODQ5LTYyMGZhNTZiOTkyNQAQABywM0urhFhOjqlJ7s2qxUI=	\N	61	https://api.link.dev.br/dvprocessamento/envio-nf/e628338261dbbeda0c778eae731b993f	2025-11-14	1	2025-10-15 19:56:43.467468	uploads/montagem_11/Relatorio_Potencia_Ferragista_E_Ar_Condicionado_Ltda_Lote_40.pdf	\N	e628338261dbbeda0c778eae731b993f	2	2025-10-15 19:57:00.930199	1	DAVID DIAS	11/2025	106.00
12	3	2025-10-15 20:15:19.092015	Em Aberto	{"items": [{"boletim": "6433858", "cliente": "LIDIANE LEMES DE ARRUDA", "adicional": 0.0, "valor_venda": 629.0, "nome_produto": "PAINEL LEONI MDF/MDP OFFW/FREI", "data_montagem": "08/10/2025", "comissao_editada": null, "comissao_calculada": 62.900000000000006}, {"boletim": "6436251", "cliente": "JAIRO ALVES DE OLIVEIRA", "adicional": 0.0, "valor_venda": 1839.0, "nome_produto": "GR ROUPA MAJ 6P 6G MDP C/ESP/PES CAPUCC", "data_montagem": "08/10/2025", "comissao_editada": null, "comissao_calculada": 183.9}, {"boletim": "6439662", "cliente": "ELMO DIVINO CALDEIRA", "adicional": 0.0, "valor_venda": 999.0, "nome_produto": "COZ AMANDA 2023 4PCS 10PTS C/GAB BC/PT", "data_montagem": "07/10/2025", "comissao_editada": null, "comissao_calculada": 99.9}, {"boletim": "6440932", "cliente": "VINICIUS GUEDES CAPETINGA", "adicional": 0.0, "valor_venda": 489.0, "nome_produto": "GABINETE PARIS 2P3G NOGAL MANCHESTER/BC", "data_montagem": "09/10/2025", "comissao_editada": null, "comissao_calculada": 48.900000000000006}, {"boletim": "6441071", "cliente": "WANDERSON RODRIGUES FERREIRA", "adicional": 0.0, "valor_venda": 659.0, "nome_produto": "ARMARIO COZ 5P 3G VERSATTI MDP FR/GRAF", "data_montagem": "09/10/2025", "comissao_editada": null, "comissao_calculada": 65.9}, {"boletim": "6441506", "cliente": "MARIELLE DA SILVA GONCALVES", "adicional": 0.0, "valor_venda": 809.03, "nome_produto": "G ROUPA CAPRI 4PT 3GAV BRANCO/ROSA/B PES", "data_montagem": "14/10/2025", "comissao_editada": null, "comissao_calculada": 80.903}, {"boletim": "6441649", "cliente": "MARIA JOSE DA SILVA", "adicional": 0.0, "valor_venda": 1899.0, "nome_produto": "G ROUPA SUPREME 6P4G FEIJO/OFF W ESP/PES", "data_montagem": "09/10/2025", "comissao_editada": null, "comissao_calculada": 189.9}, {"boletim": "6441669", "cliente": "MARCOS PAULO DA SILVA BONIFACIO", "adicional": 0.0, "valor_venda": 2799.0, "nome_produto": "ESTOF PLENITUDE 250 3LUG TEC TABACO", "data_montagem": "10/10/2025", "comissao_editada": null, "comissao_calculada": 279.90000000000003}, {"boletim": "6442428", "cliente": "CLEUZA SOARES FERREIRA", "adicional": 0.0, "valor_venda": 1129.0, "nome_produto": "COZ PARIS 3PCS NOGAL MANCHESTER/BRANCO B", "data_montagem": "14/10/2025", "comissao_editada": null, "comissao_calculada": 112.9}, {"boletim": "6442429", "cliente": "CLEUZA SOARES FERREIRA", "adicional": 0.0, "valor_venda": 489.0, "nome_produto": "GABINETE PARIS 2P3G NOGAL MANCHESTER/BC", "data_montagem": "14/10/2025", "comissao_editada": null, "comissao_calculada": 48.900000000000006}], "total_geral": 1274.0030000000002, "nome_montador": "61.277.954 JHONNATAN MARTINS FERREIRA", "total_auxilio": 100.0, "total_comissao": 1174.0030000000002, "total_adicionais": 0, "periodo_relatorio": "07/10/2025 - 14/10/2025", "percentual_comissao": 10.0}	AAQkADhmM2FmNmY0LTFiMjAtNGZmYi05ODQ5LTYyMGZhNTZiOTkyNQAQAJG_9nNTFT5EsyPo_-5uifM=	\N	62	https://api.link.dev.br/dvprocessamento/envio-nf/f34163c58fef9374fa3e87eedabc3677	2025-11-14	0	2025-10-15 20:15:20.226697	\N	\N	f34163c58fef9374fa3e87eedabc3677	0	2025-10-16 01:09:00.42932	10	61.277.954 JHONNATAN MARTINS FERREIRA	10/2025	1274.00
\.


--
-- TOC entry 3952 (class 0 OID 16576)
-- Dependencies: 234
-- Data for Name: integracoes_config; Type: TABLE DATA; Schema: public; Owner: davidgabriel
--

COPY public.integracoes_config (id, trello_api_key, trello_token, trello_board_id, trello_list_id, trello_ativo, data_atualizacao) FROM stdin;
1	8a752bd4a6a57bb608ba432319bb5317	ATTAfb91ea387fb519c1c0ff0aab3a4bb50de3f8289ef4499eeabf67bf4ddd7da5057236C458	68ef0678d435a0e69124e711	68ef0684e621c31c7d3818f5	t	2025-10-15 00:18:47.652973
\.


--
-- TOC entry 3951 (class 0 OID 16560)
-- Dependencies: 233
-- Data for Name: jobs_config; Type: TABLE DATA; Schema: public; Owner: davidgabriel
--

COPY public.jobs_config (id, nome, descricao, ativo, intervalo_minutos, ultima_execucao, proxima_execucao, total_execucoes, total_erros, ultima_mensagem, data_criacao, data_atualizacao) FROM stdin;
3	backup_banco	Backup automático do banco de dados PostgreSQL	t	60	2025-10-16 00:09:46.250672	2025-10-15 19:09:45.890936	88	70	Backup criado com sucesso	2025-10-14 23:54:20.515702	2025-10-16 00:09:46.250672
2	enviar_api	Envia lotes pendentes para a API	t	100	2025-10-16 00:49:46.373869	2025-10-15 19:49:45.904871	11	11	Erro: 'sucesso'	2025-10-14 21:10:58.852294	2025-10-16 00:49:46.373869
1	consultar_notas	Consulta e baixa arquivos de notas fiscais	t	1	2025-10-16 01:09:00.954878	2025-10-15 18:10:45.897874	1337	7	Job executado com sucesso	2025-10-14 21:10:58.852294	2025-10-16 01:09:00.954878
\.


--
-- TOC entry 3937 (class 0 OID 16444)
-- Dependencies: 219
-- Data for Name: lotes_servico; Type: TABLE DATA; Schema: public; Owner: davidgabriel
--

COPY public.lotes_servico (id, prestador_id, prestador_nome, periodo, valor_total, data_envio, status, conversation_id, anexo_path, upload_token, upload_url, upload_status, nota_fiscal_path, id_controle, link_upload, validade_link, status_api, data_envio_api, api_message, upload_hash, arquivos_nf, data_ultima_consulta, status_arquivo) FROM stdin;
4	1	david	teste	100	2025-10-13 12:50:37.145343	Em Aberto	\N	\N	\N	\N	pending	\N	22	https://api.link.dev.br/dvprocessamento/envio-nf/d2b4cb34ff85c6ed6e1b2c3b38263a68	2025-11-13	0	2025-10-14 23:02:52.180959	Registro criado com sucesso	d2b4cb34ff85c6ed6e1b2c3b38263a68	\N	2025-10-16 01:08:59.486534	0
11	1	david	teste David	1000	2025-10-13 17:32:15.941473	Em Aberto	AAQkADhmM2FmNmY0LTFiMjAtNGZmYi05ODQ5LTYyMGZhNTZiOTkyNQAQAHB_ZPIOYhdFoWP6JECZIQE=	\N	\N	\N	pending	\N	16	https://api.link.dev.br/dvprocessamento/envio-nf/8b51f9d0c8afb8f918347c5d9fa3503f	2025-11-13	0	2025-10-14 23:02:44.824139	Registro criado com sucesso	8b51f9d0c8afb8f918347c5d9fa3503f	\N	2025-10-16 01:08:53.838886	0
10	6	thiago	23/08/2025 – 04/09/2025	600	2025-10-13 15:17:27.099287	Em Aberto	AAQkADhmM2FmNmY0LTFiMjAtNGZmYi05ODQ5LTYyMGZhNTZiOTkyNQAQANbYeUzLKTlCnfGRV--Ye-4=	\N	\N	\N	pending	\N	17	https://api.link.dev.br/dvprocessamento/envio-nf/d9d43a5b6b47e72892ece042151da40f	2025-11-13	0	2025-10-14 23:02:46.011102	Registro criado com sucesso	d9d43a5b6b47e72892ece042151da40f	\N	2025-10-16 01:08:54.762978	0
9	1	david	23/08/2025 – 04/09/2025	600	2025-10-13 15:17:24.497132	Em Aberto	AAQkADhmM2FmNmY0LTFiMjAtNGZmYi05ODQ5LTYyMGZhNTZiOTkyNQAQALOQCousTUhIigoMaJNIjHw=	\N	\N	\N	pending	\N	18	https://api.link.dev.br/dvprocessamento/envio-nf/4e9f783708d8614792da906940134cf0	2025-11-13	0	2025-10-14 23:02:47.338487	Registro criado com sucesso	4e9f783708d8614792da906940134cf0	\N	2025-10-16 01:08:55.692941	0
8	1	david	23/02/2025 – 04/03/2025	600	2025-10-13 15:17:21.579851	Em Aberto	AAQkADhmM2FmNmY0LTFiMjAtNGZmYi05ODQ5LTYyMGZhNTZiOTkyNQAQAECBQ_ZGHAhKpKFmGF5Tsh4=	\N	\N	\N	pending	\N	19	https://api.link.dev.br/dvprocessamento/envio-nf/a041c8301d7186f88c809ab6a504f8d0	2025-11-13	0	2025-10-14 23:02:48.552447	Registro criado com sucesso	a041c8301d7186f88c809ab6a504f8d0	\N	2025-10-16 01:08:56.65385	0
15	1	david	01/11/2025 - 02/11/2025	150	2025-10-13 20:29:24.517415	Em Aberto	AAQkADhmM2FmNmY0LTFiMjAtNGZmYi05ODQ5LTYyMGZhNTZiOTkyNQAQAPqD6pEOkntHvN4DxRkjoYM=	\N	\N	\N	pending	\N	13	https://api.link.dev.br/dvprocessamento/envio-nf/67bcacecaae861214627674ada9ae8e8	2025-11-13	0	2025-10-14 23:02:40.856403	Registro criado com sucesso	67bcacecaae861214627674ada9ae8e8	\N	2025-10-16 01:08:51.039852	0
7	1	david	01/01/2025 - 02/01/2025	100	2025-10-13 15:06:05.073441	Em Aberto	AAQkADhmM2FmNmY0LTFiMjAtNGZmYi05ODQ5LTYyMGZhNTZiOTkyNQAQAIgJNQgcAZREtEYnbU88cMw=	\N	\N	\N	pending	\N	20	https://api.link.dev.br/dvprocessamento/envio-nf/5beacc41380934a07a4038831cdf57ea	2025-11-13	0	2025-10-14 23:02:49.731857	Registro criado com sucesso	5beacc41380934a07a4038831cdf57ea	\N	2025-10-16 01:08:57.600954	0
6	2	52.417.932 Leogilson Dos Santos Silva	05/10/2025 – 22/10/2025	8850	2025-10-13 13:15:36.679939	Em Aberto	AAQkADhmM2FmNmY0LTFiMjAtNGZmYi05ODQ5LTYyMGZhNTZiOTkyNQAQABjMv1pJzdtJku8W8EoiIg8=	\N	\N	\N	pending	\N	21	https://api.link.dev.br/dvprocessamento/envio-nf/22b406a239a4fdf9331dcd821c255bd0	2025-11-13	0	2025-10-14 23:02:50.95279	Registro criado com sucesso	22b406a239a4fdf9331dcd821c255bd0	\N	2025-10-16 01:08:58.552722	0
13	1	david	10/10/2025 - 11/10/2025	1200	2025-10-13 19:38:47.125389	Em Aberto	AAQkADhmM2FmNmY0LTFiMjAtNGZmYi05ODQ5LTYyMGZhNTZiOTkyNQAQAMYkqmhG4dZPrFjCSFOBflE=	\N	\N	\N	pending	\N	14	https://api.link.dev.br/dvprocessamento/envio-nf/3ccc68bbbc1a794bb0401f41fcf14f3b	2025-11-13	0	2025-10-14 23:02:42.326526	Registro criado com sucesso	3ccc68bbbc1a794bb0401f41fcf14f3b	\N	2025-10-16 01:08:51.956051	0
12	1	david	sei la	100	2025-10-13 19:29:06.54103	Em Aberto	AAQkADhmM2FmNmY0LTFiMjAtNGZmYi05ODQ5LTYyMGZhNTZiOTkyNQAQAET5yL08eHZBmKAVMTjRQq0=	\N	\N	\N	pending	\N	15	https://api.link.dev.br/dvprocessamento/envio-nf/2ef59838fd858c04281e0e6b07a36510	2025-11-13	0	2025-10-14 23:02:43.627496	Registro criado com sucesso	2ef59838fd858c04281e0e6b07a36510	\N	2025-10-16 01:08:52.871532	0
14	1	david	01/01/2025 - 02/01/2025	100	2025-10-13 20:02:02.672235	Em Aberto	AAQkADhmM2FmNmY0LTFiMjAtNGZmYi05ODQ5LTYyMGZhNTZiOTkyNQAQAJbIzLJdR2FHlWqls1uWzSU=	\N	\N	\N	pending	\N	3	https://api.link.com.br/dvprocessamento/envio-nf/fa611f6d1eaa2b3b9302e006edcd24d7	2025-11-12	0	2025-10-13 20:02:03.907641	Registro criado com sucesso	\N	\N	\N	0
16	1	david	01/05/2025 - 03/05/2025	100	2025-10-13 21:43:54.237483	Em Aberto	AAQkADhmM2FmNmY0LTFiMjAtNGZmYi05ODQ5LTYyMGZhNTZiOTkyNQAQACuVTE25kFFAu_FxuKR8ovU=	\N	\N	\N	pending	\N	5	https://api.link.com.br/dvprocessamento/envio-nf/ce96a5a8e204b3edba6f5756a2e7a915	2025-11-12	0	2025-10-13 21:43:57.279054	Registro criado com sucesso	\N	\N	\N	0
17	1	david	01/01/2025 - 01/10/2025	100	2025-10-14 11:09:41.852883	Em Aberto	AAQkADhmM2FmNmY0LTFiMjAtNGZmYi05ODQ5LTYyMGZhNTZiOTkyNQAQAPPcb8kiVBpAj2b1BtXl3Fo=	\N	\N	\N	pending	\N	3	https://api.link.dev.br/dvprocessamento/envio-nf/d8f25dfcab5ca6991832d2a1dd858dfb	2025-11-13	0	2025-10-14 11:09:44.884913	Registro criado com sucesso	\N	\N	\N	0
18	1	david	10/10/2025	120	2025-10-14 13:06:56.60038	Em Aberto	AAQkADhmM2FmNmY0LTFiMjAtNGZmYi05ODQ5LTYyMGZhNTZiOTkyNQAQAOtb_G2a5W5Mm8jLp4fVlCQ=	\N	\N	\N	pending	\N	4	https://api.link.dev.br/dvprocessamento/envio-nf/88c558c57f82aae676be5afcb7d21a4f	2025-11-13	0	2025-10-14 13:06:58.913071	Registro criado com sucesso	\N	\N	\N	0
53	1	david	01/01/2026	100	2025-10-15 19:53:50.981226	N.F RECEBIDA	AAQkADhmM2FmNmY0LTFiMjAtNGZmYi05ODQ5LTYyMGZhNTZiOTkyNQAQAB2mgip590RCttKN86yHR3k=	\N	\N	\N	pending	\N	60	https://api.link.dev.br/dvprocessamento/envio-nf/945a9552bea03df320cca35889385158	2025-11-14	0	2025-10-15 19:53:52.066354	Registro criado com sucesso	945a9552bea03df320cca35889385158	{"arquivos": [{"id": 44, "data_upload": "2025-10-15 19:54:17", "observacoes": "", "hash_arquivo": "6225b3be94822da5066c0744e7c8d904", "nome_arquivo": "945a9552bea03df320cca35889385158.pdf", "tipo_arquivo": "application/pdf", "link_download": "https://api.link.dev.br/dvprocessamento/envio-nf/arquivosNF/945a9552bea03df320cca35889385158.pdf", "nome_original": "Relatorio_Potencia_Ferragista_E_Ar_Condicionado_Ltda_Lote_40.pdf", "caminho_arquivo": "arquivosNF/945a9552bea03df320cca35889385158.pdf", "tamanho_arquivo": 38353, "tamanho_formatado": "37.45 KB", "status_processamento": 1}], "estatisticas": {"tipos_arquivo": {"application/pdf": 1}, "total_tamanho": 38353, "ultimo_upload": "2025-10-15 19:54:17", "total_arquivos": 1, "primeiro_upload": "2025-10-15 19:54:17", "total_tamanho_formatado": "37.45 KB"}, "data_consulta": "2025-10-15T19:54:46.348209"}	2025-10-15 19:54:46.348209	2
19	1	david	01/01/2025	100	2025-10-14 20:36:02.971502	N.F RECEBIDA	AAQkADhmM2FmNmY0LTFiMjAtNGZmYi05ODQ5LTYyMGZhNTZiOTkyNQAQAPWTf2pZqYdBq0Mk41mkG6M=	\N	\N	\N	pending	\N	7	https://api.link.dev.br/dvprocessamento/envio-nf/fe6bf11bea73b8936b83f293435a6c55	2025-11-13	0	2025-10-14 20:36:05.519364	Registro criado com sucesso	fe6bf11bea73b8936b83f293435a6c55	{"arquivos": [{"id": 12, "data_upload": "2025-10-14 20:36:37", "observacoes": "", "hash_arquivo": "fdc6da06fa3f863b68663230359de120", "nome_arquivo": "fe6bf11bea73b8936b83f293435a6c55.pdf", "tipo_arquivo": "application/pdf", "link_download": "https://api.link.dev.br/dvprocessamento/envio-nf/arquivosNF/fe6bf11bea73b8936b83f293435a6c55.pdf", "nome_original": "232323.pdf", "caminho_arquivo": "arquivosNF/fe6bf11bea73b8936b83f293435a6c55.pdf", "tamanho_arquivo": 301647, "tamanho_formatado": "294.58 KB", "status_processamento": 1}], "estatisticas": {"tipos_arquivo": {"application/pdf": 1}, "total_tamanho": 301647, "ultimo_upload": "2025-10-14 20:36:37", "total_arquivos": 1, "primeiro_upload": "2025-10-14 20:36:37", "total_tamanho_formatado": "294.58 KB"}, "data_consulta": "2025-10-14T23:53:04.153802"}	2025-10-14 23:53:04.153802	2
23	1	david	01/01/2025	120	2025-10-14 21:07:20.293614	N.F RECEBIDA	AAQkADhmM2FmNmY0LTFiMjAtNGZmYi05ODQ5LTYyMGZhNTZiOTkyNQAQAHdP7Ldsrf9El326jNt9vHU=	\N	\N	\N	pending	\N	11	https://api.link.dev.br/dvprocessamento/envio-nf/f5b5a723645837e04231238bfff38b8f	2025-11-13	0	2025-10-14 21:07:22.24112	Registro criado com sucesso	f5b5a723645837e04231238bfff38b8f	{"arquivos": [{"id": 16, "data_upload": "2025-10-14 21:07:44", "observacoes": "", "hash_arquivo": "ef6c5749cddf9595bac1ab6f941a6376", "nome_arquivo": "f5b5a723645837e04231238bfff38b8f.pdf", "tipo_arquivo": "application/pdf", "link_download": "https://api.link.dev.br/dvprocessamento/envio-nf/arquivosNF/f5b5a723645837e04231238bfff38b8f.pdf", "nome_original": "NOVO MUNDO DAVID GABRIEL NF 645.pdf", "caminho_arquivo": "arquivosNF/f5b5a723645837e04231238bfff38b8f.pdf", "tamanho_arquivo": 459446, "tamanho_formatado": "448.68 KB", "status_processamento": 1}], "estatisticas": {"tipos_arquivo": {"application/pdf": 1}, "total_tamanho": 459446, "ultimo_upload": "2025-10-14 21:07:44", "total_arquivos": 1, "primeiro_upload": "2025-10-14 21:07:44", "total_tamanho_formatado": "448.68 KB"}, "data_consulta": "2025-10-14T23:52:57.627158"}	2025-10-14 23:52:57.627158	2
22	1	david	01/01/2026	120	2025-10-14 20:56:11.805972	N.F RECEBIDA	AAQkADhmM2FmNmY0LTFiMjAtNGZmYi05ODQ5LTYyMGZhNTZiOTkyNQAQAM4Yl8HYRulGqCxsIBmkOg8=	\N	\N	\N	pending	\N	\N	https://api.link.dev.br/dvprocessamento/envio-nf/74b1ab63d2f02d33f992175844605233	2025-11-13	0	2025-10-14 20:56:13.015439	Registro criado com sucesso	74b1ab63d2f02d33f992175844605233	{"arquivos": [{"id": 15, "data_upload": "2025-10-14 20:56:38", "observacoes": "", "hash_arquivo": "39f72a29c74cbc22c570759b61633dee", "nome_arquivo": "74b1ab63d2f02d33f992175844605233.pdf", "tipo_arquivo": "application/pdf", "link_download": "https://api.link.dev.br/dvprocessamento/envio-nf/arquivosNF/74b1ab63d2f02d33f992175844605233.pdf", "nome_original": "Nf 12.pdf", "caminho_arquivo": "arquivosNF/74b1ab63d2f02d33f992175844605233.pdf", "tamanho_arquivo": 98257, "tamanho_formatado": "95.95 KB", "status_processamento": 1}], "estatisticas": {"tipos_arquivo": {"application/pdf": 1}, "total_tamanho": 98257, "ultimo_upload": "2025-10-14 20:56:38", "total_arquivos": 1, "primeiro_upload": "2025-10-14 20:56:38", "total_tamanho_formatado": "95.95 KB"}, "data_consulta": "2025-10-14T23:52:59.288943"}	2025-10-14 23:52:59.288943	2
21	1	david	01/01/2025	100	2025-10-14 20:50:11.505667	N.F RECEBIDA	AAQkADhmM2FmNmY0LTFiMjAtNGZmYi05ODQ5LTYyMGZhNTZiOTkyNQAQAACIG8TIGsxMj7Kb_i4bjRo=	\N	\N	\N	pending	\N	9	https://api.link.dev.br/dvprocessamento/envio-nf/68cacb30a7ae736d4b63559b4302199f	2025-11-13	0	2025-10-14 20:50:23.220606	Registro criado com sucesso	68cacb30a7ae736d4b63559b4302199f	{"arquivos": [{"id": 14, "data_upload": "2025-10-14 20:50:58", "observacoes": "", "hash_arquivo": "fdc6da06fa3f863b68663230359de120", "nome_arquivo": "68cacb30a7ae736d4b63559b4302199f.pdf", "tipo_arquivo": "application/pdf", "link_download": "https://api.link.dev.br/dvprocessamento/envio-nf/arquivosNF/68cacb30a7ae736d4b63559b4302199f.pdf", "nome_original": "232323.pdf", "caminho_arquivo": "arquivosNF/68cacb30a7ae736d4b63559b4302199f.pdf", "tamanho_arquivo": 301647, "tamanho_formatado": "294.58 KB", "status_processamento": 1}], "estatisticas": {"tipos_arquivo": {"application/pdf": 1}, "total_tamanho": 301647, "ultimo_upload": "2025-10-14 20:50:58", "total_arquivos": 1, "primeiro_upload": "2025-10-14 20:50:58", "total_tamanho_formatado": "294.58 KB"}, "data_consulta": "2025-10-14T23:53:00.910250"}	2025-10-14 23:53:00.91025	2
20	1	david	01/09/2025	250	2025-10-14 20:40:53.120867	N.F RECEBIDA	AAQkADhmM2FmNmY0LTFiMjAtNGZmYi05ODQ5LTYyMGZhNTZiOTkyNQAQAPWTf2pZqYdBq0Mk41mkG6M=	\N	\N	\N	pending	\N	8	https://api.link.dev.br/dvprocessamento/envio-nf/4c16655f79a49f01877c0bb9787ab168	2025-11-13	0	2025-10-14 20:40:54.590194	Registro criado com sucesso	4c16655f79a49f01877c0bb9787ab168	{"arquivos": [{"id": 13, "data_upload": "2025-10-14 20:41:40", "observacoes": "", "hash_arquivo": "fdc6da06fa3f863b68663230359de120", "nome_arquivo": "4c16655f79a49f01877c0bb9787ab168.pdf", "tipo_arquivo": "application/pdf", "link_download": "https://api.link.dev.br/dvprocessamento/envio-nf/arquivosNF/4c16655f79a49f01877c0bb9787ab168.pdf", "nome_original": "232323.pdf", "caminho_arquivo": "arquivosNF/4c16655f79a49f01877c0bb9787ab168.pdf", "tamanho_arquivo": 301647, "tamanho_formatado": "294.58 KB", "status_processamento": 1}], "estatisticas": {"tipos_arquivo": {"application/pdf": 1}, "total_tamanho": 301647, "ultimo_upload": "2025-10-14 20:41:40", "total_arquivos": 1, "primeiro_upload": "2025-10-14 20:41:40", "total_tamanho_formatado": "294.58 KB"}, "data_consulta": "2025-10-14T23:53:02.529910"}	2025-10-14 23:53:02.52991	2
28	1	david	01/01/2025	100	2025-10-15 00:54:20.075099	N.F RECEBIDA	AAQkADhmM2FmNmY0LTFiMjAtNGZmYi05ODQ5LTYyMGZhNTZiOTkyNQAQAEM_4zq_oY9JjT173eszF1k=	\N	\N	\N	pending	\N	26	https://api.link.dev.br/dvprocessamento/envio-nf/cb735f8e4056142d368b594ba20bd674	2025-11-14	0	2025-10-15 00:54:21.478804	Registro criado com sucesso	cb735f8e4056142d368b594ba20bd674	{"arquivos": [{"id": 21, "data_upload": "2025-10-15 00:54:41", "observacoes": "", "hash_arquivo": "5a49dd375e270d570c93c50e3c720adf", "nome_arquivo": "cb735f8e4056142d368b594ba20bd674.xml", "tipo_arquivo": "text/plain", "link_download": "https://api.link.dev.br/dvprocessamento/envio-nf/arquivosNF/cb735f8e4056142d368b594ba20bd674.xml", "nome_original": "14233850_NFSeNotaFiscaldeServicosEletronica_009376.xml", "caminho_arquivo": "arquivosNF/cb735f8e4056142d368b594ba20bd674.xml", "tamanho_arquivo": 4199, "tamanho_formatado": "4.1 KB", "status_processamento": 1}], "estatisticas": {"tipos_arquivo": {"text/plain": 1}, "total_tamanho": 4199, "ultimo_upload": "2025-10-15 00:54:41", "total_arquivos": 1, "primeiro_upload": "2025-10-15 00:54:41", "total_tamanho_formatado": "4.1 KB"}, "data_consulta": "2025-10-15T00:55:28.923648"}	2025-10-15 00:55:28.923648	2
30	1	david	01/01/2025	100	2025-10-15 01:19:43.93539	N.F RECEBIDA	AAQkADhmM2FmNmY0LTFiMjAtNGZmYi05ODQ5LTYyMGZhNTZiOTkyNQAQAHSJ1kkRgnpMmjBFbP9LJ7A=	\N	\N	\N	pending	\N	28	https://api.link.dev.br/dvprocessamento/envio-nf/2fc87cacd12b4e4b09c70de021390290	2025-11-14	0	2025-10-15 01:19:45.284968	Registro criado com sucesso	2fc87cacd12b4e4b09c70de021390290	{"arquivos": [{"id": 23, "data_upload": "2025-10-15 01:20:04", "observacoes": "", "hash_arquivo": "58bd22f3334fea33832d3789fbd5ae1e", "nome_arquivo": "2fc87cacd12b4e4b09c70de021390290.xml", "tipo_arquivo": "text/plain", "link_download": "https://api.link.dev.br/dvprocessamento/envio-nf/arquivosNF/2fc87cacd12b4e4b09c70de021390290.xml", "nome_original": "14233850_NFSeNotaFiscaldeServicosEletronica_009373.xml", "caminho_arquivo": "arquivosNF/2fc87cacd12b4e4b09c70de021390290.xml", "tamanho_arquivo": 4191, "tamanho_formatado": "4.09 KB", "status_processamento": 1}], "estatisticas": {"tipos_arquivo": {"text/plain": 1}, "total_tamanho": 4191, "ultimo_upload": "2025-10-15 01:20:04", "total_arquivos": 1, "primeiro_upload": "2025-10-15 01:20:04", "total_tamanho_formatado": "4.09 KB"}, "data_consulta": "2025-10-15T01:20:29.019058"}	2025-10-15 01:20:29.019058	2
29	1	david	01/01/2025	100	2025-10-15 01:13:40.853554	N.F RECEBIDA	AAQkADhmM2FmNmY0LTFiMjAtNGZmYi05ODQ5LTYyMGZhNTZiOTkyNQAQABaMFrTftLpAjTMvsvDJN6g=	\N	\N	\N	pending	\N	27	https://api.link.dev.br/dvprocessamento/envio-nf/9fd7c7ccc9f7c3c11fcb7be738cd1a87	2025-11-14	0	2025-10-15 01:13:42.065886	Registro criado com sucesso	9fd7c7ccc9f7c3c11fcb7be738cd1a87	{"arquivos": [{"id": 22, "data_upload": "2025-10-15 01:14:19", "observacoes": "", "hash_arquivo": "b5a2132b49be5b6863cdd65daa33b3f7", "nome_arquivo": "9fd7c7ccc9f7c3c11fcb7be738cd1a87.xml", "tipo_arquivo": "text/plain", "link_download": "https://api.link.dev.br/dvprocessamento/envio-nf/arquivosNF/9fd7c7ccc9f7c3c11fcb7be738cd1a87.xml", "nome_original": "14233850_NFSeNotaFiscaldeServicosEletronica_009374.xml", "caminho_arquivo": "arquivosNF/9fd7c7ccc9f7c3c11fcb7be738cd1a87.xml", "tamanho_arquivo": 4247, "tamanho_formatado": "4.15 KB", "status_processamento": 1}], "estatisticas": {"tipos_arquivo": {"text/plain": 1}, "total_tamanho": 4247, "ultimo_upload": "2025-10-15 01:14:19", "total_arquivos": 1, "primeiro_upload": "2025-10-15 01:14:19", "total_tamanho_formatado": "4.15 KB"}, "data_consulta": "2025-10-15T01:14:29.238051"}	2025-10-15 01:14:29.238051	2
31	1	david	01/01/2025	200	2025-10-15 01:25:47.328073	N.F RECEBIDA	AAQkADhmM2FmNmY0LTFiMjAtNGZmYi05ODQ5LTYyMGZhNTZiOTkyNQAQAOWkqvrjdC5Er6W3jE1OjWY=	\N	\N	\N	pending	\N	29	https://api.link.dev.br/dvprocessamento/envio-nf/48c5a75fc806b68215b5a742956ef3ac	2025-11-14	0	2025-10-15 01:25:48.840999	Registro criado com sucesso	48c5a75fc806b68215b5a742956ef3ac	{"arquivos": [{"id": 24, "data_upload": "2025-10-15 01:26:07", "observacoes": "", "hash_arquivo": "e46179a375b5f93748cdeb75aff6a479", "nome_arquivo": "48c5a75fc806b68215b5a742956ef3ac.xml", "tipo_arquivo": "text/plain", "link_download": "https://api.link.dev.br/dvprocessamento/envio-nf/arquivosNF/48c5a75fc806b68215b5a742956ef3ac.xml", "nome_original": "14233850_NFSeNotaFiscaldeServicosEletronica_009371.xml", "caminho_arquivo": "arquivosNF/48c5a75fc806b68215b5a742956ef3ac.xml", "tamanho_arquivo": 4682, "tamanho_formatado": "4.57 KB", "status_processamento": 1}], "estatisticas": {"tipos_arquivo": {"text/plain": 1}, "total_tamanho": 4682, "ultimo_upload": "2025-10-15 01:26:07", "total_arquivos": 1, "primeiro_upload": "2025-10-15 01:26:07", "total_tamanho_formatado": "4.57 KB"}, "data_consulta": "2025-10-15T01:26:28.934052"}	2025-10-15 01:26:28.934052	2
32	1	david	01/01/2025	100	2025-10-15 01:30:24.133871	N.F RECEBIDA	AAQkADhmM2FmNmY0LTFiMjAtNGZmYi05ODQ5LTYyMGZhNTZiOTkyNQAQAMlYzkWc4-xArglpFdULMP0=	\N	\N	\N	pending	\N	30	https://api.link.dev.br/dvprocessamento/envio-nf/20e1148ba750825f98195c1f337639bb	2025-11-14	0	2025-10-15 01:30:25.53813	Registro criado com sucesso	20e1148ba750825f98195c1f337639bb	{"arquivos": [{"id": 25, "data_upload": "2025-10-15 01:30:43", "observacoes": "", "hash_arquivo": "b5a2132b49be5b6863cdd65daa33b3f7", "nome_arquivo": "20e1148ba750825f98195c1f337639bb.xml", "tipo_arquivo": "text/plain", "link_download": "https://api.link.dev.br/dvprocessamento/envio-nf/arquivosNF/20e1148ba750825f98195c1f337639bb.xml", "nome_original": "14233850_NFSeNotaFiscaldeServicosEletronica_009374.xml", "caminho_arquivo": "arquivosNF/20e1148ba750825f98195c1f337639bb.xml", "tamanho_arquivo": 4247, "tamanho_formatado": "4.15 KB", "status_processamento": 1}], "estatisticas": {"tipos_arquivo": {"text/plain": 1}, "total_tamanho": 4247, "ultimo_upload": "2025-10-15 01:30:43", "total_arquivos": 1, "primeiro_upload": "2025-10-15 01:30:43", "total_tamanho_formatado": "4.15 KB"}, "data_consulta": "2025-10-15T01:30:59.250914"}	2025-10-15 01:30:59.250914	2
33	1	david	01/01/2025	100	2025-10-15 10:54:26.03919	N.F RECEBIDA	\N	\N	\N	\N	pending	\N	31	https://api.link.dev.br/dvprocessamento/envio-nf/1fb744baf0b16518810be3ff1d497151	2025-11-14	0	2025-10-15 10:54:27.876169	Registro criado com sucesso	1fb744baf0b16518810be3ff1d497151	{"arquivos": [{"id": 37, "data_upload": "2025-10-15 16:37:50", "observacoes": "", "hash_arquivo": "6225b3be94822da5066c0744e7c8d904", "nome_arquivo": "1fb744baf0b16518810be3ff1d497151.pdf", "tipo_arquivo": "application/pdf", "link_download": "https://api.link.dev.br/dvprocessamento/envio-nf/arquivosNF/1fb744baf0b16518810be3ff1d497151.pdf", "nome_original": "Relatorio_Potencia_Ferragista_E_Ar_Condicionado_Ltda_Lote_40.pdf", "caminho_arquivo": "arquivosNF/1fb744baf0b16518810be3ff1d497151.pdf", "tamanho_arquivo": 38353, "tamanho_formatado": "37.45 KB", "status_processamento": 1}], "estatisticas": {"tipos_arquivo": {"application/pdf": 1}, "total_tamanho": 38353, "ultimo_upload": "2025-10-15 16:37:50", "total_arquivos": 1, "primeiro_upload": "2025-10-15 16:37:50", "total_tamanho_formatado": "37.45 KB"}, "data_consulta": "2025-10-15T16:38:28.137558"}	2025-10-15 16:38:28.137558	2
27	1	david	23/08/2025 – 04/09/2025	1200	2025-10-15 00:37:39.442035	N.F RECEBIDA	AAQkADhmM2FmNmY0LTFiMjAtNGZmYi05ODQ5LTYyMGZhNTZiOTkyNQAQADlidLM6g-NHlhVUmk1ZJMI=	\N	\N	\N	pending	\N	25	https://api.link.dev.br/dvprocessamento/envio-nf/9ca30b1784296ca9a6cb47d7f70dfe3d	2025-11-14	0	2025-10-15 00:37:40.968572	Registro criado com sucesso	9ca30b1784296ca9a6cb47d7f70dfe3d	{"arquivos": [{"id": 19, "data_upload": "2025-10-15 00:38:37", "observacoes": "", "hash_arquivo": "9f624bc68080290f55fde9079f4889d7", "nome_arquivo": "9ca30b1784296ca9a6cb47d7f70dfe3d.xml", "tipo_arquivo": "text/plain", "link_download": "https://api.link.dev.br/dvprocessamento/envio-nf/arquivosNF/9ca30b1784296ca9a6cb47d7f70dfe3d.xml", "nome_original": "14233850_NFSeNotaFiscaldeServicosEletronica_009370.xml", "caminho_arquivo": "arquivosNF/9ca30b1784296ca9a6cb47d7f70dfe3d.xml", "tamanho_arquivo": 4188, "tamanho_formatado": "4.09 KB", "status_processamento": 1}], "estatisticas": {"tipos_arquivo": {"text/plain": 1}, "total_tamanho": 4188, "ultimo_upload": "2025-10-15 00:38:37", "total_arquivos": 1, "primeiro_upload": "2025-10-15 00:38:37", "total_tamanho_formatado": "4.09 KB"}, "data_consulta": "2025-10-15T00:39:28.981281"}	2025-10-15 00:39:28.981281	2
34	1	david	01/01/2025	100	2025-10-15 10:55:18.579332	N.F RECEBIDA	AAQkADhmM2FmNmY0LTFiMjAtNGZmYi05ODQ5LTYyMGZhNTZiOTkyNQAQAK18Kg6_2ztAtuDiD2H0iOg=	\N	\N	\N	pending	\N	32	https://api.link.dev.br/dvprocessamento/envio-nf/fc55cae615ba0d2aa6e75cbef5024644	2025-11-14	0	2025-10-15 10:55:20.006744	Registro criado com sucesso	fc55cae615ba0d2aa6e75cbef5024644	{"arquivos": [{"id": 26, "data_upload": "2025-10-15 10:57:31", "observacoes": "", "hash_arquivo": "ff6f1fc8d652975c627f5f36650979a3", "nome_arquivo": "fc55cae615ba0d2aa6e75cbef5024644.png", "tipo_arquivo": "image/png", "link_download": "https://api.link.dev.br/dvprocessamento/envio-nf/arquivosNF/fc55cae615ba0d2aa6e75cbef5024644.png", "nome_original": "Captura de Tela 2025-09-25 às 13.37.09.png", "caminho_arquivo": "arquivosNF/fc55cae615ba0d2aa6e75cbef5024644.png", "tamanho_arquivo": 770218, "tamanho_formatado": "752.17 KB", "status_processamento": 1}], "estatisticas": {"tipos_arquivo": {"image/png": 1}, "total_tamanho": 770218, "ultimo_upload": "2025-10-15 10:57:31", "total_arquivos": 1, "primeiro_upload": "2025-10-15 10:57:31", "total_tamanho_formatado": "752.17 KB"}, "data_consulta": "2025-10-15T10:57:59.877806"}	2025-10-15 10:57:59.877806	2
24	1	david	01/01/2023	100	2025-10-14 21:18:43.893631	N.F RECEBIDA	AAQkADhmM2FmNmY0LTFiMjAtNGZmYi05ODQ5LTYyMGZhNTZiOTkyNQAQAJoVQQoMXrZAoOKKdUaT99A=	\N	\N	\N	pending	\N	12	https://api.link.dev.br/dvprocessamento/envio-nf/72d3f4254bd10917fc3dbc04ce122d67	2025-11-13	0	2025-10-14 21:18:45.10213	Registro criado com sucesso	72d3f4254bd10917fc3dbc04ce122d67	{"arquivos": [{"id": 17, "data_upload": "2025-10-14 21:19:04", "observacoes": "", "hash_arquivo": "39f72a29c74cbc22c570759b61633dee", "nome_arquivo": "72d3f4254bd10917fc3dbc04ce122d67.pdf", "tipo_arquivo": "application/pdf", "link_download": "https://api.link.dev.br/dvprocessamento/envio-nf/arquivosNF/72d3f4254bd10917fc3dbc04ce122d67.pdf", "nome_original": "Nf 12.pdf", "caminho_arquivo": "arquivosNF/72d3f4254bd10917fc3dbc04ce122d67.pdf", "tamanho_arquivo": 98257, "tamanho_formatado": "95.95 KB", "status_processamento": 1}], "estatisticas": {"tipos_arquivo": {"application/pdf": 1}, "total_tamanho": 98257, "ultimo_upload": "2025-10-14 21:19:04", "total_arquivos": 1, "primeiro_upload": "2025-10-14 21:19:04", "total_tamanho_formatado": "95.95 KB"}, "data_consulta": "2025-10-14T23:52:55.970642"}	2025-10-14 23:52:55.970642	2
26	1	david	23/02/2025 – 04/03/2025	600	2025-10-15 00:37:35.263078	N.F RECEBIDA	AAQkADhmM2FmNmY0LTFiMjAtNGZmYi05ODQ5LTYyMGZhNTZiOTkyNQAQAN_W7Bmm-C9Mh-5hGxtxyG8=	\N	\N	\N	pending	\N	24	https://api.link.dev.br/dvprocessamento/envio-nf/9866fd9608965620c9519b3dbea098b8	2025-11-14	0	2025-10-15 00:37:36.502995	Registro criado com sucesso	9866fd9608965620c9519b3dbea098b8	{"arquivos": [{"id": 20, "data_upload": "2025-10-15 00:47:07", "observacoes": "", "hash_arquivo": "d1217a04d8a03f900597928d8ae7e928", "nome_arquivo": "9866fd9608965620c9519b3dbea098b8.xml", "tipo_arquivo": "text/plain", "link_download": "https://api.link.dev.br/dvprocessamento/envio-nf/arquivosNF/9866fd9608965620c9519b3dbea098b8.xml", "nome_original": "14233850_NFSeNotaFiscaldeServicosEletronica_009377.xml", "caminho_arquivo": "arquivosNF/9866fd9608965620c9519b3dbea098b8.xml", "tamanho_arquivo": 4198, "tamanho_formatado": "4.1 KB", "status_processamento": 1}], "estatisticas": {"tipos_arquivo": {"text/plain": 1}, "total_tamanho": 4198, "ultimo_upload": "2025-10-15 00:47:07", "total_arquivos": 1, "primeiro_upload": "2025-10-15 00:47:07", "total_tamanho_formatado": "4.1 KB"}, "data_consulta": "2025-10-15T00:47:29.434796"}	2025-10-15 00:47:29.434796	2
25	1	david	01/01/2025	100	2025-10-15 00:21:41.398768	N.F RECEBIDA	AAQkADhmM2FmNmY0LTFiMjAtNGZmYi05ODQ5LTYyMGZhNTZiOTkyNQAQADNfbgz_l6BPjG35cpJrXiE=	\N	\N	\N	pending	\N	23	https://api.link.dev.br/dvprocessamento/envio-nf/8087a85e38cea73d0050676447744167	2025-11-14	0	2025-10-15 00:21:43.397927	Registro criado com sucesso	8087a85e38cea73d0050676447744167	{"arquivos": [{"id": 18, "data_upload": "2025-10-15 00:22:06", "observacoes": "", "hash_arquivo": "f5afca9dc375aa689ca0b3743bd1056a", "nome_arquivo": "8087a85e38cea73d0050676447744167.pdf", "tipo_arquivo": "application/pdf", "link_download": "https://api.link.dev.br/dvprocessamento/envio-nf/arquivosNF/8087a85e38cea73d0050676447744167.pdf", "nome_original": "NFS-e 202500000000010 SNA8-UQQ4 | WebISS®.pdf", "caminho_arquivo": "arquivosNF/8087a85e38cea73d0050676447744167.pdf", "tamanho_arquivo": 255618, "tamanho_formatado": "249.63 KB", "status_processamento": 1}], "estatisticas": {"tipos_arquivo": {"application/pdf": 1}, "total_tamanho": 255618, "ultimo_upload": "2025-10-15 00:22:06", "total_arquivos": 1, "primeiro_upload": "2025-10-15 00:22:06", "total_tamanho_formatado": "249.63 KB"}, "data_consulta": "2025-10-15T00:30:29.535818"}	2025-10-15 00:30:29.535818	2
44	8	Lucelino Alves Ribeiro	05/10/2025 – 22/10/2025	1120	2025-10-15 12:25:59.995756	Em Aberto	AAQkADhmM2FmNmY0LTFiMjAtNGZmYi05ODQ5LTYyMGZhNTZiOTkyNQAQACNV1Rn66LVMnAx43rV2VIE=	\N	\N	\N	pending	\N	42	https://api.link.dev.br/dvprocessamento/envio-nf/01308a3e0bcf4f1f76d044655781803f	2025-11-14	0	2025-10-15 12:26:01.432219	Registro criado com sucesso	01308a3e0bcf4f1f76d044655781803f	\N	2025-10-16 01:08:48.198633	0
43	9	Mardem Emidio Vieira Reis	05/10/2025 – 22/10/2025	550	2025-10-15 12:19:28.110994	Em Aberto	AAQkADhmM2FmNmY0LTFiMjAtNGZmYi05ODQ5LTYyMGZhNTZiOTkyNQAQAHD7cJ54kaNLi87RO0i8mQ4=	\N	\N	\N	pending	\N	41	https://api.link.dev.br/dvprocessamento/envio-nf/7e3e2c88688f5248b52f9c8e90a1fcd5	2025-11-14	0	2025-10-15 12:19:29.560954	Registro criado com sucesso	7e3e2c88688f5248b52f9c8e90a1fcd5	\N	2025-10-16 01:08:49.190663	0
42	3	50.831.850 Eliardo Pereira De Souza	05/10/2025 – 22/10/2025	2750	2025-10-15 12:19:24.095624	Em Aberto	AAQkADhmM2FmNmY0LTFiMjAtNGZmYi05ODQ5LTYyMGZhNTZiOTkyNQAQABySUMtpiHtPkuD-BrGIxc4=	\N	\N	\N	pending	\N	40	https://api.link.dev.br/dvprocessamento/envio-nf/5c5be2336864cf42df28cee32f3ffd31	2025-11-14	0	2025-10-15 12:19:25.48619	Registro criado com sucesso	5c5be2336864cf42df28cee32f3ffd31	\N	2025-10-16 01:08:50.125109	0
35	1	david	01/01/2025 - 08/09/2025	100	2025-10-15 11:04:09.214549	N.F RECEBIDA	AAQkADhmM2FmNmY0LTFiMjAtNGZmYi05ODQ5LTYyMGZhNTZiOTkyNQAQAI3ey5tmAG9LtDXhHg9TwD4=	\N	\N	\N	pending	\N	33	https://api.link.dev.br/dvprocessamento/envio-nf/bf9d9dc2b406d4505b4d0fb406ff7fb0	2025-11-14	0	2025-10-15 11:04:10.658046	Registro criado com sucesso	bf9d9dc2b406d4505b4d0fb406ff7fb0	{"arquivos": [{"id": 27, "data_upload": "2025-10-15 11:04:35", "observacoes": "", "hash_arquivo": "b5a2132b49be5b6863cdd65daa33b3f7", "nome_arquivo": "bf9d9dc2b406d4505b4d0fb406ff7fb0.xml", "tipo_arquivo": "text/plain", "link_download": "https://api.link.dev.br/dvprocessamento/envio-nf/arquivosNF/bf9d9dc2b406d4505b4d0fb406ff7fb0.xml", "nome_original": "14233850_NFSeNotaFiscaldeServicosEletronica_009374.xml", "caminho_arquivo": "arquivosNF/bf9d9dc2b406d4505b4d0fb406ff7fb0.xml", "tamanho_arquivo": 4247, "tamanho_formatado": "4.15 KB", "status_processamento": 1}], "estatisticas": {"tipos_arquivo": {"text/plain": 1}, "total_tamanho": 4247, "ultimo_upload": "2025-10-15 11:04:35", "total_arquivos": 1, "primeiro_upload": "2025-10-15 11:04:35", "total_tamanho_formatado": "4.15 KB"}, "data_consulta": "2025-10-15T11:05:08.394690"}	2025-10-15 11:05:08.39469	2
36	1	david	01/01/2025 - 02/02/2025	100	2025-10-15 11:13:28.069391	N.F RECEBIDA	AAQkADhmM2FmNmY0LTFiMjAtNGZmYi05ODQ5LTYyMGZhNTZiOTkyNQAQAI3ey5tmAG9LtDXhHg9TwD4=	\N	\N	\N	pending	\N	34	https://api.link.dev.br/dvprocessamento/envio-nf/625fcea75c207ab61b8b1fb5f719ded6	2025-11-14	0	2025-10-15 11:13:29.433675	Registro criado com sucesso	625fcea75c207ab61b8b1fb5f719ded6	{"arquivos": [{"id": 28, "data_upload": "2025-10-15 11:13:46", "observacoes": "", "hash_arquivo": "9c0d6b63beac65b27cbc6844d038316d", "nome_arquivo": "625fcea75c207ab61b8b1fb5f719ded6.xml", "tipo_arquivo": "text/plain", "link_download": "https://api.link.dev.br/dvprocessamento/envio-nf/arquivosNF/625fcea75c207ab61b8b1fb5f719ded6.xml", "nome_original": "14233850_NFSeNotaFiscaldeServicosEletronica_009375.xml", "caminho_arquivo": "arquivosNF/625fcea75c207ab61b8b1fb5f719ded6.xml", "tamanho_arquivo": 4196, "tamanho_formatado": "4.1 KB", "status_processamento": 1}], "estatisticas": {"tipos_arquivo": {"text/plain": 1}, "total_tamanho": 4196, "ultimo_upload": "2025-10-15 11:13:46", "total_arquivos": 1, "primeiro_upload": "2025-10-15 11:13:46", "total_tamanho_formatado": "4.1 KB"}, "data_consulta": "2025-10-15T11:13:59.331093"}	2025-10-15 11:13:59.331093	2
37	1	david	05/10/2025 – 22/10/2025	14350	2025-10-15 11:17:25.386082	N.F RECEBIDA	AAQkADhmM2FmNmY0LTFiMjAtNGZmYi05ODQ5LTYyMGZhNTZiOTkyNQAQAEm4G4pa5gxDgNjHXF1_d3w=	\N	\N	\N	pending	\N	35	https://api.link.dev.br/dvprocessamento/envio-nf/3848ef926240148cd91f610a77b10d1e	2025-11-14	0	2025-10-15 11:17:26.667686	Registro criado com sucesso	3848ef926240148cd91f610a77b10d1e	{"arquivos": [{"id": 29, "data_upload": "2025-10-15 11:18:12", "observacoes": "", "hash_arquivo": "5bc766394cbb7a12197cacfba60561bf", "nome_arquivo": "3848ef926240148cd91f610a77b10d1e.pdf", "tipo_arquivo": "application/pdf", "link_download": "https://api.link.dev.br/dvprocessamento/envio-nf/arquivosNF/3848ef926240148cd91f610a77b10d1e.pdf", "nome_original": "Relatorio_Potencia_Ferragista_E_Ar_Condicionado_Ltda_Lote_48.pdf", "caminho_arquivo": "arquivosNF/3848ef926240148cd91f610a77b10d1e.pdf", "tamanho_arquivo": 27989, "tamanho_formatado": "27.33 KB", "status_processamento": 1}], "estatisticas": {"tipos_arquivo": {"application/pdf": 1}, "total_tamanho": 27989, "ultimo_upload": "2025-10-15 11:18:12", "total_arquivos": 1, "primeiro_upload": "2025-10-15 11:18:12", "total_tamanho_formatado": "27.33 KB"}, "data_consulta": "2025-10-15T11:19:00.175529"}	2025-10-15 11:19:00.175529	2
40	10	Potencia Ferragista E Ar Condicionado Ltda	05/10/2025 – 22/10/2025	13550	2025-10-15 11:24:36.39926	N.F RECEBIDA	AAQkADhmM2FmNmY0LTFiMjAtNGZmYi05ODQ5LTYyMGZhNTZiOTkyNQAQANNbnBaYNF1Jug5fd-qwPzA=	\N	\N	\N	pending	\N	38	https://api.link.dev.br/dvprocessamento/envio-nf/3973e7c77c31d16284f6eebd21689af9	2025-11-14	0	2025-10-15 11:24:37.644882	Registro criado com sucesso	3973e7c77c31d16284f6eebd21689af9	{"arquivos": [{"id": 31, "data_upload": "2025-10-15 12:59:40", "observacoes": "", "hash_arquivo": "7295363779eacad262c037b8b8fd21d2", "nome_arquivo": "3973e7c77c31d16284f6eebd21689af9.pdf", "tipo_arquivo": "application/pdf", "link_download": "https://api.link.dev.br/dvprocessamento/envio-nf/arquivosNF/3973e7c77c31d16284f6eebd21689af9.pdf", "nome_original": "NOTA FISCAL NOVO MUNDO 2.pdf", "caminho_arquivo": "arquivosNF/3973e7c77c31d16284f6eebd21689af9.pdf", "tamanho_arquivo": 146349, "tamanho_formatado": "142.92 KB", "status_processamento": 1}], "estatisticas": {"tipos_arquivo": {"application/pdf": 1}, "total_tamanho": 146349, "ultimo_upload": "2025-10-15 12:59:40", "total_arquivos": 1, "primeiro_upload": "2025-10-15 12:59:40", "total_tamanho_formatado": "142.92 KB"}, "data_consulta": "2025-10-15T13:00:03.775618"}	2025-10-15 13:00:03.775618	2
46	1	david	01/01/2025	100	2025-10-15 13:33:07.678509	N.F RECEBIDA	AAQkADhmM2FmNmY0LTFiMjAtNGZmYi05ODQ5LTYyMGZhNTZiOTkyNQAQANc8NZDEpXBGv5NTx53XohU=	\N	\N	\N	pending	\N	45	https://api.link.dev.br/dvprocessamento/envio-nf/f78f64b12de19e0bd50257e84a1e1c30	2025-11-14	0	2025-10-15 13:33:09.503231	Registro criado com sucesso	f78f64b12de19e0bd50257e84a1e1c30	{"arquivos": [{"id": 32, "data_upload": "2025-10-15 13:35:14", "observacoes": "", "hash_arquivo": "f5afca9dc375aa689ca0b3743bd1056a", "nome_arquivo": "f78f64b12de19e0bd50257e84a1e1c30.pdf", "tipo_arquivo": "application/pdf", "link_download": "https://api.link.dev.br/dvprocessamento/envio-nf/arquivosNF/f78f64b12de19e0bd50257e84a1e1c30.pdf", "nome_original": "NFS-e 202500000000010 SNA8-UQQ4 | WebISS®.pdf", "caminho_arquivo": "arquivosNF/f78f64b12de19e0bd50257e84a1e1c30.pdf", "tamanho_arquivo": 255618, "tamanho_formatado": "249.63 KB", "status_processamento": 1}], "estatisticas": {"tipos_arquivo": {"application/pdf": 1}, "total_tamanho": 255618, "ultimo_upload": "2025-10-15 13:35:14", "total_arquivos": 1, "primeiro_upload": "2025-10-15 13:35:14", "total_tamanho_formatado": "249.63 KB"}, "data_consulta": "2025-10-15T13:36:00.555422"}	2025-10-15 13:36:00.555422	2
48	1	david	01/02/2025	100	2025-10-15 15:56:06.622008	N.F RECEBIDA	AAQkADhmM2FmNmY0LTFiMjAtNGZmYi05ODQ5LTYyMGZhNTZiOTkyNQAQAGNnPKy1dbFEhUOtpwp982w=	\N	\N	\N	pending	\N	50	https://api.link.dev.br/dvprocessamento/envio-nf/4a5dda326b50a88358bac0fa8a81f69c	2025-11-14	0	2025-10-15 15:56:07.898505	Registro criado com sucesso	4a5dda326b50a88358bac0fa8a81f69c	{"arquivos": [{"id": 36, "data_upload": "2025-10-15 15:56:42", "observacoes": "", "hash_arquivo": "32a00fca3d243775e72ea3a4aa173057", "nome_arquivo": "4a5dda326b50a88358bac0fa8a81f69c.pdf", "tipo_arquivo": "application/pdf", "link_download": "https://api.link.dev.br/dvprocessamento/envio-nf/arquivosNF/4a5dda326b50a88358bac0fa8a81f69c.pdf", "nome_original": "nota fiscal novo mundo.pdf", "caminho_arquivo": "arquivosNF/4a5dda326b50a88358bac0fa8a81f69c.pdf", "tamanho_arquivo": 288050, "tamanho_formatado": "281.3 KB", "status_processamento": 1}], "estatisticas": {"tipos_arquivo": {"application/pdf": 1}, "total_tamanho": 288050, "ultimo_upload": "2025-10-15 15:56:42", "total_arquivos": 1, "primeiro_upload": "2025-10-15 15:56:42", "total_tamanho_formatado": "281.3 KB"}, "data_consulta": "2025-10-15T16:01:24.620289"}	2025-10-15 16:01:24.620289	2
47	1	david	01/01/2025	100	2025-10-15 14:06:57.786219	N.F RECEBIDA	AAQkADhmM2FmNmY0LTFiMjAtNGZmYi05ODQ5LTYyMGZhNTZiOTkyNQAQAOqM6SnrHCVPmRNArFcABrA=	\N	\N	\N	pending	\N	48	https://api.link.dev.br/dvprocessamento/envio-nf/2d6dc979cd2d550330b9c2de2de9b449	2025-11-14	0	2025-10-15 14:07:00.452971	Registro criado com sucesso	2d6dc979cd2d550330b9c2de2de9b449	{"arquivos": [{"id": 34, "data_upload": "2025-10-15 14:07:21", "observacoes": "", "hash_arquivo": "ef6c5749cddf9595bac1ab6f941a6376", "nome_arquivo": "2d6dc979cd2d550330b9c2de2de9b449.pdf", "tipo_arquivo": "application/pdf", "link_download": "https://api.link.dev.br/dvprocessamento/envio-nf/arquivosNF/2d6dc979cd2d550330b9c2de2de9b449.pdf", "nome_original": "NOVO MUNDO DAVID GABRIEL NF 645.pdf", "caminho_arquivo": "arquivosNF/2d6dc979cd2d550330b9c2de2de9b449.pdf", "tamanho_arquivo": 459446, "tamanho_formatado": "448.68 KB", "status_processamento": 1}], "estatisticas": {"tipos_arquivo": {"application/pdf": 1}, "total_tamanho": 459446, "ultimo_upload": "2025-10-15 14:07:21", "total_arquivos": 1, "primeiro_upload": "2025-10-15 14:07:21", "total_tamanho_formatado": "448.68 KB"}, "data_consulta": "2025-10-15T15:45:29.394082"}	2025-10-15 15:45:29.394082	2
41	11	20.224.238 Maigregom Santos Ribeiro	05/10/2025 – 22/10/2025	600	2025-10-15 12:19:19.831575	N.F RECEBIDA	AAQkADhmM2FmNmY0LTFiMjAtNGZmYi05ODQ5LTYyMGZhNTZiOTkyNQAQABi67WP0msdFlfy_B-RGpko=	\N	\N	\N	pending	\N	39	https://api.link.dev.br/dvprocessamento/envio-nf/6882b13e66985675ad089df3e75bac95	2025-11-14	0	2025-10-15 12:19:21.285702	Registro criado com sucesso	6882b13e66985675ad089df3e75bac95	{"arquivos": [{"id": 43, "data_upload": "2025-10-15 18:34:18", "observacoes": "", "hash_arquivo": "9347f64276d534df4fcb5b8bf3fa42ec", "nome_arquivo": "6882b13e66985675ad089df3e75bac95.pdf", "tipo_arquivo": "application/pdf", "link_download": "https://api.link.dev.br/dvprocessamento/envio-nf/arquivosNF/6882b13e66985675ad089df3e75bac95.pdf", "nome_original": "15008002220224238000108000000000010525104605831650.pdf", "caminho_arquivo": "arquivosNF/6882b13e66985675ad089df3e75bac95.pdf", "tamanho_arquivo": 73039, "tamanho_formatado": "71.33 KB", "status_processamento": 1}], "estatisticas": {"tipos_arquivo": {"application/pdf": 1}, "total_tamanho": 73039, "ultimo_upload": "2025-10-15 18:34:18", "total_arquivos": 1, "primeiro_upload": "2025-10-15 18:34:18", "total_tamanho_formatado": "71.33 KB"}, "data_consulta": "2025-10-15T18:34:49.065088"}	2025-10-15 18:34:49.065088	2
51	1	david	01/02/2026	115	2025-10-15 19:43:46.681036	Em Aberto	AAQkADhmM2FmNmY0LTFiMjAtNGZmYi05ODQ5LTYyMGZhNTZiOTkyNQAQAC1mg1I-N4JNgh8Xd-x8-Do=	\N	\N	\N	pending	\N	58	https://api.link.dev.br/dvprocessamento/envio-nf/0c125474cb5cf5d7a350fdb1e4a831b8	2025-11-14	0	2025-10-15 19:43:47.98574	Registro criado com sucesso	0c125474cb5cf5d7a350fdb1e4a831b8	\N	2025-10-16 01:08:46.348217	0
50	12	M&T Engenharia Com. E Servicos Ltda	05/10/2025 – 22/10/2025	550	2025-10-15 19:27:38.099016	Em Aberto	AAQkADhmM2FmNmY0LTFiMjAtNGZmYi05ODQ5LTYyMGZhNTZiOTkyNQAQAPVd0pZcBctAnygER0BMTf0=	\N	\N	\N	pending	\N	57	https://api.link.dev.br/dvprocessamento/envio-nf/6db6ef1f9bd6204780211e214e29e94c	2025-11-14	0	2025-10-15 19:27:39.424782	Registro criado com sucesso	6db6ef1f9bd6204780211e214e29e94c	\N	2025-10-16 01:08:47.281783	0
\.


--
-- TOC entry 3935 (class 0 OID 16430)
-- Dependencies: 217
-- Data for Name: montadores; Type: TABLE DATA; Schema: public; Owner: davidgabriel
--

COPY public.montadores (id, nome, identificador, email, percentual_comissao, auxilio_semanal, ativo, fornecedor_id, regra_envio, dias_envio, emails_adicionais) FROM stdin;
1	DAVID DIAS	1	tiodavidg3@gmail.com	0.05	100	t	12	Nenhuma		\N
2	JOSIMAR SOUZA DE RESENDE 02082283143	3956	josimar_345@hotmail.com	0.08	50	t	132612	Mensal (Dia Fixo)		\N
3	61.277.954 JHONNATAN MARTINS FERREIRA	3945	jhonnjhonn24hrs@gmail.com	0.1	50	t	1928111	Quinzenal		\N
\.


--
-- TOC entry 3949 (class 0 OID 16538)
-- Dependencies: 231
-- Data for Name: notificacoes; Type: TABLE DATA; Schema: public; Owner: davidgabriel
--

COPY public.notificacoes (id, tipo, titulo, mensagem, lote_id, lida, data_criacao, data_leitura, icone, prioridade) FROM stdin;
815	erro	❌ Erro no Backup Automático	Falha ao criar backup: Erro desconhecido	\N	t	2025-10-15 11:59:58.649094	2025-10-15 12:12:14.621113	❌	1
817	erro	❌ Erro no Backup Automático	Falha ao criar backup: Erro desconhecido	\N	t	2025-10-15 12:19:58.657079	2025-10-15 12:21:23.629953	❌	1
754	nf_recebida	📥 Nota Fiscal Recebida - Lote #21	david enviou 1 arquivo(s) da nota fiscal (294.58 KB)	21	t	2025-10-14 23:53:01.55718	2025-10-14 23:53:02.267765	📥	1
726	teste	🧪 Teste de Toast	Esta é uma notificação de teste para validar o sistema de toasts. Ela deve aparecer apenas UMA vez quando você abrir o app.	\N	t	2025-10-14 23:31:40.753465	2025-10-14 23:31:47.55064	🔔	0
753	nf_recebida	📥 Nota Fiscal Recebida - Lote #22	david enviou 1 arquivo(s) da nota fiscal (95.95 KB)	22	t	2025-10-14 23:52:59.921296	2025-10-14 23:53:02.341363	📥	1
752	nf_recebida	📥 Nota Fiscal Recebida - Lote #23	david enviou 1 arquivo(s) da nota fiscal (448.68 KB)	23	t	2025-10-14 23:52:58.285233	2025-10-14 23:53:02.34887	📥	1
751	nf_recebida	📥 Nota Fiscal Recebida - Lote #24	david enviou 1 arquivo(s) da nota fiscal (95.95 KB)	24	t	2025-10-14 23:52:56.626554	2025-10-14 23:53:02.35435	📥	1
756	nf_recebida	📥 Nota Fiscal Recebida - Lote #19	david enviou 1 arquivo(s) da nota fiscal (294.58 KB)	19	t	2025-10-14 23:53:04.809335	2025-10-14 23:53:05.017451	📥	1
755	nf_recebida	📥 Nota Fiscal Recebida - Lote #20	david enviou 1 arquivo(s) da nota fiscal (294.58 KB)	20	t	2025-10-14 23:53:03.164017	2025-10-14 23:53:05.031174	📥	1
757	sucesso	💾 Backup Automático Criado	Backup do banco criado com sucesso: backup_20251014_235428.sql (0.06 MB)	\N	t	2025-10-14 23:54:28.824057	2025-10-14 23:55:14.279391	💾	0
821	sucesso	💾 Backup Automático Criado	Backup do banco criado com sucesso: backup_20251015_124057.sql (0.12 MB)	\N	t	2025-10-15 12:40:58.344428	2025-10-15 12:41:05.669502	💾	0
758	nf_recebida	📥 Nota Fiscal Recebida - Lote #25	david enviou 1 arquivo(s) da nota fiscal (249.63 KB)	25	t	2025-10-15 00:30:32.091129	2025-10-15 00:36:26.115836	📥	1
823	sucesso	💾 Backup Automático Criado	Backup do banco criado com sucesso: backup_20251015_124657.sql (0.12 MB)	\N	t	2025-10-15 12:46:57.602815	2025-10-15 12:47:45.492936	💾	0
760	nf_recebida	📥 Nota Fiscal Recebida - Lote #27	david enviou 1 arquivo(s) da nota fiscal (4.09 KB)	27	t	2025-10-15 00:39:29.642502	2025-10-15 00:39:31.219792	📥	1
759	erro	❌ Erro no Backup Automático	Falha ao criar backup: Erro desconhecido	\N	t	2025-10-15 00:39:28.475164	2025-10-15 00:39:31.28971	❌	1
761	nf_recebida	📥 Nota Fiscal Recebida - Lote #26	david enviou 1 arquivo(s) da nota fiscal (4.1 KB)	26	t	2025-10-15 00:47:30.13524	2025-10-15 00:47:39.461971	📥	1
825	erro	❌ Erro no Backup Automático	Falha ao criar backup: Erro desconhecido	\N	t	2025-10-15 12:49:58.614555	2025-10-15 12:53:49.555543	❌	1
762	erro	❌ Erro no Backup Automático	Falha ao criar backup: Erro desconhecido	\N	t	2025-10-15 00:49:28.4551	2025-10-15 00:53:53.747541	❌	1
763	nf_recebida	📥 Nota Fiscal Recebida - Lote #28	david enviou 1 arquivo(s) da nota fiscal (4.1 KB)	28	t	2025-10-15 00:55:29.614449	2025-10-15 00:55:29.914593	📥	1
827	nf_recebida	📥 Nota Fiscal Recebida - Lote #40	Potencia Ferragista E Ar Condicionado Ltda enviou 1 arquivo(s) da nota fiscal (142.92 KB)	40	t	2025-10-15 13:00:07.533714	2025-10-15 13:15:27.431976	📥	1
764	erro	❌ Erro no Backup Automático	Falha ao criar backup: Erro desconhecido	\N	t	2025-10-15 00:59:28.471676	2025-10-15 01:09:23.742334	❌	1
765	erro	❌ Erro no Backup Automático	Falha ao criar backup: Erro desconhecido	\N	t	2025-10-15 01:09:28.452245	2025-10-15 01:13:10.339752	❌	1
829	erro	❌ Erro no Backup Automático	Falha ao criar backup: Erro desconhecido	\N	t	2025-10-15 13:19:58.627294	2025-10-15 13:30:28.947995	❌	1
766	nf_recebida	📥 Nota Fiscal Recebida - Lote #29	david enviou 1 arquivo(s) da nota fiscal (4.15 KB)	29	t	2025-10-15 01:14:29.931886	2025-10-15 01:14:30.35005	📥	1
767	erro	❌ Erro no Backup Automático	Falha ao criar backup: Erro desconhecido	\N	t	2025-10-15 01:19:28.499234	2025-10-15 01:19:40.809831	❌	1
768	nf_recebida	📥 Nota Fiscal Recebida - Lote #30	david enviou 1 arquivo(s) da nota fiscal (4.09 KB)	30	t	2025-10-15 01:20:29.707511	2025-10-15 01:20:31.143775	📥	1
833	erro	❌ Erro no Backup Automático	Falha ao criar backup: Erro desconhecido	\N	t	2025-10-15 13:49:58.643868	2025-10-15 13:51:51.596602	❌	1
769	nf_recebida	📥 Nota Fiscal Recebida - Lote #31	david enviou 1 arquivo(s) da nota fiscal (4.57 KB)	31	t	2025-10-15 01:26:29.624092	2025-10-15 01:29:52.308053	📥	1
831	nf_recebida	📥 Nota Fiscal Recebida - Lote #46	david enviou 1 arquivo(s) da nota fiscal (249.63 KB)	46	t	2025-10-15 13:36:03.90436	2025-10-15 13:51:51.748602	📥	1
770	nf_recebida	📥 Nota Fiscal Recebida - Lote #32	david enviou 1 arquivo(s) da nota fiscal (4.15 KB)	32	t	2025-10-15 01:30:59.887317	2025-10-15 01:31:16.369592	📥	1
835	erro	❌ Erro no Backup Automático	Falha ao criar backup: Erro desconhecido	\N	t	2025-10-15 13:59:58.660048	2025-10-15 14:03:23.365198	❌	1
846	nf_recebida	📥 Nota Fiscal Recebida - Lote #47	david enviou 1 arquivo(s) da nota fiscal (448.68 KB)	47	t	2025-10-15 15:45:33.860203	2025-10-15 15:54:14.855301	📥	1
845	erro	❌ Erro no Backup Automático	Falha ao criar backup: Erro desconhecido	\N	t	2025-10-15 15:39:58.618033	2025-10-15 15:54:14.863508	❌	1
843	erro	❌ Erro no Backup Automático	Falha ao criar backup: Erro desconhecido	\N	t	2025-10-15 15:19:58.646948	2025-10-15 15:54:14.8761	❌	1
841	erro	❌ Erro no Backup Automático	Falha ao criar backup: Erro desconhecido	\N	t	2025-10-15 14:59:58.619261	2025-10-15 15:54:22.608753	❌	1
839	erro	❌ Erro no Backup Automático	Falha ao criar backup: Erro desconhecido	\N	t	2025-10-15 14:39:58.621619	2025-10-15 15:54:22.63168	❌	1
837	erro	❌ Erro no Backup Automático	Falha ao criar backup: Erro desconhecido	\N	t	2025-10-15 14:19:58.646193	2025-10-15 15:54:41.741934	❌	1
771	erro	❌ Erro no Backup Automático	Falha ao criar backup: Erro desconhecido	\N	t	2025-10-15 01:39:58.831214	\N	❌	1
772	erro	❌ Erro no Backup Automático	Falha ao criar backup: Erro desconhecido	\N	t	2025-10-15 01:59:58.609327	\N	❌	1
773	erro	❌ Erro no Backup Automático	Falha ao criar backup: Erro desconhecido	\N	t	2025-10-15 02:09:58.61685	\N	❌	1
774	erro	❌ Erro no Backup Automático	Falha ao criar backup: Erro desconhecido	\N	t	2025-10-15 02:19:58.609264	\N	❌	1
6	nf_recebida	📥 Nota Fiscal Recebida - Lote #24	david enviou 1 arquivo(s) da nota fiscal (95.95 KB)	24	t	2025-10-14 21:20:18.817375	2025-10-14 23:19:19.531899	📥	1
5	nf_recebida	📥 Nota Fiscal Recebida - Lote #19	david enviou 1 arquivo(s) da nota fiscal (294.58 KB)	19	t	2025-10-14 21:08:17.186035	2025-10-14 23:19:19.537135	📥	1
4	nf_recebida	📥 Nota Fiscal Recebida - Lote #20	david enviou 1 arquivo(s) da nota fiscal (294.58 KB)	20	t	2025-10-14 21:08:15.599887	2025-10-14 23:19:19.542524	📥	1
3	nf_recebida	📥 Nota Fiscal Recebida - Lote #21	david enviou 1 arquivo(s) da nota fiscal (294.58 KB)	21	t	2025-10-14 21:08:14.05439	2025-10-14 23:19:19.547673	📥	1
2	nf_recebida	📥 Nota Fiscal Recebida - Lote #22	david enviou 1 arquivo(s) da nota fiscal (95.95 KB)	22	t	2025-10-14 21:08:12.43091	2025-10-14 23:19:19.55487	📥	1
1	nf_recebida	📥 Nota Fiscal Recebida - Lote #23	david enviou 1 arquivo(s) da nota fiscal (448.68 KB)	23	t	2025-10-14 21:08:10.676814	2025-10-14 23:19:19.561972	📥	1
816	erro	❌ Erro no Backup Automático	Falha ao criar backup: Erro desconhecido	\N	t	2025-10-15 12:09:58.76381	2025-10-15 12:12:14.601508	❌	1
818	erro	❌ Erro no Backup Automático	Falha ao criar backup: Erro desconhecido	\N	t	2025-10-15 12:29:58.649803	2025-10-15 12:30:10.823557	❌	1
820	erro	❌ Erro no Backup Automático	Falha ao criar backup: Erro desconhecido	\N	t	2025-10-15 12:39:58.620889	2025-10-15 12:40:51.469494	❌	1
822	sucesso	💾 Backup Automático Criado	Backup do banco criado com sucesso: backup_20251015_124156.sql (0.12 MB)	\N	t	2025-10-15 12:41:56.19287	2025-10-15 12:42:17.615898	💾	0
824	sucesso	💾 Backup Automático Criado	Backup do banco criado com sucesso: backup_20251015_124817.sql (0.12 MB)	\N	t	2025-10-15 12:48:17.850941	2025-10-15 12:48:31.945063	💾	0
801	erro	❌ Erro no Backup Automático	Falha ao criar backup: Erro desconhecido	\N	t	2025-10-15 10:19:58.61197	2025-10-15 10:24:17.032543	❌	1
800	erro	❌ Erro no Backup Automático	Falha ao criar backup: Erro desconhecido	\N	t	2025-10-15 10:09:58.6269	2025-10-15 10:24:17.049724	❌	1
799	erro	❌ Erro no Backup Automático	Falha ao criar backup: Erro desconhecido	\N	t	2025-10-15 09:39:58.681828	2025-10-15 10:24:17.057469	❌	1
798	erro	❌ Erro no Backup Automático	Falha ao criar backup: Erro desconhecido	\N	t	2025-10-15 09:29:58.676307	2025-10-15 10:24:17.064749	❌	1
797	erro	❌ Erro no Backup Automático	Falha ao criar backup: Erro desconhecido	\N	t	2025-10-15 09:19:58.717141	2025-10-15 10:24:17.072961	❌	1
796	erro	❌ Erro no Backup Automático	Falha ao criar backup: Erro desconhecido	\N	t	2025-10-15 09:09:58.616073	2025-10-15 10:27:36.083064	❌	1
795	erro	❌ Erro no Backup Automático	Falha ao criar backup: Erro desconhecido	\N	t	2025-10-15 08:59:58.616257	2025-10-15 10:27:36.09861	❌	1
794	erro	❌ Erro no Backup Automático	Falha ao criar backup: Erro desconhecido	\N	t	2025-10-15 08:49:58.61921	2025-10-15 10:27:36.148884	❌	1
793	erro	❌ Erro no Backup Automático	Falha ao criar backup: Erro desconhecido	\N	t	2025-10-15 08:39:58.615102	2025-10-15 10:27:36.183498	❌	1
792	erro	❌ Erro no Backup Automático	Falha ao criar backup: Erro desconhecido	\N	t	2025-10-15 08:29:58.587783	2025-10-15 10:27:36.239081	❌	1
775	erro	❌ Erro no Backup Automático	Falha ao criar backup: Erro desconhecido	\N	t	2025-10-15 02:29:58.602178	\N	❌	1
776	erro	❌ Erro no Backup Automático	Falha ao criar backup: Erro desconhecido	\N	t	2025-10-15 02:39:58.601764	\N	❌	1
777	erro	❌ Erro no Backup Automático	Falha ao criar backup: Erro desconhecido	\N	t	2025-10-15 02:49:58.616384	\N	❌	1
778	erro	❌ Erro no Backup Automático	Falha ao criar backup: Erro desconhecido	\N	t	2025-10-15 02:59:58.607474	\N	❌	1
779	erro	❌ Erro no Backup Automático	Falha ao criar backup: Erro desconhecido	\N	t	2025-10-15 03:09:58.626237	\N	❌	1
780	erro	❌ Erro no Backup Automático	Falha ao criar backup: Erro desconhecido	\N	t	2025-10-15 03:29:58.612642	\N	❌	1
781	erro	❌ Erro no Backup Automático	Falha ao criar backup: Erro desconhecido	\N	t	2025-10-15 03:39:58.603989	\N	❌	1
782	erro	❌ Erro no Backup Automático	Falha ao criar backup: Erro desconhecido	\N	t	2025-10-15 03:59:58.622723	\N	❌	1
783	erro	❌ Erro no Backup Automático	Falha ao criar backup: Erro desconhecido	\N	t	2025-10-15 04:09:58.628445	\N	❌	1
784	erro	❌ Erro no Backup Automático	Falha ao criar backup: Erro desconhecido	\N	t	2025-10-15 05:29:58.613877	\N	❌	1
785	erro	❌ Erro no Backup Automático	Falha ao criar backup: Erro desconhecido	\N	t	2025-10-15 06:19:58.620801	\N	❌	1
786	erro	❌ Erro no Backup Automático	Falha ao criar backup: Erro desconhecido	\N	t	2025-10-15 06:59:58.621061	\N	❌	1
787	erro	❌ Erro no Backup Automático	Falha ao criar backup: Erro desconhecido	\N	t	2025-10-15 07:09:59.49687	\N	❌	1
788	erro	❌ Erro no Backup Automático	Falha ao criar backup: Erro desconhecido	\N	t	2025-10-15 07:49:58.611797	\N	❌	1
789	erro	❌ Erro no Backup Automático	Falha ao criar backup: Erro desconhecido	\N	t	2025-10-15 07:59:58.70279	\N	❌	1
790	erro	❌ Erro no Backup Automático	Falha ao criar backup: Erro desconhecido	\N	t	2025-10-15 08:09:58.719079	\N	❌	1
791	erro	❌ Erro no Backup Automático	Falha ao criar backup: Erro desconhecido	\N	t	2025-10-15 08:19:58.622183	\N	❌	1
828	erro	❌ Erro no Backup Automático	Falha ao criar backup: Erro desconhecido	\N	t	2025-10-15 13:09:58.626642	2025-10-15 13:15:27.277769	❌	1
826	erro	❌ Erro no Backup Automático	Falha ao criar backup: Erro desconhecido	\N	t	2025-10-15 12:59:58.628637	2025-10-15 13:15:27.439663	❌	1
803	erro	❌ Erro no Backup Automático	Falha ao criar backup: Erro desconhecido	\N	t	2025-10-15 10:39:58.641012	2025-10-15 10:47:25.594482	❌	1
802	erro	❌ Erro no Backup Automático	Falha ao criar backup: Erro desconhecido	\N	t	2025-10-15 10:29:58.635087	2025-10-15 10:47:25.614253	❌	1
804	erro	❌ Erro no Backup Automático	Falha ao criar backup: Erro desconhecido	\N	t	2025-10-15 10:49:58.615596	2025-10-15 10:54:25.89344	❌	1
830	erro	❌ Erro no Backup Automático	Falha ao criar backup: Erro desconhecido	\N	t	2025-10-15 13:29:58.609995	2025-10-15 13:30:28.804871	❌	1
806	erro	❌ Erro no Backup Automático	Falha ao criar backup: Erro desconhecido	\N	t	2025-10-15 10:59:58.936502	2025-10-15 11:02:47.72349	❌	1
805	nf_recebida	📥 Nota Fiscal Recebida - Lote #34	david enviou 1 arquivo(s) da nota fiscal (752.17 KB)	34	t	2025-10-15 10:58:05.302524	2025-10-15 11:02:47.749163	📥	1
832	erro	❌ Erro no Backup Automático	Falha ao criar backup: Erro desconhecido	\N	t	2025-10-15 13:39:58.616082	2025-10-15 13:51:51.741182	❌	1
807	nf_recebida	📥 Nota Fiscal Recebida - Lote #35	david enviou 1 arquivo(s) da nota fiscal (4.15 KB)	35	t	2025-10-15 11:05:09.265466	2025-10-15 11:06:46.596945	📥	1
808	erro	❌ Erro no Backup Automático	Falha ao criar backup: Erro desconhecido	\N	t	2025-10-15 11:09:58.68123	2025-10-15 11:12:51.669617	❌	1
809	nf_recebida	📥 Nota Fiscal Recebida - Lote #36	david enviou 1 arquivo(s) da nota fiscal (4.1 KB)	36	t	2025-10-15 11:14:00.083626	2025-10-15 11:15:21.453374	📥	1
836	erro	❌ Erro no Backup Automático	Falha ao criar backup: Erro desconhecido	\N	t	2025-10-15 14:09:58.689801	2025-10-15 14:09:58.848006	❌	1
810	nf_recebida	📥 Nota Fiscal Recebida - Lote #37	david enviou 1 arquivo(s) da nota fiscal (27.33 KB)	37	t	2025-10-15 11:19:01.207368	2025-10-15 11:19:14.368029	📥	1
811	erro	❌ Erro no Backup Automático	Falha ao criar backup: Erro desconhecido	\N	t	2025-10-15 11:19:58.610513	2025-10-15 11:20:28.03373	❌	1
812	erro	❌ Erro no Backup Automático	Falha ao criar backup: Erro desconhecido	\N	t	2025-10-15 11:29:58.634659	2025-10-15 11:31:58.025499	❌	1
814	erro	❌ Erro no Backup Automático	Falha ao criar backup: Erro desconhecido	\N	t	2025-10-15 11:49:58.879932	2025-10-15 11:53:31.972423	❌	1
813	erro	❌ Erro no Backup Automático	Falha ao criar backup: Erro desconhecido	\N	t	2025-10-15 11:39:58.669451	2025-10-15 11:53:31.997927	❌	1
842	erro	❌ Erro no Backup Automático	Falha ao criar backup: Erro desconhecido	\N	t	2025-10-15 15:09:58.59498	2025-10-15 15:54:22.596442	❌	1
840	erro	❌ Erro no Backup Automático	Falha ao criar backup: Erro desconhecido	\N	t	2025-10-15 14:49:58.657567	2025-10-15 15:54:22.621998	❌	1
838	erro	❌ Erro no Backup Automático	Falha ao criar backup: Erro desconhecido	\N	t	2025-10-15 14:29:58.68312	2025-10-15 15:54:22.64217	❌	1
847	erro	❌ Erro no Backup Automático	Falha ao criar backup: Erro desconhecido	\N	t	2025-10-15 15:49:58.68694	2025-10-15 15:54:14.699358	❌	1
844	erro	❌ Erro no Backup Automático	Falha ao criar backup: Erro desconhecido	\N	t	2025-10-15 15:29:58.618399	2025-10-15 15:54:14.869795	❌	1
848	nf_recebida	📥 Nota Fiscal Recebida - Lote #48	david enviou 1 arquivo(s) da nota fiscal (281.3 KB)	48	t	2025-10-15 16:01:27.778758	2025-10-15 16:01:27.961695	📥	1
852	sucesso	💾 Backup Automático Criado	Backup do banco criado com sucesso: backup_20251015_163023.sql (0.13 MB)	\N	t	2025-10-15 16:30:23.961672	2025-10-15 16:34:05.620381	💾	0
851	sucesso	💾 Backup Automático Criado	Backup do banco criado com sucesso: backup_20251015_162023.sql (0.13 MB)	\N	t	2025-10-15 16:20:24.206449	2025-10-15 16:34:05.726413	💾	0
850	sucesso	💾 Backup Automático Criado	Backup do banco criado com sucesso: backup_20251015_161024.sql (0.13 MB)	\N	t	2025-10-15 16:10:24.789551	2025-10-15 16:34:05.734267	💾	0
853	nf_recebida	📥 Nota Fiscal Recebida - Lote #33	david enviou 1 arquivo(s) da nota fiscal (37.45 KB)	33	t	2025-10-15 16:38:29.159279	2025-10-15 16:38:31.944934	📥	1
854	sucesso	💾 Backup Automático Criado	Backup do banco criado com sucesso: backup_20251015_164023.sql (0.13 MB)	\N	t	2025-10-15 16:40:23.771482	2025-10-15 16:48:13.008785	💾	0
855	nf_recebida_montador	📥 Nota Fiscal Recebida - Montador #6	DAVID DIAS enviou 1 arquivo(s) da nota fiscal (27.33 KB)	6	t	2025-10-15 16:48:39.014148	2025-10-15 16:49:04.784895	📥	1
857	sucesso	💾 Backup Automático Criado	Backup do banco criado com sucesso: backup_20251015_170023.sql (0.13 MB)	\N	t	2025-10-15 17:00:24.023648	2025-10-15 17:02:16.842645	💾	0
856	sucesso	💾 Backup Automático Criado	Backup do banco criado com sucesso: backup_20251015_165023.sql (0.13 MB)	\N	t	2025-10-15 16:50:24.015882	2025-10-15 17:02:16.858952	💾	0
858	nf_recebida_montador	📥 Nota Fiscal Recebida - Montador #7	DAVID DIAS enviou 1 arquivo(s) da nota fiscal (27.33 KB)	7	t	2025-10-15 17:03:39.670647	2025-10-15 17:07:59.34921	📥	1
859	sucesso	💾 Backup Automático Criado	Backup do banco criado com sucesso: backup_20251015_171023.sql (0.13 MB)	\N	t	2025-10-15 17:10:24.211774	2025-10-15 17:11:10.272899	💾	0
860	sucesso	💾 Backup Automático Criado	Backup do banco criado com sucesso: backup_20251015_172023.sql (0.13 MB)	\N	t	2025-10-15 17:20:24.023638	2025-10-15 17:20:56.494398	💾	0
861	nf_recebida_montador	📥 Nota Fiscal Recebida - Montador #8	DAVID DIAS enviou 1 arquivo(s) da nota fiscal (37.45 KB)	8	t	2025-10-15 17:23:37.578068	2025-10-15 17:26:35.335817	📥	1
862	sucesso	💾 Backup Automático Criado	Backup do banco criado com sucesso: backup_20251015_173023.sql (0.14 MB)	\N	t	2025-10-15 17:30:24.224449	2025-10-15 17:31:37.199355	💾	0
865	sucesso	💾 Backup Automático Criado	Backup do banco criado com sucesso: backup_20251015_180023.sql (0.14 MB)	\N	t	2025-10-15 18:00:23.856631	2025-10-15 18:07:10.815919	💾	0
864	sucesso	💾 Backup Automático Criado	Backup do banco criado com sucesso: backup_20251015_175023.sql (0.14 MB)	\N	t	2025-10-15 17:50:23.851883	2025-10-15 18:07:10.937926	💾	0
863	sucesso	💾 Backup Automático Criado	Backup do banco criado com sucesso: backup_20251015_174023.sql (0.14 MB)	\N	t	2025-10-15 17:40:24.003163	2025-10-15 18:07:10.947928	💾	0
866	nf_recebida_montador	📥 Nota Fiscal Recebida - Montador #9	JOSIMAR SOUZA DE RESENDE 02082283143 enviou 1 arquivo(s) da nota fiscal (89.06 KB)	9	t	2025-10-15 18:11:01.290993	2025-10-15 18:11:02.769164	📥	1
867	nf_recebida_montador	📥 Nota Fiscal Recebida - Montador #10	DAVID DIAS enviou 1 arquivo(s) da nota fiscal (37.45 KB)	10	t	2025-10-15 18:12:59.894619	2025-10-15 18:14:39.871434	📥	1
868	nf_recebida	📥 Nota Fiscal Recebida - Lote #41	20.224.238 Maigregom Santos Ribeiro enviou 1 arquivo(s) da nota fiscal (71.33 KB)	41	t	2025-10-15 18:34:50.588075	2025-10-15 19:16:37.153039	📥	1
869	sucesso	💾 Backup Automático Criado	Backup do banco criado com sucesso: backup_20251015_190945.sql (0.14 MB)	\N	t	2025-10-15 19:09:46.339963	2025-10-15 19:16:37.176208	💾	0
870	nf_recebida	📥 Nota Fiscal Recebida - Lote #53	david enviou 1 arquivo(s) da nota fiscal (37.45 KB)	53	t	2025-10-15 19:54:48.017876	2025-10-15 19:54:54.253095	📥	1
871	nf_recebida_montador	📥 Nota Fiscal Recebida - Montador #11	DAVID DIAS enviou 1 arquivo(s) da nota fiscal (37.45 KB)	11	t	2025-10-15 19:58:02.331117	2025-10-15 19:59:45.213746	📥	1
872	sucesso	💾 Backup Automático Criado	Backup do banco criado com sucesso: backup_20251015_200945.sql (0.15 MB)	\N	t	2025-10-15 20:09:46.714746	2025-10-15 20:10:12.501868	💾	0
873	sucesso	💾 Backup Automático Criado	Backup do banco criado com sucesso: backup_20251015_210945.sql (0.15 MB)	\N	f	2025-10-15 21:09:46.34637	\N	💾	0
874	sucesso	💾 Backup Automático Criado	Backup do banco criado com sucesso: backup_20251015_220945.sql (0.15 MB)	\N	f	2025-10-15 22:09:46.227881	\N	💾	0
875	sucesso	💾 Backup Automático Criado	Backup do banco criado com sucesso: backup_20251015_230945.sql (0.15 MB)	\N	f	2025-10-15 23:09:46.217815	\N	💾	0
876	sucesso	💾 Backup Automático Criado	Backup do banco criado com sucesso: backup_20251016_000945.sql (0.15 MB)	\N	f	2025-10-16 00:09:46.245606	\N	💾	0
\.


--
-- TOC entry 3947 (class 0 OID 16517)
-- Dependencies: 229
-- Data for Name: os_blacklist; Type: TABLE DATA; Schema: public; Owner: davidgabriel
--

COPY public.os_blacklist (id, prestador_id, os_numero, data_adicao, motivo) FROM stdin;
1	2	Aqui estão todos os números separados por vírgula	2025-10-13 11:18:28.310504	ja pago. erro no sistema
2	2	conforme você pediu:  55237	2025-10-13 11:18:28.359753	ja pago. erro no sistema
3	2	55269	2025-10-13 11:18:28.36869	ja pago. erro no sistema
4	2	55280	2025-10-13 11:18:28.3777	ja pago. erro no sistema
5	2	55314	2025-10-13 11:18:28.389848	ja pago. erro no sistema
6	2	55315	2025-10-13 11:18:28.430983	ja pago. erro no sistema
7	2	55323	2025-10-13 11:18:28.442843	ja pago. erro no sistema
8	2	55375	2025-10-13 11:18:28.453886	ja pago. erro no sistema
9	2	55376	2025-10-13 11:18:28.465578	ja pago. erro no sistema
10	2	55429	2025-10-13 11:18:28.484541	ja pago. erro no sistema
11	2	55434	2025-10-13 11:18:28.50021	ja pago. erro no sistema
12	2	55473	2025-10-13 11:18:28.51553	ja pago. erro no sistema
13	2	56441	2025-10-13 11:18:28.534506	ja pago. erro no sistema
14	2	58764	2025-10-13 11:18:28.54294	ja pago. erro no sistema
15	2	60850	2025-10-13 11:18:28.554735	ja pago. erro no sistema
16	2	61873	2025-10-13 11:18:28.568837	ja pago. erro no sistema
17	2	62973	2025-10-13 11:18:28.58642	ja pago. erro no sistema
18	2	63185	2025-10-13 11:18:28.597564	ja pago. erro no sistema
19	2	55237	2025-10-13 11:18:28.612712	ja pago. erro no sistema
131	10	55255	2025-10-15 11:15:31.39811	ja pago
133	10	61558	2025-10-15 11:15:31.422553	ja pago
135	10	62212	2025-10-15 11:15:31.440986	ja pago
137	8	62520	2025-10-15 12:21:43.927428	ja pago
53	2	55298	2025-10-13 11:18:28.908764	ja pago. erro no sistema
54	2	55397	2025-10-13 11:18:28.916808	ja pago. erro no sistema
55	2	56718	2025-10-13 11:18:28.925818	ja pago. erro no sistema
56	2	57535	2025-10-13 11:18:28.932202	ja pago. erro no sistema
57	2	58252	2025-10-13 11:18:28.941138	ja pago. erro no sistema
58	2	58408	2025-10-13 11:18:28.948167	ja pago. erro no sistema
59	2	58948	2025-10-13 11:18:28.953815	ja pago. erro no sistema
60	2	58992	2025-10-13 11:18:28.965886	ja pago. erro no sistema
61	2	59308	2025-10-13 11:18:28.97398	ja pago. erro no sistema
62	2	59726	2025-10-13 11:18:28.980024	ja pago. erro no sistema
63	2	59883	2025-10-13 11:18:28.987966	ja pago. erro no sistema
64	2	60115	2025-10-13 11:23:29.164686	ja pago. erro no sistema
65	2	60220	2025-10-13 11:23:29.230174	ja pago. erro no sistema
66	2	60834	2025-10-13 11:23:29.29488	ja pago. erro no sistema
67	2	59479	2025-10-13 11:23:29.300651	ja pago. erro no sistema
68	2	60376	2025-10-13 11:23:29.307106	ja pago. erro no sistema
69	2	60386	2025-10-13 11:23:29.313316	ja pago. erro no sistema
70	2	60387	2025-10-13 11:23:29.323155	ja pago. erro no sistema
71	2	60634	2025-10-13 11:23:29.382052	ja pago. erro no sistema
72	2	60749	2025-10-13 11:23:29.390228	ja pago. erro no sistema
73	2	60845	2025-10-13 11:23:29.402287	ja pago. erro no sistema
74	2	61825	2025-10-13 11:23:29.413613	ja pago. erro no sistema
75	2	62269	2025-10-13 11:23:29.430049	ja pago. erro no sistema
76	2	62270	2025-10-13 11:23:29.444885	ja pago. erro no sistema
78	2		2025-10-13 11:23:43.243384	ja pago. erro no sistema
90	2	59619	2025-10-13 11:51:04.182292	bug
91	2	59695	2025-10-13 11:51:04.19169	bug
92	2	59820	2025-10-13 11:51:04.197416	bug
93	2	61206	2025-10-13 11:51:04.203854	bug
132	10	55438	2025-10-15 11:15:31.413184	ja pago
134	10	61866	2025-10-15 11:15:31.431235	ja pago
136	10	63473	2025-10-15 11:15:31.449076	ja pago
138	8	62522	2025-10-15 12:21:50.83293	ja pago
122	2	55424	2025-10-13 11:51:04.381657	bug
123	2	55425	2025-10-13 11:51:04.388856	bug
124	2	52894	2025-10-13 11:51:04.395498	bug
125	2	53024	2025-10-13 11:51:04.402774	bug
126	2	53186	2025-10-13 11:51:04.408481	bug
127	2	54274	2025-10-13 11:51:04.41528	bug
128	2	54275	2025-10-13 11:51:04.421588	bug
129	2	54277	2025-10-13 11:51:04.427446	bug
130	2	54725	2025-10-13 11:51:04.433298	bug
\.


--
-- TOC entry 3939 (class 0 OID 16459)
-- Dependencies: 221
-- Data for Name: os_enviadas; Type: TABLE DATA; Schema: public; Owner: davidgabriel
--

COPY public.os_enviadas (id, lote_id, os_numero, detalhes) FROM stdin;
14	4	1212121212	{"o_s": "1212121212", "cliente": "teste daviud", "periodo": "teste", "localidade": "goiania", "modalidade": "ac", "valor_extra": 0.0, "valor_total": 100.0, "motivo_extra": "", "status_envio": "Pendente", "data_execucao": "2025-10-21", "nome_prestador": "david", "valor_custo_prestador": 100.0}
26	6	55366	{"o_s": "55366", "e_mail": null, "cliente": "Evangelista Jose Pereira", "periodo": "05/10/2025 – 22/10/2025", "localidade": "GOIANIA", "modalidade": "INSTALAÇÃO DE AR CONDICIONADO 9 A 12 MIL BTUS (SEM RAPEL)", "valor_extra": 0, "valor_total": 600, "motivo_extra": null, "status_envio": "Pendente", "data_execucao": "2025-10-13T00:00:00", "nome_prestador": "52.417.932 Leogilson Dos Santos Silva", "valor_custo_prestador": 600}
27	6	55402	{"o_s": "55402", "e_mail": null, "cliente": "Jose Rodrigues De Sousa", "periodo": "05/10/2025 – 22/10/2025", "localidade": "GOIANIA", "modalidade": "INSTALAÇÃO DE AR CONDICIONADO 9 A 12 MIL BTUS (SEM RAPEL)", "valor_extra": 0, "valor_total": 600, "motivo_extra": null, "status_envio": "Pendente", "data_execucao": "2025-10-08T00:00:00", "nome_prestador": "52.417.932 Leogilson Dos Santos Silva", "valor_custo_prestador": 600}
28	6	55426	{"o_s": "55426", "e_mail": null, "cliente": "Laucirene Oliveira De Lima", "periodo": "05/10/2025 – 22/10/2025", "localidade": "GOIANIA", "modalidade": "INSTALAÇÃO DE AR CONDICIONADO 9 A 12 MIL BTUS (SEM RAPEL)", "valor_extra": 0, "valor_total": 600, "motivo_extra": null, "status_envio": "Pendente", "data_execucao": "2025-10-08T00:00:00", "nome_prestador": "52.417.932 Leogilson Dos Santos Silva", "valor_custo_prestador": 600}
29	6	55433	{"o_s": "55433", "e_mail": null, "cliente": "Fabio Correia Guimaraes Luiz", "periodo": "05/10/2025 – 22/10/2025", "localidade": "GOIANIA", "modalidade": "INSTALAÇÃO DE AR CONDICIONADO 9 A 12 MIL BTUS (SEM RAPEL)", "valor_extra": 0, "valor_total": 600, "motivo_extra": null, "status_envio": "Pendente", "data_execucao": "2025-10-13T00:00:00", "nome_prestador": "52.417.932 Leogilson Dos Santos Silva", "valor_custo_prestador": 600}
30	6	55474	{"o_s": "55474", "e_mail": null, "cliente": "Florence Rodrigues Valadares", "periodo": "05/10/2025 – 22/10/2025", "localidade": "GOIANIA", "modalidade": "DESINSTALAÇÃO + INSTALAÇÃO DE AR CONDICIONADO ATÉ 12 MIL BTUS (SEM RAPEL)", "valor_extra": 0, "valor_total": 800, "motivo_extra": null, "status_envio": "Pendente", "data_execucao": "2025-10-08T00:00:00", "nome_prestador": "52.417.932 Leogilson Dos Santos Silva", "valor_custo_prestador": 800}
31	6	55510	{"o_s": "55510", "e_mail": null, "cliente": "Thiago Medrado Rodrigues Frois", "periodo": "05/10/2025 – 22/10/2025", "localidade": "TRINDADE", "modalidade": "INSTALAÇÃO DE AR CONDICIONADO 9 A 12 MIL BTUS (SEM RAPEL)", "valor_extra": 0, "valor_total": 600, "motivo_extra": null, "status_envio": "Pendente", "data_execucao": "2025-10-08T00:00:00", "nome_prestador": "52.417.932 Leogilson Dos Santos Silva", "valor_custo_prestador": 600}
32	6	58159	{"o_s": "58159", "e_mail": null, "cliente": "Cleudson Pereira Da Silva", "periodo": "05/10/2025 – 22/10/2025", "localidade": "APARECIDA DE GOIANIA", "modalidade": "DESINSTALAÇÃO DE AR CONDICIONADO  7.000 A 14.000  BTUS (SEM RAPEL)", "valor_extra": 0, "valor_total": 250, "motivo_extra": null, "status_envio": "Pendente", "data_execucao": "2025-10-13T00:00:00", "nome_prestador": "52.417.932 Leogilson Dos Santos Silva", "valor_custo_prestador": 250}
33	6	59707	{"o_s": "59707", "e_mail": null, "cliente": "Leticia Mariana De Morais", "periodo": "05/10/2025 – 22/10/2025", "localidade": "APARECIDA DE GOIANIA", "modalidade": "INSTALAÇÃO DE AR CONDICIONADO 9 A 12 MIL BTUS (SEM RAPEL)", "valor_extra": 0, "valor_total": 600, "motivo_extra": null, "status_envio": "Pendente", "data_execucao": "2025-10-13T00:00:00", "nome_prestador": "52.417.932 Leogilson Dos Santos Silva", "valor_custo_prestador": 600}
34	6	60227	{"o_s": "60227", "e_mail": null, "cliente": "Vanessa Pereira Dos Santos", "periodo": "05/10/2025 – 22/10/2025", "localidade": "GOIANIA", "modalidade": "INSTALAÇÃO DE AR CONDICIONADO 9 A 12 MIL BTUS (SEM RAPEL)", "valor_extra": 0, "valor_total": 600, "motivo_extra": null, "status_envio": "Pendente", "data_execucao": "2025-10-13T00:00:00", "nome_prestador": "52.417.932 Leogilson Dos Santos Silva", "valor_custo_prestador": 600}
35	6	62935	{"o_s": "62935", "e_mail": null, "cliente": "Noe Luiz Da Mota", "periodo": "05/10/2025 – 22/10/2025", "localidade": "GOIANIA", "modalidade": "INSTALAÇÃO DE AR CONDICIONADO 9 A 12 MIL BTUS (SEM RAPEL)", "valor_extra": 0, "valor_total": 600, "motivo_extra": null, "status_envio": "Pendente", "data_execucao": "2025-10-13T00:00:00", "nome_prestador": "52.417.932 Leogilson Dos Santos Silva", "valor_custo_prestador": 600}
36	6	63184	{"o_s": "63184", "e_mail": null, "cliente": "Jose Alves", "periodo": "05/10/2025 – 22/10/2025", "localidade": "GOIANIA", "modalidade": "INSTALAÇÃO DE AR CONDICIONADO 9 A 12 MIL BTUS (SEM RAPEL)", "valor_extra": 0, "valor_total": 600, "motivo_extra": null, "status_envio": "Pendente", "data_execucao": "2025-10-08T00:00:00", "nome_prestador": "52.417.932 Leogilson Dos Santos Silva", "valor_custo_prestador": 600}
37	6	63758	{"o_s": "63758", "e_mail": null, "cliente": "Maureen Barbanoglo Dias", "periodo": "05/10/2025 – 22/10/2025", "localidade": "GOIANIA", "modalidade": "INSTALAÇÃO DE AR CONDICIONADO 9 A 12 MIL BTUS (SEM RAPEL)", "valor_extra": 0, "valor_total": 600, "motivo_extra": null, "status_envio": "Pendente", "data_execucao": "2025-10-13T00:00:00", "nome_prestador": "52.417.932 Leogilson Dos Santos Silva", "valor_custo_prestador": 600}
38	6	63788	{"o_s": "63788", "e_mail": null, "cliente": "Luciene Da Serra Borges", "periodo": "05/10/2025 – 22/10/2025", "localidade": "TRINDADE", "modalidade": "INSTALAÇÃO DE AR CONDICIONADO 9 A 12 MIL BTUS (SEM RAPEL)", "valor_extra": 0, "valor_total": 600, "motivo_extra": null, "status_envio": "Pendente", "data_execucao": "2025-10-13T00:00:00", "nome_prestador": "52.417.932 Leogilson Dos Santos Silva", "valor_custo_prestador": 600}
39	6	64342	{"o_s": "64342", "e_mail": null, "cliente": "Wesley Freitas Silva", "periodo": "05/10/2025 – 22/10/2025", "localidade": "GOIANIA", "modalidade": "INSTALAÇÃO DE AR CONDICIONADO 9 A 12 MIL BTUS (SEM RAPEL)", "valor_extra": 0, "valor_total": 600, "motivo_extra": null, "status_envio": "Pendente", "data_execucao": "2025-10-08T00:00:00", "nome_prestador": "52.417.932 Leogilson Dos Santos Silva", "valor_custo_prestador": 600}
40	6	64667	{"o_s": "64667", "e_mail": null, "cliente": "Deusdete Batista Da Silva", "periodo": "05/10/2025 – 22/10/2025", "localidade": "GOIANIA", "modalidade": "INSTALAÇÃO DE AR CONDICIONADO 9 A 12 MIL BTUS (SEM RAPEL)", "valor_extra": 0, "valor_total": 600, "motivo_extra": null, "status_envio": "Pendente", "data_execucao": "2025-10-13T00:00:00", "nome_prestador": "52.417.932 Leogilson Dos Santos Silva", "valor_custo_prestador": 600}
41	7	10101010	{"o_s": "10101010", "cliente": "Thiago", "periodo": "01/01/2025 - 02/01/2025", "localidade": "Goiania", "modalidade": "Instalacao ac", "valor_extra": 0.0, "valor_total": 100.0, "motivo_extra": "", "status_envio": "Pendente", "data_execucao": "2025-10-22", "nome_prestador": "david", "valor_custo_prestador": 100.0}
42	8	18233	{"o_s": "18233", "e_mail": null, "cliente": "Fabio Santos Da Cunha", "periodo": "23/02/2025 – 04/03/2025", "localidade": "GOIANIA", "modalidade": "INSTALAÇÃO DE AR CONDICIONADO 9 A 12 MIL BTUS (SEM RAPEL)", "valor_extra": 0, "valor_total": 600, "motivo_extra": null, "status_envio": "Pendente", "data_execucao": "2025-08-28T00:00:00", "nome_prestador": "david", "valor_custo_prestador": 600}
43	9	10122	{"o_s": "10122", "e_mail": null, "cliente": "Geruza Jose Da Costa Rufino", "periodo": "23/08/2025 – 04/09/2025", "localidade": "APARECIDA DE GOIANIA", "modalidade": "INSTALAÇÃO DE AR CONDICIONADO 9 A 12 MIL BTUS (SEM RAPEL)", "valor_extra": 0, "valor_total": 600, "motivo_extra": null, "status_envio": "Pendente", "data_execucao": "2025-08-28T00:00:00", "nome_prestador": "david", "valor_custo_prestador": 600}
44	10	10111	{"o_s": "10111", "e_mail": null, "cliente": "Corina Goncalves Da Silva", "periodo": "23/08/2025 – 04/09/2025", "localidade": "GOIANIA", "modalidade": "INSTALAÇÃO DE AR CONDICIONADO 9 A 12 MIL BTUS (SEM RAPEL)", "valor_extra": 0, "valor_total": 600, "motivo_extra": null, "status_envio": "Pendente", "data_execucao": "2025-08-28T00:00:00", "nome_prestador": "thiago", "valor_custo_prestador": 600}
45	11	1010101	{"o_s": "1010101", "cliente": "david", "periodo": "teste David", "localidade": "goiani", "modalidade": "ac", "valor_extra": 0.0, "valor_total": 1000.0, "motivo_extra": "", "status_envio": "Pendente", "data_execucao": "2025-10-16", "nome_prestador": "david", "valor_custo_prestador": 1000.0}
46	12	98182	{"o_s": "98182", "cliente": "david", "periodo": "sei la", "localidade": "goiania", "modalidade": "ac", "valor_extra": 0.0, "valor_total": 100.0, "motivo_extra": "", "status_envio": "Pendente", "data_execucao": "2025-10-13", "nome_prestador": "david", "valor_custo_prestador": 100.0}
47	13	8128128	{"o_s": "8128128", "cliente": "david ", "periodo": "10/10/2025 - 11/10/2025", "localidade": "gyn", "modalidade": "ac", "valor_extra": 0.0, "valor_total": 1200.0, "motivo_extra": "", "status_envio": "Pendente", "data_execucao": "2025-10-13", "nome_prestador": "david", "valor_custo_prestador": 1200.0}
48	14	8172712	{"o_s": "8172712", "cliente": "David", "periodo": "01/01/2025 - 02/01/2025", "localidade": "goiania", "modalidade": "ac", "valor_extra": 0.0, "valor_total": 100.0, "motivo_extra": "", "status_envio": "Pendente", "data_execucao": "2025-10-14", "nome_prestador": "david", "valor_custo_prestador": 100.0}
49	15	98812	{"o_s": "98812", "cliente": "david", "periodo": "01/11/2025 - 02/11/2025", "localidade": "goiania", "modalidade": "ac", "valor_extra": 0.0, "valor_total": 150.0, "motivo_extra": "", "status_envio": "Pendente", "data_execucao": "2025-10-13", "nome_prestador": "david", "valor_custo_prestador": 150.0}
50	16	1234	{"o_s": "1234", "cliente": "DAVID", "periodo": "01/05/2025 - 03/05/2025", "localidade": "GO", "modalidade": "ACC", "valor_extra": 0.0, "valor_total": 100.0, "motivo_extra": "", "status_envio": "Pendente", "data_execucao": "2025-10-08", "nome_prestador": "david", "valor_custo_prestador": 100.0}
51	17	87121111	{"o_s": "87121111", "cliente": "david", "periodo": "01/01/2025 - 01/10/2025", "localidade": "goiania", "modalidade": "ac", "valor_extra": 0.0, "valor_total": 100.0, "motivo_extra": "", "status_envio": "Pendente", "data_execucao": "2025-10-14", "nome_prestador": "david", "valor_custo_prestador": 100.0}
52	18	981212	{"o_s": "981212", "cliente": "david", "periodo": "10/10/2025", "localidade": "goiania", "modalidade": "ar teste", "valor_extra": 0.0, "valor_total": 120.0, "motivo_extra": "", "status_envio": "Pendente", "data_execucao": "2025-10-22", "nome_prestador": "david", "valor_custo_prestador": 120.0}
53	19	9182812	{"o_s": "9182812", "cliente": "david", "periodo": "01/01/2025", "localidade": "goiania", "modalidade": "ac", "valor_extra": 0.0, "valor_total": 100.0, "motivo_extra": "", "status_envio": "Pendente", "data_execucao": "2025-10-22", "nome_prestador": "david", "valor_custo_prestador": 100.0}
54	20	881212	{"o_s": "881212", "cliente": "david", "periodo": "01/09/2025", "localidade": "anaplis", "modalidade": "ac", "valor_extra": 0.0, "valor_total": 250.0, "motivo_extra": "", "status_envio": "Pendente", "data_execucao": "2025-10-23", "nome_prestador": "david", "valor_custo_prestador": 250.0}
55	21	9182182	{"o_s": "9182182", "cliente": "david", "periodo": "01/01/2025", "localidade": "sao paulo", "modalidade": "ac", "valor_extra": 0.0, "valor_total": 100.0, "motivo_extra": "", "status_envio": "Pendente", "data_execucao": "2025-10-14", "nome_prestador": "david", "valor_custo_prestador": 100.0}
56	22	9128182	{"o_s": "9128182", "cliente": "david dias", "periodo": "01/01/2026", "localidade": "goiania", "modalidade": "ac", "valor_extra": 0.0, "valor_total": 120.0, "motivo_extra": "", "status_envio": "Pendente", "data_execucao": "2025-10-14", "nome_prestador": "david", "valor_custo_prestador": 120.0}
57	23	9128182182	{"o_s": "9128182182", "cliente": "david", "periodo": "01/01/2025", "localidade": "goiania", "modalidade": "ac", "valor_extra": 0.0, "valor_total": 120.0, "motivo_extra": "", "status_envio": "Pendente", "data_execucao": "2025-10-14", "nome_prestador": "david", "valor_custo_prestador": 120.0}
58	24	09128182182	{"o_s": "09128182182", "cliente": "david", "periodo": "01/01/2023", "localidade": "goiania", "modalidade": "ac", "valor_extra": 0.0, "valor_total": 100.0, "motivo_extra": "", "status_envio": "Pendente", "data_execucao": "2025-10-14", "nome_prestador": "david", "valor_custo_prestador": 100.0}
59	25	91828128182	{"o_s": "91828128182", "cliente": "david", "periodo": "01/01/2025", "localidade": "goiania", "modalidade": "ac", "valor_extra": 0.0, "valor_total": 100.0, "motivo_extra": "", "status_envio": "Pendente", "data_execucao": "2025-10-15", "nome_prestador": "david", "valor_custo_prestador": 100.0}
60	26	928382325	{"o_s": "928382325", "e_mail": null, "cliente": "Fabio Santos Da Cunha", "periodo": "23/02/2025 – 04/03/2025", "localidade": "GOIANIA", "modalidade": "INSTALAÇÃO DE AR CONDICIONADO 9 A 12 MIL BTUS (SEM RAPEL)", "valor_extra": 0, "valor_total": 600, "motivo_extra": null, "status_envio": "Pendente", "data_execucao": "2025-08-28T00:00:00", "nome_prestador": "david", "valor_custo_prestador": 600}
61	27	928382323	{"o_s": "928382323", "e_mail": null, "cliente": "Corina Goncalves Da Silva", "periodo": "23/08/2025 – 04/09/2025", "localidade": "GOIANIA", "modalidade": "INSTALAÇÃO DE AR CONDICIONADO 9 A 12 MIL BTUS (SEM RAPEL)", "valor_extra": 0, "valor_total": 600, "motivo_extra": null, "status_envio": "Pendente", "data_execucao": "2025-08-28T00:00:00", "nome_prestador": "david", "valor_custo_prestador": 600}
62	27	928382324	{"o_s": "928382324", "e_mail": null, "cliente": "Geruza Jose Da Costa Rufino", "periodo": "23/08/2025 – 04/09/2025", "localidade": "APARECIDA DE GOIANIA", "modalidade": "INSTALAÇÃO DE AR CONDICIONADO 9 A 12 MIL BTUS (SEM RAPEL)", "valor_extra": 0, "valor_total": 600, "motivo_extra": null, "status_envio": "Pendente", "data_execucao": "2025-08-28T00:00:00", "nome_prestador": "david", "valor_custo_prestador": 600}
63	28	91821218212	{"o_s": "91821218212", "cliente": "david dias", "periodo": "01/01/2025", "localidade": "goiania", "modalidade": "ac", "valor_extra": 0.0, "valor_total": 100.0, "motivo_extra": "", "status_envio": "Pendente", "data_execucao": "2025-10-22", "nome_prestador": "david", "valor_custo_prestador": 100.0}
64	29	9188182	{"o_s": "9188182", "cliente": "david", "periodo": "01/01/2025", "localidade": "gyn", "modalidade": "ac", "valor_extra": 0.0, "valor_total": 100.0, "motivo_extra": "", "status_envio": "Pendente", "data_execucao": "2025-10-22", "nome_prestador": "david", "valor_custo_prestador": 100.0}
65	30	7654321	{"o_s": "7654321", "cliente": "david", "periodo": "01/01/2025", "localidade": "gyn", "modalidade": "ac", "valor_extra": 0.0, "valor_total": 100.0, "motivo_extra": "", "status_envio": "Pendente", "data_execucao": "2025-10-15", "nome_prestador": "david", "valor_custo_prestador": 100.0}
66	31	65231111	{"o_s": "65231111", "cliente": "david", "periodo": "01/01/2025", "localidade": "goiania", "modalidade": "ac", "valor_extra": 0.0, "valor_total": 200.0, "motivo_extra": "", "status_envio": "Pendente", "data_execucao": "2025-10-22", "nome_prestador": "david", "valor_custo_prestador": 200.0}
67	32	128172	{"o_s": "128172", "cliente": "david", "periodo": "01/01/2025", "localidade": "gyn", "modalidade": "ac", "valor_extra": 0.0, "valor_total": 100.0, "motivo_extra": "", "status_envio": "Pendente", "data_execucao": "2025-10-15", "nome_prestador": "david", "valor_custo_prestador": 100.0}
68	33	812712	{"o_s": "812712", "cliente": "David", "periodo": "01/01/2025", "localidade": "goiania", "modalidade": "ac", "valor_extra": 0.0, "valor_total": 100.0, "motivo_extra": "", "status_envio": "Pendente", "data_execucao": "2025-10-07", "nome_prestador": "david", "valor_custo_prestador": 100.0}
69	34	7623111	{"o_s": "7623111", "cliente": "david", "periodo": "01/01/2025", "localidade": "goiania", "modalidade": "ac", "valor_extra": 0.0, "valor_total": 100.0, "motivo_extra": "", "status_envio": "Pendente", "data_execucao": "2025-10-15", "nome_prestador": "david", "valor_custo_prestador": 100.0}
70	35	44312112	{"o_s": "44312112", "cliente": "david", "periodo": "01/01/2025 - 08/09/2025", "localidade": "goiania", "modalidade": "ac", "valor_extra": 0.0, "valor_total": 100.0, "motivo_extra": "", "status_envio": "Pendente", "data_execucao": "2025-10-15", "nome_prestador": "david", "valor_custo_prestador": 100.0}
71	36	2323871	{"o_s": "2323871", "cliente": "david", "periodo": "01/01/2025 - 02/02/2025", "localidade": "goiania", "modalidade": "ac", "valor_extra": 0.0, "valor_total": 100.0, "motivo_extra": "", "status_envio": "Pendente", "data_execucao": "2025-10-15", "nome_prestador": "david", "valor_custo_prestador": 100.0}
72	37	82372733	{"o_s": "82372733", "e_mail": null, "cliente": "Pedro Rosa Da Silva", "periodo": "05/10/2025 – 22/10/2025", "localidade": "GOIANIA", "modalidade": "INSTALAÇÃO DE AR CONDICIONADO 9 A 12 MIL BTUS (SEM RAPEL)", "valor_extra": 0, "valor_total": 550, "motivo_extra": null, "status_envio": "Pendente", "data_execucao": "2025-10-13T00:00:00", "nome_prestador": "david", "valor_custo_prestador": 550}
73	37	82372734	{"o_s": "82372734", "e_mail": null, "cliente": "Marcelo Ferreira Dos Santos", "periodo": "05/10/2025 – 22/10/2025", "localidade": "GOIANIA", "modalidade": "INSTALAÇÃO DE AR CONDICIONADO 9 A 12 MIL BTUS (SEM RAPEL)", "valor_extra": 0, "valor_total": 550, "motivo_extra": null, "status_envio": "Pendente", "data_execucao": "2025-10-11T00:00:00", "nome_prestador": "david", "valor_custo_prestador": 550}
74	37	82372736	{"o_s": "82372736", "e_mail": null, "cliente": "Elza Correa", "periodo": "05/10/2025 – 22/10/2025", "localidade": "GOIANIRA", "modalidade": "INSTALAÇÃO DE AR CONDICIONADO 9 A 12 MIL BTUS (SEM RAPEL)", "valor_extra": 100, "valor_total": 650, "motivo_extra": "Adição de Valor Extra - Valor: R$100,00 - Motivo - DESLOCAMENTO", "status_envio": "Pendente", "data_execucao": "2025-10-11T00:00:00", "nome_prestador": "david", "valor_custo_prestador": 550}
75	37	82372739	{"o_s": "82372739", "e_mail": null, "cliente": "Ana Maria Terra Da Silva", "periodo": "05/10/2025 – 22/10/2025", "localidade": "GOIANIA", "modalidade": "INSTALAÇÃO DE AR CONDICIONADO 9 A 12 MIL BTUS (SEM RAPEL)", "valor_extra": 0, "valor_total": 550, "motivo_extra": null, "status_envio": "Pendente", "data_execucao": "2025-10-14T00:00:00", "nome_prestador": "david", "valor_custo_prestador": 550}
76	37	82372741	{"o_s": "82372741", "e_mail": null, "cliente": "Luiz Paulo Ferreira Nascimento Da Silva", "periodo": "05/10/2025 – 22/10/2025", "localidade": "HIDROLANDIA", "modalidade": "INSTALAÇÃO DE AR CONDICIONADO 9 A 12 MIL BTUS (SEM RAPEL)", "valor_extra": 100, "valor_total": 650, "motivo_extra": "Adição de Valor Extra - Valor: R$100,00 - Motivo - DESLOCAMENTO", "status_envio": "Pendente", "data_execucao": "2025-10-10T00:00:00", "nome_prestador": "david", "valor_custo_prestador": 550}
77	37	82372743	{"o_s": "82372743", "e_mail": null, "cliente": "Orcedina Nunes Da Silva", "periodo": "05/10/2025 – 22/10/2025", "localidade": "APARECIDA DE GOIANIA", "modalidade": "DESINSTALAÇÃO + INSTALAÇÃO DE AR CONDICIONADO ATÉ 12 MIL BTUS (SEM RAPEL)", "valor_extra": 0, "valor_total": 700, "motivo_extra": null, "status_envio": "Pendente", "data_execucao": "2025-10-09T00:00:00", "nome_prestador": "david", "valor_custo_prestador": 700}
78	37	82372744	{"o_s": "82372744", "e_mail": null, "cliente": "Gleicy Kelly Oliveira", "periodo": "05/10/2025 – 22/10/2025", "localidade": "APARECIDA DE GOIANIA", "modalidade": "INSTALAÇÃO DE AR CONDICIONADO 9 A 12 MIL BTUS (SEM RAPEL)", "valor_extra": 0, "valor_total": 550, "motivo_extra": null, "status_envio": "Pendente", "data_execucao": "2025-10-06T00:00:00", "nome_prestador": "david", "valor_custo_prestador": 550}
79	37	82372745	{"o_s": "82372745", "e_mail": null, "cliente": "Andreia Moreira De Abreu Rodrigues", "periodo": "05/10/2025 – 22/10/2025", "localidade": "GOIANIA", "modalidade": "INSTALAÇÃO DE AR CONDICIONADO 9 A 12 MIL BTUS (SEM RAPEL)", "valor_extra": 0, "valor_total": 550, "motivo_extra": null, "status_envio": "Pendente", "data_execucao": "2025-10-07T00:00:00", "nome_prestador": "david", "valor_custo_prestador": 550}
80	37	82372746	{"o_s": "82372746", "e_mail": null, "cliente": "Sandro Pereira Costa", "periodo": "05/10/2025 – 22/10/2025", "localidade": "GOIANIA", "modalidade": "INSTALAÇÃO DE AR CONDICIONADO 9 A 12 MIL BTUS (SEM RAPEL)", "valor_extra": 0, "valor_total": 550, "motivo_extra": null, "status_envio": "Pendente", "data_execucao": "2025-10-14T00:00:00", "nome_prestador": "david", "valor_custo_prestador": 550}
81	37	82372747	{"o_s": "82372747", "e_mail": null, "cliente": "Weber Brito Dos Passos", "periodo": "05/10/2025 – 22/10/2025", "localidade": "GOIANIA", "modalidade": "INSTALAÇÃO DE AR CONDICIONADO 9 A 12 MIL BTUS (SEM RAPEL)", "valor_extra": 0, "valor_total": 550, "motivo_extra": null, "status_envio": "Pendente", "data_execucao": "2025-10-10T00:00:00", "nome_prestador": "david", "valor_custo_prestador": 550}
82	37	82372748	{"o_s": "82372748", "e_mail": null, "cliente": "Bruno Celio Goulart Bittar", "periodo": "05/10/2025 – 22/10/2025", "localidade": "GOIANIA", "modalidade": "INSTALAÇÃO DE AR CONDICIONADO 9 A 12 MIL BTUS (SEM RAPEL)", "valor_extra": 150, "valor_total": 700, "motivo_extra": "Adição de Valor Extra - Valor: R$150,00 - Motivo - DESINSTALACAO", "status_envio": "Pendente", "data_execucao": "2025-10-09T00:00:00", "nome_prestador": "david", "valor_custo_prestador": 550}
83	37	82372749	{"o_s": "82372749", "e_mail": null, "cliente": "Jeane Nogueira Rodrigues De Oliveira", "periodo": "05/10/2025 – 22/10/2025", "localidade": "APARECIDA DE GOIANIA", "modalidade": "INSTALAÇÃO DE AR CONDICIONADO 9 A 12 MIL BTUS (SEM RAPEL)", "valor_extra": 0, "valor_total": 550, "motivo_extra": null, "status_envio": "Pendente", "data_execucao": "2025-10-10T00:00:00", "nome_prestador": "david", "valor_custo_prestador": 550}
84	37	82372750	{"o_s": "82372750", "e_mail": null, "cliente": "Claudione Jose Alves", "periodo": "05/10/2025 – 22/10/2025", "localidade": "APARECIDA DE GOIANIA", "modalidade": "INSTALAÇÃO DE AR CONDICIONADO 9 A 12 MIL BTUS (SEM RAPEL)", "valor_extra": 500, "valor_total": 1050, "motivo_extra": "Adição de Valor Extra - Valor: R$500,00 - Motivo - RETIRADA + INSTALACAO", "status_envio": "Pendente", "data_execucao": "2025-10-09T00:00:00", "nome_prestador": "david", "valor_custo_prestador": 550}
85	37	82372751	{"o_s": "82372751", "e_mail": null, "cliente": "Uriane Oliveira Da Rocha", "periodo": "05/10/2025 – 22/10/2025", "localidade": "GOIANIA", "modalidade": "INSTALAÇÃO DE AR CONDICIONADO 9 A 12 MIL BTUS (SEM RAPEL)", "valor_extra": 250, "valor_total": 800, "motivo_extra": "Adição de Valor Extra - Valor: R$250,00 - Motivo - MAQUINA SEM GAS", "status_envio": "Pendente", "data_execucao": "2025-10-13T00:00:00", "nome_prestador": "david", "valor_custo_prestador": 550}
86	37	82372752	{"o_s": "82372752", "e_mail": null, "cliente": "Cirilo Marques Neto", "periodo": "05/10/2025 – 22/10/2025", "localidade": "GOIANIA", "modalidade": "INSTALAÇÃO DE AR CONDICIONADO 9 A 12 MIL BTUS (SEM RAPEL)", "valor_extra": 0, "valor_total": 550, "motivo_extra": null, "status_envio": "Pendente", "data_execucao": "2025-10-13T00:00:00", "nome_prestador": "david", "valor_custo_prestador": 550}
87	37	82372753	{"o_s": "82372753", "e_mail": null, "cliente": "Andreia Aparecida Santos Schimidt", "periodo": "05/10/2025 – 22/10/2025", "localidade": "APARECIDA DE GOIANIA", "modalidade": "INSTALAÇÃO DE AR CONDICIONADO 9 A 12 MIL BTUS (SEM RAPEL)", "valor_extra": 0, "valor_total": 550, "motivo_extra": null, "status_envio": "Pendente", "data_execucao": "2025-10-13T00:00:00", "nome_prestador": "david", "valor_custo_prestador": 550}
88	37	82372754	{"o_s": "82372754", "e_mail": null, "cliente": "Joaci Souza De Sa", "periodo": "05/10/2025 – 22/10/2025", "localidade": "GOIANIA", "modalidade": "INSTALAÇÃO DE AR CONDICIONADO 9 A 12 MIL BTUS (SEM RAPEL)", "valor_extra": 0, "valor_total": 550, "motivo_extra": null, "status_envio": "Pendente", "data_execucao": "2025-10-11T00:00:00", "nome_prestador": "david", "valor_custo_prestador": 550}
89	37	82372755	{"o_s": "82372755", "e_mail": null, "cliente": "Joaci Souza De Sa", "periodo": "05/10/2025 – 22/10/2025", "localidade": "GOIANIA", "modalidade": "INSTALAÇÃO DE AR CONDICIONADO 9 A 12 MIL BTUS (SEM RAPEL)", "valor_extra": 0, "valor_total": 550, "motivo_extra": null, "status_envio": "Pendente", "data_execucao": "2025-10-11T00:00:00", "nome_prestador": "david", "valor_custo_prestador": 550}
90	37	82372756	{"o_s": "82372756", "e_mail": null, "cliente": "Itamar Rodrigues Quintanilha", "periodo": "05/10/2025 – 22/10/2025", "localidade": "TRINDADE", "modalidade": "INSTALAÇÃO DE AR CONDICIONADO 9 A 12 MIL BTUS (SEM RAPEL)", "valor_extra": 100, "valor_total": 650, "motivo_extra": "Adição de Valor Extra - Valor: R$100,00 - Motivo - DESLOCAMENTO", "status_envio": "Pendente", "data_execucao": "2025-10-14T00:00:00", "nome_prestador": "david", "valor_custo_prestador": 550}
91	37	82372757	{"o_s": "82372757", "e_mail": null, "cliente": "Maria Lucia De Araujo", "periodo": "05/10/2025 – 22/10/2025", "localidade": "TRINDADE", "modalidade": "INSTALAÇÃO DE AR CONDICIONADO 9 A 12 MIL BTUS (SEM RAPEL)", "valor_extra": 100, "valor_total": 650, "motivo_extra": "Adição de Valor Extra - Valor: R$100,00 - Motivo - DESLOCAMENTO", "status_envio": "Pendente", "data_execucao": "2025-10-14T00:00:00", "nome_prestador": "david", "valor_custo_prestador": 550}
92	37	82372758	{"o_s": "82372758", "e_mail": null, "cliente": "Jackellyne Sampaio Gomide Cruz", "periodo": "05/10/2025 – 22/10/2025", "localidade": "TRINDADE", "modalidade": "INSTALAÇÃO DE AR CONDICIONADO 9 A 12 MIL BTUS (SEM RAPEL)", "valor_extra": 100, "valor_total": 650, "motivo_extra": "Adição de Valor Extra - Valor: R$100,00 - Motivo - DESLOCAMENTO", "status_envio": "Pendente", "data_execucao": "2025-10-14T00:00:00", "nome_prestador": "david", "valor_custo_prestador": 550}
93	37	82372759	{"o_s": "82372759", "e_mail": null, "cliente": "Uriane Oliveira Da Rocha", "periodo": "05/10/2025 – 22/10/2025", "localidade": "GOIANIA", "modalidade": "INSTALAÇÃO DE AR CONDICIONADO 9 A 12 MIL BTUS (SEM RAPEL)", "valor_extra": 700, "valor_total": 1250, "motivo_extra": "Adição de Valor Extra - Valor: R$700,00 - Motivo - CUSTO EXTRA GAS + INSTLA + DESIS", "status_envio": "Pendente", "data_execucao": "2025-10-15T00:00:00", "nome_prestador": "david", "valor_custo_prestador": 550}
154	47	812812	{"o_s": "812812", "cliente": "david", "periodo": "01/01/2025", "localidade": "goiania", "modalidade": "ac", "valor_extra": 0.0, "valor_total": 100.0, "motivo_extra": "", "status_envio": "Pendente", "data_execucao": "2025-10-15", "nome_prestador": "david", "valor_custo_prestador": 100.0}
155	48	872352	{"o_s": "872352", "cliente": "davi dias", "periodo": "01/02/2025", "localidade": "gyn", "modalidade": "ac", "valor_extra": 0.0, "valor_total": 100.0, "motivo_extra": "", "status_envio": "Pendente", "data_execucao": "2025-10-15", "nome_prestador": "david", "valor_custo_prestador": 100.0}
122	40	55352	{"o_s": "55352", "e_mail": null, "cliente": "Pedro Rosa Da Silva", "periodo": "05/10/2025 – 22/10/2025", "localidade": "GOIANIA", "modalidade": "INSTALAÇÃO DE AR CONDICIONADO 9 A 12 MIL BTUS (SEM RAPEL)", "valor_extra": 0, "valor_total": 550, "motivo_extra": null, "status_envio": "Pendente", "data_execucao": "2025-10-13T00:00:00", "nome_prestador": "Potencia Ferragista E Ar Condicionado Ltda", "valor_custo_prestador": 550}
123	40	55358	{"o_s": "55358", "e_mail": null, "cliente": "Marcelo Ferreira Dos Santos", "periodo": "05/10/2025 – 22/10/2025", "localidade": "GOIANIA", "modalidade": "INSTALAÇÃO DE AR CONDICIONADO 9 A 12 MIL BTUS (SEM RAPEL)", "valor_extra": 0, "valor_total": 550, "motivo_extra": null, "status_envio": "Pendente", "data_execucao": "2025-10-11T00:00:00", "nome_prestador": "Potencia Ferragista E Ar Condicionado Ltda", "valor_custo_prestador": 550}
124	40	55448	{"o_s": "55448", "e_mail": null, "cliente": "Elza Correa", "periodo": "05/10/2025 – 22/10/2025", "localidade": "GOIANIRA", "modalidade": "INSTALAÇÃO DE AR CONDICIONADO 9 A 12 MIL BTUS (SEM RAPEL)", "valor_extra": 100, "valor_total": 650, "motivo_extra": "Adição de Valor Extra - Valor: R$100,00 - Motivo - DESLOCAMENTO", "status_envio": "Pendente", "data_execucao": "2025-10-11T00:00:00", "nome_prestador": "Potencia Ferragista E Ar Condicionado Ltda", "valor_custo_prestador": 550}
125	40	62051	{"o_s": "62051", "e_mail": null, "cliente": "Ana Maria Terra Da Silva", "periodo": "05/10/2025 – 22/10/2025", "localidade": "GOIANIA", "modalidade": "INSTALAÇÃO DE AR CONDICIONADO 9 A 12 MIL BTUS (SEM RAPEL)", "valor_extra": 0, "valor_total": 550, "motivo_extra": null, "status_envio": "Pendente", "data_execucao": "2025-10-14T00:00:00", "nome_prestador": "Potencia Ferragista E Ar Condicionado Ltda", "valor_custo_prestador": 550}
126	40	63466	{"o_s": "63466", "e_mail": null, "cliente": "Luiz Paulo Ferreira Nascimento Da Silva", "periodo": "05/10/2025 – 22/10/2025", "localidade": "HIDROLANDIA", "modalidade": "INSTALAÇÃO DE AR CONDICIONADO 9 A 12 MIL BTUS (SEM RAPEL)", "valor_extra": 100, "valor_total": 650, "motivo_extra": "Adição de Valor Extra - Valor: R$100,00 - Motivo - DESLOCAMENTO", "status_envio": "Pendente", "data_execucao": "2025-10-10T00:00:00", "nome_prestador": "Potencia Ferragista E Ar Condicionado Ltda", "valor_custo_prestador": 550}
127	40	63774	{"o_s": "63774", "e_mail": null, "cliente": "Orcedina Nunes Da Silva", "periodo": "05/10/2025 – 22/10/2025", "localidade": "APARECIDA DE GOIANIA", "modalidade": "DESINSTALAÇÃO + INSTALAÇÃO DE AR CONDICIONADO ATÉ 12 MIL BTUS (SEM RAPEL)", "valor_extra": 0, "valor_total": 700, "motivo_extra": null, "status_envio": "Pendente", "data_execucao": "2025-10-09T00:00:00", "nome_prestador": "Potencia Ferragista E Ar Condicionado Ltda", "valor_custo_prestador": 700}
128	40	64124	{"o_s": "64124", "e_mail": null, "cliente": "Gleicy Kelly Oliveira", "periodo": "05/10/2025 – 22/10/2025", "localidade": "APARECIDA DE GOIANIA", "modalidade": "INSTALAÇÃO DE AR CONDICIONADO 9 A 12 MIL BTUS (SEM RAPEL)", "valor_extra": 0, "valor_total": 550, "motivo_extra": null, "status_envio": "Pendente", "data_execucao": "2025-10-06T00:00:00", "nome_prestador": "Potencia Ferragista E Ar Condicionado Ltda", "valor_custo_prestador": 550}
129	40	64166	{"o_s": "64166", "e_mail": null, "cliente": "Andreia Moreira De Abreu Rodrigues", "periodo": "05/10/2025 – 22/10/2025", "localidade": "GOIANIA", "modalidade": "INSTALAÇÃO DE AR CONDICIONADO 9 A 12 MIL BTUS (SEM RAPEL)", "valor_extra": 0, "valor_total": 550, "motivo_extra": null, "status_envio": "Pendente", "data_execucao": "2025-10-07T00:00:00", "nome_prestador": "Potencia Ferragista E Ar Condicionado Ltda", "valor_custo_prestador": 550}
130	40	64207	{"o_s": "64207", "e_mail": null, "cliente": "Sandro Pereira Costa", "periodo": "05/10/2025 – 22/10/2025", "localidade": "GOIANIA", "modalidade": "INSTALAÇÃO DE AR CONDICIONADO 9 A 12 MIL BTUS (SEM RAPEL)", "valor_extra": 0, "valor_total": 550, "motivo_extra": null, "status_envio": "Pendente", "data_execucao": "2025-10-14T00:00:00", "nome_prestador": "Potencia Ferragista E Ar Condicionado Ltda", "valor_custo_prestador": 550}
131	40	64261	{"o_s": "64261", "e_mail": null, "cliente": "Weber Brito Dos Passos", "periodo": "05/10/2025 – 22/10/2025", "localidade": "GOIANIA", "modalidade": "INSTALAÇÃO DE AR CONDICIONADO 9 A 12 MIL BTUS (SEM RAPEL)", "valor_extra": 0, "valor_total": 550, "motivo_extra": null, "status_envio": "Pendente", "data_execucao": "2025-10-10T00:00:00", "nome_prestador": "Potencia Ferragista E Ar Condicionado Ltda", "valor_custo_prestador": 550}
132	40	64432	{"o_s": "64432", "e_mail": null, "cliente": "Bruno Celio Goulart Bittar", "periodo": "05/10/2025 – 22/10/2025", "localidade": "GOIANIA", "modalidade": "INSTALAÇÃO DE AR CONDICIONADO 9 A 12 MIL BTUS (SEM RAPEL)", "valor_extra": 150, "valor_total": 700, "motivo_extra": "Adição de Valor Extra - Valor: R$150,00 - Motivo - DESINSTALACAO", "status_envio": "Pendente", "data_execucao": "2025-10-09T00:00:00", "nome_prestador": "Potencia Ferragista E Ar Condicionado Ltda", "valor_custo_prestador": 550}
133	40	64435	{"o_s": "64435", "e_mail": null, "cliente": "Jeane Nogueira Rodrigues De Oliveira", "periodo": "05/10/2025 – 22/10/2025", "localidade": "APARECIDA DE GOIANIA", "modalidade": "INSTALAÇÃO DE AR CONDICIONADO 9 A 12 MIL BTUS (SEM RAPEL)", "valor_extra": 0, "valor_total": 550, "motivo_extra": null, "status_envio": "Pendente", "data_execucao": "2025-10-10T00:00:00", "nome_prestador": "Potencia Ferragista E Ar Condicionado Ltda", "valor_custo_prestador": 550}
134	40	64655	{"o_s": "64655", "e_mail": null, "cliente": "Claudione Jose Alves", "periodo": "05/10/2025 – 22/10/2025", "localidade": "APARECIDA DE GOIANIA", "modalidade": "INSTALAÇÃO DE AR CONDICIONADO 9 A 12 MIL BTUS (SEM RAPEL)", "valor_extra": 500, "valor_total": 1050, "motivo_extra": "Adição de Valor Extra - Valor: R$500,00 - Motivo - RETIRADA + INSTALACAO", "status_envio": "Pendente", "data_execucao": "2025-10-09T00:00:00", "nome_prestador": "Potencia Ferragista E Ar Condicionado Ltda", "valor_custo_prestador": 550}
135	40	64938	{"o_s": "64938", "e_mail": null, "cliente": "Cirilo Marques Neto", "periodo": "05/10/2025 – 22/10/2025", "localidade": "GOIANIA", "modalidade": "INSTALAÇÃO DE AR CONDICIONADO 9 A 12 MIL BTUS (SEM RAPEL)", "valor_extra": 0, "valor_total": 550, "motivo_extra": null, "status_envio": "Pendente", "data_execucao": "2025-10-13T00:00:00", "nome_prestador": "Potencia Ferragista E Ar Condicionado Ltda", "valor_custo_prestador": 550}
136	40	65073	{"o_s": "65073", "e_mail": null, "cliente": "Andreia Aparecida Santos Schimidt", "periodo": "05/10/2025 – 22/10/2025", "localidade": "APARECIDA DE GOIANIA", "modalidade": "INSTALAÇÃO DE AR CONDICIONADO 9 A 12 MIL BTUS (SEM RAPEL)", "valor_extra": 0, "valor_total": 550, "motivo_extra": null, "status_envio": "Pendente", "data_execucao": "2025-10-13T00:00:00", "nome_prestador": "Potencia Ferragista E Ar Condicionado Ltda", "valor_custo_prestador": 550}
137	40	65306	{"o_s": "65306", "e_mail": null, "cliente": "Joaci Souza De Sa", "periodo": "05/10/2025 – 22/10/2025", "localidade": "GOIANIA", "modalidade": "INSTALAÇÃO DE AR CONDICIONADO 9 A 12 MIL BTUS (SEM RAPEL)", "valor_extra": 0, "valor_total": 550, "motivo_extra": null, "status_envio": "Pendente", "data_execucao": "2025-10-11T00:00:00", "nome_prestador": "Potencia Ferragista E Ar Condicionado Ltda", "valor_custo_prestador": 550}
138	40	65309	{"o_s": "65309", "e_mail": null, "cliente": "Joaci Souza De Sa", "periodo": "05/10/2025 – 22/10/2025", "localidade": "GOIANIA", "modalidade": "INSTALAÇÃO DE AR CONDICIONADO 9 A 12 MIL BTUS (SEM RAPEL)", "valor_extra": 0, "valor_total": 550, "motivo_extra": null, "status_envio": "Pendente", "data_execucao": "2025-10-11T00:00:00", "nome_prestador": "Potencia Ferragista E Ar Condicionado Ltda", "valor_custo_prestador": 550}
139	40	65360	{"o_s": "65360", "e_mail": null, "cliente": "Itamar Rodrigues Quintanilha", "periodo": "05/10/2025 – 22/10/2025", "localidade": "TRINDADE", "modalidade": "INSTALAÇÃO DE AR CONDICIONADO 9 A 12 MIL BTUS (SEM RAPEL)", "valor_extra": 100, "valor_total": 650, "motivo_extra": "Adição de Valor Extra - Valor: R$100,00 - Motivo - DESLOCAMENTO", "status_envio": "Pendente", "data_execucao": "2025-10-14T00:00:00", "nome_prestador": "Potencia Ferragista E Ar Condicionado Ltda", "valor_custo_prestador": 550}
140	40	65403	{"o_s": "65403", "e_mail": null, "cliente": "Maria Lucia De Araujo", "periodo": "05/10/2025 – 22/10/2025", "localidade": "TRINDADE", "modalidade": "INSTALAÇÃO DE AR CONDICIONADO 9 A 12 MIL BTUS (SEM RAPEL)", "valor_extra": 100, "valor_total": 650, "motivo_extra": "Adição de Valor Extra - Valor: R$100,00 - Motivo - DESLOCAMENTO", "status_envio": "Pendente", "data_execucao": "2025-10-14T00:00:00", "nome_prestador": "Potencia Ferragista E Ar Condicionado Ltda", "valor_custo_prestador": 550}
141	40	65788	{"o_s": "65788", "e_mail": null, "cliente": "Jackellyne Sampaio Gomide Cruz", "periodo": "05/10/2025 – 22/10/2025", "localidade": "TRINDADE", "modalidade": "INSTALAÇÃO DE AR CONDICIONADO 9 A 12 MIL BTUS (SEM RAPEL)", "valor_extra": 100, "valor_total": 650, "motivo_extra": "Adição de Valor Extra - Valor: R$100,00 - Motivo - DESLOCAMENTO", "status_envio": "Pendente", "data_execucao": "2025-10-14T00:00:00", "nome_prestador": "Potencia Ferragista E Ar Condicionado Ltda", "valor_custo_prestador": 550}
142	40	65983	{"o_s": "65983", "e_mail": null, "cliente": "Uriane Oliveira Da Rocha", "periodo": "05/10/2025 – 22/10/2025", "localidade": "GOIANIA", "modalidade": "INSTALAÇÃO DE AR CONDICIONADO 9 A 12 MIL BTUS (SEM RAPEL)", "valor_extra": 700, "valor_total": 1250, "motivo_extra": "Adição de Valor Extra - Valor: R$700,00 - Motivo - CUSTO EXTRA GAS + INSTLA + DESIS", "status_envio": "Pendente", "data_execucao": "2025-10-15T00:00:00", "nome_prestador": "Potencia Ferragista E Ar Condicionado Ltda", "valor_custo_prestador": 550}
143	41	63414	{"o_s": "63414", "e_mail": null, "cliente": "Nalu Medeiros Repila", "periodo": "05/10/2025 – 22/10/2025", "localidade": "BELEM", "modalidade": "INSTALAÇÃO DE AR CONDICIONADO 9 A 12 MIL BTUS (SEM RAPEL)", "valor_extra": 0, "valor_total": 600, "motivo_extra": null, "status_envio": "Pendente", "data_execucao": "2025-10-06T00:00:00", "nome_prestador": "20.224.238 Maigregom Santos Ribeiro", "valor_custo_prestador": 600}
144	42	62703	{"o_s": "62703", "e_mail": null, "cliente": "Ivaneth Cardoso Batista", "periodo": "05/10/2025 – 22/10/2025", "localidade": "PALMAS", "modalidade": "INSTALAÇÃO DE AR CONDICIONADO 9 A 12 MIL BTUS (SEM RAPEL)", "valor_extra": 0, "valor_total": 550, "motivo_extra": null, "status_envio": "Pendente", "data_execucao": "2025-10-13T00:00:00", "nome_prestador": "50.831.850 Eliardo Pereira De Souza", "valor_custo_prestador": 550}
145	42	63068	{"o_s": "63068", "e_mail": null, "cliente": "Jose Batista Nunes", "periodo": "05/10/2025 – 22/10/2025", "localidade": "PALMAS", "modalidade": "INSTALAÇÃO DE AR CONDICIONADO 9 A 12 MIL BTUS (SEM RAPEL)", "valor_extra": 0, "valor_total": 550, "motivo_extra": null, "status_envio": "Pendente", "data_execucao": "2025-10-13T00:00:00", "nome_prestador": "50.831.850 Eliardo Pereira De Souza", "valor_custo_prestador": 550}
146	42	63262	{"o_s": "63262", "e_mail": null, "cliente": "Maria Dares Dos Santos", "periodo": "05/10/2025 – 22/10/2025", "localidade": "PALMAS", "modalidade": "INSTALAÇÃO DE AR CONDICIONADO 9 A 12 MIL BTUS (SEM RAPEL)", "valor_extra": 0, "valor_total": 550, "motivo_extra": null, "status_envio": "Pendente", "data_execucao": "2025-10-13T00:00:00", "nome_prestador": "50.831.850 Eliardo Pereira De Souza", "valor_custo_prestador": 550}
147	42	63277	{"o_s": "63277", "e_mail": null, "cliente": "Raydleno Mateus Tavares", "periodo": "05/10/2025 – 22/10/2025", "localidade": "PALMAS", "modalidade": "INSTALAÇÃO DE AR CONDICIONADO 9 A 12 MIL BTUS (SEM RAPEL)", "valor_extra": 0, "valor_total": 550, "motivo_extra": null, "status_envio": "Pendente", "data_execucao": "2025-10-09T00:00:00", "nome_prestador": "50.831.850 Eliardo Pereira De Souza", "valor_custo_prestador": 550}
148	42	63921	{"o_s": "63921", "e_mail": null, "cliente": "Claudia Cristina Soares Dos Santos", "periodo": "05/10/2025 – 22/10/2025", "localidade": "PALMAS", "modalidade": "INSTALAÇÃO DE AR CONDICIONADO 9 A 12 MIL BTUS (SEM RAPEL)", "valor_extra": 0, "valor_total": 550, "motivo_extra": null, "status_envio": "Pendente", "data_execucao": "2025-10-09T00:00:00", "nome_prestador": "50.831.850 Eliardo Pereira De Souza", "valor_custo_prestador": 550}
149	43	63762	{"o_s": "63762", "e_mail": null, "cliente": "Marcia Helena Franco De Morais", "periodo": "05/10/2025 – 22/10/2025", "localidade": "JATAI", "modalidade": "INSTALAÇÃO DE AR CONDICIONADO 9 A 12 MIL BTUS (SEM RAPEL)", "valor_extra": 0, "valor_total": 550, "motivo_extra": null, "status_envio": "Pendente", "data_execucao": "2025-10-06T00:00:00", "nome_prestador": "Mardem Emidio Vieira Reis", "valor_custo_prestador": 550}
150	44	64320	{"o_s": "64320", "e_mail": null, "cliente": "Luciana Soares De Carvalho", "periodo": "05/10/2025 – 22/10/2025", "localidade": "RUBIATABA", "modalidade": "INSTALAÇÃO DE AR CONDICIONADO 9 A 12 MIL BTUS (SEM RAPEL)", "valor_extra": 60, "valor_total": 560, "motivo_extra": "Adição de Valor Extra - Valor: R$60,00 - Motivo - ADICIONAL NF", "status_envio": "Pendente", "data_execucao": "2025-10-10T00:00:00", "nome_prestador": "Lucelino Alves Ribeiro", "valor_custo_prestador": 500}
151	44	64355	{"o_s": "64355", "e_mail": null, "cliente": "Nilson Antonio De Almeida", "periodo": "05/10/2025 – 22/10/2025", "localidade": "RUBIATABA", "modalidade": "INSTALAÇÃO DE AR CONDICIONADO 9 A 12 MIL BTUS (SEM RAPEL)", "valor_extra": 60, "valor_total": 560, "motivo_extra": "Adição de Valor Extra - Valor: R$60,00 - Motivo - ADICIONAL NF", "status_envio": "Pendente", "data_execucao": "2025-10-09T00:00:00", "nome_prestador": "Lucelino Alves Ribeiro", "valor_custo_prestador": 500}
153	46	72323	{"o_s": "72323", "cliente": "david", "periodo": "01/01/2025", "localidade": "goiania", "modalidade": "ac", "valor_extra": 0.0, "valor_total": 100.0, "motivo_extra": "", "status_envio": "Pendente", "data_execucao": "2025-10-15", "nome_prestador": "david", "valor_custo_prestador": 100.0}
157	50	64104	{"o_s": "64104", "e_mail": null, "cliente": "Patricia Moroe Pinto", "periodo": "05/10/2025 – 22/10/2025", "localidade": "SAO LUIS", "modalidade": "INSTALAÇÃO DE AR CONDICIONADO 9 A 12 MIL BTUS (SEM RAPEL)", "valor_extra": 0, "valor_total": 550, "motivo_extra": null, "status_envio": "Pendente", "data_execucao": "2025-10-14T00:00:00", "nome_prestador": "M&T Engenharia Com. E Servicos Ltda", "valor_custo_prestador": 550}
158	51	8762121	{"o_s": "8762121", "cliente": "david", "periodo": "01/02/2026", "localidade": "goiania", "modalidade": "ac", "valor_extra": 0.0, "valor_total": 115.0, "motivo_extra": "", "status_envio": "Pendente", "data_execucao": "2025-10-15", "nome_prestador": "david", "valor_custo_prestador": 115.0}
160	53	523412	{"o_s": "523412", "cliente": "david dias", "periodo": "01/01/2026", "localidade": "goiania", "modalidade": "ac", "valor_extra": 0.0, "valor_total": 100.0, "motivo_extra": "", "status_envio": "Pendente", "data_execucao": "2025-10-15", "nome_prestador": "david", "valor_custo_prestador": 100.0}
\.


--
-- TOC entry 3933 (class 0 OID 16417)
-- Dependencies: 215
-- Data for Name: prestadores; Type: TABLE DATA; Schema: public; Owner: davidgabriel
--

COPY public.prestadores (id, nome, email, fornecedor_id, regra_envio, dias_envio, emails_adicionais) FROM stdin;
1	david	tiodavidg3@gmail.com	121212	Nenhuma		\N
2	52.417.932 Leogilson Dos Santos Silva	leoargoias2023@gmail.com	130972	Semanal	Segunda-feira	\N
3	50.831.850 Eliardo Pereira De Souza	eliardofera98@gmail.com	135320	Semanal	Segunda-feira	\N
4	57.527.016 Carlos Moreira Da Rocha Junior	carlosmoreiradarochajunior@gmail.com	136075	Semanal	Sexta-feira	\N
5	62.829.506 Francisco Nelson Florenco Maia	ageclimadf@gmail.com	136076	Semanal	Sexta-feira	\N
6	thiago	tthiago.dds@gmail.com	10	Semanal	Segunda-feira	\N
7	62.875.115 Marcia Fernanda Anes De Morais Bezerra	adrianoanes22@gmail.com	136215	Semanal	Segunda-feira	\N
8	Lucelino Alves Ribeiro	celinosat@gmail.com	137295	Semanal	Sexta-feira	\N
9	Mardem Emidio Vieira Reis	refrigeljti@gmail.com	48840	Semanal	Sexta-feira	\N
10	Potencia Ferragista E Ar Condicionado Ltda	andrevieiraciriaco@gmail.com	136137	Semanal	Sexta-feira	\N
11	20.224.238 Maigregom Santos Ribeiro	ocyanjr@hotmail.com	135088	Semanal	Segunda-feira	\N
12	M&T Engenharia Com. E Servicos Ltda	mtengenhariama@gmail.com	138267	Semanal	Segunda-feira	\N
\.


--
-- TOC entry 3954 (class 0 OID 16588)
-- Dependencies: 236
-- Data for Name: trello_cards; Type: TABLE DATA; Schema: public; Owner: davidgabriel
--

COPY public.trello_cards (id, lote_id, card_id, card_url, data_criacao) FROM stdin;
1	999999	68ef12f5bde1e98cc8fc4671	https://trello.com/c/MhuUnPHB	2025-10-15 00:20:23.421494
2	25	68ef1558d48a550beef376fb	https://trello.com/c/baKVIBSS	2025-10-15 00:30:34.646576
3	27	68ef1772054cea2e348d0db3	https://trello.com/c/41Y9Gs2q	2025-10-15 00:39:32.341091
4	26	68ef1952900e640e7a63f571	https://trello.com/c/gL99HrOM	2025-10-15 00:47:32.392281
5	28	68ef1b32cc64d3d5bc5267e9	https://trello.com/c/QhaObEh2	2025-10-15 00:55:32.030274
6	29	68ef1fa6ed43b4b40b775b30	https://trello.com/c/Bio3oxiJ	2025-10-15 01:14:31.957756
7	30	68ef210e1ac0961f185e3694	https://trello.com/c/X6CJZ918	2025-10-15 01:20:32.091089
8	31	68ef22762f1cf4a95ae9f095	https://trello.com/c/K2um92Ri	2025-10-15 01:26:32.02872
9	32	68ef23844f856b76802396a1	https://trello.com/c/ucPoDUp9	2025-10-15 01:31:02.825386
10	34	68efa86d2014fc2e8f847b28	https://trello.com/c/eVGogLUv	2025-10-15 10:58:09.675122
11	35	68efaa156e7c98c68b0563dd	https://trello.com/c/sTyHx7JC	2025-10-15 11:05:12.195168
12	36	68efac28b52816db02ca857a	https://trello.com/c/pEmr9ViU	2025-10-15 11:14:03.53482
13	37	68efad55d0e42789d8388ccc	https://trello.com/c/WWRoHHyh	2025-10-15 11:19:04.274695
15	40	68efc5081a87cba67f6e25c5	https://trello.com/c/gyjNKjVX	2025-10-15 13:00:10.684807
16	46	68efcd74de4b2e6fb27756c1	https://trello.com/c/QJgW803b	2025-10-15 13:36:07.459076
17	47	68efebcee2bcadb7860b99d1	https://trello.com/c/B67RQb7l	2025-10-15 15:45:37.435867
18	48	68efef8852e72dfee74b33e2	https://trello.com/c/hXOTanKd	2025-10-15 16:01:31.535349
19	33	68eff835ae2eb52b440d4408	https://trello.com/c/Kb1tlMnX	2025-10-15 16:38:32.03578
20	6	68effa972156c549c030c656	https://trello.com/c/S6z7PAMH	2025-10-15 16:48:41.867558
22	7	68effe1ce7b70ca9cedb9c67	https://trello.com/c/XuUiOMHV	2025-10-15 17:03:43.061907
23	8	68f002cae1a01c9427d25b53	https://trello.com/c/omyhST46	2025-10-15 17:23:40.62781
24	9	68f00de5898205866bdd36f9	https://trello.com/c/hyCw01YT	2025-10-15 18:11:05.105901
25	10	68f00e5cb3b0e157633d6f00	https://trello.com/c/WjrMHWfO	2025-10-15 18:13:02.748652
26	41	68f0137a0e2867c270090e79	https://trello.com/c/n7wHK5l3	2025-10-15 18:34:53.726896
27	53	68f026386cd588f258e30e6a	https://trello.com/c/rjgoaC9m	2025-10-15 19:54:50.931138
28	11	68f026fa48fcc4742c11d9d3	https://trello.com/c/OHKlbg9S	2025-10-15 19:58:05.285821
\.


--
-- TOC entry 3978 (class 0 OID 0)
-- Dependencies: 226
-- Name: boletins_blacklist_id_seq; Type: SEQUENCE SET; Schema: public; Owner: davidgabriel
--

SELECT pg_catalog.setval('public.boletins_blacklist_id_seq', 1, false);


--
-- TOC entry 3979 (class 0 OID 0)
-- Dependencies: 224
-- Name: envios_ignorados_id_seq; Type: SEQUENCE SET; Schema: public; Owner: davidgabriel
--

SELECT pg_catalog.setval('public.envios_ignorados_id_seq', 1, false);


--
-- TOC entry 3980 (class 0 OID 0)
-- Dependencies: 222
-- Name: envios_montagem_id_seq; Type: SEQUENCE SET; Schema: public; Owner: davidgabriel
--

SELECT pg_catalog.setval('public.envios_montagem_id_seq', 12, true);


--
-- TOC entry 3981 (class 0 OID 0)
-- Dependencies: 232
-- Name: jobs_config_id_seq; Type: SEQUENCE SET; Schema: public; Owner: davidgabriel
--

SELECT pg_catalog.setval('public.jobs_config_id_seq', 3, true);


--
-- TOC entry 3982 (class 0 OID 0)
-- Dependencies: 218
-- Name: lotes_servico_id_seq; Type: SEQUENCE SET; Schema: public; Owner: davidgabriel
--

SELECT pg_catalog.setval('public.lotes_servico_id_seq', 53, true);


--
-- TOC entry 3983 (class 0 OID 0)
-- Dependencies: 216
-- Name: montadores_id_seq; Type: SEQUENCE SET; Schema: public; Owner: davidgabriel
--

SELECT pg_catalog.setval('public.montadores_id_seq', 3, true);


--
-- TOC entry 3984 (class 0 OID 0)
-- Dependencies: 230
-- Name: notificacoes_id_seq; Type: SEQUENCE SET; Schema: public; Owner: davidgabriel
--

SELECT pg_catalog.setval('public.notificacoes_id_seq', 876, true);


--
-- TOC entry 3985 (class 0 OID 0)
-- Dependencies: 228
-- Name: os_blacklist_id_seq; Type: SEQUENCE SET; Schema: public; Owner: davidgabriel
--

SELECT pg_catalog.setval('public.os_blacklist_id_seq', 138, true);


--
-- TOC entry 3986 (class 0 OID 0)
-- Dependencies: 220
-- Name: os_enviadas_id_seq; Type: SEQUENCE SET; Schema: public; Owner: davidgabriel
--

SELECT pg_catalog.setval('public.os_enviadas_id_seq', 160, true);


--
-- TOC entry 3987 (class 0 OID 0)
-- Dependencies: 214
-- Name: prestadores_id_seq; Type: SEQUENCE SET; Schema: public; Owner: davidgabriel
--

SELECT pg_catalog.setval('public.prestadores_id_seq', 12, true);


--
-- TOC entry 3988 (class 0 OID 0)
-- Dependencies: 235
-- Name: trello_cards_id_seq; Type: SEQUENCE SET; Schema: public; Owner: davidgabriel
--

SELECT pg_catalog.setval('public.trello_cards_id_seq', 28, true);


--
-- TOC entry 3763 (class 2606 OID 16509)
-- Name: boletins_blacklist boletins_blacklist_pkey; Type: CONSTRAINT; Schema: public; Owner: davidgabriel
--

ALTER TABLE ONLY public.boletins_blacklist
    ADD CONSTRAINT boletins_blacklist_pkey PRIMARY KEY (id);


--
-- TOC entry 3760 (class 2606 OID 16498)
-- Name: envios_ignorados envios_ignorados_pkey; Type: CONSTRAINT; Schema: public; Owner: davidgabriel
--

ALTER TABLE ONLY public.envios_ignorados
    ADD CONSTRAINT envios_ignorados_pkey PRIMARY KEY (id);


--
-- TOC entry 3755 (class 2606 OID 16483)
-- Name: envios_montagem envios_montagem_pkey; Type: CONSTRAINT; Schema: public; Owner: davidgabriel
--

ALTER TABLE ONLY public.envios_montagem
    ADD CONSTRAINT envios_montagem_pkey PRIMARY KEY (id);


--
-- TOC entry 3778 (class 2606 OID 16586)
-- Name: integracoes_config integracoes_config_pkey; Type: CONSTRAINT; Schema: public; Owner: davidgabriel
--

ALTER TABLE ONLY public.integracoes_config
    ADD CONSTRAINT integracoes_config_pkey PRIMARY KEY (id);


--
-- TOC entry 3774 (class 2606 OID 16575)
-- Name: jobs_config jobs_config_nome_key; Type: CONSTRAINT; Schema: public; Owner: davidgabriel
--

ALTER TABLE ONLY public.jobs_config
    ADD CONSTRAINT jobs_config_nome_key UNIQUE (nome);


--
-- TOC entry 3776 (class 2606 OID 16573)
-- Name: jobs_config jobs_config_pkey; Type: CONSTRAINT; Schema: public; Owner: davidgabriel
--

ALTER TABLE ONLY public.jobs_config
    ADD CONSTRAINT jobs_config_pkey PRIMARY KEY (id);


--
-- TOC entry 3747 (class 2606 OID 16452)
-- Name: lotes_servico lotes_servico_pkey; Type: CONSTRAINT; Schema: public; Owner: davidgabriel
--

ALTER TABLE ONLY public.lotes_servico
    ADD CONSTRAINT lotes_servico_pkey PRIMARY KEY (id);


--
-- TOC entry 3749 (class 2606 OID 16533)
-- Name: lotes_servico lotes_servico_upload_token_key; Type: CONSTRAINT; Schema: public; Owner: davidgabriel
--

ALTER TABLE ONLY public.lotes_servico
    ADD CONSTRAINT lotes_servico_upload_token_key UNIQUE (upload_token);


--
-- TOC entry 3741 (class 2606 OID 16442)
-- Name: montadores montadores_fornecedor_id_key; Type: CONSTRAINT; Schema: public; Owner: davidgabriel
--

ALTER TABLE ONLY public.montadores
    ADD CONSTRAINT montadores_fornecedor_id_key UNIQUE (fornecedor_id);


--
-- TOC entry 3743 (class 2606 OID 16440)
-- Name: montadores montadores_identificador_key; Type: CONSTRAINT; Schema: public; Owner: davidgabriel
--

ALTER TABLE ONLY public.montadores
    ADD CONSTRAINT montadores_identificador_key UNIQUE (identificador);


--
-- TOC entry 3745 (class 2606 OID 16438)
-- Name: montadores montadores_pkey; Type: CONSTRAINT; Schema: public; Owner: davidgabriel
--

ALTER TABLE ONLY public.montadores
    ADD CONSTRAINT montadores_pkey PRIMARY KEY (id);


--
-- TOC entry 3772 (class 2606 OID 16549)
-- Name: notificacoes notificacoes_pkey; Type: CONSTRAINT; Schema: public; Owner: davidgabriel
--

ALTER TABLE ONLY public.notificacoes
    ADD CONSTRAINT notificacoes_pkey PRIMARY KEY (id);


--
-- TOC entry 3767 (class 2606 OID 16525)
-- Name: os_blacklist os_blacklist_pkey; Type: CONSTRAINT; Schema: public; Owner: davidgabriel
--

ALTER TABLE ONLY public.os_blacklist
    ADD CONSTRAINT os_blacklist_pkey PRIMARY KEY (id);


--
-- TOC entry 3751 (class 2606 OID 16468)
-- Name: os_enviadas os_enviadas_os_numero_key; Type: CONSTRAINT; Schema: public; Owner: davidgabriel
--

ALTER TABLE ONLY public.os_enviadas
    ADD CONSTRAINT os_enviadas_os_numero_key UNIQUE (os_numero);


--
-- TOC entry 3753 (class 2606 OID 16466)
-- Name: os_enviadas os_enviadas_pkey; Type: CONSTRAINT; Schema: public; Owner: davidgabriel
--

ALTER TABLE ONLY public.os_enviadas
    ADD CONSTRAINT os_enviadas_pkey PRIMARY KEY (id);


--
-- TOC entry 3735 (class 2606 OID 16428)
-- Name: prestadores prestadores_fornecedor_id_key; Type: CONSTRAINT; Schema: public; Owner: davidgabriel
--

ALTER TABLE ONLY public.prestadores
    ADD CONSTRAINT prestadores_fornecedor_id_key UNIQUE (fornecedor_id);


--
-- TOC entry 3737 (class 2606 OID 16426)
-- Name: prestadores prestadores_nome_key; Type: CONSTRAINT; Schema: public; Owner: davidgabriel
--

ALTER TABLE ONLY public.prestadores
    ADD CONSTRAINT prestadores_nome_key UNIQUE (nome);


--
-- TOC entry 3739 (class 2606 OID 16424)
-- Name: prestadores prestadores_pkey; Type: CONSTRAINT; Schema: public; Owner: davidgabriel
--

ALTER TABLE ONLY public.prestadores
    ADD CONSTRAINT prestadores_pkey PRIMARY KEY (id);


--
-- TOC entry 3781 (class 2606 OID 16596)
-- Name: trello_cards trello_cards_pkey; Type: CONSTRAINT; Schema: public; Owner: davidgabriel
--

ALTER TABLE ONLY public.trello_cards
    ADD CONSTRAINT trello_cards_pkey PRIMARY KEY (id);


--
-- TOC entry 3783 (class 2606 OID 16598)
-- Name: trello_cards unique_lote_card; Type: CONSTRAINT; Schema: public; Owner: davidgabriel
--

ALTER TABLE ONLY public.trello_cards
    ADD CONSTRAINT unique_lote_card UNIQUE (lote_id);


--
-- TOC entry 3756 (class 1259 OID 16606)
-- Name: idx_envios_montagem_status_api; Type: INDEX; Schema: public; Owner: davidgabriel
--

CREATE INDEX idx_envios_montagem_status_api ON public.envios_montagem USING btree (status_api);


--
-- TOC entry 3757 (class 1259 OID 16605)
-- Name: idx_envios_montagem_upload_hash; Type: INDEX; Schema: public; Owner: davidgabriel
--

CREATE INDEX idx_envios_montagem_upload_hash ON public.envios_montagem USING btree (upload_hash);


--
-- TOC entry 3768 (class 1259 OID 16556)
-- Name: idx_notificacoes_data; Type: INDEX; Schema: public; Owner: davidgabriel
--

CREATE INDEX idx_notificacoes_data ON public.notificacoes USING btree (data_criacao DESC);


--
-- TOC entry 3769 (class 1259 OID 16555)
-- Name: idx_notificacoes_lida; Type: INDEX; Schema: public; Owner: davidgabriel
--

CREATE INDEX idx_notificacoes_lida ON public.notificacoes USING btree (lida);


--
-- TOC entry 3770 (class 1259 OID 16557)
-- Name: idx_notificacoes_lote; Type: INDEX; Schema: public; Owner: davidgabriel
--

CREATE INDEX idx_notificacoes_lote ON public.notificacoes USING btree (lote_id);


--
-- TOC entry 3779 (class 1259 OID 16599)
-- Name: idx_trello_cards_lote; Type: INDEX; Schema: public; Owner: davidgabriel
--

CREATE INDEX idx_trello_cards_lote ON public.trello_cards USING btree (lote_id);


--
-- TOC entry 3764 (class 1259 OID 16515)
-- Name: idx_unique_boletim_blacklist; Type: INDEX; Schema: public; Owner: davidgabriel
--

CREATE UNIQUE INDEX idx_unique_boletim_blacklist ON public.boletins_blacklist USING btree (montador_id, boletim);


--
-- TOC entry 3761 (class 1259 OID 16499)
-- Name: idx_unique_ignore; Type: INDEX; Schema: public; Owner: davidgabriel
--

CREATE UNIQUE INDEX idx_unique_ignore ON public.envios_ignorados USING btree (tipo, entidade_id, ano, periodo_chave);


--
-- TOC entry 3758 (class 1259 OID 16489)
-- Name: idx_unique_montagem; Type: INDEX; Schema: public; Owner: davidgabriel
--

CREATE UNIQUE INDEX idx_unique_montagem ON public.envios_montagem USING btree (((detalhes ->> 'periodo_relatorio'::text)), montador_id);


--
-- TOC entry 3765 (class 1259 OID 16531)
-- Name: idx_unique_os_blacklist; Type: INDEX; Schema: public; Owner: davidgabriel
--

CREATE UNIQUE INDEX idx_unique_os_blacklist ON public.os_blacklist USING btree (prestador_id, os_numero);


--
-- TOC entry 3787 (class 2606 OID 16510)
-- Name: boletins_blacklist boletins_blacklist_montador_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: davidgabriel
--

ALTER TABLE ONLY public.boletins_blacklist
    ADD CONSTRAINT boletins_blacklist_montador_id_fkey FOREIGN KEY (montador_id) REFERENCES public.montadores(id) ON DELETE CASCADE;


--
-- TOC entry 3786 (class 2606 OID 16484)
-- Name: envios_montagem envios_montagem_montador_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: davidgabriel
--

ALTER TABLE ONLY public.envios_montagem
    ADD CONSTRAINT envios_montagem_montador_id_fkey FOREIGN KEY (montador_id) REFERENCES public.montadores(id);


--
-- TOC entry 3784 (class 2606 OID 16453)
-- Name: lotes_servico lotes_servico_prestador_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: davidgabriel
--

ALTER TABLE ONLY public.lotes_servico
    ADD CONSTRAINT lotes_servico_prestador_id_fkey FOREIGN KEY (prestador_id) REFERENCES public.prestadores(id);


--
-- TOC entry 3789 (class 2606 OID 16550)
-- Name: notificacoes notificacoes_lote_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: davidgabriel
--

ALTER TABLE ONLY public.notificacoes
    ADD CONSTRAINT notificacoes_lote_id_fkey FOREIGN KEY (lote_id) REFERENCES public.lotes_servico(id);


--
-- TOC entry 3788 (class 2606 OID 16526)
-- Name: os_blacklist os_blacklist_prestador_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: davidgabriel
--

ALTER TABLE ONLY public.os_blacklist
    ADD CONSTRAINT os_blacklist_prestador_id_fkey FOREIGN KEY (prestador_id) REFERENCES public.prestadores(id) ON DELETE CASCADE;


--
-- TOC entry 3785 (class 2606 OID 16469)
-- Name: os_enviadas os_enviadas_lote_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: davidgabriel
--

ALTER TABLE ONLY public.os_enviadas
    ADD CONSTRAINT os_enviadas_lote_id_fkey FOREIGN KEY (lote_id) REFERENCES public.lotes_servico(id) ON DELETE CASCADE;


-- Completed on 2025-10-16 01:09:46 -03

--
-- PostgreSQL database dump complete
--

\unrestrict jyDJGisTo1AjQYfsoyIbueakhpi81cUdGaaCrgkvI2QBa5o1apRCfLy5KBSX0lZ

