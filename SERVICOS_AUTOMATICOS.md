# 🚀 Sistema de Inicialização Automática

## Serviços Incluídos

Quando você executa `./run_app.sh`, os seguintes serviços são iniciados automaticamente:

1. **📱 Serviço WhatsApp** (porta 3000)
2. **🌐 Interface Streamlit** (porta 8501)

## Como Usar

### Iniciar Tudo
```bash
./run_app.sh
```

### Parar Tudo
```bash
./stop_app.sh
```

### Verificar Status
```bash
# Status do WhatsApp
./status_whatsapp_daemon.sh

# Verificar se Streamlit está rodando
ps aux | grep streamlit
```

## O que Acontece Quando Você Inicia

```
┌─────────────────────────────────────────┐
│  ./run_app.sh                           │
└─────────────────────────────────────────┘
              ↓
    ┌─────────────────────┐
    │ Verificações        │
    │ - Node.js instalado?│
    │ - Dependências OK?  │
    └─────────────────────┘
              ↓
    ┌─────────────────────┐
    │ Inicia WhatsApp     │
    │ (background)        │
    │ PID salvo em:       │
    │ whatsapp_service.pid│
    └─────────────────────┘
              ↓
    Aguarda 5 segundos
              ↓
    ┌─────────────────────┐
    │ Verifica se iniciou │
    │ - Teste na porta    │
    │ - Consulta API      │
    └─────────────────────┘
              ↓
    ┌─────────────────────┐
    │ Inicia Streamlit    │
    │ (foreground)        │
    │ Browser abre auto   │
    └─────────────────────┘
```

## Logs

### WhatsApp
- Saída padrão: `logs/whatsapp_service.log`
- Erros: `logs/whatsapp_stderr.log`

### Streamlit
- Saída no terminal onde foi executado

## Arquivos de PID

- WhatsApp: `whatsapp_service.pid`
- Contém o Process ID do serviço

## Portas Usadas

| Serviço | Porta | URL |
|---------|-------|-----|
| WhatsApp API | 3000 | http://localhost:3000 |
| WhatsApp QR | 3000 | http://localhost:3000/qr |
| Streamlit | 8501 | http://localhost:8501 |

## Comandos Manuais

### WhatsApp

```bash
# Iniciar
./start_whatsapp_daemon.sh

# Parar
./stop_whatsapp_daemon.sh

# Status
./status_whatsapp_daemon.sh
```

### Streamlit

```bash
# Iniciar
streamlit run streamlit_app.py

# Parar
Ctrl+C no terminal
```

## Troubleshooting

### "Port 3000 already in use"
```bash
# Matar processo na porta 3000
lsof -ti:3000 | xargs kill -9

# Ou usar o script
./stop_whatsapp_daemon.sh
```

### "WhatsApp não conectou"
1. Abra: http://localhost:3000/qr
2. Escaneie o QR Code
3. Aguarde confirmação

### "Streamlit não abre"
```bash
# Verificar se está rodando
ps aux | grep streamlit

# Se não, inicie manualmente
streamlit run streamlit_app.py
```

### Logs de erro
```bash
# Ver logs do WhatsApp
tail -f logs/whatsapp_service.log
tail -f logs/whatsapp_stderr.log

# Ver erros recentes
tail -50 logs/whatsapp_stderr.log
```

## Reiniciar Apenas um Serviço

### Reiniciar WhatsApp
```bash
./stop_whatsapp_daemon.sh
./start_whatsapp_daemon.sh
```

### Reiniciar Streamlit
```bash
# Ctrl+C no terminal
# Depois:
streamlit run streamlit_app.py
```

## Inicialização Automática no Boot (Opcional)

Se quiser que o WhatsApp inicie automaticamente quando o Mac ligar:

```bash
./install_whatsapp_autostart.sh
```

Para remover:
```bash
./uninstall_whatsapp_autostart.sh
```

## Checklist de Verificação

Após iniciar com `./run_app.sh`:

- [ ] WhatsApp API respondendo em http://localhost:3000/status
- [ ] WhatsApp conectado (verificar na interface)
- [ ] Streamlit aberto no browser
- [ ] Menu WhatsApp funcionando na interface

## Estrutura de Arquivos

```
disparador-email/
├── run_app.sh                    # Inicia tudo
├── stop_app.sh                   # Para tudo
├── start_whatsapp_daemon.sh      # Inicia só WhatsApp
├── stop_whatsapp_daemon.sh       # Para só WhatsApp
├── status_whatsapp_daemon.sh     # Status do WhatsApp
├── whatsapp_service.pid          # PID do WhatsApp
├── whatsapp_service.js           # Código do serviço
├── streamlit_app.py              # Interface principal
└── logs/
    ├── whatsapp_service.log      # Logs gerais
    ├── whatsapp_stdout.log       # Saída padrão
    └── whatsapp_stderr.log       # Erros
```

---

**✅ Tudo configurado para iniciar junto!**
