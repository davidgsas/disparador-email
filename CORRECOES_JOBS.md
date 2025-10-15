# 🐛 Correções Realizadas - Jobs Automáticos

## Data: 14/10/2025

### ❌ Problema 1: Crash do Scheduler no macOS

**Sintoma:**
```
*** multi-threaded process forked ***
crashed on child side of fork pre-exec
Exception Type: EXC_BAD_ACCESS (SIGSEGV)
```

**Causa:**
- macOS tem problemas com `fork()` em processos multi-threaded
- APScheduler usa threads, causando conflito ao fazer fork

**Solução:**
Adicionado configuração para usar `spawn` ao invés de `fork` no macOS:

```python
import multiprocessing

# CRÍTICO: Configurar método de spawn para evitar crashes no macOS
if sys.platform == 'darwin':  # macOS
    multiprocessing.set_start_method('spawn', force=True)
```

**Arquivo modificado:** `scheduler_service.py` (linha 15)

---

### ❌ Problema 2: Arquivos não sendo baixados (HTTP 406)

**Sintoma:**
- Jobs executando com sucesso
- Dados salvos no banco de dados
- Pastas criadas mas vazias
- Erro: `HTTP 406` ao tentar baixar arquivos

**Causa:**
- Mod_Security bloqueando requisições sem User-Agent
- Método `baixar_arquivo()` não enviava headers necessários
- Apenas as consultas tinham o User-Agent correto

**Solução:**
Adicionado headers no método de download:

```python
headers = {
    'User-Agent': 'NovoMundo-DisparadorEmail/1.0',
    'Accept': '*/*'
}

response = requests.get(
    link_download, 
    headers=headers,
    stream=True, 
    timeout=60,
    verify=False
)
```

**Arquivo modificado:** `consulta_nf_client.py` (linha 224-230)

---

## ✅ Resultados

### Antes:
- ❌ Scheduler crashava ao executar jobs
- ❌ Arquivos não eram baixados
- ❌ Pastas vazias

### Depois:
- ✅ Scheduler roda estável sem crashes
- ✅ Arquivos baixados com sucesso
- ✅ Arquivos salvos nas pastas corretas (`uploads/lote_XX/`)

### Teste de Validação:

```bash
# Ver arquivos baixados
ls -lh uploads/lote_*/

# Resultado:
lote_19: 232323.pdf (295K)
lote_20: 232323.pdf (295K)
lote_21: 232323.pdf (295K)
lote_22: Nf 12.pdf (96K)
lote_23: NOVO MUNDO DAVID GABRIEL NF 645.pdf (449K)
lote_24: Nf 12.pdf (96K)
```

---

## 🔍 Detecção dos Problemas

### Problema 1 - Crash:
1. Análise do crash report macOS
2. Identificação da mensagem `multi-threaded process forked`
3. Pesquisa sobre problemas conhecidos de fork no macOS com Python

### Problema 2 - Downloads:
1. Verificação dos logs do scheduler
2. Execução manual do job para debug
3. Identificação do HTTP 406 nas mensagens de erro
4. Análise do código de download vs código de consulta
5. Constatação da ausência de User-Agent no download

---

## 📝 Notas Técnicas

### macOS e Fork:
- macOS tem restrições mais rigorosas com fork em processos multi-threaded
- `spawn` é mais seguro mas mais lento (cria novo processo limpo)
- `fork` é rápido mas problemático com threads

### Mod_Security:
- Servidor web bloqueia requisições sem User-Agent identificável
- Necessário em TODAS as requisições HTTP:
  - Consultas à API ✅
  - Upload de dados ✅
  - **Download de arquivos** ✅ (agora corrigido)

---

## 🚀 Próximos Passos

1. ✅ **Monitorar execuções automáticas** - Verificar logs após 1-2 horas
2. ✅ **Validar notificações** - Confirmar que notificações são criadas
3. ✅ **Testar interface** - Ver arquivos no histórico do lote
4. ⏳ **Deployment em produção** - Configurar como serviço do sistema

---

## 🔧 Como Aplicar Correções

Se precisar aplicar manualmente:

```bash
# 1. Parar scheduler
python scheduler_service.py stop

# 2. Aplicar mudanças nos arquivos
# (já aplicadas automaticamente)

# 3. Reiniciar scheduler
python scheduler_service.py

# 4. Monitorar logs
tail -f scheduler.log
```

---

## 📚 Referências

- [Python multiprocessing contexts](https://docs.python.org/3/library/multiprocessing.html#contexts-and-start-methods)
- [macOS fork issues](https://bugs.python.org/issue33725)
- [Mod_Security User-Agent filtering](https://github.com/SpiderLabs/ModSecurity/wiki/Reference-Manual-(v2.x)#SecRule)
