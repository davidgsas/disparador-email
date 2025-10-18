# 🖥️ Guia de Configuração - Novo Mac

**Data:** 18 de outubro de 2025

## 📦 1. Instalar Homebrew

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Após instalação, adicione ao PATH (siga as instruções que aparecem no terminal).

---

## 🐘 2. Instalar PostgreSQL

```bash
# Instalar PostgreSQL
brew install postgresql@15

# Iniciar serviço do PostgreSQL
brew services start postgresql@15

# Adicionar ao PATH (adicione ao ~/.zshrc)
echo 'export PATH="/opt/homebrew/opt/postgresql@15/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

### Verificar instalação:

```bash
psql --version
```

---

## 🗄️ 3. Criar Banco de Dados

```bash
# Criar banco de dados
createdb email

# Verificar se foi criado
psql -l
```

---

## 🔄 4. Restaurar Backup

### Opção A: Restaurar backup mais recente (RECOMENDADO)

```bash
# Listar backups disponíveis (ordenados por data)
ls -lt backups/*.sql | head -10

# Restaurar o mais recente
psql email < backups/backup_YYYYMMDD_HHMMSS.sql
```

### Opção B: Usar script Python (depois de instalar dependências)

```bash
python backup_database.py
# Escolher opção 3 (Restaurar backup)
```

---

## 🐍 5. Instalar Python e Dependências

### Verificar Python:

```bash
python3 --version
```

### Criar ambiente virtual e instalar dependências:

```bash
# Criar ambiente virtual
python3 -m venv venv

# Ativar ambiente virtual
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
```

---

## ⚙️ 6. Configurar Variáveis de Ambiente

```bash
# Copiar arquivo de exemplo
cp .env.example .env

# Editar arquivo .env
nano .env
```

### Configurar no arquivo `.env`:

```bash
# Microsoft Azure AD (usar as mesmas credenciais antigas)
CLIENT_ID=seu-client-id
TENANT_ID=seu-tenant-id

# Banco de Dados PostgreSQL
DB_HOST="localhost"
DB_NAME="email"
DB_USER="seu-usuario-mac"  # geralmente seu username do Mac
DB_PASS=""                  # deixe vazio se não configurou senha
DB_PORT="5432"

# API de Upload de Notas Fiscais (copiar do Mac antigo)
UPLOAD_API_URL="https://api-upload.exemplo.com"
UPLOAD_API_KEY="sua-api-key"
```

**⚠️ IMPORTANTE:** Copie as credenciais do `.env` do Mac antigo!

---

## 🧪 7. Testar Aplicação

```bash
# Ativar ambiente virtual
source venv/bin/activate

# Testar conexão com banco
python -c "from database import get_db_connection; conn = get_db_connection(); print('✅ Conexão OK!'); conn.close()"

# Executar aplicação
streamlit run main.py
```

---

## 📋 8. Dependências Adicionais (se necessário)

### Para geração de PDF (weasyprint):

```bash
# Instalar dependências do sistema
brew install cairo pango gdk-pixbuf libffi
```

---

## 🔐 9. Configurar Credenciais Microsoft (se necessário)

Se precisar renovar o token de acesso:

1. Acesse o [Portal Azure](https://portal.azure.com)
2. Vá em **Azure Active Directory** > **App registrations**
3. Encontre sua aplicação
4. Copie `Client ID` e `Tenant ID` para o `.env`

---

## ⏰ 10. Configurar Backup Automático (Opcional)

```bash
# Dar permissão de execução
chmod +x backup_auto.sh

# Editar crontab
crontab -e

# Adicionar linha (backup diário às 3h)
0 3 * * * cd /Users/david/Documents/GitHub/disparador-email && ./backup_auto.sh
```

---

## 📝 Checklist de Instalação

- [ ] Homebrew instalado
- [ ] PostgreSQL instalado e rodando
- [ ] Banco `email` criado
- [ ] Backup restaurado com sucesso
- [ ] Python 3 disponível
- [ ] Ambiente virtual criado
- [ ] Dependências instaladas (`pip install -r requirements.txt`)
- [ ] Arquivo `.env` configurado com credenciais
- [ ] Teste de conexão com banco OK
- [ ] Aplicação Streamlit rodando
- [ ] (Opcional) Backup automático configurado

---

## 🆘 Problemas Comuns

### Erro: "psql: command not found"
```bash
# Adicionar PostgreSQL ao PATH
echo 'export PATH="/opt/homebrew/opt/postgresql@15/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

### Erro de conexão com banco de dados
```bash
# Verificar se PostgreSQL está rodando
brew services list

# Reiniciar se necessário
brew services restart postgresql@15
```

### Erro ao importar psycopg2
```bash
# Reinstalar com flag de compilação
pip uninstall psycopg2-binary
pip install psycopg2-binary --no-cache-dir
```

### Erro de permissão no PostgreSQL
```bash
# Criar usuário se necessário
createuser -s seu-usuario
```

---

## 📞 Próximos Passos

Após concluir a instalação:

1. ✅ Testar envio de e-mails
2. ✅ Verificar jobs automáticos
3. ✅ Testar interface web
4. ✅ Validar integração com Trello (se aplicável)
5. ✅ Fazer um backup de teste

---

**Observação:** Mantenha o Mac antigo acessível até confirmar que tudo está funcionando no novo!
