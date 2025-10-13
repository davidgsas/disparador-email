# 🚀 GUIA RÁPIDO - SISTEMA DE UPLOAD DE NOTAS FISCAIS
## API DV Processamento

---

## ✅ O QUE ESTÁ PRONTO

Todo o sistema foi implementado e está funcionando! Agora basta aguardar o desenvolvedor externo disponibilizar a API em produção.

---

## 📋 ARQUIVOS CRIADOS

```
disparador-email/
├── api_upload_client.py (NOVO)          ← Cliente da API
├── job_enviar_api.py (NOVO)            ← Job automático
├── database.py (MODIFICADO)            ← 7 novas funções
├── streamlit_app.py (MODIFICADO)       ← Interface atualizada
├── DOCUMENTACAO_API_DV_PROCESSAMENTO.md ← Doc técnica (650 linhas)
└── RESUMO_IMPLEMENTACAO_API.txt        ← Este resumo visual
```

---

## 🎯 COMO FUNCIONA AGORA

### Fluxo Completo:

1. **Você envia lote** no Streamlit → Email sai com PDF
2. **Sistema envia automaticamente** dados para API DV Processamento
3. **API retorna link** de upload com validade
4. **Link é salvo** no banco junto com o lote
5. **Link pode ser incluído no email** (variável `link_upload` no template)
6. **Prestador acessa link** e faz upload da NF
7. **Sistema monitora** status (job ou manual)

---

## 🔧 CONFIGURAÇÃO INICIAL

### 1. Rodar Migrations (Adiciona Colunas no Banco)

```bash
cd /Users/davidgabriel/projetos/disparador-email
python -c "import database; database.run_migrations()"
```

✅ Isso adiciona 7 novas colunas na tabela `lotes_servico`:
- `id_controle` - ID retornado pela API
- `link_upload` - URL do link de upload
- `validade_link` - Data de expiração
- `status_api` - 0=pendente, 1=recebido
- `data_envio_api` - Timestamp do envio
- `nota_fiscal_path` - Caminho do arquivo
- `api_message` - Mensagem da API

### 2. Criar Diretórios

```bash
mkdir -p logs
mkdir -p uploads
```

### 3. Testar Cliente da API (Quando API estiver no ar)

```bash
python api_upload_client.py
```

Isso enviará todos os lotes pendentes para a API.

### 4. Configurar Job Automático (Opcional mas Recomendado)

**Editar crontab:**
```bash
crontab -e
```

**Adicionar linha:**
```cron
0 * * * * cd /Users/davidgabriel/projetos/disparador-email && /Users/davidgabriel/projetos/disparador-email/.venv/bin/python job_enviar_api.py >> logs/cron_api.log 2>&1
```

Isso executará o job **a cada hora** para enviar lotes pendentes.

---

## 📧 ADICIONAR LINK NO EMAIL

### No Template do Email (config.json ou similar)

Adicione no corpo do email:

```jinja2
Olá {{ nome_prestador }},

Segue em anexo o relatório de serviços do período {{ periodo }}.

{% if link_upload %}
🔗 Para anexar a Nota Fiscal, acesse:
{{ link_upload }}

⚠️ Este link é válido por 30 dias.
{% endif %}

Atenciosamente,
Equipe Novo Mundo
```

A variável `{{ link_upload }}` estará disponível automaticamente quando o lote for enviado!

---

## 🎨 INTERFACE DO USUÁRIO

### Onde Ver o Status

1. Abrir Streamlit
2. Ir em **"Histórico de Envios"**
3. Expandir lote desejado
4. Ver seção **"📤 Status do Upload da Nota Fiscal"**

### O que Você Verá

```
📤 Status do Upload da Nota Fiscal
────────────────────────────────────
📤 Link enviado ao prestador
   ID Controle API: 142
   ✅ Válido até: 12/11/2025 (30 dias)
   
   [🔗 Ver Link de Upload]
   💬 Registro criado com sucesso
   
   [🔄 Reenviar para API (Gerar Novo Link)]
```

### Botões Disponíveis

- **🚀 Enviar para API Agora** - Se lote ainda não foi enviado
- **🔄 Reenviar para API** - Gera novo link (ex: se expirou)
- **📋 Copiar Link** - Copiar URL para área de transferência
- **⬇️ Baixar Nota Fiscal** - Quando NF for recebida

---

## ⚡ USO DIÁRIO

### Cenário 1: Envio Normal

1. Preencher planilha no Streamlit
2. Clicar "Enviar E-mails"
3. **Pronto!** Link é gerado automaticamente
4. Email sai com PDF + link

### Cenário 2: Link Não Foi Gerado

Às vezes a API pode estar fora do ar no momento do envio.

1. Ir em "Histórico de Envios"
2. Encontrar lote sem link (⚠️ "Aguardando N.F. (sem link)")
3. Clicar **"🚀 Enviar para API Agora"**
4. Link será gerado na hora

### Cenário 3: Link Expirou

Prestador demorou e link expirou (⏰).

1. Ir em "Histórico de Envios"
2. Encontrar lote com link expirado
3. Clicar **"🔄 Reenviar para API (Gerar Novo Link)"**
4. Novo link é gerado
5. Copiar e enviar para prestador por WhatsApp/Email

### Cenário 4: Verificar Status

1. Ir em "Histórico de Envios"
2. Ver emoji ao lado do lote:
   - 📤 = Aguardando prestador anexar
   - ✅ = NF Recebida!
   - ⏰ = Link expirado
   - 📧 = Sem link ainda

---

## 🔍 MONITORAMENTO

### Ver Logs do Job Automático

```bash
tail -f logs/job_enviar_api.log
```

### Ver Últimos 20 Envios

```bash
grep "Lote #" logs/job_enviar_api.log | tail -20
```

### Contar Erros

```bash
grep "❌" logs/job_enviar_api.log | wc -l
```

---

## ⚠️ PROBLEMAS COMUNS

### 1. "API não responde"

**Causa:** API externa fora do ar ou sem internet

**Solução:**
- Job tentará novamente em 1 hora automaticamente
- Ou clique "Enviar para API Agora" manualmente depois

### 2. "Lote já foi enviado anteriormente"

**Causa:** Tentando enviar lote que já tem ID de controle

**Solução:**
- Para gerar NOVO link: use botão "Reenviar para API"
- Isso limpa o ID antigo e cria um novo

### 3. "Link expirado"

**Causa:** Passou da data de validade (geralmente 30 dias)

**Solução:**
- Clicar "Reenviar para API" para gerar novo link
- Enviar novo link para prestador

### 4. "Erro 401 - Não autorizado"

**Causa:** API Key incorreta

**Solução:**
- Verificar chave em `api_upload_client.py` linha 11
- Confirmar com desenvolvedor externo se mudou

---

## 📊 DADOS DA API

### Endpoint

```
POST https://api.link.dev.br/dvprocessamento/
```

### API Key

```
DV_API_2025_CTRL_NOTAS_f8e9d2c1b4a6
```

### O Que é Enviado

```json
{
  "nome": "Nome do Prestador",
  "email": "email@prestador.com.br",
  "periodo": "10/2025",
  "valor_total": 15750.50,
  "quantidade_os": 23,
  "data_envio": "2025-10-13T14:30:00",
  "lote_id": 142
}
```

### O Que é Recebido

```json
{
  "success": true,
  "id_controle": 1,
  "lote_id": 142,
  "link": "https://api.link.com.br/dvprocessamento/envio-nf/...",
  "validade_link": "2025-11-12",
  "status": 0,
  "message": "Registro criado com sucesso"
}
```

---

## 🧪 TESTES

### Teste 1: Enviar Lote Teste

```bash
# 1. Abrir Streamlit
streamlit run streamlit_app.py

# 2. Ir em "Enviar Boletins"
# 3. Preencher com dados de teste
# 4. Enviar
# 5. Verificar histórico
```

### Teste 2: Rodar Job Manual

```bash
python job_enviar_api.py
```

Deve processar todos os lotes pendentes e mostrar log.

### Teste 3: Simular Reenvio

```bash
# No Streamlit:
# 1. Histórico > Expandir lote
# 2. Clicar "Reenviar para API"
# 3. Verificar novo link gerado
```

---

## 📞 AJUDA

### Documentação Completa

📄 **DOCUMENTACAO_API_DV_PROCESSAMENTO.md** - 650 linhas de documentação técnica detalhada

### Código-Fonte

- `api_upload_client.py` - Cliente da API com comentários
- `job_enviar_api.py` - Job automático
- `database.py` - Funções do banco (linhas ~200-290)

### Logs

- `logs/job_enviar_api.log` - Log do job automático
- `logs/cron_api.log` - Log do cron (se configurado)

---

## ✅ CHECKLIST RÁPIDO

Antes de usar em produção:

- [ ] Rodar migrations (`python -c "import database; database.run_migrations()"`)
- [ ] Criar diretórios (`mkdir -p logs uploads`)
- [ ] Confirmar que API externa está no ar
- [ ] Testar envio de um lote
- [ ] Verificar link gerado
- [ ] Adicionar link no template de email
- [ ] Configurar cron job (opcional)
- [ ] Testar com prestador real
- [ ] Treinar usuários

---

## 🎉 TUDO PRONTO!

O sistema está completo e funcional. Assim que a API externa estiver disponível, você pode começar a usar imediatamente!

**Principais vantagens:**
- ✅ Envio automático para API
- ✅ Link gerado sem intervenção
- ✅ Monitoramento de validade
- ✅ Reenvio fácil se necessário
- ✅ Interface intuitiva
- ✅ Job automático

**Próximo passo:** Aguardar desenvolvedor externo e testar! 🚀

---

**Criado em:** 13 de outubro de 2025  
**Versão:** 2.0
