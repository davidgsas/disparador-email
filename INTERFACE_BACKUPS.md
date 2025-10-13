# 🗄️ Interface de Backups no Sistema

## 📋 Visão Geral

Uma interface completa foi adicionada ao sistema Streamlit para gerenciar backups do banco de dados PostgreSQL de forma visual e intuitiva.

## 🎯 Acesso

1. Inicie o sistema: `streamlit run streamlit_app.py`
2. No menu lateral, selecione: **🗄️ Backups do Banco**

## 📑 Funcionalidades

### 1️⃣ Listar Backups

**Visualização Completa:**
- Lista todos os backups disponíveis
- Informações detalhadas: Nome, Data/Hora, Tamanho
- Ordenados do mais recente para o mais antigo

**Ações Disponíveis:**
- ⬇️ **Download Backup** - Baixar backup para seu computador
- ℹ️ **Ver Detalhes** - Informações completas do backup
- 🗑️ **Excluir Backup** - Remover backup (com confirmação)

### 2️⃣ Criar Backup

**Criação com Um Clique:**
- Botão "🚀 Criar Backup Agora"
- Processo automático usando `pg_dump`
- Feedback em tempo real
- Confirmação com tamanho do arquivo

**Informações Exibidas:**
- Nome do arquivo gerado
- Tamanho do backup (MB)
- Localização completa

**Backup Manual:**
- Comandos para terminal incluídos
- Scripts rápidos disponíveis

### 3️⃣ Configurações

**Política de Backups:**
- Máximo de 30 backups mantidos
- Recomendações de frequência:
  - Diário para produção
  - A cada 6 horas para dados críticos
  - Semanal para testes

**Backup Automático:**
- Instruções para configurar crontab
- Exemplos de diferentes frequências
- Scripts prontos para uso

**Estatísticas:**
- Total de backups
- Espaço utilizado (MB)
- Tamanho médio
- Backup mais antigo
- Backup mais recente

**Manutenção:**
- Limpar backups antigos
- Configurar limite de retenção
- Informações sobre restauração

## 🎨 Interface

### Tab 1: 📋 Listar Backups

```
┌─────────────────────────────────────────────────────────────┐
│  📋 Backups Disponíveis                                      │
│                                                              │
│  ✅ 5 backup(s) disponível(eis)                             │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ Arquivo              │ Data/Hora        │ Tamanho(MB)│   │
│  ├──────────────────────────────────────────────────────┤   │
│  │ backup_email_...sql  │ 13/10/2025 12:00 │ 0.02      │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
│  🔧 Ações nos Backups                                        │
│  Selecione um backup: [dropdown]                             │
│                                                              │
│  [⬇️ Download] [ℹ️ Ver Detalhes] [🗑️ Excluir]              │
└─────────────────────────────────────────────────────────────┘
```

### Tab 2: ➕ Criar Backup

```
┌─────────────────────────────────────────────────────────────┐
│  ➕ Criar Novo Backup                                        │
│                                                              │
│  💡 Sobre os Backups                                         │
│  - Formato PostgreSQL Custom (comprimido)                   │
│  - Incluem todas as tabelas e dados                         │
│  - Podem ser restaurados via pg_restore                     │
│                                                              │
│  [🚀 Criar Backup Agora]                                     │
│                                                              │
│  ─────────────────────────────────────────────────────────  │
│                                                              │
│  📝 Backup via Terminal                                      │
│  python backup_database.py --auto                           │
└─────────────────────────────────────────────────────────────┘
```

### Tab 3: ⚙️ Configurações

```
┌─────────────────────────────────────────────────────────────┐
│  ⚙️ Configurações de Backup                                  │
│                                                              │
│  📊 Política de Backups                                      │
│  - Máximo: 30 backups                                       │
│  - Automático: Remove mais antigos                          │
│                                                              │
│  🤖 Backup Automático                                        │
│  Configurar crontab:                                        │
│  0 3 * * * /caminho/backup_auto.sh                          │
│                                                              │
│  📈 Estatísticas                                             │
│  ┌─────────┬─────────────┬──────────────┐                   │
│  │ Total   │ Espaço (MB) │ Tamanho Médio│                   │
│  │   5     │    0.10     │    0.02      │                   │
│  └─────────┴─────────────┴──────────────┘                   │
│                                                              │
│  🧹 Manutenção                                               │
│  Máximo: [30] backups                                       │
│  [🧹 Limpar Backups Antigos]                                │
│                                                              │
│  ♻️ Como Restaurar um Backup                                 │
│  python backup_database.py (opção 3)                        │
└─────────────────────────────────────────────────────────────┘
```

## 🔧 Funcionalidades Detalhadas

### Download de Backup
- Baixa o arquivo .sql para seu computador
- Mantém nome original do arquivo
- Formato compatível com pg_restore

### Ver Detalhes
Mostra:
- Nome completo do arquivo
- Caminho no sistema
- Tamanho exato em MB
- Data e hora de criação
- Formato do backup

### Excluir Backup
- Confirmação obrigatória
- Botões claros (Sim/Cancelar)
- Feedback visual
- Atualização automática da lista

### Criar Backup
- Usa `pg_dump` automaticamente
- Formato custom comprimido
- Nome com timestamp
- Validação de sucesso/erro
- Mostra tamanho do arquivo criado

### Limpar Backups Antigos
- Define limite personalizável
- Remove apenas os mais antigos
- Mantém os N mais recentes
- Confirmação do número removido

## 📊 Estatísticas Disponíveis

1. **Total de Backups** - Quantidade total de arquivos
2. **Espaço Utilizado** - Soma de todos os backups (MB)
3. **Tamanho Médio** - Média de tamanho por backup
4. **Mais Antigo** - Nome e data do backup mais antigo
5. **Mais Recente** - Nome e data do backup mais recente

## ⚙️ Configurações Recomendadas

### Produção
```bash
# Backup diário às 3h da manhã
0 3 * * * /caminho/backup_auto.sh
```

### Dados Críticos
```bash
# Backup a cada 6 horas
0 */6 * * * /caminho/backup_auto.sh
```

### Desenvolvimento
```bash
# Backup semanal (segunda às 2h)
0 2 * * 1 /caminho/backup_auto.sh
```

## 🔐 Segurança

- Backups em formato comprimido
- Credenciais lidas do `.env`
- Confirmação para ações destrutivas
- Logs de operações
- Validação de comandos

## 📱 Responsividade

- Interface adaptável
- Funciona em diferentes resoluções
- Tabs para organização
- Colunas responsivas

## 🎯 Benefícios

1. **Visual** - Interface gráfica intuitiva
2. **Rápido** - Backup com um clique
3. **Seguro** - Confirmações e validações
4. **Completo** - Todas as funcionalidades em um lugar
5. **Informativo** - Estatísticas e detalhes
6. **Prático** - Download e exclusão fáceis

## 🚀 Como Usar

### Criar Backup Rápido
1. Acesse **🗄️ Backups do Banco**
2. Vá para aba **➕ Criar Backup**
3. Clique em **🚀 Criar Backup Agora**
4. Aguarde confirmação

### Download de Backup
1. Acesse **🗄️ Backups do Banco**
2. Aba **📋 Listar Backups**
3. Selecione o backup desejado
4. Clique em **⬇️ Download Backup**

### Limpar Espaço
1. Acesse **🗄️ Backups do Banco**
2. Aba **⚙️ Configurações**
3. Seção **🧹 Manutenção**
4. Configure limite e clique em **Limpar**

## 📝 Notas Importantes

- ⚠️ Backups grandes podem demorar alguns segundos
- 🔄 A interface atualiza automaticamente após ações
- 💾 Backups são salvos em `backups/`
- 🗑️ Exclusão é permanente (sem lixeira)
- ♻️ Restauração deve ser feita com cuidado

---

**Versão**: 3.0.0  
**Data**: 13 de outubro de 2025  
**Status**: ✅ Implementado e Testado
