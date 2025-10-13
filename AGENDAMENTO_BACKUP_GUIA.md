# 🤖 Sistema de Agendamento Automático de Backups

## 📋 Visão Geral

Sistema integrado à interface Streamlit que permite configurar backups automáticos do banco de dados através de uma interface gráfica amigável, sem necessidade de editar o crontab manualmente.

## ✨ Funcionalidades

### 1️⃣ Interface Gráfica
- ✅ Configuração via interface web
- ✅ Opções pré-definidas de agendamento
- ✅ Editor de expressões cron personalizadas
- ✅ Visualização do agendamento atual
- ✅ Remoção de agendamentos com um clique

### 2️⃣ Opções de Agendamento

#### Pré-definidas:
- 🌅 **Diário às 3h da manhã** - `0 3 * * *`
- ⏰ **A cada 6 horas** - `0 */6 * * *`
- 🕐 **A cada 12 horas** - `0 */12 * * *`
- 📅 **Toda segunda-feira às 2h** - `0 2 * * 1`
- 🌙 **Todo domingo às 23h** - `0 23 * * 0`
- ⚡ **De hora em hora** - `0 * * * *`

#### Personalizado:
- Permite criar expressões cron customizadas
- Validação e descrição em tempo real
- Guia completo de sintaxe disponível

## 🎯 Como Usar

### Acesso
1. Abra o sistema: `streamlit run streamlit_app.py`
2. Navegue até: **🗄️ Backups do Banco**
3. Selecione a aba: **⚙️ Configurações**
4. Encontre a seção: **🤖 Agendamento Automático de Backup**

### Configurar Novo Agendamento

#### Opção 1: Usar Pré-definição
```
1. Em "Escolha a frequência", selecione uma opção
2. Revise a descrição apresentada
3. Clique em "💾 Salvar Agendamento"
4. Aguarde confirmação
```

#### Opção 2: Criar Expressão Personalizada
```
1. Selecione "Personalizado"
2. Digite a expressão cron desejada
3. Verifique a sintaxe no guia
4. Clique em "💾 Salvar Agendamento"
```

### Verificar Agendamento Atual
- O sistema mostra automaticamente se há backup agendado
- Exibe a expressão cron configurada
- Mostra descrição em linguagem natural

### Remover Agendamento
```
1. Na seção de agendamento ativo
2. Clique em "🗑️ Remover Agendamento"
3. Aguarde confirmação
```

## 📖 Guia de Expressões Cron

### Formato
```
minuto hora dia mês dia_da_semana
```

### Campos
- **Minuto**: 0-59
- **Hora**: 0-23
- **Dia do mês**: 1-31
- **Mês**: 1-12
- **Dia da semana**: 0-6 (0 = Domingo)

### Caracteres Especiais
- `*` - Qualquer valor
- `/` - Incremento (ex: */6 = a cada 6)
- `,` - Lista (ex: 1,3,5)
- `-` - Intervalo (ex: 1-5)

### Exemplos Práticos

```bash
# Todo dia às 3:00
0 3 * * *

# A cada 2 horas no minuto 30
30 */2 * * *

# De hora em hora, das 9h às 17h, segunda a sexta
0 9-17 * * 1-5

# Todo dia 1º e 15 do mês às 2h
0 2 1,15 * *

# Toda segunda, quarta e sexta às 8h
0 8 * * 1,3,5

# Último dia útil do mês
0 0 28-31 * *
```

## 🔧 Arquivos do Sistema

### `backup_scheduler.py`
Gerenciador de agendamento que interage com o crontab:

**Métodos principais:**
- `get_current_schedule()` - Obtém agendamento atual
- `set_schedule(cron, script)` - Define novo agendamento
- `remove_schedule()` - Remove agendamento
- `get_schedule_description(cron)` - Converte cron em descrição

### `backup_auto.sh`
Script executado pelo cron:
```bash
#!/bin/bash
cd "$(dirname "$0")"
source .venv/bin/activate
python3 backup_database.py --auto
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Backup executado" >> backups/backup.log
```

### `backup_schedule.conf`
Arquivo de configuração que armazena o agendamento atual.

## 🔍 Verificação e Monitoramento

### Ver Agendamentos Ativos
```bash
# Listar todos os crons do usuário
crontab -l

# Ver apenas o backup
crontab -l | grep "Backup Disparador Email"
```

### Monitorar Execuções
```bash
# Ver log de backups automáticos
tail -f backups/backup.log

# Ver últimas 20 linhas
tail -n 20 backups/backup.log
```

### Verificar Último Backup
```bash
# Listar backups por data
ls -lht backups/backup_*.sql | head -5
```

## ⚠️ Requisitos e Permissões

### Sistema Operacional
- ✅ macOS (testado)
- ✅ Linux
- ❌ Windows (requer WSL ou alternativa)

### Permissões Necessárias
```bash
# Script deve ser executável
chmod +x backup_auto.sh

# Usuário deve ter acesso ao crontab
crontab -l  # Deve funcionar sem erros
```

### Dependências
- PostgreSQL (`pg_dump` disponível no PATH)
- Python 3.9+ com ambiente virtual
- Permissões de escrita no diretório `backups/`

## 🆘 Solução de Problemas

### Erro: "Módulo de agendamento não disponível"
```bash
# Verificar se o arquivo existe
ls -l backup_scheduler.py

# Se não existir, criar novamente
# (o arquivo foi criado automaticamente)
```

### Erro: "Script backup_auto.sh não encontrado"
```bash
# Verificar se existe
ls -l backup_auto.sh

# Dar permissão de execução
chmod +x backup_auto.sh
```

### Agendamento não está executando
```bash
# 1. Verificar se o cron está no crontab
crontab -l

# 2. Verificar log do sistema
tail -f backups/backup.log

# 3. Testar script manualmente
./backup_auto.sh

# 4. Verificar serviço cron (Linux)
sudo systemctl status cron

# 5. Verificar serviço cron (macOS)
# O cron roda automaticamente
```

### Backup executado mas sem resultado
```bash
# Verificar permissões do diretório
ls -ld backups/

# Verificar espaço em disco
df -h

# Testar comando pg_dump manualmente
pg_dump -h localhost -U davidgabriel -d email -F c -f teste.sql
```

## 📊 Boas Práticas

### Frequência Recomendada por Ambiente

**Produção:**
- Mínimo: Diário às 3h
- Recomendado: A cada 6 horas
- Crítico: A cada 2-3 horas

**Desenvolvimento:**
- Semanal ou manual

**Staging/Teste:**
- Diário ou a cada 12 horas

### Retenção de Backups
- Mínimo: 7 dias
- Recomendado: 30 dias
- Máximo (disco): Ajustar conforme espaço

### Backup Adicional (Nuvem)
```bash
# Sincronizar backups com nuvem (exemplo)
# Adicionar ao backup_auto.sh:

# AWS S3
aws s3 sync backups/ s3://seu-bucket/backups/

# Google Drive (rclone)
rclone sync backups/ gdrive:backups/

# Rsync para servidor remoto
rsync -avz backups/ user@server:/backup/
```

## 🎓 Exemplos de Uso

### Cenário 1: Loja Online (Dados Críticos)
```
Agendamento: A cada 4 horas
Expressão: 0 */4 * * *
Retenção: 30 backups (5 dias de histórico)
```

### Cenário 2: Sistema Interno (Uso Comercial)
```
Agendamento: Diário às 2h da manhã
Expressão: 0 2 * * *
Retenção: 30 backups (1 mês de histórico)
```

### Cenário 3: Projeto Pessoal
```
Agendamento: Semanal aos domingos
Expressão: 0 3 * * 0
Retenção: 10 backups (2,5 meses de histórico)
```

## 📝 Logs e Auditoria

### Formato do Log
```
[2025-10-13 03:00:01] Executando backup automático...
🔄 Iniciando backup do banco 'email'...
✅ Backup concluído com sucesso!
📁 Arquivo: backups/backup_email_20251013_030001.sql
📊 Tamanho: 0.05 MB
```

### Análise de Logs
```bash
# Contar backups bem-sucedidos
grep -c "Backup concluído com sucesso" backups/backup.log

# Ver backups com erros
grep "Erro" backups/backup.log

# Verificar última execução
tail -n 5 backups/backup.log
```

---

**Versão**: 1.0.0  
**Data**: 13 de outubro de 2025  
**Autor**: Sistema Disparador Email
