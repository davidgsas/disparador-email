# 🚀 Guia Rápido - Jobs Automáticos

## ⚡ Início Rápido (3 passos)

### 1. Inicie o Scheduler
```bash
./manage_scheduler.sh start
```

### 2. Acesse o Painel
1. Abra o Streamlit
2. Vá em **"⚙️ Jobs Automáticos"**
3. Configure os jobs

### 3. Pronto!
Os jobs vão rodar automaticamente em background! 🎉

---

## 📱 Painel Streamlit

**O que você pode fazer:**

- ✅ **Ver Status**: Serviço rodando ou parado
- ▶️ **Iniciar/Parar**: Controle total do serviço
- ⚙️ **Configurar Jobs**: Ativar/desativar e ajustar intervalos
- 📊 **Monitorar**: Ver execuções, erros e próximas rodadas
- 📋 **Logs**: Acompanhar em tempo real

---

## 🔧 Comandos Úteis

```bash
# Ver status
./manage_scheduler.sh status

# Parar
./manage_scheduler.sh stop

# Reiniciar
./manage_scheduler.sh restart

# Recarregar configurações (sem parar)
./manage_scheduler.sh reload

# Ver logs
./manage_scheduler.sh logs

# Acompanhar logs ao vivo
./manage_scheduler.sh follow
```

---

## 📦 Jobs Disponíveis

### 🔍 consultar_notas
- **O que faz**: Busca e baixa notas fiscais enviadas pelos prestadores
- **Intervalo recomendado**: 60 minutos
- **Quando roda**: Quando há lotes com status "Enviado API"

### 📤 enviar_api  
- **O que faz**: Envia lotes pendentes para a API
- **Intervalo recomendado**: 30-60 minutos
- **Quando roda**: Quando há lotes com envio_api_pendente = true

---

## 🎯 Como Funciona

```
┌─────────────────────────────────────────┐
│   Scheduler Service (Background)        │
│   - Roda independente do Streamlit      │
│   - Executa jobs nos intervalos         │
│   - Lê configurações do banco           │
└─────────────────────────────────────────┘
           ↓                    ↑
    ┌──────────────┐    ┌──────────────┐
    │  PostgreSQL  │    │  Streamlit   │
    │  (Config)    │    │  (Controle)  │
    └──────────────┘    └──────────────┘
```

**Importante**: 
- 🔥 O scheduler roda SOZINHO, não precisa manter o Streamlit aberto
- 💾 Configurações salvas no banco de dados
- 🔄 Mudanças no painel aplicadas instantaneamente (reload)

---

## ❓ Problemas?

### Scheduler não inicia
```bash
# Teste direto
python scheduler_service.py

# Veja erros completos
tail -f scheduler.log
```

### Jobs não executam
```bash
# Recarregue configurações
./manage_scheduler.sh reload

# Verifique status
./manage_scheduler.sh status
```

### Mais ajuda
Leia **JOBS_AUTOMATICOS.md** para documentação completa

---

## 📚 Documentação Completa

- **JOBS_AUTOMATICOS.md** - Documentação técnica completa
- **DOCUMENTACAO_CONSULTA_NF.md** - API de consulta de notas
- **DOWNLOAD_AUTOMATICO_NF.md** - Sistema de download automático

---

## ✨ Novidades

### v1.0.0 - Sistema de Jobs Automáticos

**O que mudou:**
- ✅ Jobs rodam automaticamente sem precisar executar código
- ✅ Painel de controle completo no Streamlit
- ✅ Configuração via interface (sem editar código)
- ✅ Logs detalhados de todas as operações
- ✅ Hot reload de configurações
- ✅ Notificações quando notas são recebidas

**Antes:**
```bash
# Tinha que rodar manualmente
python job_consultar_notas.py
```

**Agora:**
```bash
# Inicia uma vez
./manage_scheduler.sh start

# Roda sozinho para sempre! 🚀
```

---

**Feito com ❤️ para simplificar sua vida!**
