import streamlit as st
from core.cotacoes_agricultura import consultar_preco_agricultura

st.set_page_config(page_title="🌽 Cotações Agrícolas", layout="centered")
st.title("🌽 Cotações Agrícolas - CEPEA")
st.markdown("Acompanhe os valores atualizados das principais commodities agrícolas segundo o CEPEA/ESALQ-USP.")

produtos_agricultura = [
    {"nome": "Milho", "unidade": "R$ / saca (60 kg)", "emoji": "🌽"},
    {"nome": "Soja", "unidade": "R$ / saca (60 kg)", "emoji": "🌱"},
    {"nome": "Algodão", "unidade": "R$ / kg", "emoji": "☁️"},
    {"nome": "Café arábica", "unidade": "R$ / saca (60 kg)", "emoji": "☕"},
    {"nome": "Trigo", "unidade": "R$ / tonelada", "emoji": "🌾"},
    {"nome": "Arroz", "unidade": "R$ / saca (50 kg)", "emoji": "🍚"},
]

for produto in produtos_agricultura:
    resultado = consultar_preco_agricultura(produto["nome"])
    with st.container():
        col1, col2 = st.columns([1, 2])
        with col1:
            st.markdown(f"### {produto['emoji']} {produto['nome']}")
        with col2:
            if "erro" in resultado:
                st.error(resultado["erro"])
            else:
                st.markdown(f"""
                <div style="font-size: 32px; font-weight: bold; color: #2E8B57;">
                    {resultado['preco']} {produto['unidade']}
                </div>
                <div style="font-size: 14px; color: #666;">
                    Cotação de {resultado['data']}
                </div>
                """, unsafe_allow_html=True)
        st.markdown("---")
