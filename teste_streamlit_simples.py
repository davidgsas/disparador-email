import streamlit as st

st.title("📱 WhatsApp - TESTE SIMPLES")
st.write("Se você está vendo isso, o Streamlit está funcionando!")

st.success("✅ Teste OK")

col1, col2 = st.columns(2)
col1.metric("Status", "Online")
col2.metric("Versão", "1.0")

if st.button("Clique aqui"):
    st.balloons()
    st.success("Botão funcionando!")
