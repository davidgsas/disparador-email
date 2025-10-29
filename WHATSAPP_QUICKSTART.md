# 🚀 GUIA RÁPIDO - WhatsApp

## ⚡ Início Rápido

### 1️⃣ Instalar (Apenas primeira vez)

```bash
./install_whatsapp.sh
```

Se não tiver Node.js, o script tentará instalar via Homebrew.

### 2️⃣ Iniciar Serviço

```bash
./start_whatsapp.sh
```

ou

```bash
npm start
```

### 3️⃣ Conectar WhatsApp

**Opção A - Terminal:**
- Escaneie o QR Code que aparece no terminal

**Opção B - Browser (Mais fácil):**
1. Abra: http://localhost:3000/qr
2. Escaneie o QR Code com WhatsApp
3. Aguarde confirmação

### 4️⃣ Usar no Python

```python
from whatsapp_client import WhatsAppClient

# Criar cliente
whatsapp = WhatsAppClient()

# Verificar se está conectado
if whatsapp.is_connected():
    # Enviar mensagem
    whatsapp.send_message(
        number="11999999999",
        message="Olá! Mensagem automática."
    )
```

---

## 📡 Endpoints da API

### Status
```bash
curl http://localhost:3000/status
```

### Enviar Mensagem
```bash
curl -X POST http://localhost:3000/send \
  -H "Content-Type: application/json" \
  -d '{
    "number": "5511999999999",
    "message": "Teste"
  }'
```

### Enviar para Múltiplos
```bash
curl -X POST http://localhost:3000/send-bulk \
  -H "Content-Type: application/json" \
  -d '{
    "numbers": ["5511999999999", "5511988888888"],
    "message": "Mensagem para todos"
  }'
```

---

## 🎯 Integração com Sistema

### Notificar Prestador
```python
from integracao_whatsapp_exemplo import NotificacaoIntegrada

notificador = NotificacaoIntegrada()

# Enviar notificação de nota fiscal
resultado = notificador.notificar_prestador_nota_fiscal(
    prestador_id=1,
    periodo="01/10/2025 a 31/10/2025",
    valor=1500.00,
    email=True,      # Enviar email também
    whatsapp=True    # Enviar WhatsApp
)
```

### Notificar Múltiplos
```python
prestadores = [
    {"id": 1, "periodo": "01-31/10", "valor": 1500.00},
    {"id": 2, "periodo": "01-31/10", "valor": 2300.00},
]

resultados = notificador.notificar_multiplos_prestadores(
    prestadores=prestadores,
    whatsapp=True
)
```

---

## 🔧 Comandos Úteis

```bash
# Iniciar serviço
npm start

# Modo desenvolvimento (auto-reload)
npm run dev

# Ver status
curl http://localhost:3000/status

# Parar serviço
# Ctrl+C ou:
kill $(lsof -t -i:3000)
```

---

## ❓ Problemas Comuns

### QR Code não aparece
- Aguarde 10-15 segundos
- Acesse http://localhost:3000/qr

### Porta 3000 ocupada
```bash
# Matar processo na porta 3000
kill $(lsof -t -i:3000)
```

### WhatsApp desconecta
- Reescaneie o QR Code
- Evite enviar muitas mensagens seguidas
- Use delay de 2-3 segundos entre mensagens

### Erro "npm: command not found"
```bash
# Instalar Node.js via Homebrew
brew install node

# Ou baixe em: https://nodejs.org
```

---

## 📁 Arquivos Importantes

- `whatsapp_service.js` - Serviço Node.js (API REST)
- `whatsapp_client.py` - Cliente Python
- `integracao_whatsapp_exemplo.py` - Exemplos de uso
- `whatsapp_session/` - Sessão salva (não deletar!)

---

## ✅ Checklist

- [ ] Node.js instalado
- [ ] Dependências instaladas (`npm install`)
- [ ] Serviço iniciado (`npm start`)
- [ ] QR Code escaneado
- [ ] Status = "connected"
- [ ] Teste de envio funcionando

---

**Dúvidas? Veja: WHATSAPP_INTEGRATION.md**
