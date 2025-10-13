# 🚀 Sistema de Upload de Notas Fiscais - Guia de Implementação

## 📋 Visão Geral

Sistema completo para gerenciamento de upload de notas fiscais através de API externa. O prestador recebe um link único por email e faz o upload da nota fiscal em um sistema externo.

## 🎯 Arquivos Criados

### 1. `API_UPLOAD_NOTAS_ESPECIFICACAO.md`
**Especificação completa para o desenvolvedor do sistema externo**

Contém:
- Endpoints necessários (criar link, consultar status, download)
- Estrutura de dados (requests/responses)
- Exemplos de requisições
- Estrutura de banco de dados sugerida
- Interface web de upload
- Políticas de segurança e expiração

### 2. `upload_api_client.py`
**Cliente Python para integração com a API**

Funções principais:
- `criar_link_upload()` - Cria link único para upload
- `consultar_status()` - Verifica se nota fiscal foi enviada
- `download_arquivo()` - Baixa o arquivo recebido
- `verificar_conexao()` - Testa conectividade

### 3. Modificações em `database.py`
**Novas colunas e funções para gerenciar uploads**

Colunas adicionadas em `lotes_servico`:
- `upload_token` - Token único do upload
- `upload_url` - URL completa para o prestador acessar
- `upload_status` - Status (pending/completed/expired)
- `nota_fiscal_path` - Caminho do arquivo recebido

Funções adicionadas:
- `atualizar_lote_com_upload_info()`
- `atualizar_status_upload()`
- `salvar_nota_fiscal()`
- `get_lotes_upload_pendente()`
- `get_lote_by_upload_token()`

### 4. `.env.example`
**Template de configuração**

Novas variáveis:
```env
UPLOAD_API_URL="https://api-upload.exemplo.com"
UPLOAD_API_KEY="sua-api-key-aqui"
```

### 5. `teste_upload_api.py`
**Script de teste e demonstração**

Testa todo o fluxo:
- Conectividade com API
- Criação de link
- Consulta de status
- Download de arquivo

## 🔄 Fluxo Completo

```
┌─────────────────────────────────────────────────────────────────┐
│ 1. CRIAÇÃO DO LOTE                                              │
├─────────────────────────────────────────────────────────────────┤
│ Sistema Disparador cria lote de serviço com as OS              │
│ ↓                                                                │
│ Chama: criar_lote_servico()                                     │
│ Retorna: lote_id                                                │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ 2. CRIAÇÃO DO LINK DE UPLOAD                                    │
├─────────────────────────────────────────────────────────────────┤
│ Sistema chama API externa para criar link único                │
│ ↓                                                                │
│ upload_api.criar_link_upload(lote_id, prestador, lote_info)    │
│ API retorna: {token, upload_url, expires_at}                   │
│ ↓                                                                │
│ Salva no banco: atualizar_lote_com_upload_info()               │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ 3. ENVIO DO EMAIL                                               │
├─────────────────────────────────────────────────────────────────┤
│ Email inclui:                                                    │
│ - Relatório PDF (como anexo)                                    │
│ - Link para upload da nota fiscal                               │
│ - Instruções                                                     │
│ ↓                                                                │
│ Prestador recebe email com link                                 │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ 4. PRESTADOR FAZ UPLOAD                                         │
├─────────────────────────────────────────────────────────────────┤
│ Prestador clica no link                                         │
│ ↓                                                                │
│ Abre página no sistema externo                                  │
│ ↓                                                                │
│ Página mostra dados do lote (prestador, período, valor)        │
│ ↓                                                                │
│ Prestador seleciona arquivo PDF e envia                        │
│ ↓                                                                │
│ Sistema externo valida e armazena arquivo                       │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ 5. CONSULTA AUTOMÁTICA (JOB)                                    │
├─────────────────────────────────────────────────────────────────┤
│ Job roda periodicamente (ex: a cada hora)                       │
│ ↓                                                                │
│ get_lotes_upload_pendente() - busca lotes aguardando           │
│ ↓                                                                │
│ Para cada lote:                                                 │
│   upload_api.consultar_status(token)                           │
│   ↓                                                              │
│   Se file_available = true:                                     │
│     upload_api.download_arquivo(token, save_path)              │
│     salvar_nota_fiscal(lote_id, file_path)                     │
│     atualizar_status_upload(lote_id, 'completed')              │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ 6. ARQUIVO RECEBIDO                                             │
├─────────────────────────────────────────────────────────────────┤
│ Sistema marca lote como "N.F. RECEBIDA"                        │
│ Arquivo salvo em: uploads/nota_fiscal_lote_{id}.pdf            │
│ Status do lote atualizado no histórico                         │
└─────────────────────────────────────────────────────────────────┘
```

## 💻 Integração no Código Existente

### Modificar `streamlit_app.py` - Envio de Emails

Adicionar após criar o lote:

```python
# Após: lote_id = db.criar_lote_servico(...)

# Criar link de upload
from upload_api_client import upload_api

prestador_data = {
    'id': prestador_info['id'],
    'nome': prestador_info['nome'],
    'email': prestador_info['email']
}

lote_data = {
    'periodo': periodo,
    'valor_total': total_geral,
    'quantidade_os': len(items_raw),
    'data_envio': datetime.datetime.now().isoformat()
}

success, result = upload_api.criar_link_upload(lote_id, prestador_data, lote_data)

if success:
    # Salvar informações do upload
    db.atualizar_lote_com_upload_info(
        lote_id, 
        result['token'], 
        result['upload_url']
    )
    
    # Adicionar link no email
    upload_link = result['upload_url']
else:
    st.warning(f"Não foi possível criar link de upload: {result}")
    upload_link = None
```

### Atualizar Template do Email

Adicionar no `email_template.html` ou no corpo do email:

```html
<p><strong>📤 Upload de Nota Fiscal:</strong></p>
<p>
    Para enviar a nota fiscal referente a este lote, 
    <a href="{{ upload_link }}" target="_blank">clique aqui</a>.
</p>
<p>
    <small>Este link é válido por 30 dias.</small>
</p>
```

No código Python:

```python
body_html = body_template.render(
    nome_prestador=nome_prestador,
    periodo=periodo,
    upload_link=upload_link,  # ← ADICIONAR AQUI
    # ... outros campos
)
```

### Criar Job de Consulta Automática

Criar arquivo `job_consultar_notas.py`:

```python
"""
Job para consultar status de uploads de notas fiscais
Executar periodicamente via cron
"""

import database as db
from upload_api_client import upload_api
from pathlib import Path
import time

def processar_uploads_pendentes():
    print("🔍 Consultando uploads pendentes...")
    
    lotes = db.get_lotes_upload_pendente()
    print(f"📋 {len(lotes)} lote(s) aguardando nota fiscal")
    
    for lote in lotes:
        lote_id = lote['id']
        token = lote['upload_token']
        
        print(f"\n   Consultando lote #{lote_id}...")
        
        # Consultar status
        success, result = upload_api.consultar_status(token)
        
        if not success:
            print(f"   ❌ Erro: {result}")
            continue
        
        status = result.get('status')
        
        if status == 'completed' and result.get('file_available'):
            print(f"   ✅ Arquivo disponível!")
            
            # Download
            save_path = f"uploads/nota_fiscal_lote_{lote_id}.pdf"
            success_download, message = upload_api.download_arquivo(token, save_path)
            
            if success_download:
                print(f"   💾 {message}")
                
                # Salvar no banco
                db.salvar_nota_fiscal(lote_id, save_path)
                print(f"   ✅ Lote #{lote_id} atualizado")
            else:
                print(f"   ❌ Erro no download: {message}")
        
        elif status == 'expired':
            print(f"   ⏰ Link expirado")
            db.atualizar_status_upload(lote_id, 'expired')
        
        else:
            print(f"   ⏳ Aguardando upload")
        
        time.sleep(1)  # Evitar sobrecarga
    
    print("\n✅ Processamento concluído")

if __name__ == "__main__":
    processar_uploads_pendentes()
```

Adicionar ao crontab:

```bash
# Executar a cada hora
0 * * * * cd /caminho/projeto && source .venv/bin/activate && python job_consultar_notas.py >> logs/consulta_notas.log 2>&1
```

## 🧪 Testando o Sistema

### 1. Executar Migrações do Banco

```bash
python -c "import database as db; print('Migrações executadas!')"
```

### 2. Rodar Teste da API

```bash
python teste_upload_api.py
```

### 3. Configurar Variáveis de Ambiente

Editar `.env`:

```env
UPLOAD_API_URL="https://api-upload.novomundo.com.br"
UPLOAD_API_KEY="chave-fornecida-pelo-outro-dev"
```

### 4. Testar Integração Real

Quando a API externa estiver pronta:

```python
from upload_api_client import upload_api

# Teste de conectividade
if upload_api.verificar_conexao():
    print("✅ API está online!")

# Teste de criação de link
success, result = upload_api.criar_link_upload(
    lote_id=1,
    prestador_info={'id': 1, 'nome': 'Teste', 'email': 'teste@teste.com'},
    lote_info={'periodo': '10/2025', 'valor_total': 100, 'quantidade_os': 1}
)

if success:
    print(f"Link criado: {result['upload_url']}")
```

## 📦 Entrega para Outro Desenvolvedor

### Arquivos para Enviar:

1. **API_UPLOAD_NOTAS_ESPECIFICACAO.md** ⭐
   - Especificação completa da API
   - Exemplos de requests/responses
   - Estrutura de dados
   - Interface web sugerida

2. **Exemplo de JSON** (do teste)
   - JSON real que será enviado
   - Estrutura de dados esperada no retorno

3. **Requisitos Técnicos:**
   - Endpoints: POST /create, GET /status/{token}, GET /download/{token}
   - Autenticação: Bearer Token
   - Armazenamento: Arquivos PDF, máx 10MB
   - Expiração: 30 dias
   - Banco: Postgres/MySQL/Mongo (sugestão)

### Informações para Fornecer:

- **URL Base da API**: Onde será hospedada?
- **API Key**: Gerar chave para autenticação
- **Callback/Webhook** (opcional): Para notificar quando upload concluir
- **Ambiente de Teste**: URL para testes antes de produção

## 🔐 Segurança

### Validações Necessárias na API Externa:

1. ✅ Verificar API Key em todas requisições
2. ✅ Validar tipo de arquivo (apenas PDF)
3. ✅ Validar tamanho (máximo 10MB)
4. ✅ Verificar se token é válido e não expirou
5. ✅ Rate limiting (max 10 req/min por token)
6. ✅ Sanitizar nome de arquivos
7. ✅ Armazenar hash SHA256 do arquivo

### Dados Sensíveis:

- Token deve ser único e não-sequencial (UUID recomendado)
- Arquivos devem ser armazenados com permissões restritas
- Links devem expirar após prazo definido
- Logs de auditoria para todas operações

## 📊 Monitoramento

### Métricas Importantes:

- Total de links criados
- Taxa de uploads concluídos vs pendentes
- Links expirados sem upload
- Tempo médio para upload
- Tamanho médio dos arquivos

### Logs Recomendados:

```
[2025-10-13 15:30:00] Link criado - Lote #12345 - Token abc123
[2025-10-13 16:45:00] Upload recebido - Lote #12345 - 2.5MB
[2025-10-13 16:46:00] Arquivo baixado - Lote #12345
```

## 🆘 Troubleshooting

### Erro: "API não acessível"
- Verificar UPLOAD_API_URL no .env
- Testar conectividade: `curl -I $UPLOAD_API_URL`
- Verificar firewall/proxy

### Erro: "Unauthorized"
- Verificar UPLOAD_API_KEY no .env
- Confirmar chave com outro desenvolvedor
- Verificar formato do header (Bearer TOKEN)

### Upload não aparece
- Verificar se job está rodando: `ps aux | grep consultar_notas`
- Ver log: `tail -f logs/consulta_notas.log`
- Testar manualmente: `python job_consultar_notas.py`

### Arquivo não baixa
- Verificar permissões do diretório uploads/
- Verificar espaço em disco: `df -h`
- Testar download manual: `curl $URL -o teste.pdf`

---

**Status**: ✅ Pronto para implementação  
**Versão**: 1.0.0  
**Data**: 13 de outubro de 2025
