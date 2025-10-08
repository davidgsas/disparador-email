import streamlit as st

def mostrar_variaveis_disponiveis():
    """Adiciona uma seção na interface mostrando as variáveis disponíveis para templates de email."""
    with st.expander("ℹ️ Variáveis Disponíveis para Templates"):
        st.markdown("""
        ### 📧 Email para Prestadores
        Estas variáveis podem ser usadas no assunto e corpo do email:
        - `{{nome_prestador}}` - Nome do prestador
        - `{{periodo}}` - Período do serviço
        - `{{link_upload_nf}}` - Link único para upload da nota fiscal

        ### 📧 Email para Montadores
        Estas variáveis podem ser usadas no assunto e corpo do email:
        - `{{nome_montador}}` - Nome do montador
        - `{{periodo_relatorio}}` - Período do relatório
        - `{{link_upload_nf}}` - Link único para upload da nota fiscal
        """)
        
        st.markdown("""
        ### 💡 Como usar
        1. Copie a variável desejada (incluindo as chaves duplas)
        2. Cole no campo de assunto ou corpo do email
        3. A variável será substituída pelo valor correspondente ao enviar o email
        
        **Exemplo:**
        ```
        Prezado {{nome_montador}},
        
        Seu relatório do período {{periodo_relatorio}} está pronto.
        
        Para enviar a nota fiscal, acesse: {{link_upload_nf}}
        ```
        
        ### 📄 Upload de Nota Fiscal
        - `{{link_upload_nf}}` - Link único e seguro para upload da NF
        - Válido por 30 dias após geração
        - Aceita formatos: PDF, JPG, JPEG, PNG (máx. 10MB)
        - Cada pagamento gera um link exclusivo
        
        **Exemplo de uso no HTML:**
        ```html
        <a href="{{link_upload_nf}}" 
           style="background:#28a745; color:white; padding:10px 20px; text-decoration:none; border-radius:5px;">
            📤 ENVIAR NOTA FISCAL
        </a>
        ```
        """)
