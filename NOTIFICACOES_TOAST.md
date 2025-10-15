# 🔔 Sistema de Notificações Toast

## 📋 Visão Geral

Sistema de notificações flutuantes (toast) para o Streamlit, substituindo o sistema anterior de modal/badge que causava duplicações.

## ✨ Novidades

### Antes ❌
- Notificações no sidebar com modal
- Criadas toda vez que o job rodava
- **Problema:** 119 notificações para o mesmo lote!
- Usuário tinha que clicar para ver

### Agora ✅
- **Notificações flutuantes automáticas** (toasts)
- Aparecem automaticamente quando você abre o sistema
- **Sem duplicações** - apenas uma notificação por lote
- Marcadas como lidas automaticamente após exibição
- Contador de notificações não lidas no sidebar

## 🎯 Como Funciona

### 1. Quando Job Baixa Arquivos

```python
# job_consultar_notas.py

# ✅ Verifica se já foi processado antes
if status_arquivo_atual == 2:  # Já baixado
    continue  # Não cria notificação novamente

# ✅ Cria notificação apenas na PRIMEIRA vez
db.criar_notificacao(
    tipo='nf_recebida',
    titulo=f"📥 Nota Fiscal Recebida - Lote #{lote_id}",
    mensagem=f"{prestador} enviou {total_arqs} arquivo(s)",
    lote_id=lote_id,
    icone='📥',
    prioridade=1
)
```

### 2. Quando Usuário Abre Sistema

```python
# streamlit_app.py (linha 136)

# 🔔 PROCESSAR NOTIFICAÇÕES TOAST (exibe automaticamente)
processar_notificacoes_toast()
```

**O que acontece:**
1. Busca notificações não lidas no banco
2. Para cada notificação não lida:
   - Exibe toast flutuante
   - Marca como lida automaticamente
   - Adiciona ao cache da sessão (evita reexibição)

### 3. Toast na Tela

```
╔════════════════════════════════════╗
║ 📥 Nota Fiscal Recebida - Lote #24 ║
║                                     ║
║ david enviou 1 arquivo(s) da nota  ║
║ fiscal (95.95 KB)                  ║
╚════════════════════════════════════╝
```

- Aparece no canto superior direito
- Desaparece automaticamente após 4 segundos
- Pode ter até 3 toasts simultâneos

## 📁 Arquivos

### Novos Arquivos

1. **`notificacoes_toast.py`** (139 linhas)
   - `processar_notificacoes_toast()` - Exibe toasts automáticos
   - `badge_contador_notificacoes()` - Contador sidebar
   - `mostrar_historico_notificacoes_sidebar()` - Histórico (opcional)
   - `criar_notificacao_toast()` - Wrapper para criar notificações

2. **`limpar_notificacoes_duplicadas.py`** (99 linhas)
   - Script para limpar notificações duplicadas existentes
   - Remove 707 notificações duplicadas em execução inicial

### Arquivos Modificados

1. **`streamlit_app.py`**
   - Linha 17: Import `processar_notificacoes_toast, badge_contador_notificacoes`
   - Linha 136: Chama `processar_notificacoes_toast()` automaticamente
   - Linha 141-143: Contador de notificações no sidebar

2. **`job_consultar_notas.py`**
   - Linha 78-82: Verifica se já foi processado antes
   - Linha 83: `continue` se status_arquivo == 2 (evita duplicação)
   - Linha 91-94: Verifica se arquivo já existe antes de baixar

## 🚀 Como Usar

### Para Usuários

1. **Abra o sistema normalmente**
2. **Toasts aparecem automaticamente** se houver notificações novas
3. **Veja o contador** no sidebar: "🔔 X nova(s) notificação(ões)"

### Para Desenvolvedores

#### Criar Notificação

```python
from notificacoes_toast import criar_notificacao_toast

criar_notificacao_toast(
    tipo='sucesso',        # nf_recebida, erro, sucesso, aviso, info
    titulo='Operação Concluída',
    mensagem='Arquivo processado com sucesso',
    lote_id=123,          # Opcional
    icone='✅',           # Opcional (usa padrão do tipo)
    prioridade=0          # 0=normal, 1=alta
)
```

#### Tipos de Notificação

| Tipo | Ícone Padrão | Uso |
|------|--------------|-----|
| `nf_recebida` | 📥 | Nota fiscal recebida |
| `sucesso` | ✅ | Operação bem-sucedida |
| `erro` | ❌ | Erro ou falha |
| `aviso` | ⚠️ | Atenção necessária |
| `info` | ℹ️ | Informação geral |

## 🐛 Resolução de Problemas

### Problema: Notificações Duplicadas

**Sintoma:** Mesma notificação aparece múltiplas vezes

**Causa:** Job criando notificação toda vez que roda

**Solução:**
```bash
# 1. Limpar duplicadas existentes
python limpar_notificacoes_duplicadas.py

# 2. Job já corrigido para não duplicar
# Verifica status_arquivo antes de processar
```

### Problema: Toasts Não Aparecem

**Sintoma:** Contador mostra notificações mas toasts não aparecem

**Causa:** Cache da sessão ou notificações antigas

**Solução:**
```python
# No streamlit_app.py, adicionar botão para limpar cache
from notificacoes_toast import limpar_cache_notificacoes

if st.sidebar.button("🔄 Recarregar Notificações"):
    limpar_cache_notificacoes()
    st.rerun()
```

### Problema: Muitos Toasts de Uma Vez

**Sintoma:** 10+ toasts aparecem ao mesmo tempo

**Causa:** Muitas notificações não lidas acumuladas

**Solução:**
```bash
# Marcar todas como lidas
python -c "
import database as db
conn = db.get_db_connection()
cur = conn.cursor()
cur.execute('UPDATE notificacoes SET lida = true')
conn.commit()
print('✅ Todas notificações marcadas como lidas')
"
```

## 📊 Estatísticas da Limpeza Inicial

Executado em: 14/10/2025 23:20

```
📝 Total de notificações a remover: 707

🗑️  Removendo notificações duplicadas...
  ✓ Lote #19: 118 notificações removidas
  ✓ Lote #20: 118 notificações removidas
  ✓ Lote #21: 118 notificações removidas
  ✓ Lote #22: 118 notificações removidas
  ✓ Lote #23: 118 notificações removidas
  ✓ Lote #24: 117 notificações removidas

✅ Total removido: 707 notificações
✅ Mantidas: 6 notificações (uma por lote)
```

## 🔧 Configurações Avançadas

### Alterar Duração do Toast

```python
# notificacoes_toast.py, linha 43
st.toast(
    f"**{titulo}**\n\n{mensagem}",
    icon=toast_icon
    # Streamlit não permite customizar duração (fixo 4s)
)
```

### Limitar Quantidade de Toasts

```python
# notificacoes_toast.py
def processar_notificacoes_toast():
    notificacoes = db.get_notificacoes_nao_lidas()
    
    # Limitar a 5 toasts por vez
    for notif in notificacoes[:5]:  # <-- Adicionar limite
        # ... resto do código
```

## 📚 Referências

- [Streamlit Toast API](https://docs.streamlit.io/library/api-reference/status/st.toast)
- [Streamlit Session State](https://docs.streamlit.io/library/api-reference/session-state)

## 🎉 Resultado Final

- ✅ **707 notificações duplicadas removidas**
- ✅ **Sistema de toasts implementado**
- ✅ **Sem mais duplicações**
- ✅ **Notificações aparecem automaticamente**
- ✅ **Interface limpa e moderna**

---

**Desenvolvido com ❤️ para melhorar a experiência do usuário**
