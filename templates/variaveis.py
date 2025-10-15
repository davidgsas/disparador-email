import streamlit as st

def mostrar_variaveis_disponiveis():
    """Adiciona uma seção na interface mostrando as variáveis disponíveis para templates de email."""
    with st.expander("ℹ️ Variáveis Disponíveis para Templates"):
        st.markdown("""
        ### 📧 Email para Prestadores
        Estas variáveis podem ser usadas no assunto e corpo do email:
        - `{{nome_prestador}}` - Nome do prestador
        - `{{periodo}}` - Período do serviço
        - `{{link}}` - Link para upload de arquivos (gerado automaticamente)

        ### 📧 Email para Montadores
        Estas variáveis podem ser usadas no assunto e corpo do email:
        - `{{nome_montador}}` - Nome do montador
        - `{{periodo_relatorio}}` - Período do relatório
        - `{{link}}` - Link para upload de arquivos (gerado automaticamente)
        - `{{total_geral}}` - Valor total do pagamento
        - `{{total_comissao}}` - Valor da comissão
        - `{{total_auxilio}}` - Valor do auxílio
        - `{{percentual_comissao}}` - Percentual de comissão (%)
        """)
        
        st.markdown("""
        ### 💡 Como usar
        1. Copie a variável desejada (incluindo as chaves duplas)
        2. Cole no campo de assunto ou corpo do email
        3. A variável será substituída pelo valor correspondente ao enviar o email
        
        **Exemplo para Montador:**
        ```
        Prezado {{nome_montador}},
        
        Seu relatório do período {{periodo_relatorio}} está pronto.
        Total a receber: R$ {{total_geral}}
        
        Para upload de documentos, acesse: {{link}}
        ```
        
        **Exemplo para Prestador:**
        ```
        Olá {{nome_prestador}},
        
        Segue o relatório do período {{periodo}}
        
        Link para envio de NF: {{link}}
        ```
        """)
