--
-- PostgreSQL database dump
--

\restrict ZMXaTxRIaMMtMcMmDPJ7MXGKD3mI9zm8kj9DAqVzS60pBFMSgIEMRUZ2NmuYyNL

-- Dumped from database version 15.14 (Homebrew)
-- Dumped by pg_dump version 15.14 (Homebrew)

-- Started on 2025-10-14 23:54:28 -03

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
-- TOC entry 3956 (class 0 OID 0)
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
-- TOC entry 3957 (class 0 OID 0)
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
    anexo_path text
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
-- TOC entry 3958 (class 0 OID 0)
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
-- TOC entry 3959 (class 0 OID 0)
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
-- TOC entry 3960 (class 0 OID 0)
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
-- TOC entry 3961 (class 0 OID 0)
-- Dependencies: 219
-- Name: COLUMN lotes_servico.arquivos_nf; Type: COMMENT; Schema: public; Owner: davidgabriel
--

COMMENT ON COLUMN public.lotes_servico.arquivos_nf IS 'Dados dos arquivos recebidos (JSON)';


--
-- TOC entry 3962 (class 0 OID 0)
-- Dependencies: 219
-- Name: COLUMN lotes_servico.data_ultima_consulta; Type: COMMENT; Schema: public; Owner: davidgabriel
--

COMMENT ON COLUMN public.lotes_servico.data_ultima_consulta IS 'Data da última consulta à API';


--
-- TOC entry 3963 (class 0 OID 0)
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
-- TOC entry 3964 (class 0 OID 0)
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
-- TOC entry 3965 (class 0 OID 0)
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
-- TOC entry 3966 (class 0 OID 0)
-- Dependencies: 231
-- Name: TABLE notificacoes; Type: COMMENT; Schema: public; Owner: davidgabriel
--

COMMENT ON TABLE public.notificacoes IS 'Notificações do sistema';


--
-- TOC entry 3967 (class 0 OID 0)
-- Dependencies: 231
-- Name: COLUMN notificacoes.tipo; Type: COMMENT; Schema: public; Owner: davidgabriel
--

COMMENT ON COLUMN public.notificacoes.tipo IS 'Tipo: nf_recebida, nf_baixada, link_gerado, etc';


--
-- TOC entry 3968 (class 0 OID 0)
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
-- TOC entry 3969 (class 0 OID 0)
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
-- TOC entry 3970 (class 0 OID 0)
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
-- TOC entry 3971 (class 0 OID 0)
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
-- TOC entry 3972 (class 0 OID 0)
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
-- TOC entry 3973 (class 0 OID 0)
-- Dependencies: 235
-- Name: trello_cards_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: davidgabriel
--

ALTER SEQUENCE public.trello_cards_id_seq OWNED BY public.trello_cards.id;


--
-- TOC entry 3710 (class 2604 OID 16504)
-- Name: boletins_blacklist id; Type: DEFAULT; Schema: public; Owner: davidgabriel
--

ALTER TABLE ONLY public.boletins_blacklist ALTER COLUMN id SET DEFAULT nextval('public.boletins_blacklist_id_seq'::regclass);


--
-- TOC entry 3709 (class 2604 OID 16494)
-- Name: envios_ignorados id; Type: DEFAULT; Schema: public; Owner: davidgabriel
--

ALTER TABLE ONLY public.envios_ignorados ALTER COLUMN id SET DEFAULT nextval('public.envios_ignorados_id_seq'::regclass);


--
-- TOC entry 3707 (class 2604 OID 16478)
-- Name: envios_montagem id; Type: DEFAULT; Schema: public; Owner: davidgabriel
--

ALTER TABLE ONLY public.envios_montagem ALTER COLUMN id SET DEFAULT nextval('public.envios_montagem_id_seq'::regclass);


--
-- TOC entry 3719 (class 2604 OID 16563)
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
-- TOC entry 3714 (class 2604 OID 16541)
-- Name: notificacoes id; Type: DEFAULT; Schema: public; Owner: davidgabriel
--

ALTER TABLE ONLY public.notificacoes ALTER COLUMN id SET DEFAULT nextval('public.notificacoes_id_seq'::regclass);


--
-- TOC entry 3712 (class 2604 OID 16520)
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
-- TOC entry 3729 (class 2604 OID 16591)
-- Name: trello_cards id; Type: DEFAULT; Schema: public; Owner: davidgabriel
--

ALTER TABLE ONLY public.trello_cards ALTER COLUMN id SET DEFAULT nextval('public.trello_cards_id_seq'::regclass);


--
-- TOC entry 3941 (class 0 OID 16501)
-- Dependencies: 227
-- Data for Name: boletins_blacklist; Type: TABLE DATA; Schema: public; Owner: davidgabriel
--

COPY public.boletins_blacklist (id, montador_id, boletim, data_adicao, motivo) FROM stdin;
\.


--
-- TOC entry 3939 (class 0 OID 16491)
-- Dependencies: 225
-- Data for Name: envios_ignorados; Type: TABLE DATA; Schema: public; Owner: davidgabriel
--

COPY public.envios_ignorados (id, tipo, entidade_id, ano, periodo_chave, data_ignorada) FROM stdin;
\.


--
-- TOC entry 3937 (class 0 OID 16475)
-- Dependencies: 223
-- Data for Name: envios_montagem; Type: TABLE DATA; Schema: public; Owner: davidgabriel
--

COPY public.envios_montagem (id, montador_id, data_envio, status, detalhes, conversation_id, anexo_path) FROM stdin;
\.


--
-- TOC entry 3948 (class 0 OID 16576)
-- Dependencies: 234
-- Data for Name: integracoes_config; Type: TABLE DATA; Schema: public; Owner: davidgabriel
--

COPY public.integracoes_config (id, trello_api_key, trello_token, trello_board_id, trello_list_id, trello_ativo, data_atualizacao) FROM stdin;
1	9869e57754f5109c97773f9fca23ae4c	8140b5528fb96969db573adfc7674f75eb1b41ada7afee01e1987fb649031c21	https://trello.com/b/kcR2WofW/lancamento-nf	Pendente	t	2025-10-14 23:53:14.872323
\.


--
-- TOC entry 3947 (class 0 OID 16560)
-- Dependencies: 233
-- Data for Name: jobs_config; Type: TABLE DATA; Schema: public; Owner: davidgabriel
--

COPY public.jobs_config (id, nome, descricao, ativo, intervalo_minutos, ultima_execucao, proxima_execucao, total_execucoes, total_erros, ultima_mensagem, data_criacao, data_atualizacao) FROM stdin;
1	consultar_notas	Consulta e baixa arquivos de notas fiscais	t	5	2025-10-14 23:53:15.208866	2025-10-14 23:22:55.033859	122	0	Job executado com sucesso	2025-10-14 21:10:58.852294	2025-10-14 23:53:15.208866
3	backup_banco	Backup automático do banco de dados PostgreSQL	t	1440	\N	\N	0	0	\N	2025-10-14 23:54:20.515702	2025-10-14 23:54:20.515702
2	enviar_api	Envia lotes pendentes para a API	t	100	2025-10-14 23:02:52.193633	2025-10-15 00:57:55.039197	1	1	Processados: 11, Sucesso: 10, Erros: 1	2025-10-14 21:10:58.852294	2025-10-14 23:02:52.193633
\.


--
-- TOC entry 3933 (class 0 OID 16444)
-- Dependencies: 219
-- Data for Name: lotes_servico; Type: TABLE DATA; Schema: public; Owner: davidgabriel
--

COPY public.lotes_servico (id, prestador_id, prestador_nome, periodo, valor_total, data_envio, status, conversation_id, anexo_path, upload_token, upload_url, upload_status, nota_fiscal_path, id_controle, link_upload, validade_link, status_api, data_envio_api, api_message, upload_hash, arquivos_nf, data_ultima_consulta, status_arquivo) FROM stdin;
15	1	david	01/11/2025 - 02/11/2025	150	2025-10-13 20:29:24.517415	Em Aberto	AAQkADhmM2FmNmY0LTFiMjAtNGZmYi05ODQ5LTYyMGZhNTZiOTkyNQAQAPqD6pEOkntHvN4DxRkjoYM=	\N	\N	\N	pending	\N	13	https://api.link.dev.br/dvprocessamento/envio-nf/67bcacecaae861214627674ada9ae8e8	2025-11-13	0	2025-10-14 23:02:40.856403	Registro criado com sucesso	67bcacecaae861214627674ada9ae8e8	\N	\N	0
13	1	david	10/10/2025 - 11/10/2025	1200	2025-10-13 19:38:47.125389	Em Aberto	AAQkADhmM2FmNmY0LTFiMjAtNGZmYi05ODQ5LTYyMGZhNTZiOTkyNQAQAMYkqmhG4dZPrFjCSFOBflE=	\N	\N	\N	pending	\N	14	https://api.link.dev.br/dvprocessamento/envio-nf/3ccc68bbbc1a794bb0401f41fcf14f3b	2025-11-13	0	2025-10-14 23:02:42.326526	Registro criado com sucesso	3ccc68bbbc1a794bb0401f41fcf14f3b	\N	\N	0
12	1	david	sei la	100	2025-10-13 19:29:06.54103	Em Aberto	AAQkADhmM2FmNmY0LTFiMjAtNGZmYi05ODQ5LTYyMGZhNTZiOTkyNQAQAET5yL08eHZBmKAVMTjRQq0=	\N	\N	\N	pending	\N	15	https://api.link.dev.br/dvprocessamento/envio-nf/2ef59838fd858c04281e0e6b07a36510	2025-11-13	0	2025-10-14 23:02:43.627496	Registro criado com sucesso	2ef59838fd858c04281e0e6b07a36510	\N	\N	0
14	1	david	01/01/2025 - 02/01/2025	100	2025-10-13 20:02:02.672235	Em Aberto	AAQkADhmM2FmNmY0LTFiMjAtNGZmYi05ODQ5LTYyMGZhNTZiOTkyNQAQAJbIzLJdR2FHlWqls1uWzSU=	\N	\N	\N	pending	\N	3	https://api.link.com.br/dvprocessamento/envio-nf/fa611f6d1eaa2b3b9302e006edcd24d7	2025-11-12	0	2025-10-13 20:02:03.907641	Registro criado com sucesso	\N	\N	\N	0
11	1	david	teste David	1000	2025-10-13 17:32:15.941473	Em Aberto	AAQkADhmM2FmNmY0LTFiMjAtNGZmYi05ODQ5LTYyMGZhNTZiOTkyNQAQAHB_ZPIOYhdFoWP6JECZIQE=	\N	\N	\N	pending	\N	16	https://api.link.dev.br/dvprocessamento/envio-nf/8b51f9d0c8afb8f918347c5d9fa3503f	2025-11-13	0	2025-10-14 23:02:44.824139	Registro criado com sucesso	8b51f9d0c8afb8f918347c5d9fa3503f	\N	\N	0
10	6	thiago	23/08/2025 – 04/09/2025	600	2025-10-13 15:17:27.099287	Em Aberto	AAQkADhmM2FmNmY0LTFiMjAtNGZmYi05ODQ5LTYyMGZhNTZiOTkyNQAQANbYeUzLKTlCnfGRV--Ye-4=	\N	\N	\N	pending	\N	17	https://api.link.dev.br/dvprocessamento/envio-nf/d9d43a5b6b47e72892ece042151da40f	2025-11-13	0	2025-10-14 23:02:46.011102	Registro criado com sucesso	d9d43a5b6b47e72892ece042151da40f	\N	\N	0
16	1	david	01/05/2025 - 03/05/2025	100	2025-10-13 21:43:54.237483	Em Aberto	AAQkADhmM2FmNmY0LTFiMjAtNGZmYi05ODQ5LTYyMGZhNTZiOTkyNQAQACuVTE25kFFAu_FxuKR8ovU=	\N	\N	\N	pending	\N	5	https://api.link.com.br/dvprocessamento/envio-nf/ce96a5a8e204b3edba6f5756a2e7a915	2025-11-12	0	2025-10-13 21:43:57.279054	Registro criado com sucesso	\N	\N	\N	0
9	1	david	23/08/2025 – 04/09/2025	600	2025-10-13 15:17:24.497132	Em Aberto	AAQkADhmM2FmNmY0LTFiMjAtNGZmYi05ODQ5LTYyMGZhNTZiOTkyNQAQALOQCousTUhIigoMaJNIjHw=	\N	\N	\N	pending	\N	18	https://api.link.dev.br/dvprocessamento/envio-nf/4e9f783708d8614792da906940134cf0	2025-11-13	0	2025-10-14 23:02:47.338487	Registro criado com sucesso	4e9f783708d8614792da906940134cf0	\N	\N	0
17	1	david	01/01/2025 - 01/10/2025	100	2025-10-14 11:09:41.852883	Em Aberto	AAQkADhmM2FmNmY0LTFiMjAtNGZmYi05ODQ5LTYyMGZhNTZiOTkyNQAQAPPcb8kiVBpAj2b1BtXl3Fo=	\N	\N	\N	pending	\N	3	https://api.link.dev.br/dvprocessamento/envio-nf/d8f25dfcab5ca6991832d2a1dd858dfb	2025-11-13	0	2025-10-14 11:09:44.884913	Registro criado com sucesso	\N	\N	\N	0
18	1	david	10/10/2025	120	2025-10-14 13:06:56.60038	Em Aberto	AAQkADhmM2FmNmY0LTFiMjAtNGZmYi05ODQ5LTYyMGZhNTZiOTkyNQAQAOtb_G2a5W5Mm8jLp4fVlCQ=	\N	\N	\N	pending	\N	4	https://api.link.dev.br/dvprocessamento/envio-nf/88c558c57f82aae676be5afcb7d21a4f	2025-11-13	0	2025-10-14 13:06:58.913071	Registro criado com sucesso	\N	\N	\N	0
8	1	david	23/02/2025 – 04/03/2025	600	2025-10-13 15:17:21.579851	Em Aberto	AAQkADhmM2FmNmY0LTFiMjAtNGZmYi05ODQ5LTYyMGZhNTZiOTkyNQAQAECBQ_ZGHAhKpKFmGF5Tsh4=	\N	\N	\N	pending	\N	19	https://api.link.dev.br/dvprocessamento/envio-nf/a041c8301d7186f88c809ab6a504f8d0	2025-11-13	0	2025-10-14 23:02:48.552447	Registro criado com sucesso	a041c8301d7186f88c809ab6a504f8d0	\N	\N	0
7	1	david	01/01/2025 - 02/01/2025	100	2025-10-13 15:06:05.073441	Em Aberto	AAQkADhmM2FmNmY0LTFiMjAtNGZmYi05ODQ5LTYyMGZhNTZiOTkyNQAQAIgJNQgcAZREtEYnbU88cMw=	\N	\N	\N	pending	\N	20	https://api.link.dev.br/dvprocessamento/envio-nf/5beacc41380934a07a4038831cdf57ea	2025-11-13	0	2025-10-14 23:02:49.731857	Registro criado com sucesso	5beacc41380934a07a4038831cdf57ea	\N	\N	0
6	2	52.417.932 Leogilson Dos Santos Silva	05/10/2025 – 22/10/2025	8850	2025-10-13 13:15:36.679939	Em Aberto	AAQkADhmM2FmNmY0LTFiMjAtNGZmYi05ODQ5LTYyMGZhNTZiOTkyNQAQABjMv1pJzdtJku8W8EoiIg8=	\N	\N	\N	pending	\N	21	https://api.link.dev.br/dvprocessamento/envio-nf/22b406a239a4fdf9331dcd821c255bd0	2025-11-13	0	2025-10-14 23:02:50.95279	Registro criado com sucesso	22b406a239a4fdf9331dcd821c255bd0	\N	\N	0
4	1	david	teste	100	2025-10-13 12:50:37.145343	Em Aberto	\N	\N	\N	\N	pending	\N	22	https://api.link.dev.br/dvprocessamento/envio-nf/d2b4cb34ff85c6ed6e1b2c3b38263a68	2025-11-13	0	2025-10-14 23:02:52.180959	Registro criado com sucesso	d2b4cb34ff85c6ed6e1b2c3b38263a68	\N	\N	0
19	1	david	01/01/2025	100	2025-10-14 20:36:02.971502	Em Aberto	AAQkADhmM2FmNmY0LTFiMjAtNGZmYi05ODQ5LTYyMGZhNTZiOTkyNQAQAPWTf2pZqYdBq0Mk41mkG6M=	\N	\N	\N	pending	\N	7	https://api.link.dev.br/dvprocessamento/envio-nf/fe6bf11bea73b8936b83f293435a6c55	2025-11-13	0	2025-10-14 20:36:05.519364	Registro criado com sucesso	fe6bf11bea73b8936b83f293435a6c55	{"arquivos": [{"id": 12, "data_upload": "2025-10-14 20:36:37", "observacoes": "", "hash_arquivo": "fdc6da06fa3f863b68663230359de120", "nome_arquivo": "fe6bf11bea73b8936b83f293435a6c55.pdf", "tipo_arquivo": "application/pdf", "link_download": "https://api.link.dev.br/dvprocessamento/envio-nf/arquivosNF/fe6bf11bea73b8936b83f293435a6c55.pdf", "nome_original": "232323.pdf", "caminho_arquivo": "arquivosNF/fe6bf11bea73b8936b83f293435a6c55.pdf", "tamanho_arquivo": 301647, "tamanho_formatado": "294.58 KB", "status_processamento": 1}], "estatisticas": {"tipos_arquivo": {"application/pdf": 1}, "total_tamanho": 301647, "ultimo_upload": "2025-10-14 20:36:37", "total_arquivos": 1, "primeiro_upload": "2025-10-14 20:36:37", "total_tamanho_formatado": "294.58 KB"}, "data_consulta": "2025-10-14T23:53:04.153802"}	2025-10-14 23:53:04.153802	2
23	1	david	01/01/2025	120	2025-10-14 21:07:20.293614	Em Aberto	AAQkADhmM2FmNmY0LTFiMjAtNGZmYi05ODQ5LTYyMGZhNTZiOTkyNQAQAHdP7Ldsrf9El326jNt9vHU=	\N	\N	\N	pending	\N	11	https://api.link.dev.br/dvprocessamento/envio-nf/f5b5a723645837e04231238bfff38b8f	2025-11-13	0	2025-10-14 21:07:22.24112	Registro criado com sucesso	f5b5a723645837e04231238bfff38b8f	{"arquivos": [{"id": 16, "data_upload": "2025-10-14 21:07:44", "observacoes": "", "hash_arquivo": "ef6c5749cddf9595bac1ab6f941a6376", "nome_arquivo": "f5b5a723645837e04231238bfff38b8f.pdf", "tipo_arquivo": "application/pdf", "link_download": "https://api.link.dev.br/dvprocessamento/envio-nf/arquivosNF/f5b5a723645837e04231238bfff38b8f.pdf", "nome_original": "NOVO MUNDO DAVID GABRIEL NF 645.pdf", "caminho_arquivo": "arquivosNF/f5b5a723645837e04231238bfff38b8f.pdf", "tamanho_arquivo": 459446, "tamanho_formatado": "448.68 KB", "status_processamento": 1}], "estatisticas": {"tipos_arquivo": {"application/pdf": 1}, "total_tamanho": 459446, "ultimo_upload": "2025-10-14 21:07:44", "total_arquivos": 1, "primeiro_upload": "2025-10-14 21:07:44", "total_tamanho_formatado": "448.68 KB"}, "data_consulta": "2025-10-14T23:52:57.627158"}	2025-10-14 23:52:57.627158	2
22	1	david	01/01/2026	120	2025-10-14 20:56:11.805972	Em Aberto	AAQkADhmM2FmNmY0LTFiMjAtNGZmYi05ODQ5LTYyMGZhNTZiOTkyNQAQAM4Yl8HYRulGqCxsIBmkOg8=	\N	\N	\N	pending	\N	\N	https://api.link.dev.br/dvprocessamento/envio-nf/74b1ab63d2f02d33f992175844605233	2025-11-13	0	2025-10-14 20:56:13.015439	Registro criado com sucesso	74b1ab63d2f02d33f992175844605233	{"arquivos": [{"id": 15, "data_upload": "2025-10-14 20:56:38", "observacoes": "", "hash_arquivo": "39f72a29c74cbc22c570759b61633dee", "nome_arquivo": "74b1ab63d2f02d33f992175844605233.pdf", "tipo_arquivo": "application/pdf", "link_download": "https://api.link.dev.br/dvprocessamento/envio-nf/arquivosNF/74b1ab63d2f02d33f992175844605233.pdf", "nome_original": "Nf 12.pdf", "caminho_arquivo": "arquivosNF/74b1ab63d2f02d33f992175844605233.pdf", "tamanho_arquivo": 98257, "tamanho_formatado": "95.95 KB", "status_processamento": 1}], "estatisticas": {"tipos_arquivo": {"application/pdf": 1}, "total_tamanho": 98257, "ultimo_upload": "2025-10-14 20:56:38", "total_arquivos": 1, "primeiro_upload": "2025-10-14 20:56:38", "total_tamanho_formatado": "95.95 KB"}, "data_consulta": "2025-10-14T23:52:59.288943"}	2025-10-14 23:52:59.288943	2
21	1	david	01/01/2025	100	2025-10-14 20:50:11.505667	Em Aberto	AAQkADhmM2FmNmY0LTFiMjAtNGZmYi05ODQ5LTYyMGZhNTZiOTkyNQAQAACIG8TIGsxMj7Kb_i4bjRo=	\N	\N	\N	pending	\N	9	https://api.link.dev.br/dvprocessamento/envio-nf/68cacb30a7ae736d4b63559b4302199f	2025-11-13	0	2025-10-14 20:50:23.220606	Registro criado com sucesso	68cacb30a7ae736d4b63559b4302199f	{"arquivos": [{"id": 14, "data_upload": "2025-10-14 20:50:58", "observacoes": "", "hash_arquivo": "fdc6da06fa3f863b68663230359de120", "nome_arquivo": "68cacb30a7ae736d4b63559b4302199f.pdf", "tipo_arquivo": "application/pdf", "link_download": "https://api.link.dev.br/dvprocessamento/envio-nf/arquivosNF/68cacb30a7ae736d4b63559b4302199f.pdf", "nome_original": "232323.pdf", "caminho_arquivo": "arquivosNF/68cacb30a7ae736d4b63559b4302199f.pdf", "tamanho_arquivo": 301647, "tamanho_formatado": "294.58 KB", "status_processamento": 1}], "estatisticas": {"tipos_arquivo": {"application/pdf": 1}, "total_tamanho": 301647, "ultimo_upload": "2025-10-14 20:50:58", "total_arquivos": 1, "primeiro_upload": "2025-10-14 20:50:58", "total_tamanho_formatado": "294.58 KB"}, "data_consulta": "2025-10-14T23:53:00.910250"}	2025-10-14 23:53:00.91025	2
20	1	david	01/09/2025	250	2025-10-14 20:40:53.120867	Em Aberto	AAQkADhmM2FmNmY0LTFiMjAtNGZmYi05ODQ5LTYyMGZhNTZiOTkyNQAQAPWTf2pZqYdBq0Mk41mkG6M=	\N	\N	\N	pending	\N	8	https://api.link.dev.br/dvprocessamento/envio-nf/4c16655f79a49f01877c0bb9787ab168	2025-11-13	0	2025-10-14 20:40:54.590194	Registro criado com sucesso	4c16655f79a49f01877c0bb9787ab168	{"arquivos": [{"id": 13, "data_upload": "2025-10-14 20:41:40", "observacoes": "", "hash_arquivo": "fdc6da06fa3f863b68663230359de120", "nome_arquivo": "4c16655f79a49f01877c0bb9787ab168.pdf", "tipo_arquivo": "application/pdf", "link_download": "https://api.link.dev.br/dvprocessamento/envio-nf/arquivosNF/4c16655f79a49f01877c0bb9787ab168.pdf", "nome_original": "232323.pdf", "caminho_arquivo": "arquivosNF/4c16655f79a49f01877c0bb9787ab168.pdf", "tamanho_arquivo": 301647, "tamanho_formatado": "294.58 KB", "status_processamento": 1}], "estatisticas": {"tipos_arquivo": {"application/pdf": 1}, "total_tamanho": 301647, "ultimo_upload": "2025-10-14 20:41:40", "total_arquivos": 1, "primeiro_upload": "2025-10-14 20:41:40", "total_tamanho_formatado": "294.58 KB"}, "data_consulta": "2025-10-14T23:53:02.529910"}	2025-10-14 23:53:02.52991	2
24	1	david	01/01/2023	100	2025-10-14 21:18:43.893631	Em Aberto	AAQkADhmM2FmNmY0LTFiMjAtNGZmYi05ODQ5LTYyMGZhNTZiOTkyNQAQAJoVQQoMXrZAoOKKdUaT99A=	\N	\N	\N	pending	\N	12	https://api.link.dev.br/dvprocessamento/envio-nf/72d3f4254bd10917fc3dbc04ce122d67	2025-11-13	0	2025-10-14 21:18:45.10213	Registro criado com sucesso	72d3f4254bd10917fc3dbc04ce122d67	{"arquivos": [{"id": 17, "data_upload": "2025-10-14 21:19:04", "observacoes": "", "hash_arquivo": "39f72a29c74cbc22c570759b61633dee", "nome_arquivo": "72d3f4254bd10917fc3dbc04ce122d67.pdf", "tipo_arquivo": "application/pdf", "link_download": "https://api.link.dev.br/dvprocessamento/envio-nf/arquivosNF/72d3f4254bd10917fc3dbc04ce122d67.pdf", "nome_original": "Nf 12.pdf", "caminho_arquivo": "arquivosNF/72d3f4254bd10917fc3dbc04ce122d67.pdf", "tamanho_arquivo": 98257, "tamanho_formatado": "95.95 KB", "status_processamento": 1}], "estatisticas": {"tipos_arquivo": {"application/pdf": 1}, "total_tamanho": 98257, "ultimo_upload": "2025-10-14 21:19:04", "total_arquivos": 1, "primeiro_upload": "2025-10-14 21:19:04", "total_tamanho_formatado": "95.95 KB"}, "data_consulta": "2025-10-14T23:52:55.970642"}	2025-10-14 23:52:55.970642	2
\.


--
-- TOC entry 3931 (class 0 OID 16430)
-- Dependencies: 217
-- Data for Name: montadores; Type: TABLE DATA; Schema: public; Owner: davidgabriel
--

COPY public.montadores (id, nome, identificador, email, percentual_comissao, auxilio_semanal, ativo, fornecedor_id, regra_envio, dias_envio, emails_adicionais) FROM stdin;
\.


--
-- TOC entry 3945 (class 0 OID 16538)
-- Dependencies: 231
-- Data for Name: notificacoes; Type: TABLE DATA; Schema: public; Owner: davidgabriel
--

COPY public.notificacoes (id, tipo, titulo, mensagem, lote_id, lida, data_criacao, data_leitura, icone, prioridade) FROM stdin;
754	nf_recebida	📥 Nota Fiscal Recebida - Lote #21	david enviou 1 arquivo(s) da nota fiscal (294.58 KB)	21	t	2025-10-14 23:53:01.55718	2025-10-14 23:53:02.267765	📥	1
726	teste	🧪 Teste de Toast	Esta é uma notificação de teste para validar o sistema de toasts. Ela deve aparecer apenas UMA vez quando você abrir o app.	\N	t	2025-10-14 23:31:40.753465	2025-10-14 23:31:47.55064	🔔	0
753	nf_recebida	📥 Nota Fiscal Recebida - Lote #22	david enviou 1 arquivo(s) da nota fiscal (95.95 KB)	22	t	2025-10-14 23:52:59.921296	2025-10-14 23:53:02.341363	📥	1
752	nf_recebida	📥 Nota Fiscal Recebida - Lote #23	david enviou 1 arquivo(s) da nota fiscal (448.68 KB)	23	t	2025-10-14 23:52:58.285233	2025-10-14 23:53:02.34887	📥	1
751	nf_recebida	📥 Nota Fiscal Recebida - Lote #24	david enviou 1 arquivo(s) da nota fiscal (95.95 KB)	24	t	2025-10-14 23:52:56.626554	2025-10-14 23:53:02.35435	📥	1
756	nf_recebida	📥 Nota Fiscal Recebida - Lote #19	david enviou 1 arquivo(s) da nota fiscal (294.58 KB)	19	t	2025-10-14 23:53:04.809335	2025-10-14 23:53:05.017451	📥	1
755	nf_recebida	📥 Nota Fiscal Recebida - Lote #20	david enviou 1 arquivo(s) da nota fiscal (294.58 KB)	20	t	2025-10-14 23:53:03.164017	2025-10-14 23:53:05.031174	📥	1
6	nf_recebida	📥 Nota Fiscal Recebida - Lote #24	david enviou 1 arquivo(s) da nota fiscal (95.95 KB)	24	t	2025-10-14 21:20:18.817375	2025-10-14 23:19:19.531899	📥	1
5	nf_recebida	📥 Nota Fiscal Recebida - Lote #19	david enviou 1 arquivo(s) da nota fiscal (294.58 KB)	19	t	2025-10-14 21:08:17.186035	2025-10-14 23:19:19.537135	📥	1
4	nf_recebida	📥 Nota Fiscal Recebida - Lote #20	david enviou 1 arquivo(s) da nota fiscal (294.58 KB)	20	t	2025-10-14 21:08:15.599887	2025-10-14 23:19:19.542524	📥	1
3	nf_recebida	📥 Nota Fiscal Recebida - Lote #21	david enviou 1 arquivo(s) da nota fiscal (294.58 KB)	21	t	2025-10-14 21:08:14.05439	2025-10-14 23:19:19.547673	📥	1
2	nf_recebida	📥 Nota Fiscal Recebida - Lote #22	david enviou 1 arquivo(s) da nota fiscal (95.95 KB)	22	t	2025-10-14 21:08:12.43091	2025-10-14 23:19:19.55487	📥	1
1	nf_recebida	📥 Nota Fiscal Recebida - Lote #23	david enviou 1 arquivo(s) da nota fiscal (448.68 KB)	23	t	2025-10-14 21:08:10.676814	2025-10-14 23:19:19.561972	📥	1
\.


--
-- TOC entry 3943 (class 0 OID 16517)
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
-- TOC entry 3935 (class 0 OID 16459)
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
\.


--
-- TOC entry 3929 (class 0 OID 16417)
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
\.


--
-- TOC entry 3950 (class 0 OID 16588)
-- Dependencies: 236
-- Data for Name: trello_cards; Type: TABLE DATA; Schema: public; Owner: davidgabriel
--

COPY public.trello_cards (id, lote_id, card_id, card_url, data_criacao) FROM stdin;
\.


--
-- TOC entry 3974 (class 0 OID 0)
-- Dependencies: 226
-- Name: boletins_blacklist_id_seq; Type: SEQUENCE SET; Schema: public; Owner: davidgabriel
--

SELECT pg_catalog.setval('public.boletins_blacklist_id_seq', 1, false);


--
-- TOC entry 3975 (class 0 OID 0)
-- Dependencies: 224
-- Name: envios_ignorados_id_seq; Type: SEQUENCE SET; Schema: public; Owner: davidgabriel
--

SELECT pg_catalog.setval('public.envios_ignorados_id_seq', 1, false);


--
-- TOC entry 3976 (class 0 OID 0)
-- Dependencies: 222
-- Name: envios_montagem_id_seq; Type: SEQUENCE SET; Schema: public; Owner: davidgabriel
--

SELECT pg_catalog.setval('public.envios_montagem_id_seq', 1, false);


--
-- TOC entry 3977 (class 0 OID 0)
-- Dependencies: 232
-- Name: jobs_config_id_seq; Type: SEQUENCE SET; Schema: public; Owner: davidgabriel
--

SELECT pg_catalog.setval('public.jobs_config_id_seq', 3, true);


--
-- TOC entry 3978 (class 0 OID 0)
-- Dependencies: 218
-- Name: lotes_servico_id_seq; Type: SEQUENCE SET; Schema: public; Owner: davidgabriel
--

SELECT pg_catalog.setval('public.lotes_servico_id_seq', 24, true);


--
-- TOC entry 3979 (class 0 OID 0)
-- Dependencies: 216
-- Name: montadores_id_seq; Type: SEQUENCE SET; Schema: public; Owner: davidgabriel
--

SELECT pg_catalog.setval('public.montadores_id_seq', 1, false);


--
-- TOC entry 3980 (class 0 OID 0)
-- Dependencies: 230
-- Name: notificacoes_id_seq; Type: SEQUENCE SET; Schema: public; Owner: davidgabriel
--

SELECT pg_catalog.setval('public.notificacoes_id_seq', 756, true);


--
-- TOC entry 3981 (class 0 OID 0)
-- Dependencies: 228
-- Name: os_blacklist_id_seq; Type: SEQUENCE SET; Schema: public; Owner: davidgabriel
--

SELECT pg_catalog.setval('public.os_blacklist_id_seq', 130, true);


--
-- TOC entry 3982 (class 0 OID 0)
-- Dependencies: 220
-- Name: os_enviadas_id_seq; Type: SEQUENCE SET; Schema: public; Owner: davidgabriel
--

SELECT pg_catalog.setval('public.os_enviadas_id_seq', 58, true);


--
-- TOC entry 3983 (class 0 OID 0)
-- Dependencies: 214
-- Name: prestadores_id_seq; Type: SEQUENCE SET; Schema: public; Owner: davidgabriel
--

SELECT pg_catalog.setval('public.prestadores_id_seq', 10, true);


--
-- TOC entry 3984 (class 0 OID 0)
-- Dependencies: 235
-- Name: trello_cards_id_seq; Type: SEQUENCE SET; Schema: public; Owner: davidgabriel
--

SELECT pg_catalog.setval('public.trello_cards_id_seq', 1, false);


--
-- TOC entry 3759 (class 2606 OID 16509)
-- Name: boletins_blacklist boletins_blacklist_pkey; Type: CONSTRAINT; Schema: public; Owner: davidgabriel
--

ALTER TABLE ONLY public.boletins_blacklist
    ADD CONSTRAINT boletins_blacklist_pkey PRIMARY KEY (id);


--
-- TOC entry 3756 (class 2606 OID 16498)
-- Name: envios_ignorados envios_ignorados_pkey; Type: CONSTRAINT; Schema: public; Owner: davidgabriel
--

ALTER TABLE ONLY public.envios_ignorados
    ADD CONSTRAINT envios_ignorados_pkey PRIMARY KEY (id);


--
-- TOC entry 3753 (class 2606 OID 16483)
-- Name: envios_montagem envios_montagem_pkey; Type: CONSTRAINT; Schema: public; Owner: davidgabriel
--

ALTER TABLE ONLY public.envios_montagem
    ADD CONSTRAINT envios_montagem_pkey PRIMARY KEY (id);


--
-- TOC entry 3774 (class 2606 OID 16586)
-- Name: integracoes_config integracoes_config_pkey; Type: CONSTRAINT; Schema: public; Owner: davidgabriel
--

ALTER TABLE ONLY public.integracoes_config
    ADD CONSTRAINT integracoes_config_pkey PRIMARY KEY (id);


--
-- TOC entry 3770 (class 2606 OID 16575)
-- Name: jobs_config jobs_config_nome_key; Type: CONSTRAINT; Schema: public; Owner: davidgabriel
--

ALTER TABLE ONLY public.jobs_config
    ADD CONSTRAINT jobs_config_nome_key UNIQUE (nome);


--
-- TOC entry 3772 (class 2606 OID 16573)
-- Name: jobs_config jobs_config_pkey; Type: CONSTRAINT; Schema: public; Owner: davidgabriel
--

ALTER TABLE ONLY public.jobs_config
    ADD CONSTRAINT jobs_config_pkey PRIMARY KEY (id);


--
-- TOC entry 3745 (class 2606 OID 16452)
-- Name: lotes_servico lotes_servico_pkey; Type: CONSTRAINT; Schema: public; Owner: davidgabriel
--

ALTER TABLE ONLY public.lotes_servico
    ADD CONSTRAINT lotes_servico_pkey PRIMARY KEY (id);


--
-- TOC entry 3747 (class 2606 OID 16533)
-- Name: lotes_servico lotes_servico_upload_token_key; Type: CONSTRAINT; Schema: public; Owner: davidgabriel
--

ALTER TABLE ONLY public.lotes_servico
    ADD CONSTRAINT lotes_servico_upload_token_key UNIQUE (upload_token);


--
-- TOC entry 3739 (class 2606 OID 16442)
-- Name: montadores montadores_fornecedor_id_key; Type: CONSTRAINT; Schema: public; Owner: davidgabriel
--

ALTER TABLE ONLY public.montadores
    ADD CONSTRAINT montadores_fornecedor_id_key UNIQUE (fornecedor_id);


--
-- TOC entry 3741 (class 2606 OID 16440)
-- Name: montadores montadores_identificador_key; Type: CONSTRAINT; Schema: public; Owner: davidgabriel
--

ALTER TABLE ONLY public.montadores
    ADD CONSTRAINT montadores_identificador_key UNIQUE (identificador);


--
-- TOC entry 3743 (class 2606 OID 16438)
-- Name: montadores montadores_pkey; Type: CONSTRAINT; Schema: public; Owner: davidgabriel
--

ALTER TABLE ONLY public.montadores
    ADD CONSTRAINT montadores_pkey PRIMARY KEY (id);


--
-- TOC entry 3768 (class 2606 OID 16549)
-- Name: notificacoes notificacoes_pkey; Type: CONSTRAINT; Schema: public; Owner: davidgabriel
--

ALTER TABLE ONLY public.notificacoes
    ADD CONSTRAINT notificacoes_pkey PRIMARY KEY (id);


--
-- TOC entry 3763 (class 2606 OID 16525)
-- Name: os_blacklist os_blacklist_pkey; Type: CONSTRAINT; Schema: public; Owner: davidgabriel
--

ALTER TABLE ONLY public.os_blacklist
    ADD CONSTRAINT os_blacklist_pkey PRIMARY KEY (id);


--
-- TOC entry 3749 (class 2606 OID 16468)
-- Name: os_enviadas os_enviadas_os_numero_key; Type: CONSTRAINT; Schema: public; Owner: davidgabriel
--

ALTER TABLE ONLY public.os_enviadas
    ADD CONSTRAINT os_enviadas_os_numero_key UNIQUE (os_numero);


--
-- TOC entry 3751 (class 2606 OID 16466)
-- Name: os_enviadas os_enviadas_pkey; Type: CONSTRAINT; Schema: public; Owner: davidgabriel
--

ALTER TABLE ONLY public.os_enviadas
    ADD CONSTRAINT os_enviadas_pkey PRIMARY KEY (id);


--
-- TOC entry 3733 (class 2606 OID 16428)
-- Name: prestadores prestadores_fornecedor_id_key; Type: CONSTRAINT; Schema: public; Owner: davidgabriel
--

ALTER TABLE ONLY public.prestadores
    ADD CONSTRAINT prestadores_fornecedor_id_key UNIQUE (fornecedor_id);


--
-- TOC entry 3735 (class 2606 OID 16426)
-- Name: prestadores prestadores_nome_key; Type: CONSTRAINT; Schema: public; Owner: davidgabriel
--

ALTER TABLE ONLY public.prestadores
    ADD CONSTRAINT prestadores_nome_key UNIQUE (nome);


--
-- TOC entry 3737 (class 2606 OID 16424)
-- Name: prestadores prestadores_pkey; Type: CONSTRAINT; Schema: public; Owner: davidgabriel
--

ALTER TABLE ONLY public.prestadores
    ADD CONSTRAINT prestadores_pkey PRIMARY KEY (id);


--
-- TOC entry 3777 (class 2606 OID 16596)
-- Name: trello_cards trello_cards_pkey; Type: CONSTRAINT; Schema: public; Owner: davidgabriel
--

ALTER TABLE ONLY public.trello_cards
    ADD CONSTRAINT trello_cards_pkey PRIMARY KEY (id);


--
-- TOC entry 3779 (class 2606 OID 16598)
-- Name: trello_cards unique_lote_card; Type: CONSTRAINT; Schema: public; Owner: davidgabriel
--

ALTER TABLE ONLY public.trello_cards
    ADD CONSTRAINT unique_lote_card UNIQUE (lote_id);


--
-- TOC entry 3764 (class 1259 OID 16556)
-- Name: idx_notificacoes_data; Type: INDEX; Schema: public; Owner: davidgabriel
--

CREATE INDEX idx_notificacoes_data ON public.notificacoes USING btree (data_criacao DESC);


--
-- TOC entry 3765 (class 1259 OID 16555)
-- Name: idx_notificacoes_lida; Type: INDEX; Schema: public; Owner: davidgabriel
--

CREATE INDEX idx_notificacoes_lida ON public.notificacoes USING btree (lida);


--
-- TOC entry 3766 (class 1259 OID 16557)
-- Name: idx_notificacoes_lote; Type: INDEX; Schema: public; Owner: davidgabriel
--

CREATE INDEX idx_notificacoes_lote ON public.notificacoes USING btree (lote_id);


--
-- TOC entry 3775 (class 1259 OID 16599)
-- Name: idx_trello_cards_lote; Type: INDEX; Schema: public; Owner: davidgabriel
--

CREATE INDEX idx_trello_cards_lote ON public.trello_cards USING btree (lote_id);


--
-- TOC entry 3760 (class 1259 OID 16515)
-- Name: idx_unique_boletim_blacklist; Type: INDEX; Schema: public; Owner: davidgabriel
--

CREATE UNIQUE INDEX idx_unique_boletim_blacklist ON public.boletins_blacklist USING btree (montador_id, boletim);


--
-- TOC entry 3757 (class 1259 OID 16499)
-- Name: idx_unique_ignore; Type: INDEX; Schema: public; Owner: davidgabriel
--

CREATE UNIQUE INDEX idx_unique_ignore ON public.envios_ignorados USING btree (tipo, entidade_id, ano, periodo_chave);


--
-- TOC entry 3754 (class 1259 OID 16489)
-- Name: idx_unique_montagem; Type: INDEX; Schema: public; Owner: davidgabriel
--

CREATE UNIQUE INDEX idx_unique_montagem ON public.envios_montagem USING btree (((detalhes ->> 'periodo_relatorio'::text)), montador_id);


--
-- TOC entry 3761 (class 1259 OID 16531)
-- Name: idx_unique_os_blacklist; Type: INDEX; Schema: public; Owner: davidgabriel
--

CREATE UNIQUE INDEX idx_unique_os_blacklist ON public.os_blacklist USING btree (prestador_id, os_numero);


--
-- TOC entry 3783 (class 2606 OID 16510)
-- Name: boletins_blacklist boletins_blacklist_montador_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: davidgabriel
--

ALTER TABLE ONLY public.boletins_blacklist
    ADD CONSTRAINT boletins_blacklist_montador_id_fkey FOREIGN KEY (montador_id) REFERENCES public.montadores(id) ON DELETE CASCADE;


--
-- TOC entry 3782 (class 2606 OID 16484)
-- Name: envios_montagem envios_montagem_montador_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: davidgabriel
--

ALTER TABLE ONLY public.envios_montagem
    ADD CONSTRAINT envios_montagem_montador_id_fkey FOREIGN KEY (montador_id) REFERENCES public.montadores(id);


--
-- TOC entry 3780 (class 2606 OID 16453)
-- Name: lotes_servico lotes_servico_prestador_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: davidgabriel
--

ALTER TABLE ONLY public.lotes_servico
    ADD CONSTRAINT lotes_servico_prestador_id_fkey FOREIGN KEY (prestador_id) REFERENCES public.prestadores(id);


--
-- TOC entry 3785 (class 2606 OID 16550)
-- Name: notificacoes notificacoes_lote_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: davidgabriel
--

ALTER TABLE ONLY public.notificacoes
    ADD CONSTRAINT notificacoes_lote_id_fkey FOREIGN KEY (lote_id) REFERENCES public.lotes_servico(id);


--
-- TOC entry 3784 (class 2606 OID 16526)
-- Name: os_blacklist os_blacklist_prestador_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: davidgabriel
--

ALTER TABLE ONLY public.os_blacklist
    ADD CONSTRAINT os_blacklist_prestador_id_fkey FOREIGN KEY (prestador_id) REFERENCES public.prestadores(id) ON DELETE CASCADE;


--
-- TOC entry 3781 (class 2606 OID 16469)
-- Name: os_enviadas os_enviadas_lote_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: davidgabriel
--

ALTER TABLE ONLY public.os_enviadas
    ADD CONSTRAINT os_enviadas_lote_id_fkey FOREIGN KEY (lote_id) REFERENCES public.lotes_servico(id) ON DELETE CASCADE;


-- Completed on 2025-10-14 23:54:28 -03

--
-- PostgreSQL database dump complete
--

\unrestrict ZMXaTxRIaMMtMcMmDPJ7MXGKD3mI9zm8kj9DAqVzS60pBFMSgIEMRUZ2NmuYyNL

