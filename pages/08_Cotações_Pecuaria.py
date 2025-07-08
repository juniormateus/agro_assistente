import streamlit as st
from core.cotacoes_cepea import consultar_preco_cepea

st.set_page_config(page_title="📉 Cotações Pecuárias", layout="centered")
st.title("📉 Cotações Pecuárias - CEPEA")
st.markdown("Acompanhe os valores atualizados das principais commodities pecuárias segundo o CEPEA/ESALQ-USP.")

produtos_pecuaria = [
    {"nome": "Boi Gordo", "unidade": "R$ / @ (15 kg)", "emoji": "🐂"},
    {"nome": "Bezerro - MS", "unidade": "R$ / cabeça", "emoji": "🐄"},
    {"nome": "Bezerro - SP", "unidade": "R$ / cabeça", "emoji": "🐄"},
    {"nome": "Frango", "unidade": "R$ / kg", "emoji": "🐓"},
    {"nome": "Leite (Brasil)", "unidade": "R$ / litro", "emoji": "🥛"},
]

for produto in produtos_pecuaria:
    resultado = consultar_preco_cepea(produto["nome"])
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
