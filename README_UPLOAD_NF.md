# Sistema de Upload de Notas Fiscais

## 🎯 Funcionalidades Implementadas

✅ **Sistema de Tokens Únicos**: Cada pagamento gera um link único para upload de NF  
✅ **Página de Upload**: Interface bonita e intuitiva para upload de arquivos  
✅ **Banco de Dados Atualizado**: Tabelas para controlar tokens e uploads  
✅ **Integração com Emails**: Links automáticos nos templates de email  
✅ **Armazenamento Seguro**: Validação de arquivos e organização por prestador/montador  
✅ **Painel Administrativo**: Interface para gerenciar todos os uploads  

## 🚀 Como Usar

### 1. Configuração Inicial

Execute as migrações do banco de dados (já incluídas no sistema):
```bash
# As migrações são executadas automaticamente quando o sistema inicia
```

### 2. Executar o Sistema Principal

```bash
# Aplicativo principal (porta 8501)
streamlit run streamlit_app.py
```

### 3. Executar o Servidor de Upload

```bash
# Servidor de upload de notas fiscais (porta 8502)
./start_upload_server.sh
```

### 4. Configuração do Servidor Web

Configure seu nginx/apache para fazer proxy da URL pública:

```nginx
# Exemplo de configuração nginx
server {
    listen 443 ssl;
    server_name uploadnf.novomundo.com.br;
    
    location / {
        proxy_pass http://localhost:8502;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 📋 Fluxo de Funcionamento

1. **📧 Envio de Email**: Quando um pagamento é processado, um token único é gerado
2. **🔗 Link no Email**: O email inclui automaticamente o link para upload da NF
3. **📄 Upload da NF**: Prestador/montador acessa o link e faz upload do arquivo
4. **💾 Armazenamento**: Arquivo é salvo de forma segura e token é marcado como usado
5. **📊 Acompanhamento**: Administrador pode acompanhar todos os uploads pelo painel

## 🗂️ Estrutura de Arquivos

```
uploads/
└── notas_fiscais/
    ├── prestador/
    │   └── [ID_PRESTADOR]/
    │       └── NF_YYYYMMDD_HHMMSS_[HASH].pdf
    └── montador/
        └── [ID_MONTADOR]/
            └── NF_YYYYMMDD_HHMMSS_[HASH].pdf
```

## 🛡️ Segurança

- **Tokens únicos** com expiração de 30 dias
- **Validação de arquivos** (apenas PDF, JPG, PNG)
- **Limite de tamanho** de 10MB por arquivo
- **Uso único** de cada token
- **Armazenamento organizado** por entidade

## 📊 Painel Administrativo

Acesse a página "Gerenciar Uploads NF" no sistema principal para:

- ✅ Visualizar estatísticas de uploads
- 🔗 Ver tokens gerados e status
- 📁 Gerenciar arquivos enviados
- 🧹 Limpar tokens expirados
- 📊 Gerar relatórios CSV

## 🔧 Configurações

### Variáveis de Ambiente Necessárias

As mesmas variáveis do sistema principal (banco de dados PostgreSQL).

### URL Base do Servidor de Upload

Por padrão configurada como: `https://uploadnf.novomundo.com.br`

Pode ser alterada no painel administrativo ou diretamente no código.

## 📱 Templates de Email Atualizados

Os templates foram automaticamente atualizados para incluir:

- 🎨 Seção visual destacada para upload de NF
- 🔗 Botão chamativo para acesso ao upload
- ℹ️ Informações sobre validade e formatos aceitos

## 🆘 Suporte

Em caso de problemas:

1. Verifique se o servidor de upload está rodando na porta 8502
2. Confirme se o proxy está configurado corretamente
3. Verifique se as permissões de escrita estão corretas na pasta uploads/
4. Consulte os logs do Streamlit para erros específicos

## 🎉 Benefícios

- ✨ **Experiência melhorada** para prestadores e montadores
- 🎯 **Controle centralizado** de todas as notas fiscais
- 📈 **Rastreabilidade completa** do processo de upload
- ⚡ **Automação total** - nenhuma configuração manual necessária
- 🔒 **Segurança aprimorada** com tokens únicos e validações

---

**Sistema desenvolvido para otimizar o processo de coleta de notas fiscais de prestadores e montadores.**
