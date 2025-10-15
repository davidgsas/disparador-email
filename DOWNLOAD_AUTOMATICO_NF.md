# 📥 Sistema de Download Automático de Notas Fiscais

## 🎯 Visão Geral

O sistema baixa automaticamente todos os arquivos de notas fiscais enviados pelos prestadores através do job `job_consultar_notas.py`.

---

## 🔄 Como Funciona

### 1. Fluxo Automático

```
Job executa (cron ou manual)
    ↓
Consulta API para cada lote com link válido
    ↓
Detecta arquivos novos
    ↓
Baixa TODOS os arquivos automaticamente
    ↓
Salva em: uploads/lote_{ID}/
    ↓
Atualiza banco de dados
    ↓
Cria notificação
```

### 2. Estrutura de Pastas

```
disparador-email/
└── uploads/
    ├── lote_13/
    │   ├── nota_fiscal.pdf
    │   └── comprovante.xml
    ├── lote_22/
    │   └── Nf 12.pdf
    └── lote_45/
        ├── NF_Outubro.pdf
        └── Anexo1.jpg
```

Cada lote tem sua própria pasta com todos os arquivos recebidos.

---

## ⚙️ Execução do Job

### Opção 1: Manualmente (Teste)

```bash
python job_consultar_notas.py
```

**Saída esperada:**
```
============================================================
🔍 JOB DE CONSULTA DE NOTAS FISCAIS
============================================================
⏰ Executado em: 14/10/2025 21:30:00

📋 3 lote(s) aguardando nota fiscal

────────────────────────────────────────────────────────────
📦 Lote #22
   👤 Prestador: david
   📅 Período: 01/2026
   🔑 Hash: 74b1ab63d2f02d33f992...
   🔍 Consultando arquivos...
   ✅ Consulta realizada com sucesso
   📊 1 arquivo(s) encontrado(s)
   📊 Status: Arquivos recebidos
   📁 Arquivos encontrados: 1
   📦 Total: 95.95 KB
   ✅ Dados salvos no banco
   ⬇️  Baixando: Nf 12.pdf (95.95 KB)
   ✅ Arquivo baixado com sucesso
   ✅ Arquivo salvo em: uploads/lote_22/Nf 12.pdf
   ✅ Status atualizado: Arquivos baixados
   🔔 Notificação criada

============================================================
📊 RESUMO DO PROCESSAMENTO
============================================================
📁 Lotes com arquivos: 1
⬇️  Arquivos baixados: 1
⏳ Ainda pendentes: 2
⏰ Concluído em: 14/10/2025 21:30:15
============================================================
```

### Opção 2: Automático (Cron)

#### Para Mac/Linux:

Editar crontab:
```bash
crontab -e
```

Adicionar linha (executa a cada hora):
```bash
0 * * * * cd /Users/davidgabriel/projetos/disparador-email && /Users/davidgabriel/projetos/disparador-email/.venv/bin/python job_consultar_notas.py >> /tmp/job_consultar_notas.log 2>&1
```

**Outras opções de frequência:**
```bash
# A cada 30 minutos
*/30 * * * * cd ...

# A cada 2 horas
0 */2 * * * cd ...

# Todos os dias às 8h, 12h e 18h
0 8,12,18 * * * cd ...
```

Verificar se foi adicionado:
```bash
crontab -l
```

Ver logs:
```bash
tail -f /tmp/job_consultar_notas.log
```

---

## 📊 Banco de Dados

### Status dos Arquivos

| status_arquivo | Descrição | Significado |
|----------------|-----------|-------------|
| 0 | Aguardando | Link gerado, aguardando envio do prestador |
| 1 | Recebido | Arquivo foi enviado, mas não baixado localmente |
| 2 | Baixado | Arquivo já foi baixado e está em uploads/ |

### Consultar Lotes com Arquivos

```sql
-- Ver todos os lotes com arquivos baixados
SELECT 
    id,
    prestador_nome,
    periodo,
    status_arquivo,
    data_ultima_consulta,
    arquivos_nf->>'estatisticas' as stats
FROM lotes_servico 
WHERE status_arquivo = 2
ORDER BY data_ultima_consulta DESC;

-- Ver arquivos de um lote específico
SELECT 
    id,
    prestador_nome,
    jsonb_pretty(arquivos_nf) as arquivos_detalhados
FROM lotes_servico 
WHERE id = 22;

-- Contar arquivos por lote
SELECT 
    id,
    prestador_nome,
    (arquivos_nf->'estatisticas'->>'total_arquivos')::int as total_arquivos,
    arquivos_nf->'estatisticas'->>'total_tamanho_formatado' as tamanho_total
FROM lotes_servico 
WHERE status_arquivo >= 1;
```

---

## 🔍 Acessar Arquivos Baixados

### Via Python

```python
import os
import json
import database as db

# Buscar lote
lote = db.get_lote_by_id(22)

if lote and lote['arquivos_nf']:
    # Parsear JSON
    arquivos_data = json.loads(lote['arquivos_nf']) if isinstance(lote['arquivos_nf'], str) else lote['arquivos_nf']
    
    # Listar arquivos
    for arquivo in arquivos_data['arquivos']:
        nome = arquivo['nome_original']
        caminho = f"uploads/lote_{lote['id']}/{nome}"
        
        print(f"Arquivo: {nome}")
        print(f"Caminho: {caminho}")
        print(f"Existe: {os.path.exists(caminho)}")
        print(f"Tamanho: {arquivo['tamanho_formatado']}")
        print("---")
```

### Via Terminal

```bash
# Listar arquivos de um lote
ls -lh uploads/lote_22/

# Ver todos os lotes com arquivos
ls -d uploads/lote_*/

# Contar total de arquivos
find uploads/ -type f | wc -l

# Ver tamanho total
du -sh uploads/
```

---

## 🚀 Próximos Passos (Encaminhamento)

### Estrutura Preparada

Os arquivos estão organizados e prontos para serem encaminhados:

```python
def encaminhar_arquivos_lote(lote_id, destinatarios):
    """Exemplo de função para encaminhar arquivos"""
    
    # Buscar dados do lote
    lote = db.get_lote_by_id(lote_id)
    
    # Parsear arquivos
    arquivos_data = json.loads(lote['arquivos_nf'])
    
    # Lista de caminhos para anexar
    anexos = []
    for arquivo in arquivos_data['arquivos']:
        caminho = f"uploads/lote_{lote_id}/{arquivo['nome_original']}"
        if os.path.exists(caminho):
            anexos.append(caminho)
    
    # Enviar email com anexos
    enviar_email(
        destinatarios=destinatarios,
        assunto=f"NF - Lote {lote_id} - {lote['prestador_nome']}",
        corpo="Seguem em anexo os arquivos da nota fiscal",
        anexos=anexos
    )
    
    return len(anexos)
```

---

## 🛡️ Segurança e Backup

### Backup dos Arquivos

```bash
# Backup diário dos uploads
tar -czf backup_uploads_$(date +%Y%m%d).tar.gz uploads/

# Mover para pasta de backup
mv backup_uploads_*.tar.gz ~/backups/
```

### Limpeza Periódica

```bash
# Remover arquivos de lotes mais antigos que 90 dias
find uploads/ -type f -mtime +90 -delete

# Ou criar script de limpeza:
# cleanup_old_uploads.py
```

---

## 📝 Verificações

### 1. Verificar se Job está funcionando

```bash
# Executar manualmente
python job_consultar_notas.py

# Verificar se baixou arquivos
ls -lR uploads/
```

### 2. Verificar permissões

```bash
# Pasta uploads deve ter permissão de escrita
chmod 755 uploads/
```

### 3. Verificar espaço em disco

```bash
# Ver espaço disponível
df -h

# Ver espaço usado por uploads
du -sh uploads/
```

---

## 🐛 Troubleshooting

### Arquivos não estão sendo baixados

1. **Verificar se job está rodando:**
   ```bash
   python job_consultar_notas.py
   ```

2. **Verificar logs:**
   - Procurar por erros no output
   - Verificar mensagens "❌"

3. **Verificar permissões da pasta:**
   ```bash
   ls -ld uploads/
   ```

4. **Verificar conexão com API:**
   - Testar manualmente: `python testar_consulta_nf.py HASH`

### Arquivos incompletos

- Job pode ter sido interrompido
- Executar novamente (irá baixar novamente se necessário)

### Espaço em disco cheio

- Implementar rotina de limpeza
- Mover arquivos antigos para backup
- Compactar arquivos PDF

---

## 📊 Estatísticas

### Ver estatísticas de downloads

```sql
-- Total de arquivos baixados
SELECT 
    COUNT(*) as total_lotes,
    SUM((arquivos_nf->'estatisticas'->>'total_arquivos')::int) as total_arquivos
FROM lotes_servico 
WHERE status_arquivo = 2;

-- Por prestador
SELECT 
    prestador_nome,
    COUNT(*) as lotes_com_arquivos,
    SUM((arquivos_nf->'estatisticas'->>'total_arquivos')::int) as total_arquivos
FROM lotes_servico 
WHERE status_arquivo >= 1
GROUP BY prestador_nome
ORDER BY total_arquivos DESC;
```

---

## 🎯 Checklist de Funcionamento

- [x] ✅ Job consulta API automaticamente
- [x] ✅ Arquivos são baixados para uploads/lote_X/
- [x] ✅ Dados salvos no banco (arquivos_nf)
- [x] ✅ Status atualizado para "Baixado" (2)
- [x] ✅ Notificações criadas
- [x] ✅ Estrutura pronta para encaminhamento
- [ ] ⏳ Cron configurado (fazer)
- [ ] ⏳ Backup automático (fazer)
- [ ] ⏳ Sistema de encaminhamento (próximo)

---

## 📞 Resumo Executivo

**✅ SISTEMA FUNCIONAL E PRONTO!**

1. Execute: `python job_consultar_notas.py`
2. Arquivos baixados em: `uploads/lote_{ID}/`
3. Configure cron para automático
4. Use os arquivos para próxima etapa (encaminhamento)

**Tudo está funcionando e pronto para uso!** 🎉
