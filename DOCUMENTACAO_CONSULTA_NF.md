# 📋 Sistema de Consulta de Notas Fiscais

## 🎯 Visão Geral

Sistema implementado para consultar e baixar arquivos de notas fiscais enviadas pelos prestadores através do hash gerado pela API DV Processamento.

## 📦 Arquivos Criados/Modificados

### ✨ Novos Arquivos

1. **`consulta_nf_client.py`** - Cliente para consultar arquivos da API
2. **`testar_consulta_nf.py`** - Script de teste para consultas

### 🔧 Arquivos Modificados

1. **`database.py`** - Novas funções para gerenciar arquivos NF
2. **`job_consultar_notas.py`** - Atualizado para usar novo sistema
3. **Banco de Dados** - Novas colunas adicionadas

---

## 🗄️ Estrutura do Banco de Dados

### Novas Colunas em `lotes_servico`

```sql
ALTER TABLE lotes_servico 
ADD COLUMN upload_hash VARCHAR(255),          -- Hash para consultar arquivos
ADD COLUMN arquivos_nf JSONB,                  -- Dados dos arquivos (JSON)
ADD COLUMN data_ultima_consulta TIMESTAMP,     -- Data da última consulta
ADD COLUMN status_arquivo INTEGER DEFAULT 0;   -- Status: 0=Aguardando, 1=Recebido, 2=Baixado
```

---

## 🔑 API de Consulta

### Endpoint

```
POST http://api.link.dev.br/dvprocessamento/consulta-nf/
```

### Headers

```
Content-Type: application/json
X-API-Key: DV_API_2025_CTRL_NOTAS_f8e9d2c1b4a6
```

### Request Body

```json
{
    "hash": "03de0449e11849318f7d67e08377f150"
}
```

### Response (Sucesso)

```json
{
    "success": true,
    "data": {
        "nota_fiscal": {
            "id_controle": 6,
            "lote_id": 999997848,
            "nome": "Prestador LTDA",
            "email": "prestador@email.com",
            "periodo": "10/2025",
            "valor_total": 15750.50,
            "quantidade_os": 8,
            "status": 1,
            "validade_link": "2025-11-14 14:30:00"
        },
        "arquivos": [
            {
                "id": 1,
                "nome_original": "nota_fiscal.pdf",
                "tipo_arquivo": "PDF",
                "tamanho_formatado": "2.00 MB",
                "link_download": "https://api.link.dev.br/...",
                "data_upload": "2025-10-14 15:30:00",
                "status_processamento": "processado"
            }
        ],
        "estatisticas": {
            "total_arquivos": 1,
            "total_tamanho_formatado": "2.00 MB"
        }
    }
}
```

---

## 🛠️ Uso do Sistema

### 1. Teste de Consulta Manual

```bash
# Testar consulta com um hash específico
python testar_consulta_nf.py 03de0449e11849318f7d67e08377f150
```

### 2. Job Automático

```bash
# Executar job de consulta (verifica todos os lotes pendentes)
python job_consultar_notas.py
```

### 3. Uso Programático

```python
from consulta_nf_client import ConsultaNFClient

# Criar cliente
client = ConsultaNFClient()

# Consultar nota fiscal
sucesso, dados, erro = client.consultar_e_processar(hash_nota)

if sucesso:
    nota = dados['nota']
    arquivos = dados['arquivos']
    
    # Processar arquivos
    for arquivo in arquivos:
        print(f"Arquivo: {arquivo['nome_original']}")
        print(f"Tamanho: {arquivo['tamanho_formatado']}")
        
        # Baixar arquivo
        client.baixar_arquivo(
            arquivo['link_download'],
            f"./downloads/{arquivo['nome_original']}"
        )
```

---

## 📊 Funções do Database.py

### `salvar_arquivos_nf(lote_id, arquivos_dados, estatisticas)`
Salva dados dos arquivos recebidos no banco de dados.

```python
db.salvar_arquivos_nf(
    lote_id=13,
    arquivos_dados=lista_arquivos,
    estatisticas=stats
)
```

### `get_arquivos_nf(lote_id)`
Retorna dados dos arquivos salvos.

```python
dados = db.get_arquivos_nf(lote_id=13)
if dados:
    arquivos = dados['arquivos_nf']
```

### `atualizar_status_arquivo(lote_id, status)`
Atualiza status do arquivo (0=Aguardando, 1=Recebido, 2=Baixado).

```python
db.atualizar_status_arquivo(lote_id=13, status=2)
```

### `get_lotes_com_arquivos()`
Retorna todos os lotes que já receberam arquivos.

```python
lotes = db.get_lotes_com_arquivos()
for lote in lotes:
    print(f"Lote {lote['id']}: {lote['prestador_nome']}")
```

---

## 🔄 Fluxo do Sistema

### 1. Envio para API
```
Lote criado → Enviar para API → Recebe hash + link
                                 ↓
                         Salva no banco (upload_hash)
```

### 2. Consulta de Arquivos
```
Job automático → Busca lotes com link válido
                 ↓
              Consulta API com hash
                 ↓
            Recebe lista de arquivos
                 ↓
         Salva dados no banco (arquivos_nf)
                 ↓
            Baixa cada arquivo
                 ↓
      Atualiza status (status_arquivo = 2)
```

### 3. Visualização
```
Interface Streamlit → Exibe arquivos recebidos
                      ↓
               Permite download local
```

---

## 🎨 Status dos Arquivos

| Código | Status | Descrição |
|--------|--------|-----------|
| 0 | Aguardando | Link gerado, aguardando upload |
| 1 | Recebido | Arquivo foi enviado pelo prestador |
| 2 | Baixado | Arquivo já foi baixado localmente |

---

## 🧪 Como Testar

### 1. Criar um lote e enviar para API

Pelo Streamlit:
1. Criar novo lote
2. Clicar em "Enviar para API"
3. Copiar o hash retornado

### 2. Simular envio de arquivo (se houver ambiente de teste)

Use o link recebido para fazer upload de um arquivo de teste.

### 3. Consultar arquivos

```bash
# Com o hash copiado
python testar_consulta_nf.py SEU_HASH_AQUI
```

### 4. Executar job automático

```bash
python job_consultar_notas.py
```

### 5. Verificar no banco

```sql
-- Ver lotes com arquivos
SELECT id, prestador_nome, status_arquivo, data_ultima_consulta 
FROM lotes_servico 
WHERE upload_hash IS NOT NULL;

-- Ver dados dos arquivos
SELECT id, prestador_nome, arquivos_nf 
FROM lotes_servico 
WHERE status_arquivo >= 1;
```

---

## 📁 Estrutura de Pastas

```
disparador-email/
├── consulta_nf_client.py       # Cliente de consulta
├── testar_consulta_nf.py        # Script de teste
├── job_consultar_notas.py       # Job automático
├── database.py                  # Funções do banco
└── uploads/                     # Arquivos baixados
    └── lote_13/                 # Pasta por lote
        ├── nota_fiscal.pdf
        └── comprovante.xml
```

---

## 🔒 Segurança

- ✅ API Key armazenada no código (ambiente de desenvolvimento)
- ✅ SSL desabilitado temporariamente (certificado não ativo)
- ✅ Validação de hash antes de consultar
- ✅ Timeout de 30 segundos nas requisições
- ✅ Tratamento de erros completo

**🚨 Para produção:**
- Mover API Key para variável de ambiente
- Ativar SSL quando certificado estiver disponível
- Implementar logs de auditoria
- Adicionar rate limiting

---

## 📝 Próximos Passos

1. ✅ Sistema de consulta implementado
2. ✅ Job automático configurado
3. ⏳ Interface Streamlit (a implementar)
4. ⏳ Configurar cron para job automático
5. ⏳ Notificações quando arquivos forem recebidos

---

## 🆘 Troubleshooting

### Erro 401 - API Key inválida
Verifique se a API Key está correta no `consulta_nf_client.py`

### Erro 404 - Nota não encontrada
O hash pode estar incorreto ou a nota não existe

### Erro 410 - Link expirado
O link expira após 30 dias. Gerar novo link.

### Timeout
Aumente o timeout na requisição ou verifique conexão com a internet

---

## 📞 Suporte

Para dúvidas sobre a API, consulte o desenvolvedor externo que forneceu as credenciais.
