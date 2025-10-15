# 🔧 Solução: Offset de IDs para Montadores

## 📋 Problema Identificado

**Sintoma**: Ao criar múltiplos envios de montagem para o mesmo montador e período, a API retornava erro 409 (conflito/duplicado).

```
⚠️ Erro ao gerar link: Lote já foi enviado anteriormente (duplicado)
```

**Causa Raiz**: A API DV Processamento usa os seguintes campos para detectar duplicação:
- `nome` (montador/prestador)
- `periodo` (MM/YYYY)
- `quantidade_os`
- `valor_total`
- **`lote_id`** ← Campo principal de unicidade

Como prestadores e montadores compartilham a mesma API, e ambos começavam com IDs baixos (1, 2, 3...), havia conflito de IDs.

### Exemplo do Problema
```
Prestador - Lote #3:
  nome: "João Silva"
  periodo: "10/2025"
  lote_id: 3
  ✅ Criado com sucesso

Montador - Envio #3:
  nome: "Maria Santos"
  periodo: "10/2025"
  lote_id: 3
  ❌ Erro: lote_id 3 já existe!
```

---

## ✅ Solução Implementada

**Estratégia**: Adicionar um **offset fixo de 876231** aos IDs de montadores antes de enviar para a API.

### Mapeamento de IDs

| ID Local | Tipo | ID na API | Cálculo |
|----------|------|-----------|---------|
| 1 | Prestador | 1 | 1 |
| 2 | Prestador | 2 | 2 |
| 3 | Prestador | 3 | 3 |
| **1** | **Montador** | **876232** | **876231 + 1** |
| **2** | **Montador** | **876233** | **876231 + 2** |
| **3** | **Montador** | **876234** | **876231 + 3** |
| **6** | **Montador** | **876237** | **876231 + 6** |

### Faixa de IDs
- **Prestadores**: 1 a 876230
- **Montadores**: 876232 em diante (876231 + ID local)

Isso garante **876.230 IDs únicos** para cada tipo, mais do que suficiente para o sistema.

---

## 🔧 Implementação

**Arquivo Modificado**: `api_upload_client.py`

### Código Adicionado

```python
# 🔧 OFFSET para montadores: Adicionar 876231 ao ID para evitar conflito com prestadores
if tipo == 'montagem':
    lote_id_api = 876231 + lote_ou_envio_id
    print(f"🔧 ID Montagem: {lote_ou_envio_id} → ID API: {lote_id_api}")
else:
    lote_id_api = lote_ou_envio_id

# ... resto do código ...

payload = {
    "nome": nome_empresa,
    "email": email_contato,
    "periodo": periodo,
    "valor_total": float(lote['valor_total']),
    "quantidade_os": quantidade_os,
    "data_envio": data_envio_iso,
    "lote_id": lote_id_api,  # ✅ ID com offset para montadores
    "tipo": tipo
}
```

---

## 🧪 Teste de Verificação

### Antes da Correção
```bash
Envio #6 (Montador):
  ID Local: 6
  ID API: 6
  Resultado: ❌ Erro 409 - Duplicado (conflito com lote de prestador)
```

### Depois da Correção
```bash
Envio #6 (Montador):
  ID Local: 6
  ID API: 876237 (876231 + 6)
  ID Controle: 51
  Link: https://api.link.dev.br/dvprocessamento/envio-nf/87e48819...
  Resultado: ✅ Sucesso!
```

---

## 📊 Comportamento Atual

### Prestadores
```python
lote_id = 22  # ID no banco local
lote_id_api = 22  # ID enviado para API
# API cria registro com lote_id=22
```

### Montadores
```python
envio_id = 6  # ID no banco local
lote_id_api = 876237  # 876231 + 6 = ID enviado para API
# API cria registro com lote_id=876237
```

### Consulta Posterior
Quando a API retorna dados, ela usa o `lote_id` (com offset), mas o sistema local já sabe que:
- `lote_id < 876231` → Prestador
- `lote_id >= 876231` → Montador

---

## 🎯 Vantagens da Solução

✅ **Simples**: Apenas uma linha de código adicional  
✅ **Transparente**: Não afeta o banco de dados local  
✅ **Escalável**: Suporta até 876.230 registros de cada tipo  
✅ **Retrocompatível**: Não afeta registros existentes  
✅ **Manutenível**: Fácil de entender e modificar  

---

## 📝 Considerações

### Por que 876231?
- Número alto o suficiente para evitar conflitos
- Fácil de identificar visualmente (não começa com 1, 10, 100...)
- Permite crescimento ilimitado de prestadores até 876230

### Alternativas Consideradas

1. **Usar prefixo no lote_id** (ex: "M-6", "P-22")
   - ❌ API valida lote_id como número inteiro

2. **Modificar período** (ex: "10/2025-6")
   - ❌ API valida formato MM/YYYY

3. **Usar microssegundos na data**
   - ❌ API valida formato ISO sem microssegundos

4. **Tabela separada na API**
   - ❌ Requer mudança no back-end (fora do escopo)

5. **Offset fixo** ✅
   - ✅ Funciona sem modificar API
   - ✅ Simples de implementar
   - ✅ Transparente para usuário

---

## 🔄 Integração Automática

A mudança já está integrada com a função `log_sent_montagem()` que chama automaticamente a API ao criar um envio:

```python
def log_sent_montagem(montador_id, group_details, conversation_id):
    # ... criar registro ...
    
    # 🚀 ENVIAR PARA API IMEDIATAMENTE
    from api_upload_client import APIUploadClient
    client = APIUploadClient()
    sucesso, mensagem, dados = client.enviar_e_salvar(envio_id, tipo='montagem')
    # O offset é aplicado automaticamente dentro de enviar_e_salvar()
```

---

## ✅ Status

**Implementado**: 15 de Outubro de 2025  
**Testado**: ✅ Envio #6 criado com sucesso (ID API: 876237)  
**Em Produção**: ✅ Ativo para todos os novos envios  

---

**Offset Definido**: 876231  
**Faixa Prestadores**: 1 - 876230  
**Faixa Montadores**: 876232+  
