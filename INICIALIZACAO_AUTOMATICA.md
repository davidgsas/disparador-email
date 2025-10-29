# 🚀 Inicialização Automática do Sistema

## Como Funciona

Quando você executa `./run_app.sh`, o sistema automaticamente:

1. ✅ **Verifica** se o serviço WhatsApp está rodando
2. 🚀 **Inicia** o serviço WhatsApp (se não estiver rodando)
3. 🌐 **Inicia** a interface Streamlit

## Scripts Disponíveis

### Iniciar Sistema Completo
```bash
./run_app.sh
```
**O que faz:**
- Inicia serviço WhatsApp em background
- Inicia interface Streamlit
- Configura variáveis de ambiente necessárias

### Parar Sistema Completo
```bash
./stop_app.sh
```
**O que faz:**
- Para o serviço WhatsApp
- Para a interface Streamlit
- Limpa processos em background

### Verificar Status do WhatsApp
```bash
./status_whatsapp_daemon.sh
```
**O que faz:**
- Mostra se o serviço está rodando
- Exibe PID do processo
- Mostra status da API

### Controle Manual do WhatsApp

#### Iniciar apenas WhatsApp
```bash
./start_whatsapp_daemon.sh
```

#### Parar apenas WhatsApp
```bash
./stop_whatsapp_daemon.sh
```

## Inicialização Automática no Boot do Mac

Se você quiser que o WhatsApp inicie automaticamente quando ligar o Mac:

### Instalar
```bash
./install_whatsapp_autostart.sh
```

### Desinstalar
```bash
./uninstall_whatsapp_autostart.sh
```

## Arquivos e Logs

### PID Files
- `whatsapp_service.pid` - PID do processo WhatsApp

### Logs
- `logs/whatsapp_service.log` - Log principal do serviço
- `logs/whatsapp_stdout.log` - Saída padrão
- `logs/whatsapp_stderr.log` - Erros

## Fluxo de Execução

```
┌─────────────────────────────────────────────┐
│  ./run_app.sh                               │
└─────────────────┬───────────────────────────┘
                  │
                  ├─→ Verifica WhatsApp
                  │   ├─ Rodando? → OK
                  │   └─ Não? → Inicia
                  │
                  └─→ Inicia Streamlit
                      └─ Interface disponível
```

## Uso Recomendado

### Desenvolvimento
```bash
# Inicia tudo
./run_app.sh

# Quando terminar
./stop_app.sh
```

### Produção
```bash
# Instalar inicialização automática
./install_whatsapp_autostart.sh

# Iniciar interface
./run_app.sh
```

## Troubleshooting

### WhatsApp não inicia
```bash
# Ver logs
cat logs/whatsapp_service.log

# Verificar se Node.js está instalado
node -v

# Verificar se dependências estão instaladas
ls node_modules/
```

### Porta 3000 ocupada
```bash
# Verificar o que está usando a porta
lsof -i :3000

# Matar processo
kill $(lsof -t -i:3000)
```

### Interface não carrega
```bash
# Verificar se ambiente virtual está ativo
which python

# Verificar se Streamlit está instalado
streamlit --version
```

## Variáveis de Ambiente

O script `run_app.sh` configura automaticamente:
- `DYLD_LIBRARY_PATH` - Bibliotecas do Homebrew
- `PKG_CONFIG_PATH` - Configurações de pacotes

## URLs

Após iniciar:
- **Streamlit**: http://localhost:8501
- **WhatsApp API**: http://localhost:3000
- **WhatsApp QR Code**: http://localhost:3000/qr

---

**✅ Agora o WhatsApp inicia automaticamente junto com o sistema!**
