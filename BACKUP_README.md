# 🗄️ Sistema de Backup do Banco de Dados

Sistema completo para backup e restauração do banco de dados PostgreSQL.

## 📋 Funcionalidades

- ✅ Backup completo do banco de dados
- ✅ Compressão automática (formato custom do PostgreSQL)
- ✅ Rotação automática de backups (mantém os 30 mais recentes)
- ✅ Restauração de backups
- ✅ Modo interativo e automático
- ✅ Logs de execução

## 🚀 Uso Manual (Interativo)

Execute o script principal:

```bash
python backup_database.py
```

### Menu Interativo

```
1. Criar novo backup       - Faz backup imediato do banco
2. Listar backups          - Mostra todos os backups disponíveis
3. Restaurar backup        - Restaura um backup específico
4. Limpar backups antigos  - Remove backups além do limite configurado
5. Sair
```

## ⚙️ Backup Automático

### Configurar Backup Diário

Para executar backups automaticamente todos os dias às 3h da manhã:

```bash
# Dar permissão de execução
chmod +x backup_auto.sh

# Editar crontab
crontab -e

# Adicionar linha (backup diário às 3h)
0 3 * * * /Users/davidgabriel/projetos/disparador-email/backup_auto.sh
```

### Outras Frequências

```bash
# A cada 6 horas
0 */6 * * * /caminho/para/backup_auto.sh

# Toda segunda-feira às 2h
0 2 * * 1 /caminho/para/backup_auto.sh

# De hora em hora
0 * * * * /caminho/para/backup_auto.sh
```

## 🔧 Configurações

Edite as variáveis no arquivo `backup_database.py`:

```python
MAX_BACKUPS = 30  # Número de backups a manter
BACKUP_DIR = Path("backups")  # Diretório de backups
```

## 📁 Estrutura de Arquivos

```
projetos/disparador-email/
├── backup_database.py      # Script principal
├── backup_auto.sh          # Script para cron
└── backups/                # Diretório de backups
    ├── backup_email_20231013_150000.sql
    ├── backup_email_20231012_150000.sql
    └── backup.log          # Log de execuções automáticas
```

## 🔄 Restaurar Backup

### Via Menu Interativo

```bash
python backup_database.py
# Escolha opção 3
# Selecione o backup desejado
# Digite CONFIRMAR para prosseguir
```

### Via Linha de Comando

```bash
# Listar backups
ls -lh backups/

# Restaurar backup específico
pg_restore -h localhost -p 5432 -U davidgabriel -d email -c -v backups/backup_email_20231013_150000.sql
```

## ⚠️ Avisos Importantes

1. **Restauração**: Ao restaurar um backup, **TODOS** os dados atuais serão substituídos
2. **Espaço em disco**: Monitore o espaço disponível no diretório de backups
3. **Credenciais**: Certifique-se de que o arquivo `.env` está configurado corretamente
4. **Permissões**: O usuário do banco precisa ter permissões adequadas

## 🧪 Testar Backup

```bash
# 1. Criar backup de teste
python backup_database.py
# Escolha opção 1

# 2. Verificar se o arquivo foi criado
ls -lh backups/

# 3. Testar restauração (CUIDADO!)
# Use um banco de dados de teste primeiro!
```

## 📊 Monitorar Backups

```bash
# Ver últimos backups
ls -lht backups/ | head -10

# Ver log de backups automáticos
tail -f backups/backup.log

# Verificar tamanho total dos backups
du -sh backups/
```

## 🆘 Solução de Problemas

### Erro: "pg_dump: command not found"

PostgreSQL não está no PATH. Adicione ao `.bashrc` ou `.zshrc`:

```bash
export PATH="/usr/local/pgsql/bin:$PATH"
# ou
export PATH="/Applications/Postgres.app/Contents/Versions/latest/bin:$PATH"
```

### Erro: "permission denied"

```bash
# Dar permissão ao script
chmod +x backup_database.py
chmod +x backup_auto.sh
```

### Backup muito grande

Ajuste a configuração `MAX_BACKUPS` para manter menos backups:

```python
MAX_BACKUPS = 10  # Manter apenas 10 backups
```

## 💾 Backup para Nuvem (Opcional)

Para maior segurança, sincronize os backups com a nuvem:

```bash
# Exemplo com rsync para servidor remoto
rsync -avz backups/ usuario@servidor:/backup/disparador-email/

# Exemplo com rclone (Google Drive, Dropbox, etc)
rclone sync backups/ googledrive:backup/disparador-email/
```

## 📝 Logs

Os logs de execução automática ficam em:
```
backups/backup.log
```

Visualizar logs:
```bash
tail -n 50 backups/backup.log
```
