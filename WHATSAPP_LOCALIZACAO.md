# 📱 WhatsApp - Onde Está Cada Coisa

## 🎯 Localização na Interface

A funcionalidade WhatsApp está integrada na interface Streamlit:

**Menu Principal → 📱 WhatsApp**

### Abas Disponíveis:

1. **🔌 Status & Conexão**
   - Ver status da conexão
   - QR Code para conectar
   - Informações do usuário conectado
   - Instruções de como conectar

2. **📤 Enviar Mensagens**
   - Enviar para número manual
   - Enviar para prestador (lista todos com telefone)
   - Enviar para montador (lista todos com telefone)
   - Envio em massa (múltiplos números)
   - Formatação de mensagens (negrito, itálico)
   - Controle de delay entre mensagens

3. **📊 Histórico**
   - Ver todas as mensagens enviadas
   - Filtrar por tipo (manual, nota_fiscal, lembrete, etc)
   - Filtrar por status (enviado, erro)
   - Ver detalhes de cada envio

4. **⚙️ Configurações**
   - URLs dos endpoints da API
   - Adicionar telefones em prestadores sem cadastro
   - Adicionar telefones em montadores sem cadastro
   - Executar teste de conexão

---

## 📂 Estrutura de Arquivos

### Backend (API Node.js)
- `whatsapp_service.js` - Serviço principal com API REST
- `package.json` - Dependências do Node.js

### Frontend (Interface Streamlit)
- `painel_whatsapp.py` - Painel completo na interface
- `streamlit_app.py` - Menu principal (linha 156 e 2095)

### Cliente Python
- `whatsapp_client.py` - Cliente para usar no código Python
- `integracao_whatsapp_exemplo.py` - Exemplos práticos

### Scripts Auxiliares
- `install_whatsapp.sh` - Instalação automática
- `start_whatsapp.sh` - Iniciar serviço
- `teste_whatsapp.py` - Teste interativo

### Banco de Dados
- `database.py` - Tabela `notificacoes_whatsapp` (linhas 103-118)
- Campos `telefone` em prestadores e montadores

### Documentação
- `WHATSAPP_INTEGRATION.md` - Documentação completa
- `WHATSAPP_QUICKSTART.md` - Guia rápido
- `WHATSAPP_LOCALIZACAO.md` - Este arquivo

---

## 🚀 Como Usar

### 1. Iniciar o Serviço (Primeira Vez)

```bash
# Terminal
./install_whatsapp.sh
./start_whatsapp.sh
```

### 2. Conectar WhatsApp

**Via Interface:**
1. Abra a aplicação Streamlit
2. Menu → **📱 WhatsApp**
3. Aba **🔌 Status & Conexão**
4. Clique em "Ver QR Code"
5. Escaneie com WhatsApp

**Via Browser:**
- Acesse: http://localhost:3000/qr

### 3. Cadastrar Telefones

**Via Interface:**
1. Menu → **📱 WhatsApp**
2. Aba **⚙️ Configurações**
3. Em "Adicionar Telefones"
4. Digite telefones dos prestadores/montadores
5. Clique em 💾 para salvar

**Via Banco (SQL):**
```sql
UPDATE prestadores SET telefone = '11999999999' WHERE id = 1;
UPDATE montadores SET telefone = '11988888888' WHERE id = 1;
```

### 4. Enviar Mensagens

**Via Interface:**
1. Menu → **📱 WhatsApp**
2. Aba **📤 Enviar Mensagens**
3. Escolha o tipo (manual, prestador, montador, lista)
4. Digite a mensagem
5. Clique em "📤 Enviar Mensagem"

**Via Python:**
```python
from whatsapp_client import WhatsAppClient

whatsapp = WhatsAppClient()
whatsapp.send_message("11999999999", "Olá!")
```

**Via Integração Automática:**
```python
from integracao_whatsapp_exemplo import NotificacaoIntegrada

notificador = NotificacaoIntegrada()
notificador.notificar_prestador_nota_fiscal(
    prestador_id=1,
    periodo="01-31/10",
    valor=1500.00,
    whatsapp=True
)
```

### 5. Ver Histórico

**Via Interface:**
1. Menu → **📱 WhatsApp**
2. Aba **📊 Histórico**
3. Aplique filtros se necessário
4. Clique nos cards para ver detalhes

**Via SQL:**
```sql
SELECT * FROM notificacoes_whatsapp 
ORDER BY data_envio DESC 
LIMIT 50;
```

---

## 🔗 URLs Importantes

| Recurso | URL |
|---------|-----|
| **QR Code** | http://localhost:3000/qr |
| **Status** | http://localhost:3000/status |
| **Info Usuário** | http://localhost:3000/info |
| **Enviar** | POST http://localhost:3000/send |
| **Enviar Massa** | POST http://localhost:3000/send-bulk |

---

## 🎨 Capturas de Tela

### Menu Principal
```
┌─────────────────────────────────┐
│ MENU                            │
├─────────────────────────────────┤
│ Selecione a Página:             │
│ ┌─────────────────────────────┐ │
│ │ 📱 WhatsApp              ⏷ │ │
│ └─────────────────────────────┘ │
└─────────────────────────────────┘
```

### Página WhatsApp
```
┌─────────────────────────────────────────────┐
│ 📱 WhatsApp                                 │
├─────────────────────────────────────────────┤
│ [🔌 Status] [📤 Enviar] [📊 Histórico] [⚙️] │
├─────────────────────────────────────────────┤
│                                             │
│  Status da Conexão                          │
│  ┌─────────────┬──────────────┬───────────┐ │
│  │ ✅ Conectado│ 🔗 Autenticado│ 🔄 Atualizar│ │
│  └─────────────┴──────────────┴───────────┘ │
│                                             │
│  👤 Usuário Conectado                       │
│  Nome: David | Número: 5511999... | Android │
│                                             │
└─────────────────────────────────────────────┘
```

---

## 🔍 Busca Rápida

### Como adicionar telefone em prestador?
→ Interface: Menu → WhatsApp → Configurações → Prestadores
→ Código: `database.py` função para atualizar

### Como enviar mensagem?
→ Interface: Menu → WhatsApp → Enviar Mensagens
→ Código: `whatsapp_client.send_message()`

### Onde ver histórico de envios?
→ Interface: Menu → WhatsApp → Histórico
→ Banco: Tabela `notificacoes_whatsapp`

### Como reconectar WhatsApp?
→ Interface: Menu → WhatsApp → Status → Ver QR Code
→ Browser: http://localhost:3000/qr

### O serviço não inicia, o que fazer?
→ Verificar Node.js: `node -v`
→ Instalar: `./install_whatsapp.sh`
→ Iniciar: `./start_whatsapp.sh`

---

## 💡 Dicas

1. **Mantenha o serviço sempre rodando** para receber mensagens
2. **Use delay de 3-5 segundos** em envios em massa
3. **Teste primeiro** com seu próprio número
4. **Cadastre telefones** antes de usar automações
5. **Monitore o histórico** para ver falhas

---

## 📞 Suporte

- **Documentação completa:** `WHATSAPP_INTEGRATION.md`
- **Guia rápido:** `WHATSAPP_QUICKSTART.md`
- **Exemplos de código:** `integracao_whatsapp_exemplo.py`
- **Teste interativo:** `python teste_whatsapp.py`

---

**✅ Tudo pronto para usar WhatsApp no sistema!**
