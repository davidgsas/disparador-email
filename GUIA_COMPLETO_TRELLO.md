# 🎯 Guia Definitivo - API do Trello

## ✅ Confirmação: A API Está CORRETA!

Confirmado pela documentação oficial da Atlassian:
- **URL Base:** `https://api.trello.com/1/`
- **Endpoint para boards:** `GET /1/members/me/boards`
- **Endpoint para listas:** `GET /1/boards/{idBoard}/lists`
- **Endpoint para criar card:** `POST /1/cards`

🔗 **Fonte oficial:** https://developer.atlassian.com/cloud/trello/guides/rest-api/api-introduction/

---

## 📋 Como Funciona a Autenticação

### 1. API Key (32 caracteres)
- Identifica sua aplicação/Power-Up
- **É pública** (pode ser compartilhada)
- Sozinha, NÃO dá acesso aos dados

### 2. Token (64 caracteres)
- Identifica o USUÁRIO que autorizou
- **É privada** (NUNCA compartilhar)
- Dá acesso total aos dados do usuário

### 3. Como Usar
```bash
# Formato correto
GET https://api.trello.com/1/members/me/boards?key={API_KEY}&token={TOKEN}
```

---

## 🔑 Passo a Passo GARANTIDO

### PASSO 1: Acessar o Portal
1. Abra: https://trello.com/power-ups/admin
2. Faça login na sua conta do Trello
3. Você verá uma lista (pode estar vazia)

### PASSO 2: Criar Power-Up
Se não tiver nenhuma Power-Up ainda:

1. Clique em **"New"** (botão azul no canto superior direito)
2. Preencha:
   - **Power-Up name:** "Meu Sistema" (ou qualquer nome)
   - **Workspace:** Escolha seu workspace
   - **Iframe connector URL:** `http://localhost` (pode colocar qualquer URL)
3. Clique em **"Create"**

### PASSO 3: Copiar API Key
Após criar (ou se já tem uma Power-Up):

1. Você está na página da Power-Up
2. Procure a aba/seção **"API Key"** (geralmente já está visível)
3. Você verá algo como:

```
API Key
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

4. **COPIE EXATAMENTE** esses 32 caracteres
5. Cole em um arquivo de texto temporário

### PASSO 4: Gerar Token
1. Na mesma página, procure por **"Token"**
2. Clique no link: **"you can manually generate a Token"**
3. Você será redirecionado para uma página de autorização
4. Você verá:
   - Nome da aplicação
   - Permissões solicitadas (read, write, account)
   - Tempo de expiração (never = recomendado)
5. Clique em **"Allow"** (botão verde)
6. Você verá algo como:

```
Your token is:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6a7b8c9d0e1f2g3h4i5j6k7l8m9n0o1p2
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

7. **COPIE EXATAMENTE** esses 64 caracteres
8. Cole no arquivo de texto temporário

### PASSO 5: Validar
Agora você tem:
- ✅ API Key = 32 caracteres
- ✅ Token = 64 caracteres

**Exemplo de formato correto:**
```
API Key:  a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6
Token:    a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6a7b8c9d0e1f2g3h4i5j6k7l8m9n0o1p2
```

---

## 🧪 Teste Rápido no Terminal

Execute este comando substituindo os valores:

```bash
curl "https://api.trello.com/1/members/me/boards?key=SUA_API_KEY&token=SEU_TOKEN"
```

**Se funcionar:**
- ✅ Você verá um JSON com seus boards
- ✅ As credenciais estão CORRETAS!

**Se der erro 401:**
- ❌ API Key ou Token incorretos
- ❌ Copie novamente com mais cuidado

---

## 🎯 Teste no Sistema

Depois de obter as credenciais corretas:

```bash
cd /Users/davidgabriel/projetos/disparador-email

# Edite o arquivo e cole suas credenciais
nano testar_credenciais_trello.py

# Execute o teste
.venv/bin/python3 testar_credenciais_trello.py
```

---

## ⚠️ Erros Comuns

### Erro: "invalid key"
**Causa:** API Key incorreta
**Solução:** 
- Volte em https://trello.com/power-ups/admin
- Entre na sua Power-Up
- Copie a API Key INTEIRA (32 caracteres)
- Não deixe espaços no início/fim

### Erro: "unauthorized token"
**Causa:** Token incorreto ou expirado
**Solução:**
- Gere um NOVO token
- Clique em "manually generate a Token"
- Autorize novamente
- Copie o token INTEIRO (64 caracteres)

### Erro: "token expired"
**Causa:** Token com prazo de validade venceu
**Solução:**
- Ao gerar novo token, escolha "never" (nunca expirar)

---

## 📞 Checklist Final

Antes de testar no sistema, confirme:

- [ ] Está logado na conta CORRETA do Trello
- [ ] Criou uma Power-Up (ou tem acesso a uma existente)
- [ ] Copiou a API Key COMPLETA (32 caracteres)
- [ ] Gerou o Token NOVO (não use um antigo)
- [ ] Autorizou o Token (clicou em "Allow")
- [ ] Copiou o Token COMPLETO (64 caracteres)
- [ ] Não há espaços ou quebras de linha
- [ ] Testou com curl e funcionou

---

## 🎉 Próximos Passos

Quando as credenciais funcionarem:

1. ✅ Sistema vai listar seus boards
2. ✅ Você copia o Board ID do "lancamento-nf"
3. ✅ Sistema vai listar as listas desse board
4. ✅ Você copia o List ID da lista "Pendente"
5. ✅ Sistema cria cards automaticamente quando baixar notas fiscais

---

## 💡 Dica Extra: Teste Manual com curl

```bash
# Substitua pelos seus valores reais
API_KEY="sua_api_key_aqui"
TOKEN="seu_token_aqui"

# Teste 1: Listar seus boards
curl "https://api.trello.com/1/members/me/boards?key=$API_KEY&token=$TOKEN"

# Se funcionou, teste 2: Ver detalhes de um board específico
# (use um ID que apareceu no resultado acima)
BOARD_ID="id_do_board"
curl "https://api.trello.com/1/boards/$BOARD_ID?key=$API_KEY&token=$TOKEN"

# Teste 3: Listar listas do board
curl "https://api.trello.com/1/boards/$BOARD_ID/lists?key=$API_KEY&token=$TOKEN"

# Teste 4: Criar um card de teste
LIST_ID="id_da_lista"
curl -X POST "https://api.trello.com/1/cards?key=$API_KEY&token=$TOKEN" \
  -d "idList=$LIST_ID" \
  -d "name=Card de Teste" \
  -d "desc=Testando a API"
```

Se TODOS esses comandos funcionarem, sua API está 100% configurada! 🚀
