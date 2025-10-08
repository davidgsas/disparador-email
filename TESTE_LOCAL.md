# 🏠 Guia para Testar o Sistema de Upload Localmente

## 🚀 Passo a Passo

### 1. **Preparar o Ambiente**
```bash
cd /Users/davidgabriel/projetos/disparador-email
source .venv/bin/activate
```

### 2. **Iniciar o Sistema Principal** (Terminal 1)
```bash
streamlit run streamlit_app.py
```
- Abrirá em: `http://localhost:8501`

### 3. **Iniciar o Servidor de Upload** (Terminal 2)
```bash
./start_upload_server.sh
```
- Abrirá em: `http://localhost:8502`

### 4. **Configurar URLs no Sistema**
1. No sistema principal (`localhost:8501`)
2. Vá em "Gerenciar Uploads NF" 
3. Seção "Configurações"
4. Configure URL como: `http://localhost:8502`

### 5. **Testar o Fluxo**
1. **Enviar um Pagamento:**
   - No sistema principal, processe um pagamento de prestador ou montador
   - O sistema gerará automaticamente um link único

2. **Verificar o Link:**
   - O link será algo como: `http://localhost:8502/?token=abc123xyz`
   - Copie este link

3. **Testar o Upload:**
   - Cole o link no navegador
   - Faça upload de um arquivo de teste (PDF, JPG, PNG)
   - Verifique se o upload foi bem-sucedido

4. **Verificar no Painel:**
   - Volte ao sistema principal
   - Vá em "Gerenciar Uploads NF"
   - Veja os uploads realizados

## 🔧 Configurações Locais

### Arquivo `.env.local`
```bash
AMBIENTE=local
UPLOAD_BASE_URL=http://localhost:8502
UPLOAD_HOST=localhost
UPLOAD_PORT=8502
```

### URLs do Sistema
- **Sistema Principal:** http://localhost:8501
- **Upload de NF:** http://localhost:8502
- **Links Gerados:** http://localhost:8502/?token=xxxxx

## 📋 Checklist de Teste

- [ ] Sistema principal rodando na porta 8501
- [ ] Servidor de upload rodando na porta 8502
- [ ] URL configurada como `http://localhost:8502`
- [ ] Processar um pagamento teste
- [ ] Link de upload gerado corretamente
- [ ] Upload de arquivo funcionando
- [ ] Arquivo salvo na pasta `uploads/`
- [ ] Status atualizado no painel administrativo

## 🐛 Solução de Problemas

### Erro: "Token não encontrado"
- Verifique se o link está completo com `?token=xxxxx`
- Certifique-se de que o servidor de upload está rodando

### Erro: "Conexão recusada"
- Verifique se ambos os servidores estão rodando
- Confirme as portas 8501 e 8502

### Erro: "psycopg2 não encontrado"
- Execute: `pip install psycopg2-binary`

### Links externos em vez de localhost
- Verifique as variáveis de ambiente
- Configure a URL no painel administrativo
- Reinicie o sistema principal

## 🎯 Resultado Esperado

Quando tudo estiver funcionando:
1. ✅ Emails terão links localhost para upload
2. ✅ Upload funcionará perfeitamente local
3. ✅ Arquivos serão salvos em `uploads/notas_fiscais/`
4. ✅ Status será atualizado no banco de dados
5. ✅ Painel mostrará estatísticas corretas

## 📞 Suporte

Se algo não funcionar, verifique:
1. Logs do terminal para erros
2. Portas disponíveis (8501 e 8502)
3. Permissões de escrita na pasta uploads/
4. Configurações de URL no sistema
