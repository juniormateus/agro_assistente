import streamlit as st
import json

st.set_page_config(page_title="Calendário Agronômico", page_icon="📅")

st.title("📅 Calendário Agronômico por Região")

# Carrega os dados do JSON
with open("data/calendario_agronomico.json", "r", encoding="utf-8") as f:
    dados = json.load(f)

# Interface
estados = list(dados.keys())
estado = st.selectbox("🌍 Selecione o estado", estados)

municipios = list(dados[estado].keys())
municipio = st.selectbox("🏙️ Selecione o município", municipios)

culturas = list(dados[estado][municipio].keys())
cultura = st.selectbox("🌱 Selecione a cultura", culturas)

if st.button("🔍 Consultar Calendário"):
    info = dados[estado][municipio][cultura]
    st.success(f"📍 {cultura.title()} em {municipio}, {estado}")
    st.markdown(f"""
    - **📆 Época de Plantio:** {info['plantio']}
    - **🌾 Época de Colheita:** {info['colheita']}
    """)
