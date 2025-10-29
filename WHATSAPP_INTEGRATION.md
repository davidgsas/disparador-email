# 📱 Integração WhatsApp

## Visão Geral

Este projeto agora inclui integração completa com WhatsApp usando **whatsapp-web.js**, permitindo enviar mensagens automatizadas através de uma API REST.

## 🚀 Como Funcionar

### 1. Instalar Dependências

```bash
npm install
```

### 2. Iniciar o Serviço WhatsApp

```bash
npm start
```

Ou para desenvolvimento com auto-reload:

```bash
npm run dev
```

### 3. Conectar o WhatsApp

Após iniciar o serviço, você verá um QR Code no terminal. Existem duas formas de conectar:

#### Opção 1: Pelo Terminal
- Escaneie o QR Code mostrado no terminal com o WhatsApp do seu celular

#### Opção 2: Pelo Navegador (Mais Fácil)
1. Acesse: http://localhost:3000/qr
2. Escaneie o QR Code com o WhatsApp do seu celular
3. Aguarde a confirmação de conexão

**Como escanear:**
1. Abra o WhatsApp no seu celular
2. Toque em **Menu** (⋮) ou **Configurações**
3. Toque em **Aparelhos conectados**
4. Toque em **Conectar um aparelho**
5. Aponte a câmera para o QR Code

## 📡 API REST

O serviço expõe uma API REST na porta **3000** com os seguintes endpoints:

### Status da Conexão

```bash
GET http://localhost:3000/status
```

Resposta:
```json
{
  "status": "connected",
  "hasQrCode": false,
  "message": "WhatsApp conectado e pronto"
}
```

### Ver QR Code

```bash
GET http://localhost:3000/qr
```

Abre uma página HTML com o QR Code para escanear.

### Informações do Usuário

```bash
GET http://localhost:3000/info
```

Resposta:
```json
{
  "success": true,
  "info": {
    "number": "5511999999999",
    "name": "Seu Nome",
    "platform": "android"
  }
}
```

### Enviar Mensagem

```bash
POST http://localhost:3000/send
Content-Type: application/json

{
  "number": "5511999999999",
  "message": "Olá! Esta é uma mensagem automática."
}
```

Com mídia (imagem, PDF, etc):
```json
{
  "number": "5511999999999",
  "message": "Segue o arquivo em anexo",
  "media": {
    "path": "/caminho/completo/para/arquivo.pdf"
  }
}
```

Resposta:
```json
{
  "success": true,
  "message": "Mensagem enviada com sucesso",
  "to": "5511999999999"
}
```

### Enviar para Múltiplos Números

```bash
POST http://localhost:3000/send-bulk
Content-Type: application/json

{
  "numbers": [
    "5511999999999",
    "5511988888888",
    "5511977777777"
  ],
  "message": "Mensagem para todos!",
  "delay": 3000
}
```

Parâmetros:
- `numbers`: Array de números
- `message`: Texto da mensagem
- `delay`: Delay entre mensagens em milissegundos (padrão: 2000)
- `media` (opcional): Objeto com `path` para arquivo

Resposta:
```json
{
  "success": true,
  "results": [
    { "number": "5511999999999", "success": true },
    { "number": "5511988888888", "success": true },
    { "number": "5511977777777", "success": false, "error": "Número inválido" }
  ],
  "total": 3,
  "sent": 2,
  "failed": 1
}
```

### Desconectar

```bash
POST http://localhost:3000/disconnect
```

## 🐍 Cliente Python

Use o cliente Python para facilitar a integração:

```python
from whatsapp_client import WhatsAppClient

# Criar cliente
whatsapp = WhatsAppClient()

# Verificar status
if whatsapp.is_connected():
    print("WhatsApp conectado!")
    
    # Obter info do usuário
    info = whatsapp.get_info()
    print(f"Usuário: {info['info']['name']}")
    
    # Enviar mensagem
    result = whatsapp.send_message(
        number="11999999999",
        message="Olá! Mensagem automática."
    )
    
    if result["success"]:
        print("Mensagem enviada!")
    
    # Enviar para múltiplos
    result = whatsapp.send_bulk_messages(
        numbers=["11999999999", "11988888888"],
        message="Mensagem em massa!",
        delay=3000  # 3 segundos entre cada mensagem
    )
    
    print(f"Enviadas: {result['sent']}/{result['total']}")
else:
    print("WhatsApp não conectado!")
    print("Acesse: http://localhost:3000/qr")
```

### Aguardar Conexão

```python
from whatsapp_client import WhatsAppClient

whatsapp = WhatsAppClient()

print("Aguardando conexão do WhatsApp...")
if whatsapp.wait_for_connection(timeout=120):
    print("Conectado!")
    # Continuar com o código...
else:
    print("Timeout: não foi possível conectar")
```

## 🎯 Casos de Uso

### 1. Notificações de Notas Fiscais

```python
from whatsapp_client import WhatsAppClient

def notificar_nota_fiscal(numero, nome_prestador, valor, periodo):
    whatsapp = WhatsAppClient()
    
    if not whatsapp.is_connected():
        print("WhatsApp não conectado!")
        return False
    
    mensagem = f"""
🧾 *Nova Nota Fiscal*

Prestador: {nome_prestador}
Período: {periodo}
Valor: R$ {valor:.2f}

Por favor, emita a nota fiscal conforme especificado no email.
    """.strip()
    
    result = whatsapp.send_message(numero, mensagem)
    return result.get("success", False)
```

### 2. Lembretes de Pendências

```python
def enviar_lembretes_pendencias(contatos):
    whatsapp = WhatsAppClient()
    
    for contato in contatos:
        mensagem = f"""
⚠️ *Lembrete*

Olá, {contato['nome']}!

Você ainda tem pendências relacionadas a:
{contato['pendencia']}

Por favor, regularize o quanto antes.
        """.strip()
        
        whatsapp.send_message(contato['numero'], mensagem)
        time.sleep(3)  # Aguarda 3 segundos entre mensagens
```

### 3. Confirmação de Upload

```python
def confirmar_upload(numero, nome_arquivo):
    whatsapp = WhatsAppClient()
    
    mensagem = f"""
✅ *Upload Concluído*

O arquivo {nome_arquivo} foi recebido e está sendo processado.

Você receberá uma notificação quando o processamento for concluído.
    """.strip()
    
    return whatsapp.send_message(numero, mensagem)
```

### 4. Enviar Relatórios

```python
def enviar_relatorio_mensal(contatos, arquivo_relatorio):
    whatsapp = WhatsAppClient()
    
    mensagem = """
📊 *Relatório Mensal*

Segue o relatório consolidado do mês.

Qualquer dúvida, estamos à disposição!
    """.strip()
    
    result = whatsapp.send_bulk_messages(
        numbers=[c['numero'] for c in contatos],
        message=mensagem,
        media_path=arquivo_relatorio,
        delay=5000  # 5 segundos entre mensagens
    )
    
    return result
```

## ⚙️ Configurações

### Portas

A API roda na porta **3000** por padrão. Para mudar:

```bash
PORT=8080 npm start
```

Ou no Python:
```python
whatsapp = WhatsAppClient(base_url="http://localhost:8080")
```

### Sessão Persistente

A sessão do WhatsApp é salva na pasta `whatsapp_session/`. Isso significa que você só precisa escanear o QR Code uma vez. Nas próximas execuções, a conexão será automática.

Para forçar uma nova autenticação, delete a pasta:
```bash
rm -rf whatsapp_session/
```

## 🔒 Segurança

### Recomendações:

1. **Não exponha a API publicamente** sem autenticação
2. **Use HTTPS** em produção
3. **Implemente rate limiting** para evitar abuso
4. **Valide números** antes de enviar
5. **Respeite limites do WhatsApp** (não envie spam!)

### Exemplo com autenticação básica:

Adicione no `whatsapp_service.js`:

```javascript
// Middleware de autenticação
const authenticate = (req, res, next) => {
    const token = req.headers['authorization'];
    
    if (token !== 'Bearer SEU_TOKEN_SECRETO') {
        return res.status(401).json({ error: 'Não autorizado' });
    }
    
    next();
};

// Proteger endpoints
app.post('/send', authenticate, async (req, res) => {
    // ... código existente
});
```

## 🐛 Problemas Comuns

### QR Code não aparece
- Certifique-se que o Node.js está instalado (versão 16+)
- Verifique se não há outro processo na porta 3000
- Execute `npm install` novamente

### Sessão desconecta sozinha
- O WhatsApp pode desconectar se detectar atividade suspeita
- Evite enviar muitas mensagens em pouco tempo
- Respeite o delay entre mensagens (mínimo 2 segundos)

### Erro ao enviar mensagem
- Verifique se o número está correto (com código do país)
- Certifique-se que o WhatsApp está conectado (`GET /status`)
- Verifique se o número existe no WhatsApp

## 📚 Recursos Adicionais

- [Documentação whatsapp-web.js](https://wwebjs.dev/)
- [Exemplos de uso](https://github.com/pedroslopez/whatsapp-web.js/tree/main/example)

## 🤝 Suporte

Se tiver problemas ou dúvidas, verifique:
1. Logs do terminal onde o serviço está rodando
2. Status da conexão (`GET /status`)
3. Se o QR Code foi escaneado corretamente

---

**🎉 Pronto! Agora você pode enviar mensagens automatizadas pelo WhatsApp!**
