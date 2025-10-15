# 🔧 Migração - Sistema de API para Montadores

## ✅ O que já foi feito:

### 1. Database (database.py)
- ✅ Adicionadas colunas na tabela `envios_montagem`:
  - `id_controle`: ID retornado pela API
  - `link_upload`: Link de upload gerado
  - `validade_link`: Data de validade do link
  - `status_api`: 0=pendente, 1=NF recebida
  - `data_envio_api`: Timestamp do envio para API
  - `nota_fiscal_path`: Caminho do arquivo recebido
  - `api_message`: Mensagem da API
  - `upload_hash`: Hash único para consulta
  - `status_arquivo`: 0=Aguardando, 1=Recebido, 2=Baixado
  - `data_ultima_consulta`: Última consulta à API
  - `quantidade_os`: Quantidade de OSs (similar a lotes)
  - `montador_nome`: Nome do montador (cache)

- ✅ Criados índices:
  - `idx_envios_montagem_upload_hash`
  - `idx_envios_montagem_status_api`

- ✅ Funções criadas:
  - `get_envios_montagem_sem_api()`: Retorna envios sem API
  - `get_envios_montagem_upload_pendente()`: Retorna envios aguardando upload
  - `atualizar_status_api_montagem()`: Atualiza status da API
  - `atualizar_status_arquivo_montagem()`: Atualiza status do arquivo
  - `salvar_nota_fiscal_montagem()`: Salva caminho da NF recebida
  - `get_envio_montagem_by_id_controle()`: Busca por ID de controle
  - `delete_envio_montagem()`: Delete com cascade para notificações e Trello

## 📋 O que precisa ser implementado:

### 2. Job de Envio para API (job_enviar_api.py)
- ⏳ Adaptar para incluir envios de montagem
- ⏳ Calcular `quantidade_os` a partir do JSONB `detalhes`
- ⏳ Preencher `montador_nome` no cache

### 3. Job de Consulta de Notas (job_consultar_notas.py)
- ⏳ Criar versão para montadores ou unificar com prestadores
- ⏳ Consultar notas de montadores na API
- ⏳ Baixar arquivos em `uploads/montagem_{envio_id}/`
- ⏳ Atualizar status para "N.F RECEBIDA"
- ⏳ Criar notificações
- ⏳ Integrar com Trello (criar cards)

### 4. Integração Trello (trello_integration.py)
- ⏳ Adaptar `criar_card_download` para aceitar tipo (prestador/montador)
- ⏳ Ou criar método separado `criar_card_montagem`

### 5. Interface Streamlit (streamlit_app.py)
- ⏳ Adicionar visualização de links de upload para montadores
- ⏳ Mostrar status de arquivos (Aguardando/Recebido/Baixado)
- ⏳ Botão para reenviar para API (se necessário)
- ⏳ Download de arquivos recebidos

### 6. Scheduler (scheduler_service.py)
- ⏳ Adicionar job de envio de montadores para API
- ⏳ Adicionar job de consulta de notas de montadores

## 📊 Estrutura Similar a Prestadores:

| Prestadores | Montadores |
|-------------|------------|
| `lotes_servico` | `envios_montagem` |
| `prestador_id` | `montador_id` |
| `prestador_nome` | `montador_nome` |
| `uploads/lote_{id}/` | `uploads/montagem_{id}/` |
| `job_enviar_api.py` | (mesmo job, adaptar) |
| `job_consultar_notas.py` | (mesmo job ou criar separado) |

## 🎯 Próximos Passos Recomendados:

1. **Testar migrations:**
   ```bash
   python -c "import database as db; db.run_migrations()"
   ```

2. **Adaptar job_enviar_api.py:**
   - Adicionar lógica para processar `envios_montagem`
   - Extrair `quantidade_os` do JSONB
   - Popular `montador_nome`

3. **Criar job_consultar_notas_montagem.py:**
   - Copiar de `job_consultar_notas.py`
   - Adaptar para usar funções de montagem
   - Testar com um envio real

4. **Atualizar interface:**
   - Adicionar tab ou seção para montadores
   - Mostrar links de upload
   - Status de arquivos

5. **Integrar Trello:**
   - Cards separados para montadores
   - Ou usar mesma lista com tag diferente

## 💡 Notas Importantes:

- O campo `detalhes` em `envios_montagem` é JSONB e contém a estrutura do envio
- Precisa extrair informações como quantidade de OSs/boletins
- O período pode estar em `detalhes->>'periodo_relatorio'`
- Manter compatibilidade com sistema antigo de anexos por email
