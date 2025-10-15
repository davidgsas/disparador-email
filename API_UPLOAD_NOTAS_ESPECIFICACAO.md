# 📋 API de Upload de Notas Fiscais - Especificação para Desenvolvedor Externo

## 📖 Visão Geral

Sistema para recebimento de notas fiscais de prestadores através de links únicos gerados por lote de serviço.

## 🎯 Fluxo Completo

```
1. Sistema Disparador → Cria lote de serviço
2. Sistema Disparador → Envia dados via API → Sistema Externo
3. Sistema Externo → Gera link único com token
4. Sistema Externo → Retorna link para Sistema Disparador
5. Sistema Disparador → Envia email com link ao prestador
6. Prestador → Acessa link → Faz upload da nota fiscal
7. Sistema Disparador → Consulta API periodicamente
8. Sistema Externo → Retorna arquivo quando disponível
9. Sistema Disparador → Salva arquivo localmente
```

## 🔌 Endpoints Necessários

### 1. Criar Link de Upload

**Endpoint:** `POST /api/upload/create`

**Descrição:** Cria um link único para upload de nota fiscal

**Headers:**
```json
{
  "Content-Type": "application/json",
  "Authorization": "Bearer {API_KEY}"
}
```

**Request Body:**
```json
{
  "lote_id": 12345,
  "prestador": {
    "id": 10,
    "nome": "João Silva Instalações LTDA",
    "email": "joao.silva@empresa.com.br"
  },
  "lote_info": {
    "periodo": "10/2025",
    "valor_total": 1250.50,
    "quantidade_os": 5,
    "data_envio": "2025-10-13T14:30:00"
  },
  "metadata": {
    "sistema": "disparador-email",
    "versao": "1.0",
    "empresa": "Novo Mundo"
  }
}
```

**Response Success (201):**
```json
{
  "success": true,
  "data": {
    "token": "abc123xyz789unique",
    "upload_url": "https://seu-sistema.com/upload/abc123xyz789unique",
    "expires_at": "2025-11-13T14:30:00",
    "lote_id": 12345
  },
  "message": "Link de upload criado com sucesso"
}
```

**Response Error (400/500):**
```json
{
  "success": false,
  "error": {
    "code": "INVALID_DATA",
    "message": "Descrição do erro"
  }
}
```

---

### 2. Consultar Status do Upload

**Endpoint:** `GET /api/upload/status/{token}`

**Descrição:** Consulta se a nota fiscal foi enviada e está disponível

**Headers:**
```json
{
  "Authorization": "Bearer {API_KEY}"
}
```

**URL Parameters:**
- `token` (string, required): Token único do upload

**Response - Pendente (200):**
```json
{
  "success": true,
  "data": {
    "token": "abc123xyz789unique",
    "lote_id": 12345,
    "status": "pending",
    "uploaded": false,
    "upload_date": null,
    "file_available": false
  }
}
```

**Response - Upload Concluído (200):**
```json
{
  "success": true,
  "data": {
    "token": "abc123xyz789unique",
    "lote_id": 12345,
    "status": "completed",
    "uploaded": true,
    "upload_date": "2025-10-14T10:25:30",
    "file_available": true,
    "file_info": {
      "filename": "nota_fiscal_lote_12345.pdf",
      "size": 245678,
      "mimetype": "application/pdf",
      "hash": "sha256:abc123..."
    }
  }
}
```

**Response - Expirado (200):**
```json
{
  "success": true,
  "data": {
    "token": "abc123xyz789unique",
    "lote_id": 12345,
    "status": "expired",
    "uploaded": false,
    "expired_at": "2025-11-13T14:30:00"
  }
}
```

---

### 3. Download do Arquivo

**Endpoint:** `GET /api/upload/download/{token}`

**Descrição:** Faz download do arquivo enviado

**Headers:**
```json
{
  "Authorization": "Bearer {API_KEY}"
}
```

**Response Success (200):**
- Content-Type: `application/pdf` (ou tipo do arquivo)
- Content-Disposition: `attachment; filename="nota_fiscal_lote_12345.pdf"`
- Body: Binário do arquivo

**Response Error (404):**
```json
{
  "success": false,
  "error": {
    "code": "FILE_NOT_FOUND",
    "message": "Arquivo não disponível ou token inválido"
  }
}
```

---

## 🌐 Página de Upload (Interface Web)

### URL Pattern
```
https://seu-sistema.com/upload/{token}
```

### Informações a Exibir na Página

1. **Dados do Lote:**
   - Nome do prestador
   - Período
   - Valor total
   - Quantidade de OS

2. **Formulário de Upload:**
   - Campo de seleção de arquivo (aceitar apenas PDF)
   - Botão "Enviar Nota Fiscal"
   - Barra de progresso
   - Mensagem de sucesso/erro

3. **Validações:**
   - Arquivo deve ser PDF
   - Tamanho máximo: 10MB
   - Token válido e não expirado

### Exemplo de Interface HTML (sugestão)

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>Upload de Nota Fiscal - Lote #{lote_id}</title>
</head>
<body>
    <h1>Upload de Nota Fiscal</h1>
    
    <div class="info">
        <h2>Dados do Lote</h2>
        <p><strong>Prestador:</strong> {prestador_nome}</p>
        <p><strong>Período:</strong> {periodo}</p>
        <p><strong>Valor Total:</strong> R$ {valor_total}</p>
        <p><strong>Quantidade de OS:</strong> {quantidade_os}</p>
    </div>
    
    <form id="uploadForm" enctype="multipart/form-data">
        <label>Selecione a Nota Fiscal (PDF):</label>
        <input type="file" name="nota_fiscal" accept=".pdf" required>
        <button type="submit">Enviar Nota Fiscal</button>
    </form>
    
    <div id="status"></div>
</body>
</html>
```

---

## 🔐 Autenticação

### API Key
- Deve ser enviada no header `Authorization: Bearer {API_KEY}`
- API Key será fornecida pelo Sistema Disparador
- Validar em todas as requisições

### Sugestão de Implementação
```python
# Exemplo em Python/Flask
@app.before_request
def validate_api_key():
    api_key = request.headers.get('Authorization', '').replace('Bearer ', '')
    if api_key != VALID_API_KEY:
        return jsonify({"success": False, "error": "Unauthorized"}), 401
```

---

## 💾 Armazenamento

### Estrutura de Dados Sugerida

**Tabela: uploads**
```sql
CREATE TABLE uploads (
    id SERIAL PRIMARY KEY,
    token VARCHAR(255) UNIQUE NOT NULL,
    lote_id INTEGER NOT NULL,
    prestador_id INTEGER NOT NULL,
    prestador_nome VARCHAR(255),
    prestador_email VARCHAR(255),
    periodo VARCHAR(50),
    valor_total DECIMAL(10,2),
    quantidade_os INTEGER,
    status VARCHAR(50) DEFAULT 'pending',
    upload_date TIMESTAMP,
    file_path VARCHAR(500),
    file_name VARCHAR(255),
    file_size INTEGER,
    file_mimetype VARCHAR(100),
    file_hash VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP,
    metadata JSONB
);
```

---

## ⏰ Políticas

### Expiração
- Links devem expirar em **30 dias** após criação
- Após expiração, retornar status `expired`

### Segurança
- Validar tamanho máximo: **10MB**
- Validar tipo de arquivo: **apenas PDF**
- Validar token em todas as requisições
- Rate limiting: máximo 10 requisições por minuto

---

## 📊 Exemplos de Requisições

### 1. Criar Link
```bash
curl -X POST https://seu-sistema.com/api/upload/create \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer sua-api-key" \
  -d '{"lote_id": 12345, "prestador": {...}}'
```

### 2. Consultar Status
```bash
curl -X GET https://seu-sistema.com/api/upload/status/abc123xyz \
  -H "Authorization: Bearer sua-api-key"
```

### 3. Download
```bash
curl -X GET https://seu-sistema.com/api/upload/download/abc123xyz \
  -H "Authorization: Bearer sua-api-key" -o nota.pdf
```

---

**Versão:** 1.0.0  
**Data:** 13 de outubro de 2025
