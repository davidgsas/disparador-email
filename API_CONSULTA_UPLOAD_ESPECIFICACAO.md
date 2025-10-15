# API de Consulta de Upload de Notas Fiscais - Especificação

## 📋 Visão Geral

Esta API permite que o sistema Disparador de Emails consulte o status de upload de notas fiscais e faça download dos arquivos quando disponíveis.

**⚠️ IMPORTANTE:** O sistema Disparador **NÃO** gera links de upload. Ele apenas **CONSULTA** se um lote teve nota fiscal anexada.

## 🎯 Responsabilidades

### Sistema Disparador (quem consulta):
- Envia relatório de serviços por email aos prestadores
- Consulta periodicamente se nota fiscal foi recebida
- Baixa arquivo quando disponível
- Exibe status na interface interna

### Seu Sistema (quem fornece a API):
- Gera link único de upload por lote
- Envia link ao prestador (email/SMS/WhatsApp/etc)
- Recebe upload da nota fiscal do prestador
- Valida e armazena arquivo
- **Fornece endpoint para consulta de status por lote_id**
- **Fornece URL para download do arquivo**

## 🔌 Endpoint Necessário

### Consultar Status de um Lote

```
GET /api/lotes/{lote_id}/status
```

**Descrição:** Consulta se um lote específico teve nota fiscal anexada.

**Parâmetros:**
- `lote_id` (path, integer, obrigatório): ID do lote no sistema Disparador

**Headers:**
```
Authorization: Bearer {API_KEY}
Content-Type: application/json
```

**Autenticação:**
- Bearer Token (API Key fornecida por você)
- Validar API Key em cada requisição
- Retornar 401 se não autorizada

## 📊 Respostas da API

### Caso 1: Upload Pendente (Prestador ainda não enviou)

**Status Code:** `200 OK`

**Response:**
```json
{
  "lote_id": 123,
  "status": "pending",
  "message": "Aguardando upload do prestador",
  "link_gerado_em": "2025-10-13T14:30:00Z",
  "expira_em": "2025-11-13T14:30:00Z"
}
```

**Campos:**
- `lote_id`: ID do lote (mesmo enviado na requisição)
- `status`: Estado atual (`pending`)
- `message`: Mensagem descritiva
- `link_gerado_em` (opcional): Quando o link foi criado
- `expira_em` (opcional): Data de expiração do link

---

### Caso 2: Upload Completo (Nota fiscal recebida)

**Status Code:** `200 OK`

**Response:**
```json
{
  "lote_id": 123,
  "status": "completed",
  "nota_fiscal": {
    "filename": "nota_fiscal_123.pdf",
    "download_url": "https://api-externa.com/api/downloads/abc123xyz789unique",
    "uploaded_at": "2025-10-14T10:30:00Z",
    "file_size": 245678,
    "content_type": "application/pdf",
    "checksum": "sha256:abc123def456..."
  },
  "prestador": {
    "nome": "João Silva Instalações LTDA",
    "email": "joao.silva@empresa.com.br"
  }
}
```

**Campos:**
- `lote_id`: ID do lote
- `status`: Estado atual (`completed`)
- `nota_fiscal`: Objeto com informações do arquivo
  - `filename`: Nome do arquivo original
  - `download_url`: **URL COMPLETA para download** (com autenticação)
  - `uploaded_at`: Data/hora do upload (ISO 8601)
  - `file_size`: Tamanho em bytes
  - `content_type`: Tipo MIME (sempre `application/pdf`)
  - `checksum` (opcional): Hash do arquivo para validação
- `prestador` (opcional): Informações do prestador que fez upload

**⚠️ IMPORTANTE sobre download_url:**
- Deve ser uma URL completa e acessível
- Deve aceitar autenticação via Bearer Token (mesmo API_KEY)
- Deve retornar o arquivo PDF diretamente
- Exemplo: `GET https://api-externa.com/api/downloads/abc123xyz789unique`

---

### Caso 3: Link Expirado (30 dias sem uso)

**Status Code:** `200 OK`

**Response:**
```json
{
  "lote_id": 123,
  "status": "expired",
  "message": "Link de upload expirou após 30 dias",
  "link_gerado_em": "2025-09-13T14:30:00Z",
  "expirou_em": "2025-10-13T14:30:00Z"
}
```

---

### Caso 4: Lote Não Encontrado

**Status Code:** `404 Not Found`

**Response:**
```json
{
  "error": "Lote não encontrado",
  "lote_id": 999,
  "message": "O lote 999 não está cadastrado no sistema de upload"
}
```

---

### Caso 5: Não Autorizado

**Status Code:** `401 Unauthorized`

**Response:**
```json
{
  "error": "Não autorizado",
  "message": "API Key inválida ou ausente"
}
```

---

### Caso 6: Erro Interno

**Status Code:** `500 Internal Server Error`

**Response:**
```json
{
  "error": "Erro interno do servidor",
  "message": "Ocorreu um erro ao processar sua requisição"
}
```

## 📥 Endpoint de Download

### Baixar Arquivo da Nota Fiscal

```
GET /api/downloads/{token}
```

**Descrição:** Faz download do arquivo PDF da nota fiscal.

**Headers:**
```
Authorization: Bearer {API_KEY}
```

**Response:**
- **Status Code:** `200 OK`
- **Content-Type:** `application/pdf`
- **Body:** Arquivo PDF (binary)
- **Headers sugeridos:**
  - `Content-Disposition: attachment; filename="nota_fiscal_123.pdf"`
  - `Content-Length: 245678`

**Erros:**
- `401`: API Key inválida
- `404`: Token não encontrado ou expirado
- `410`: Arquivo foi removido

## 🔐 Segurança

### API Key
- Gere uma API Key única e segura para o sistema Disparador
- Formato recomendado: String aleatória de 32+ caracteres
- Exemplo: `nmrj_2K8dP9mN3qR7sT1vW5xY4zA6bC0eF2gH8jK3mL9nP1qR5sT7vW0xY4zA6`
- Prefixo `nmrj_` (Novo Mundo Resolve Jobs) facilita identificação

### Validação
- Sempre validar API Key no header Authorization
- Retornar 401 se ausente ou inválida
- Registrar tentativas de acesso não autorizado

### Rate Limiting
- Recomendado: 60 requisições por minuto por API Key
- Retornar 429 se limite excedido
- Header: `X-RateLimit-Remaining: 45`

### HTTPS
- **Obrigatório** usar HTTPS em produção
- Não aceitar requisições HTTP

## 📝 Exemplos de Uso

### Exemplo 1: Consultar lote pendente

**Request:**
```bash
curl -X GET "https://api-externa.com/api/lotes/123/status" \
  -H "Authorization: Bearer nmrj_2K8dP9mN3qR7sT1vW5xY4zA6bC0eF2gH8jK3mL9nP1qR5sT7vW0xY4zA6" \
  -H "Content-Type: application/json"
```

**Response:**
```json
{
  "lote_id": 123,
  "status": "pending",
  "message": "Aguardando upload do prestador"
}
```

---

### Exemplo 2: Consultar lote com N.F. recebida

**Request:**
```bash
curl -X GET "https://api-externa.com/api/lotes/124/status" \
  -H "Authorization: Bearer nmrj_2K8dP9mN3qR7sT1vW5xY4zA6bC0eF2gH8jK3mL9nP1qR5sT7vW0xY4zA6"
```

**Response:**
```json
{
  "lote_id": 124,
  "status": "completed",
  "nota_fiscal": {
    "filename": "nota_fiscal_124.pdf",
    "download_url": "https://api-externa.com/api/downloads/xyz789abc456def123",
    "uploaded_at": "2025-10-14T10:30:00Z",
    "file_size": 245678,
    "content_type": "application/pdf"
  }
}
```

---

### Exemplo 3: Baixar arquivo

**Request:**
```bash
curl -X GET "https://api-externa.com/api/downloads/xyz789abc456def123" \
  -H "Authorization: Bearer nmrj_2K8dP9mN3qR7sT1vW5xY4zA6bC0eF2gH8jK3mL9nP1qR5sT7vW0xY4zA6" \
  -o nota_fiscal_124.pdf
```

**Response:**
- Arquivo PDF baixado com sucesso

## 🔄 Fluxo Completo

```
┌─────────────────────────────────────────────────────────────────┐
│  1. SISTEMA DISPARADOR                                          │
│     └─ Envia email com relatório de serviços                   │
│     └─ Registra lote_id no banco de dados                      │
│     └─ Status inicial: "pending"                                │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│  2. SEU SISTEMA                                                 │
│     └─ Recebe notificação de novo lote (webhook ou polling)    │
│     └─ Gera link único de upload                               │
│     └─ Envia link ao prestador (email/SMS/WhatsApp)           │
│     └─ Status: "pending" (aguardando upload)                   │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│  3. PRESTADOR                                                   │
│     └─ Recebe link                                              │
│     └─ Acessa página de upload                                  │
│     └─ Seleciona PDF da nota fiscal                            │
│     └─ Faz upload                                               │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│  4. SEU SISTEMA                                                 │
│     └─ Recebe arquivo                                           │
│     └─ Valida (tipo, tamanho, etc)                             │
│     └─ Armazena arquivo                                         │
│     └─ Status: "completed"                                      │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│  5. SISTEMA DISPARADOR (consulta periódica)                    │
│     └─ Job executa a cada hora                                 │
│     └─ GET /api/lotes/123/status                               │
│     └─ Recebe status "completed"                               │
│     └─ Baixa arquivo via download_url                          │
│     └─ Salva localmente                                         │
│     └─ Atualiza status no banco                                │
└─────────────────────────────────────────────────────────────────┘
```

## 🧪 Testes Recomendados

### Teste 1: Lote Pendente
```bash
GET /api/lotes/123/status
→ Deve retornar status: "pending"
```

### Teste 2: Lote Completo
```bash
GET /api/lotes/124/status
→ Deve retornar status: "completed" + download_url
```

### Teste 3: Download de Arquivo
```bash
GET {download_url}
→ Deve retornar PDF (binary)
```

### Teste 4: Lote Inexistente
```bash
GET /api/lotes/999999/status
→ Deve retornar 404
```

### Teste 5: Sem Autenticação
```bash
GET /api/lotes/123/status (sem header Authorization)
→ Deve retornar 401
```

### Teste 6: API Key Inválida
```bash
GET /api/lotes/123/status (com API Key errada)
→ Deve retornar 401
```

## 📊 Políticas

### Expiração de Links
- Links de upload devem expirar após **30 dias** sem uso
- Após expiração, retornar `status: "expired"`

### Armazenamento de Arquivos
- Arquivos devem ser mantidos por pelo menos **2 anos**
- Após período, podem ser arquivados ou removidos

### Validação de Arquivos
- Aceitar apenas arquivos PDF
- Tamanho máximo: **10 MB**
- Rejeitar arquivos corrompidos ou inválidos

### Notificação (Opcional)
Se quiser implementar webhook para notificar quando upload completo:
```
POST https://sistema-disparador.com/webhook/nota-recebida
Content-Type: application/json

{
  "lote_id": 123,
  "status": "completed",
  "download_url": "https://api-externa.com/api/downloads/xyz789"
}
```

## 🚀 Prazos Sugeridos

1. **Semana 1-2**: Implementar endpoint de consulta de status
2. **Semana 2-3**: Implementar endpoint de download
3. **Semana 3**: Testes de integração
4. **Semana 4**: Deploy em produção

## 📞 Informações para Fornecer ao Disparador

Após implementação, enviar:

1. **URL Base da API**
   - Exemplo: `https://api-externa.novomundo.com.br`

2. **API Key**
   - Exemplo: `nmrj_2K8dP9mN3qR7sT1vW5xY4zA6bC0eF2gH8jK3mL9nP1qR5sT7vW0xY4zA6`

3. **Formato dos Endpoints**
   - Confirmar se seguem o padrão desta especificação

4. **Rate Limits**
   - Informar limites de requisições

5. **Ambiente de Teste**
   - Fornecer credenciais de homologação (se disponível)

## ❓ Perguntas Frequentes

**P: O Disparador vai criar os links de upload?**
R: Não! Apenas seu sistema cria e gerencia links.

**P: Como o Disparador saberá qual lote consultar?**
R: Ele consulta pelo lote_id que ele próprio gerou ao enviar o email.

**P: Com que frequência o Disparador vai consultar?**
R: Por padrão, a cada hora via job automático. Também há consulta manual pela interface.

**P: O que fazer se o prestador não enviar a N.F.?**
R: Após 30 dias, o link expira. O status fica "expired" e o processo manual deve ser acionado.

**P: Posso mudar a estrutura dos endpoints?**
R: Sim, mas avise para ajustarmos o cliente. Esta é apenas uma sugestão.

## 📄 Resumo

**Endpoint Principal:**
```
GET /api/lotes/{lote_id}/status
Authorization: Bearer {API_KEY}
```

**Responses:**
- `200` + `status: "pending"` → Aguardando
- `200` + `status: "completed"` + `download_url` → Recebido
- `200` + `status: "expired"` → Expirado
- `404` → Lote não encontrado
- `401` → Não autorizado

**Endpoint de Download:**
```
GET /api/downloads/{token}
Authorization: Bearer {API_KEY}
→ Retorna arquivo PDF (binary)
```

---

**Versão:** 2.0 (Corrigida)  
**Data:** 13 de outubro de 2025  
**Status:** Aguardando Implementação
