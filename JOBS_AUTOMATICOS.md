# 🤖 Sistema de Jobs Automáticos

## 📋 Visão Geral

O sistema de jobs automáticos permite que tarefas recorrentes sejam executadas sem intervenção manual. O serviço roda em background de forma independente do Streamlit, garantindo operação contínua.

## 🎯 Características Principais

- ✅ **Execução Automática**: Jobs rodam em background sem necessidade de manter aplicação aberta
- ✅ **Configuração Via Interface**: Controle completo via painel do Streamlit
- ✅ **Banco de Dados**: Configurações armazenadas em PostgreSQL
- ✅ **Hot Reload**: Recarrega configurações sem parar o serviço
- ✅ **Logs Detalhados**: Registro completo de execuções
- ✅ **Monitoramento**: Status em tempo real e estatísticas

## 🏗️ Arquitetura

### Componentes

1. **scheduler_service.py**: Serviço principal que roda em background
2. **painel_jobs.py**: Interface Streamlit para gerenciamento
3. **database.py**: Funções para manipulação de configurações
4. **manage_scheduler.sh**: Script auxiliar para controle via terminal

### Banco de Dados

#### Tabela: jobs_config

```sql
CREATE TABLE jobs_config (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) UNIQUE NOT NULL,
    descricao TEXT,
    ativo BOOLEAN DEFAULT true,
    intervalo_minutos INTEGER DEFAULT 60,
    ultima_execucao TIMESTAMP,
    proxima_execucao TIMESTAMP,
    total_execucoes INTEGER DEFAULT 0,
    total_erros INTEGER DEFAULT 0,
    ultima_mensagem TEXT,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 🚀 Como Usar

### Método 1: Via Interface Streamlit (Recomendado)

1. Acesse o sistema e faça login
2. No menu lateral, selecione "⚙️ Jobs Automáticos"
3. Clique em "▶️ Iniciar Serviço"
4. Configure os jobs:
   - Ative/desative usando o toggle
   - Ajuste o intervalo em minutos
   - Clique em "💾 Salvar"
5. Monitore as execuções e logs em tempo real

### Método 2: Via Terminal

```bash
# Iniciar serviço
./manage_scheduler.sh start

# Ver status
./manage_scheduler.sh status

# Parar serviço
./manage_scheduler.sh stop

# Recarregar configurações
./manage_scheduler.sh reload

# Ver logs
./manage_scheduler.sh logs

# Acompanhar logs em tempo real
./manage_scheduler.sh follow
```

### Método 3: Python Direto

```bash
# Iniciar
python scheduler_service.py

# Parar
python scheduler_service.py stop

# Status
python scheduler_service.py status

# Recarregar
python scheduler_service.py reload
```

## 📦 Jobs Disponíveis

### 1. consultar_notas

**Descrição**: Consulta e baixa arquivos de notas fiscais enviadas por prestadores

**Funcionamento**:
- Busca todos os lotes com status "Enviado API" (status 4)
- Para cada lote, consulta a API usando o hash
- Baixa todos os arquivos anexados
- Salva na pasta `uploads/lote_{ID}/`
- Atualiza status para "Arquivo Baixado" (status 2)
- Cria notificação para o usuário

**Intervalo Recomendado**: 60 minutos

**Arquivos Envolvidos**:
- `job_consultar_notas.py`
- `consulta_nf_client.py`

### 2. enviar_api

**Descrição**: Envia lotes pendentes para a API de upload

**Funcionamento**:
- Busca lotes com envio_api_pendente = true
- Para cada lote, gera link de upload via API
- Salva o hash retornado
- Atualiza status e marca como enviado

**Intervalo Recomendado**: 30-60 minutos

**Arquivos Envolvidos**:
- `api_upload_client.py`

## ⚙️ Configuração Avançada

### Alterar Fuso Horário

Edite `scheduler_service.py`:

```python
scheduler = BackgroundScheduler(
    daemon=True,
    timezone='America/Sao_Paulo'  # Altere aqui
)
```

### Adicionar Novo Job

1. **Crie a função executora** em `scheduler_service.py`:

```python
def executar_job_novo():
    """Executa novo job"""
    try:
        job_config = get_job_config('novo_job')
        if not job_config or not job_config['ativo']:
            logger.info("Job novo_job não está ativo")
            return
        
        logger.info("=== Iniciando job: novo_job ===")
        
        # Sua lógica aqui
        
        registrar_execucao_job('novo_job', True, "Executado com sucesso")
        logger.info("=== Job novo_job concluído ===")
        
    except Exception as e:
        logger.error(f"Erro no job novo_job: {e}", exc_info=True)
        registrar_execucao_job('novo_job', False, str(e))
```

2. **Adicione no configurador**:

```python
def configurar_jobs():
    """Configura jobs no scheduler"""
    jobs_config = get_jobs_config()
    
    for job in jobs_config:
        if not job['ativo']:
            continue
        
        if job['nome'] == 'novo_job':
            scheduler.add_job(
                executar_job_novo,
                'interval',
                minutes=job['intervalo_minutos'],
                id='novo_job',
                replace_existing=True
            )
```

3. **Insira no banco de dados**:

```sql
INSERT INTO jobs_config (nome, descricao, ativo, intervalo_minutos)
VALUES ('novo_job', 'Descrição do novo job', true, 60);
```

## 📊 Monitoramento

### Status do Serviço

```bash
./manage_scheduler.sh status
```

Saída:
```
✅ Scheduler está rodando (PID: 12345)
```

### Logs

O serviço registra todas as operações em `scheduler.log`:

```
2025-01-15 10:00:00,123 - INFO - Scheduler iniciado
2025-01-15 10:00:00,456 - INFO - 2 jobs configurados
2025-01-15 10:00:00,789 - INFO - Job consultar_notas agendado (intervalo: 60 minutos)
2025-01-15 11:00:00,123 - INFO - === Iniciando job: consultar_notas ===
2025-01-15 11:00:05,456 - INFO - Consultando 3 lotes
2025-01-15 11:00:10,789 - INFO - === Job consultar_notas concluído ===
```

### Métricas no Painel

O painel Streamlit mostra:
- ✅ Status do serviço (rodando/parado)
- ⏰ Última execução de cada job
- 📊 Total de execuções e erros
- 📈 Taxa de sucesso
- ⏭️ Próxima execução programada
- 💬 Última mensagem de status

## 🔧 Troubleshooting

### Serviço não inicia

**Sintoma**: `scheduler.pid` não é criado

**Soluções**:
1. Verifique se o ambiente virtual está ativado
2. Confirme permissões de escrita no diretório
3. Verifique logs para erros específicos
4. Teste conexão com banco de dados

```bash
# Teste direto
python scheduler_service.py

# Verifique saída de erros
```

### Jobs não executam

**Sintoma**: Serviço roda mas jobs não são acionados

**Soluções**:
1. Verifique se jobs estão ativos no banco
2. Confirme intervalos configurados
3. Recarregue configurações

```bash
# Ver status dos jobs
psql -d prestadores -c "SELECT nome, ativo, intervalo_minutos FROM jobs_config;"

# Recarregar
./manage_scheduler.sh reload
```

### Erro de conexão com banco

**Sintoma**: `OperationalError: connection failed`

**Soluções**:
1. Verifique se PostgreSQL está rodando
2. Confirme credenciais no `.env`
3. Teste conexão manual

```bash
# Testar conexão
psql -U postgres -d prestadores -c "SELECT 1;"
```

### Logs não aparecem

**Sintoma**: `scheduler.log` vazio ou inexistente

**Soluções**:
1. Verifique permissões do diretório
2. Confirme se serviço está realmente rodando
3. Teste escrita manual

```bash
# Criar log manualmente
touch scheduler.log
chmod 644 scheduler.log

# Reiniciar serviço
./manage_scheduler.sh restart
```

## 🔐 Segurança

### PID File

O arquivo `scheduler.pid` garante que apenas uma instância do serviço rode por vez:

- ✅ Criado na inicialização
- ✅ Verificado antes de novo start
- ✅ Removido no stop limpo
- ✅ Limpeza automática de PIDs órfãos

### Logs

Logs podem conter informações sensíveis:

- 🔒 Não commitar `scheduler.log` no git
- 🔒 Adicionar ao `.gitignore`
- 🔒 Rotacionar logs periodicamente
- 🔒 Limitar acesso ao arquivo

## 🚀 Deployment em Produção

### Como Serviço do Sistema (Linux)

1. **Crie arquivo de serviço** `/etc/systemd/system/scheduler.service`:

```ini
[Unit]
Description=Disparador Email Scheduler
After=network.target postgresql.service

[Service]
Type=forking
User=seu_usuario
WorkingDirectory=/caminho/para/disparador-email
ExecStart=/caminho/para/.venv/bin/python scheduler_service.py
ExecStop=/caminho/para/.venv/bin/python scheduler_service.py stop
ExecReload=/caminho/para/.venv/bin/python scheduler_service.py reload
PIDFile=/caminho/para/disparador-email/scheduler.pid
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

2. **Ative o serviço**:

```bash
sudo systemctl daemon-reload
sudo systemctl enable scheduler.service
sudo systemctl start scheduler.service
sudo systemctl status scheduler.service
```

### Como Serviço do Sistema (macOS)

1. **Crie arquivo plist** `~/Library/LaunchAgents/com.novomundo.scheduler.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.novomundo.scheduler</string>
    <key>ProgramArguments</key>
    <array>
        <string>/caminho/para/.venv/bin/python</string>
        <string>/caminho/para/scheduler_service.py</string>
    </array>
    <key>WorkingDirectory</key>
    <string>/caminho/para/disparador-email</string>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>/caminho/para/scheduler.log</string>
    <key>StandardErrorPath</key>
    <string>/caminho/para/scheduler_error.log</string>
</dict>
</plist>
```

2. **Carregue o serviço**:

```bash
launchctl load ~/Library/LaunchAgents/com.novomundo.scheduler.plist
launchctl start com.novomundo.scheduler
launchctl list | grep scheduler
```

### Variáveis de Ambiente

Certifique-se de que o arquivo `.env` está configurado:

```bash
# Database
DB_HOST=localhost
DB_PORT=5432
DB_NAME=prestadores
DB_USER=postgres
DB_PASSWORD=sua_senha

# API
API_URL=http://api.link.dev.br/dvprocessamento/
API_KEY=DV_API_2025_CTRL_NOTAS_f8e9d2c1b4a6
```

## 📚 Referências

- **APScheduler**: https://apscheduler.readthedocs.io/
- **PostgreSQL**: https://www.postgresql.org/docs/
- **Streamlit**: https://docs.streamlit.io/

## 🆘 Suporte

Para problemas ou dúvidas:

1. Verifique os logs: `./manage_scheduler.sh logs`
2. Consulte esta documentação
3. Teste conexões e permissões
4. Entre em contato com o desenvolvedor

## 📝 Changelog

### v1.0.0 (2025-01-15)

- ✨ Sistema inicial de jobs automáticos
- ✨ Painel de configuração Streamlit
- ✨ Jobs: consultar_notas, enviar_api
- ✨ Hot reload de configurações
- ✨ Logs detalhados
- ✨ Scripts de gerenciamento
