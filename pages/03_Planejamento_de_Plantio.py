import streamlit as st
from core.espacamento_pop_plantas import (
    populacao_plantas,
    numero_plantas_area,
    espacamento_plantas_populacao_desejada,
    densidade_semeadura,
    numero_linhas,
    estimativa_producao
)

def formatar_numero(valor, casas_decimais=0):
    if abs(valor) < 1000:
        return f"{valor:.{casas_decimais}f}".replace(".", ",")
    else:
        return f"{valor:,.{casas_decimais}f}".replace(",", "X").replace(".", ",").replace("X", ".")

st.set_page_config(page_title="🌱 Planejamento de Plantio", layout="wide")
st.title("🌱 Planejamento de Plantio")

opcao = st.radio("Selecione o cálculo desejado:", [
    "População de plantas por hectare",
    "Número total de plantas por área",
    "Espaçamento entre plantas para população desejada",
    "Densidade de semeadura (kg/ha)",
    "Número de linhas de plantio por área",
    "Estimativa de produção total"
])

st.markdown("---")

if opcao == "População de plantas por hectare":
    st.subheader("🌿 População de plantas por hectare")
    espac_linhas = st.number_input("Espaçamento entre linhas (m)", min_value=0.1, step=0.1, format="%.2f")
    espac_plantas = st.number_input("Espaçamento entre plantas (m)", min_value=0.1, step=0.1, format="%.2f")

    if espac_linhas > 0 and espac_plantas > 0:
        pop = populacao_plantas(espac_linhas, espac_plantas)
        st.success(f"🌿 População estimada: **{formatar_numero(pop)} plantas/ha**")

elif opcao == "Número total de plantas por área":
    st.subheader("🌾 Total de plantas por área")
    populacao = st.number_input("População (plantas/ha)", min_value=1.0, step=1.0, format="%.0f")
    area = st.number_input("Área (ha)", min_value=0.01, step=0.01, format="%.2f")

    if populacao > 0 and area > 0:
        total = numero_plantas_area(populacao, area)
        st.success(f"🌾 Total de plantas: **{formatar_numero(total)} plantas**")

elif opcao == "Espaçamento entre plantas para população desejada":
    st.subheader("📏 Espaçamento para população desejada")
    pop_desejada = st.number_input("População desejada (plantas/ha)", min_value=1.0, step=1.0, format="%.0f")
    espac_linhas2 = st.number_input("Espaçamento entre linhas (m)", min_value=0.1, step=0.1, format="%.2f")

    if pop_desejada > 0 and espac_linhas2 > 0:
        espacamento = espacamento_plantas_populacao_desejada(pop_desejada, espac_linhas2)
        st.success(f"📏 Espaçamento entre plantas: **{formatar_numero(espacamento, 2)} m**")

elif opcao == "Densidade de semeadura (kg/ha)":
    st.subheader("🌰 Densidade de Semeadura")
    pms = st.number_input("Peso de mil sementes (g)", min_value=1.0, step=1.0, format="%.1f")
    pop_desejada = st.number_input("População desejada (plantas/ha)", min_value=100.0, step=100.0, format="%.0f")
    germinacao = st.number_input("Taxa de germinação (%)", min_value=1.0, max_value=100.0, step=1.0, format="%.0f")

    if pms > 0 and pop_desejada > 0 and germinacao > 0:
        densidade = densidade_semeadura(pms, pop_desejada, germinacao)
        st.success(f"🌱 Densidade de semeadura: **{formatar_numero(densidade, 2)} kg/ha**")

elif opcao == "Número de linhas de plantio por área":
    st.subheader("📏 Número de Linhas na Área")
    area_ha = st.number_input("Área (ha)", min_value=0.01, step=0.01, format="%.2f")
    espac_linha = st.number_input("Espaçamento entre linhas (m)", min_value=0.1, step=0.1, format="%.2f")
    comprimento = st.number_input("Comprimento de cada linha (m)", min_value=1.0, step=1.0, format="%.1f")

    if area_ha > 0 and espac_linha > 0 and comprimento > 0:
        n_linhas = numero_linhas(area_ha, espac_linha, comprimento)
        st.success(f"📐 Número estimado de linhas: **{formatar_numero(n_linhas, 0)} linhas**")

elif opcao == "Estimativa de produção total":
    st.subheader("📦 Estimativa de Produção")
    populacao_total = st.number_input("Número total de plantas", min_value=1.0, step=1.0, format="%.0f")
    produtividade = st.number_input("Produtividade por planta (kg/planta)", min_value=0.01, step=0.01, format="%.2f")

    if populacao_total > 0 and produtividade > 0:
        producao = estimativa_producao(populacao_total, produtividade)
        st.success(f"📦 Estimativa total de produção: **{formatar_numero(producao, 2)} kg**")

st.markdown("---")