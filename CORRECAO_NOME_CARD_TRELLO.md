# 🔧 Correção: Nome "None" no Card do Trello para Montadores

## 📋 Problema Identificado

**Sintoma**: Cards do Trello para montadores exibiam "None" no lugar do nome:

```
Título do Card: 📦 Lote #6 - None - R$ 160.00
```

**Causa Raiz**: A função `criar_card_download()` usava `prestador_nome` diretamente no título, mas para montadores esse valor é `None`.

### Código Problemático
```python
# Linha 115 - trello_integration.py
if valor_lote and valor_lote > 0:
    titulo = f"📦 Lote #{lote_id} - {prestador_nome} - R$ {valor_lote:,.2f}"
    #                                    ^^^^^^^^^^^^^^
    #                                    None para montadores
else:
    titulo = f"📦 Lote #{lote_id} - {prestador_nome}"
```

### Chamada da Função
```python
# job_consultar_notas.py - Linha 404
card_result = trello.criar_card_download(
    lote_id=envio_id,
    prestador_nome=None,      # ❌ None para montadores
    montador_nome=montador,   # ✅ "DAVID DIAS"
    arquivos_baixados=arquivos_baixados,
    nota_fiscal=nota_fiscal,
    arquivos_para_anexar=arquivos_para_anexar,
    valor_lote=valor_envio
)
```

---

## ✅ Solução Implementada

**Arquivo Modificado**: `integracoes/trello_integration.py`

### Mudança 1: Título do Card

**Antes**:
```python
# Usava prestador_nome direto (None para montadores)
if valor_lote and valor_lote > 0:
    titulo = f"📦 Lote #{lote_id} - {prestador_nome} - R$ {valor_lote:,.2f}"
else:
    titulo = f"📦 Lote #{lote_id} - {prestador_nome}"
```

**Depois**:
```python
# Determina qual nome usar baseado em qual está disponível
nome_entidade = prestador_nome if prestador_nome else montador_nome

if valor_lote and valor_lote > 0:
    titulo = f"📦 Lote #{lote_id} - {nome_entidade} - R$ {valor_lote:,.2f}"
else:
    titulo = f"📦 Lote #{lote_id} - {nome_entidade}"
```

### Mudança 2: Descrição do Card

**Antes**:
```python
# Mostrava ambos sempre, mesmo quando None
descricao = f"""## 📋 Informações do Lote

**Lote:** #{lote_id}
**Prestador:** {prestador_nome}
**Montador:** {montador_nome}
**Data/Hora:** {data_hora}
"""
```

**Depois**:
```python
# Mostra apenas o que está preenchido
descricao = f"""## 📋 Informações do Lote

**Lote:** #{lote_id}
"""

# Adicionar apenas prestador OU montador, não ambos
if prestador_nome:
    descricao += f"**Prestador:** {prestador_nome}\n"
if montador_nome:
    descricao += f"**Montador:** {montador_nome}\n"

descricao += f"**Data/Hora:** {data_hora}\n"
```

---

## 🧪 Teste de Verificação

### Antes da Correção
```
Título: 📦 Lote #6 - None - R$ 160.00 ❌

Descrição:
  Lote: #6
  Prestador: None ❌
  Montador: DAVID DIAS
  Data/Hora: 15/10/2025 às 17:15
```

### Depois da Correção
```
Título: 📦 Lote #6 - DAVID DIAS - R$ 160.00 ✅

Descrição:
  Lote: #6
  Montador: DAVID DIAS ✅
  Data/Hora: 15/10/2025 às 17:15
```

---

## 📊 Comportamento por Tipo

### Para Prestadores
```python
criar_card_download(
    lote_id=47,
    prestador_nome="João Silva",  # ✅ Preenchido
    montador_nome=None,
    ...
)
```
**Resultado**:
- Título: `📦 Lote #47 - João Silva - R$ 1.250,00`
- Descrição mostra: **Prestador:** João Silva

### Para Montadores
```python
criar_card_download(
    lote_id=6,
    prestador_nome=None,
    montador_nome="DAVID DIAS",  # ✅ Preenchido
    ...
)
```
**Resultado**:
- Título: `📦 Lote #6 - DAVID DIAS - R$ 160,00`
- Descrição mostra: **Montador:** DAVID DIAS

---

## 🎯 Lógica de Prioridade

A função agora segue esta lógica:

```python
nome_entidade = prestador_nome if prestador_nome else montador_nome
```

**Ordem de Preferência**:
1. Se `prestador_nome` não for None → usa prestador
2. Se `prestador_nome` for None → usa montador

Isso garante que sempre haverá um nome válido no título do card.

---

## 📝 Casos de Uso

### Cenário 1: Lote de Prestador
```python
prestador_nome = "Maria Santos"
montador_nome = None
→ Usa: "Maria Santos"
```

### Cenário 2: Envio de Montador
```python
prestador_nome = None
montador_nome = "DAVID DIAS"
→ Usa: "DAVID DIAS"
```

### Cenário 3: Ambos Preenchidos (improvável, mas tratado)
```python
prestador_nome = "João Silva"
montador_nome = "DAVID DIAS"
→ Usa: "João Silva" (prioridade para prestador)
→ Descrição mostra ambos
```

---

## ✅ Status

**Implementado**: 15 de Outubro de 2025  
**Testado**: ✅ Card criado com nome correto  
**Em Produção**: ✅ Ativo para todos os novos cards  

---

**Arquivo**: `integracoes/trello_integration.py`  
**Linhas Modificadas**: 114-120, 245-252  
**Impacto**: Apenas visual (títulos e descrições dos cards)  
