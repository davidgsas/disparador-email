import streamlit as st
import os
import tempfile
from datetime import datetime
from database import validar_token_upload, marcar_token_usado, get_token_info_completa
import hashlib

def main():
    # Configuração da página
    st.set_page_config(
        page_title="Upload de Nota Fiscal",
        page_icon="📄",
        layout="centered",
        initial_sidebar_state="collapsed"
    )
    
    # CSS personalizado para deixar bonito
    st.markdown("""
    <style>
    .main-header {
        text-align: center;
        color: #1f77b4;
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 2rem;
        padding: 1rem;
        background: linear-gradient(90deg, #f0f8ff, #e6f3ff);
        border-radius: 10px;
        border: 2px solid #1f77b4;
    }
    
    .info-card {
        background: #f8f9fa;
        color: #333;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #28a745;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .info-card h3, .info-card h4 {
        color: #333 !important;
        margin-top: 0;
    }
    
    .info-card p, .info-card strong {
        color: #333 !important;
    }
    
    .warning-card {
        background: #fff3cd;
        color: #856404 !important;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #ffc107;
        margin: 1rem 0;
    }
    
    .warning-card h4, .warning-card p {
        color: #856404 !important;
    }
    
    .success-card {
        background: #d4edda;
        color: #155724 !important;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #28a745;
        margin: 1rem 0;
    }
    
    .success-card h3, .success-card p {
        color: #155724 !important;
    }
    
    .error-card {
        background: #f8d7da;
        color: #721c24 !important;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #dc3545;
        margin: 1rem 0;
    }
    
    .error-card p {
        color: #721c24 !important;
    }
    
    .upload-area {
        border: 2px dashed #1f77b4;
        border-radius: 10px;
        padding: 2rem;
        text-align: center;
        background: #fafafa;
        margin: 1rem 0;
        color: #333;
    }
    
    .upload-area h3 {
        color: #1f77b4 !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header principal
    st.markdown('<div class="main-header">📄 Upload de Nota Fiscal</div>', unsafe_allow_html=True)
    
    # Verificar se tem token na URL
    query_params = st.query_params
    token = query_params.get('token', None)
    
    if not token:
        st.markdown('<div class="error-card">❌ Token não fornecido. Verifique o link enviado por email.</div>', unsafe_allow_html=True)
        st.stop()
    
    # Validar token
    token_info = validar_token_upload(token)
    
    if not token_info:
        st.markdown('<div class="error-card">❌ Token inválido, expirado ou já utilizado.</div>', unsafe_allow_html=True)
        st.stop()
    
    # Obter informações completas
    info_completa = get_token_info_completa(token)
    
    # Mostrar informações do pagamento
    tipo_entidade = "Prestador" if token_info['tipo'] == 'prestador' else "Montador"
    
    st.markdown(f"""
    <div class="info-card">
        <h3>🎯 Informações do Pagamento</h3>
        <p><strong>{tipo_entidade}:</strong> {token_info['entidade_nome']}</p>
        <p><strong>Email:</strong> {token_info['entidade_email']}</p>
        <p><strong>Período:</strong> {info_completa.get('periodo', 'N/A')}</p>
        {f"<p><strong>Valor Total:</strong> R$ {info_completa['valor_total']:,.2f}</p>" if info_completa.get('valor_total') else ""}
        <p><strong>Válido até:</strong> {token_info['data_expiracao'].strftime('%d/%m/%Y às %H:%M')}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Área de upload
    st.markdown('<div class="upload-area">', unsafe_allow_html=True)
    st.markdown("### 📤 Faça o upload da sua Nota Fiscal")
    st.markdown("**Formatos aceitos:** PDF, JPG, JPEG, PNG (máximo 10MB)")
    
    uploaded_file = st.file_uploader(
        "Escolha o arquivo da nota fiscal",
        type=['pdf', 'jpg', 'jpeg', 'png'],
        help="Selecione um arquivo da nota fiscal em formato PDF ou imagem"
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    if uploaded_file is not None:
        # Validar tamanho do arquivo (10MB max)
        if uploaded_file.size > 10 * 1024 * 1024:
            st.markdown('<div class="error-card">❌ Arquivo muito grande. Tamanho máximo permitido: 10MB</div>', unsafe_allow_html=True)
            return
        
        # Mostrar informações do arquivo
        st.markdown(f"""
        <div class="info-card">
            <h4>📋 Informações do Arquivo</h4>
            <p><strong>Nome:</strong> {uploaded_file.name}</p>
            <p><strong>Tipo:</strong> {uploaded_file.type}</p>
            <p><strong>Tamanho:</strong> {uploaded_file.size / 1024:.1f} KB</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Botão de upload
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🚀 Confirmar Upload", type="primary", use_container_width=True):
                try:
                    # Criar diretório de upload se não existir
                    upload_dir = os.path.join("uploads", "notas_fiscais", token_info['tipo'], str(token_info['entidade_id']))
                    os.makedirs(upload_dir, exist_ok=True)
                    
                    # Gerar nome único para o arquivo
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    file_extension = uploaded_file.name.split('.')[-1].lower()
                    file_hash = hashlib.md5(uploaded_file.getvalue()).hexdigest()[:8]
                    
                    safe_filename = f"NF_{timestamp}_{file_hash}.{file_extension}"
                    file_path = os.path.join(upload_dir, safe_filename)
                    
                    # Salvar arquivo
                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.getvalue())
                    
                    # Marcar token como usado e obter info para notificação
                    token_info = marcar_token_usado(token, uploaded_file.name, file_path)
                    
                    # Enviar notificação automática
                    st.info("📧 Enviando notificação automática...")
                    try:
                        # Importar módulos necessários
                        from database import get_dados_para_notificacao
                        from notificacao_nf import enviar_notificacao_nf_upload, get_cached_access_token
                        
                        if token_info:
                            # Buscar dados do lote
                            dados_lote = get_dados_para_notificacao(token_info[0], token_info[1])
                            
                            # Tentar obter access_token via MSAL
                            access_token = get_cached_access_token()
                            
                            # Enviar notificação COM TOKEN DO CACHE - COM ANEXO
                            resultado = enviar_notificacao_nf_upload(token_info, dados_lote, uploaded_file.name, access_token, file_path)
                            
                            if resultado.get("success"):
                                st.success(f"📧 {resultado['message']}")
                                if resultado.get('emails'):
                                    st.info(f"📬 Email enviado para: {', '.join(resultado['emails'])}")
                            else:
                                # Mostrar que upload foi realizado mesmo se notificação falhou
                                st.info("✅ Upload realizado com sucesso!")
                                
                                if "preview" in resultado:
                                    st.warning("📧 Token expirado - Preview da notificação:")
                                    with st.expander("👁️ Ver detalhes da notificação que seria enviada", expanded=True):
                                        st.write(f"**Para:** {', '.join(resultado['preview']['para'])}")
                                        st.write(f"**Assunto:** {resultado['preview']['assunto']}")
                                        st.text_area("**Corpo:**", resultado['preview']['corpo'], height=150, disabled=True)
                                        if resultado['preview'].get('anexo'):
                                            st.write(f"**📎 Anexo:** {resultado['preview']['anexo']}")
                                    
                                    st.info("""
                                    **� Para reativar emails automáticos:**
                                    1. Acesse o sistema principal de gestão
                                    2. Faça login com sua conta Microsoft
                                    3. Os próximos uploads enviarão emails automaticamente
                                    """)
                                else:
                                    st.warning(f"⚠️ Problema com notificação: {resultado.get('message', 'Erro desconhecido')}")
                        else:
                            st.warning("⚠️ Não foi possível obter informações para notificação")
                            
                    except Exception as e:
                        st.warning(f"⚠️ Upload realizado! Erro na notificação: {str(e)}")
                        st.caption("💡 O upload foi concluído com sucesso, mas a notificação automática falhou.")
                    
                    
                    # Sucesso
                    st.markdown(f"""
                    <div class="success-card">
                        <h3>✅ Upload Realizado com Sucesso!</h3>
                        <p>Sua nota fiscal foi recebida e salva com segurança.</p>
                        <p><strong>Arquivo:</strong> {uploaded_file.name}</p>
                        <p><strong>Data/Hora:</strong> {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}</p>
                        <p><em>Este link não pode mais ser utilizado.</em></p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Balloons de celebração
                    st.balloons()
                    
                    # Instruções finais
                    st.markdown("""
                    <div class="info-card">
                        <h4>📞 Próximos Passos</h4>
                        <p>• Sua nota fiscal foi recebida e está sendo processada</p>
                        <p>• Em caso de dúvidas, entre em contato conosco</p>
                        <p>• Você pode fechar esta página</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                except Exception as e:
                    st.markdown(f'<div class="error-card">❌ Erro ao fazer upload: {str(e)}</div>', unsafe_allow_html=True)
    
    # Avisos importantes
    st.markdown("""
    <div class="warning-card">
        <h4>⚠️ Informações Importantes</h4>
        <p>• Este link é único e só pode ser usado uma vez</p>
        <p>• O link expira automaticamente após 30 dias</p>
        <p>• Certifique-se de que a nota fiscal está legível</p>
        <p>• Em caso de problemas, entre em contato conosco</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; font-size: 0.8rem;">
        <p>Sistema de Upload de Notas Fiscais - Novo Mundo</p>
        <p>Para suporte técnico, entre em contato conosco</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
