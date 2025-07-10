import streamlit as st
from core import chat_agro

st.set_page_config(layout="wide")

st.title("👩‍🌾💬 Chat Agronômico")

tab1, tab2 = st.tabs(["Chat", "Instruções"])

with tab1:
    if "chat" not in st.session_state:
        st.session_state.chat = []

    with st.form(key="form_pergunta", clear_on_submit=True):
        pergunta = st.text_input("Faça sua pergunta ao Agroassistente:")
        enviar = st.form_submit_button("Enviar")

    if enviar and pergunta:
        ip_usuario = st.query_params.get("ip", ["127.0.0.1"])[0]
        resposta = chat_agro.perguntar_agronomo(pergunta, ip_usuario)
        st.session_state.chat.append(("Você", pergunta))
        st.session_state.chat.append(("Agrônomo", resposta))

    for autor, msg in st.session_state.chat:
        if autor == "Você":
            with st.chat_message("user"):
                st.markdown(msg)
        else:
            with st.chat_message("assistant"):
                st.markdown(msg)

with tab2:
    st.markdown("""
    ### Como usar esta ferramenta

    1. Digite sua dúvida relacionada à agronomia no campo abaixo e clique em **Enviar**.
    2. O Agroassistente responderá com base em informações técnicas e científicas.
    3. As conversas ficam salvas durante sua navegação, permitindo acompanhar o histórico de perguntas e respostas.

    💡 Este módulo pode ser usado para tirar dúvidas sobre adubação, pragas, doenças, manejo, clima, variedades, entre outros temas técnicos.

    **Observação:** As respostas são geradas por inteligência artificial e não substituem a recomendação de um agrônomo habilitado para situações específicas em campo.
    """)
