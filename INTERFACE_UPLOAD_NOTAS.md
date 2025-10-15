# 📤 Interface de Upload de Notas Fiscais

## 📋 Visão Geral

Nova seção adicionada à interface do Streamlit para monitorar e gerenciar o sistema de upload de notas fiscais dos prestadores.

## 🎯 Como Acessar

1. Faça login no sistema
2. No menu lateral, selecione: **"📤 Upload de Notas Fiscais"**

## 📊 Funcionalidades

### Tab 1: Status dos Uploads

**Estatísticas em Tempo Real:**
- 📊 Total de lotes com upload
- ⏳ Uploads pendentes
- ✅ Notas fiscais recebidas
- ⏰ Links expirados

**Filtros e Ordenação:**
- Filtrar por status: Todos, Pendente, Completo, Expirado, Falha
- Ordenar por: Mais recentes, Mais antigos, Prestador

**Informações de Cada Lote:**
- Número do lote e prestador
- Período e data de envio
- Status visual com emoji
- Link de upload (com botão copiar)
- Token de acesso

**Ações Disponíveis:**
- 🔄 **Consultar Status Agora**: Verifica na API se o arquivo foi enviado
- ⬇️ **Baixar N.F.**: Download da nota fiscal recebida
- 🔗 **Reenviar Link**: Reenviar link de upload ao prestador

**Consulta Automática:**
Quando você clica em "Consultar Status Agora":
1. Sistema consulta a API externa
2. Atualiza o status no banco de dados
3. Se o arquivo estiver disponível, faz download automaticamente
4. Salva o arquivo em `uploads/nota_fiscal_lote_{id}.pdf`
5. Atualiza a interface

### Tab 2: Histórico Completo

**Visão Geral:**
- Tabela com todos os lotes que tiveram upload
- Informações: Lote, Prestador, Período, Data, Status, N.F. Recebida
- Valores totais de cada lote

**Exportação:**
- 📊 **Exportar para Excel**: Gera relatório completo em formato Excel
- Nome do arquivo: `historico_uploads_YYYYMMDD_HHMMSS.xlsx`

### Tab 3: Configurações da API

**Status da Configuração:**
- ✅ API Configurada (verde)
- ⚠️ API Não Configurada (amarelo)

**Informações Exibidas:**
- 🔗 URL da API
- 🔑 API Key (mascarada por segurança)

**Teste de Conexão:**
- 🚀 **Testar Conexão**: Verifica se a API está acessível
- Retorna sucesso ou erro com mensagem detalhada

**Job Automático:**
- Instruções para configurar cron
- Comando para execução manual
- Logs de execução

**Documentação:**
- Links para arquivos de documentação:
  - `API_UPLOAD_NOTAS_ESPECIFICACAO.md`
  - `IMPLEMENTACAO_UPLOAD_NOTAS.md`
  - `teste_upload_api.py`
  - `job_consultar_notas.py`
- Botão para visualizar conteúdo de cada arquivo

## 🎨 Interface Visual

### Códigos de Status

| Status | Emoji | Descrição |
|--------|-------|-----------|
| `pending` | ⏳ | Aguardando upload do prestador |
| `completed` | ✅ | Nota fiscal recebida com sucesso |
| `expired` | ⏰ | Link de upload expirado (30 dias) |
| `failed` | ❌ | Falha no processo de upload |

### Cores e Métricas

- **Métricas em Cards**: Total, Pendentes, Recebidos, Expirados
- **Delta Percentual**: Mostra proporção de cada status
- **Status Visual**: Emojis e cores para identificação rápida

## 🔄 Fluxo de Uso

### 1. Após Enviar Lote de Serviços

```
Você envia lote → Link gerado automaticamente → Email enviado ao prestador
```

A interface agora mostra:
- Lote aparece na lista com status "⏳ Aguardando Upload"
- Link disponível para copiar/reenviar
- Token registrado no sistema

### 2. Consulta Manual

```
Você clica "Consultar Status Agora" → Sistema verifica API → Atualiza status
```

Se arquivo disponível:
- Status muda para "✅ Nota Fiscal Recebida"
- Arquivo é baixado automaticamente
- Botão "Baixar N.F." fica disponível

### 3. Consulta Automática (Job)

```
Job executa a cada hora → Verifica todos pendentes → Baixa automaticamente
```

Sem necessidade de intervenção manual!

## 📊 Exemplo de Uso Real

### Cenário 1: Verificar Status de um Lote Específico

1. Acesse **"📤 Upload de Notas Fiscais"**
2. Na Tab **"Status dos Uploads"**
3. Localize o lote pelo número ou prestador
4. Clique em **"Ver Detalhes"**
5. Veja link de upload e status atual
6. Clique **"Consultar Status Agora"** para atualizar

### Cenário 2: Reenviar Link ao Prestador

1. Encontre o lote na interface
2. Expanda os detalhes
3. Clique em **"📋 Copiar Link"**
4. Envie o link por WhatsApp/Email/SMS ao prestador

### Cenário 3: Gerar Relatório de Uploads

1. Vá para Tab **"Histórico Completo"**
2. Visualize todos os uploads na tabela
3. Clique em **"📊 Exportar para Excel"**
4. Baixe o relatório completo

### Cenário 4: Configurar Sistema pela Primeira Vez

1. Acesse Tab **"Configurações da API"**
2. Se aparecer aviso amarelo, configure o `.env`:
   ```bash
   UPLOAD_API_URL="https://api-externa.novomundo.com.br"
   UPLOAD_API_KEY="sua-chave-aqui"
   ```
3. Reinicie o Streamlit
4. Clique em **"Testar Conexão"**
5. Se tudo OK, sistema está pronto!

## 🚀 Vantagens da Interface

### Antes (Sem Interface)
- ❌ Precisava consultar banco de dados manualmente
- ❌ Não sabia quais uploads estavam pendentes
- ❌ Difícil reenviar links aos prestadores
- ❌ Sem visão geral do sistema

### Agora (Com Interface)
- ✅ Visão completa de todos os uploads
- ✅ Estatísticas em tempo real
- ✅ Consulta manual com um clique
- ✅ Reenvio fácil de links
- ✅ Download direto das notas fiscais
- ✅ Relatórios exportáveis
- ✅ Teste de conexão com API
- ✅ Documentação integrada

## 🔧 Recursos Técnicos

### Integração com Backend

A interface se conecta diretamente com:
- **`database.py`**: Consulta lotes e status
- **`upload_api_client.py`**: Comunica com API externa
- **`.env`**: Lê configurações da API

### Funções Utilizadas

```python
# Consultar lotes com upload
db.get_all_lotes_servico()

# Atualizar status
db.atualizar_status_upload(lote_id, novo_status)

# Salvar nota fiscal
db.salvar_nota_fiscal(lote_id, caminho_arquivo)

# Consultar API
upload_api.consultar_status(token)

# Download de arquivo
upload_api.download_arquivo(token, save_path)

# Testar conexão
upload_api.verificar_conexao()
```

## 📱 Responsividade

A interface foi desenvolvida usando Streamlit com:
- **Colunas responsivas**: Adapta-se ao tamanho da tela
- **Tabs organizadas**: Conteúdo separado logicamente
- **Expanders**: Detalhes só quando necessário
- **Métricas visuais**: Cards com informações resumidas

## 🔐 Segurança

- **API Key mascarada**: Mostra apenas 4 primeiros e 4 últimos caracteres
- **Links únicos**: Cada lote tem token exclusivo
- **Validação de arquivos**: Apenas PDFs são aceitos
- **Expiração automática**: Links expiram após 30 dias

## 📚 Documentação Relacionada

- [`API_UPLOAD_NOTAS_ESPECIFICACAO.md`](./API_UPLOAD_NOTAS_ESPECIFICACAO.md) - Especificação da API
- [`IMPLEMENTACAO_UPLOAD_NOTAS.md`](./IMPLEMENTACAO_UPLOAD_NOTAS.md) - Guia de implementação
- [`RESUMO_UPLOAD_NOTAS.txt`](./RESUMO_UPLOAD_NOTAS.txt) - Resumo executivo do sistema

## 🎯 Próximos Passos

1. **Configurar API Externa**: Aguardar implementação pelo outro desenvolvedor
2. **Adicionar .env**: Configurar URL e API Key
3. **Testar Conexão**: Usar botão de teste na interface
4. **Configurar Cron Job**: Ativar consulta automática
5. **Monitorar**: Usar interface para acompanhar uploads

## 💡 Dicas de Uso

### Performance
- Use filtros para encontrar lotes rapidamente
- Ordene por "Mais Recentes" para ver últimos envios
- Exporte relatórios periodicamente para histórico

### Troubleshooting
- Se status não atualiza, verifique conexão com API
- Se arquivo não baixa, verifique permissões da pasta `uploads/`
- Se link não funciona, verifique se não expirou (30 dias)

### Boas Práticas
- Consulte status manualmente apenas se necessário (job faz isso automaticamente)
- Mantenha a API Key segura (nunca compartilhe)
- Faça backup dos arquivos de notas fiscais periodicamente

---

## 📞 Suporte

Em caso de dúvidas ou problemas:
1. Consulte a documentação completa em `IMPLEMENTACAO_UPLOAD_NOTAS.md`
2. Verifique logs do job em `logs/consulta_notas.log`
3. Teste a API usando `python teste_upload_api.py`

**Sistema desenvolvido em:** 13 de outubro de 2025
**Versão:** 1.0
