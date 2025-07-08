import streamlit as st
from core import chat_agro

st.set_page_config(layout="wide")

st.title("🌱 Chat Agronômico - Agroassistente")
#st.caption(
#    "💡 Limite de uso: são permitidas até 3 perguntas a cada 3 horas. "
#    "Essa restrição ajuda a garantir que o Agroassistente possa responder com qualidade e evitar sobrecarga no sistema."
#)

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
