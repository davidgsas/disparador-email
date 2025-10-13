# ⚠️ CONFIGURAÇÃO TEMPORÁRIA - CERTIFICADO SSL

## 🔧 SITUAÇÃO ATUAL

O sistema externo (API DV Processamento) ainda **NÃO tem certificado SSL ativo**.

Por isso, temporariamente estamos usando:
- ✅ **HTTP** (ao invés de HTTPS)
- ✅ **verify_ssl=False** (não verifica certificado)

---

## 📝 O QUE FOI CONFIGURADO

### 1. URL da API

**Configuração Atual (TEMPORÁRIA):**
```python
API_URL = "http://api.link.dev.br/dvprocessamento/"
```

**Quando certificado estiver ativo, alterar para:**
```python
API_URL = "https://api.link.dev.br/dvprocessamento/"
```

### 2. Verificação SSL Desabilitada

**Configuração Atual:**
```python
verify_ssl = False  # Não verifica certificado
```

**Quando certificado estiver ativo, alterar para:**
```python
verify_ssl = True  # Verifica certificado
```

### 3. Avisos Suprimidos

Para não encher o console de avisos sobre SSL, adicionamos:
```python
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
```

---

## 🔄 QUANDO ALTERAR

### Sinais de que certificado está ativo:

1. ✅ Desenvolvedor externo confirma que SSL está configurado
2. ✅ URL passa a funcionar com HTTPS
3. ✅ Navegador não mostra aviso de "não seguro"

### Como atualizar:

**Arquivo:** `api_upload_client.py`

**Passo 1: Alterar URL (linha ~15)**
```python
# De:
API_URL = "http://api.link.dev.br/dvprocessamento/"

# Para:
API_URL = "https://api.link.dev.br/dvprocessamento/"
```

**Passo 2: Ativar verificação SSL (linha ~29)**
```python
# De:
def __init__(self, api_url=None, api_key=None, verify_ssl=False):

# Para:
def __init__(self, api_url=None, api_key=None, verify_ssl=True):
```

**Passo 3: (Opcional) Remover supressão de avisos (linhas ~8-10)**
```python
# Pode comentar ou remover estas linhas:
# import urllib3
# urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
```

---

## 🧪 TESTAR

### Teste 1: Verificar se HTTP funciona

```bash
curl http://api.link.dev.br/dvprocessamento/
```

Deve retornar alguma resposta (mesmo que erro 405 ou 404).

### Teste 2: Verificar se HTTPS está ativo

```bash
curl https://api.link.dev.br/dvprocessamento/
```

Se retornar erro de certificado, SSL ainda não está ativo.

### Teste 3: Via Python

```python
import requests

# Teste HTTP (deve funcionar)
resp = requests.get("http://api.link.dev.br/dvprocessamento/", verify=False)
print(f"HTTP Status: {resp.status_code}")

# Teste HTTPS (só funciona se certificado estiver ativo)
try:
    resp = requests.get("https://api.link.dev.br/dvprocessamento/", verify=True)
    print(f"HTTPS Status: {resp.status_code}")
    print("✅ Certificado SSL está ativo!")
except:
    print("❌ Certificado SSL ainda não está ativo")
```

---

## ⚠️ SEGURANÇA

### Por que desabilitar SSL é problemático?

- ❌ Dados trafegam sem criptografia
- ❌ Vulnerável a ataques man-in-the-middle
- ❌ Não recomendado para produção

### Por que está OK temporariamente?

- ✅ Apenas em desenvolvimento/homologação
- ✅ API interna (não exposta publicamente)
- ✅ Dados não são sensíveis (relatórios de serviço)
- ✅ Será corrigido quando certificado estiver ativo

### Quando NÃO usar HTTP:

- ❌ Em produção com dados sensíveis
- ❌ APIs públicas
- ❌ Dados de pagamento ou pessoais
- ❌ Após certificado estar disponível

---

## 📊 STATUS ATUAL

```
┌─────────────────────────────────────────────────────────┐
│ Configuração: HTTP (sem SSL)                            │
│ Motivo: Certificado ainda não está ativo               │
│ Quando mudar: Quando desenvolvedor confirmar SSL       │
│ Segurança: OK para desenvolvimento/homologação         │
│ Produção: Aguardar HTTPS funcionar                     │
└─────────────────────────────────────────────────────────┘
```

---

## 📧 COMUNICAÇÃO COM DESENVOLVEDOR

**Perguntar ao desenvolvedor externo:**

1. ❓ Quando o certificado SSL estará ativo?
2. ❓ A URL continuará sendo `api.link.dev.br`?
3. ❓ Precisarei fazer alguma configuração adicional?
4. ❓ Haverá período de testes antes de produção?

**Quando receber confirmação:**

✅ "Certificado SSL está ativo!"

➡️ Seguir passos da seção "QUANDO ALTERAR" acima

---

## 🔍 VERIFICAÇÃO NO NAVEGADOR

### HTTP (atual - sem SSL):
```
http://api.link.dev.br/dvprocessamento/envio-nf/...
```
- Navegador mostra: ⚠️ "Não seguro"
- Normal, é esperado

### HTTPS (futuro - com SSL):
```
https://api.link.dev.br/dvprocessamento/envio-nf/...
```
- Navegador mostra: 🔒 Cadeado (seguro)
- Certificado válido

---

## 📋 CHECKLIST

**Antes de ir para produção:**

- [ ] Confirmar com desenvolvedor que SSL está ativo
- [ ] Testar HTTPS no navegador (deve mostrar cadeado 🔒)
- [ ] Alterar URL para HTTPS no código
- [ ] Alterar verify_ssl para True
- [ ] Testar envio de lote com HTTPS
- [ ] Verificar logs (não deve ter avisos de SSL)
- [ ] Documentar mudança

---

## 💻 CÓDIGO ATUAL

### api_upload_client.py

```python
# CONFIGURAÇÃO TEMPORÁRIA
API_URL = "http://api.link.dev.br/dvprocessamento/"  # HTTP
verify_ssl = False  # Não verifica certificado

# Requisição
response = requests.post(
    self.api_url,
    json=payload,
    headers=headers,
    timeout=30,
    verify=self.verify_ssl  # False = aceita sem certificado
)
```

---

## 🎯 RESUMO

**AGORA (Temporário):**
- ✅ Usa HTTP (sem SSL)
- ✅ verify_ssl = False
- ✅ Funciona mesmo sem certificado
- ⚠️ Dados não criptografados

**DEPOIS (Definitivo):**
- ✅ Usará HTTPS (com SSL)
- ✅ verify_ssl = True
- ✅ Certificado validado
- ✅ Dados criptografados

---

## 📞 CONTATO

Se tiver dúvidas sobre quando ativar SSL:
- Perguntar ao desenvolvedor externo (Thiago Silva)
- Aguardar confirmação oficial
- Não ativar HTTPS antes de certificado estar pronto

---

**Data:** 13 de outubro de 2025  
**Status:** ✅ HTTP configurado (temporário)  
**Próximo passo:** Aguardar desenvolvedor ativar SSL
