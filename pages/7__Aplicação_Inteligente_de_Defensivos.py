import streamlit as st
from core.dose_volume_cauda import volume_calda
from core.dose_volume_cauda import dose_produto
from core.dose_volume_cauda import dose_tanque

st.set_page_config(page_title="Doses de Defensivos Agrícolas", layout="wide")

# Volume total de calda ----------------------------------------------------
st.title("Aplicação Inteligente de Defensivos 💧🧪")
st.markdown("### 💧 Volume total de calda (L)")

with st.form("calculo_volume_calda"):
    col1, col2 = st.columns(2)
    with col1:
        vol_ha = st.number_input("🚜 Volume por hectare (L/ha)", min_value=0.0, format="%.2f", value=0.0, step=1.0)
    with col2:
        area_tratada1 = st.number_input("🌾 Área tratada (ha)", min_value=0.0, format="%.2f", value=0.0, step=1.0)

    submitted1 = st.form_submit_button("📊 Calcular")

    if submitted1:
        if vol_ha == 0 or area_tratada1 == 0:
            st.warning("⚠️ Preencha todos os campos com valores maiores que zero.")
        else:
            volume_total_calda = volume_calda(vol_ha, area_tratada1)
            st.success(f"✅ O volume total da calda será de **{volume_total_calda:.2f} Litros**.")

# Dose total de produto -----------------------------------------------------
st.markdown("### 🧪 Dose total de produto (em mL ou g)")

with st.form("calculo_dose_produto"):
    col1, col2 = st.columns(2)
    with col1:
        dose_recomendada = st.number_input("📏 Dose recomendada (ml/ha ou g/ha)", min_value=0.0, format="%.2f", value=0.0, step=1.0)
    with col2:
        area_tratada2 = st.number_input("🌱 Área tratada (ha)", min_value=0.0, format="%.2f", value=0.0, step=1.0)

    submitted2 = st.form_submit_button("📊 Calcular")

    if submitted2:
        if dose_recomendada == 0 or area_tratada2 == 0:
            st.warning("⚠️ Preencha todos os campos com valores maiores que zero.")
        else:
            dose_total_produto = dose_produto(dose_recomendada, area_tratada2)
            st.success(f"✅ A dose total de produto é **{dose_total_produto:.2f} mL ou g**, dependendo da formulação.")

# Dose por tanque -------------------------------------------------------------
st.markdown("### 🔄 Dose por tanque")
st.markdown("💡 *Use este cálculo caso trabalhe com dose por pulverizador e não por área total.*")

with st.form("calculo_dose_tanque"):
    col1, col2, col3 = st.columns(3)
    with col1:
        dose_recomendada_tanque = st.number_input("📏 Dose recomendada (L/ha ou g/ha)", min_value=0.0, format="%.2f", value=0.0, step=1.0)
    with col2:
        volume_tanque = st.number_input("🛢️ Volume do tanque (L)", min_value=0.0, format="%.2f", value=0.0, step=1.0)
    with col3:
        volume_aplicacao = st.number_input("💦 Volume de aplicação por ha (L/ha)", min_value=0.0, format="%.2f", value=0.0, step=1.0)

    submitted3 = st.form_submit_button("📊 Calcular")

    if submitted3:
        if dose_recomendada_tanque == 0 or volume_tanque == 0 or volume_aplicacao == 0:
            st.warning("⚠️ Preencha todos os campos com valores maiores que zero.")
        else:
            dose_total_tanque = dose_tanque(dose_recomendada_tanque, volume_tanque, volume_aplicacao)
            st.success(f"✅ A dose total no tanque é de **{dose_total_tanque:.2f} mL ou g**, conforme a formulação.")
