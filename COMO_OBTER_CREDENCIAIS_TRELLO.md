# 🔐 Como Obter Credenciais Corretas do Trello

## ❌ Problema Identificado

As credenciais fornecidas estão incorretas. Ambas resultam em erro `401 - invalid key`.

**Testado:**
- `1fb13b06df471a152b6c332c7b9d926d` 
- `08054455b9d94f7ed488ef5ebdb4ded9b510545219e9b91d80e3a7b3f0b9e95a`

Nenhuma das duas funciona como API Key ou Token.

---

## ✅ Como Obter Credenciais CORRETAS

### Passo 1: Obter API Key

1. **Acesse:** https://trello.com/power-ups/admin
2. **Faça login** com sua conta Trello
3. Você verá uma lista de Power-Ups (ou estará vazia)
4. **Clique em "New"** (Nova Power-Up) se não tiver nenhuma
5. Preencha:
   - **Name:** "Disparador Email" (ou qualquer nome)
   - **Workspace:** Selecione seu workspace
6. **Clique em "Create"**
7. Você será redirecionado para a página da Power-Up
8. **COPIE a "API Key"** que aparece no topo da página
   - É um código de **32 caracteres** hexadecimais
   - Exemplo: `a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6`

### Passo 2: Gerar Token

1. **Ainda na página da Power-Up**, procure por **"Token"**
2. Clique no link **"manually generate a Token"**
3. Você será levado para uma página de autorização
4. **Leia as permissões** e clique em **"Allow"** (Permitir)
5. **COPIE o Token** que aparece
   - É um código de **64 caracteres** hexadecimais
   - Exemplo: `a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6a7b8c9d0e1f2g3h4i5j6k7l8m9n0o1p2`

### Passo 3: Identificar Qual é Qual

**API Key:**
- ✅ Código de **32 caracteres**
- ✅ Aparece na página da Power-Up
- ✅ É chamada de "API Key" ou "Key"

**Token:**
- ✅ Código de **64 caracteres** 
- ✅ Você precisa gerar manualmente
- ✅ É chamado de "Token" ou "Secret Token"

---

## 🔍 Como Testar

Depois de obter as credenciais corretas:

```bash
cd /Users/davidgabriel/projetos/disparador-email
.venv/bin/python3 testar_credenciais_trello.py
```

Se aparecer **"✅ TODOS OS TESTES PASSARAM!"**, as credenciais estão corretas!

---

## 💡 Dica: Visualizando no Navegador

Enquanto estiver na página https://trello.com/power-ups/admin:

1. **Abra o Console do navegador** (F12 ou Cmd+Option+I)
2. Cole este código:

```javascript
// Mostrar API Key se estiver disponível
const apiKey = document.querySelector('[data-testid="api-key"]');
if (apiKey) {
    console.log('API Key:', apiKey.textContent);
}
```

---

## 📞 Ainda com Dúvidas?

Se as credenciais ainda não funcionarem:

1. Verifique se está logado na conta **correta** do Trello
2. Confirme que tem acesso ao board "lancamento-nf"
3. Tente **regenerar o token** (na mesma página)
4. Verifique se não há espaços ou quebras de linha ao copiar

---

## ⚠️ Importante

- **Nunca compartilhe** suas credenciais publicamente
- O Token tem **permissões de leitura e escrita** na sua conta
- Se comprometer as credenciais, **revogue o token** e gere um novo
