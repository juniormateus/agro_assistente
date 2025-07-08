import streamlit as st
from core.dose_volume_cauda import (
    volume_calda, dose_produto, dose_tanque,
    diluicao_produto, numero_tanques, tempo_aplicacao
)

st.set_page_config(page_title="Doses de Defensivos Agrícolas", layout="wide")
st.title("Aplicação Inteligente de Defensivos 💧🧪")

opcao = st.radio(
    "Selecione o tipo de cálculo:",
    (
        "Volume total de calda",
        "Dose total de produto",
        "Dose por tanque",
        "Diluição do produto",
        "Número de tanques necessários",
        "Tempo estimado de aplicação",
    ),
)

st.divider()

if opcao == "Volume total de calda":
    st.subheader("💧 Volume total de calda (L)")

    with st.form("form_volume_calda"):
        col1, col2 = st.columns(2)
        with col1:
            vol_ha = st.number_input("🚜 Volume por hectare (L/ha)", min_value=0.0, format="%.2f", value=0.0, step=1.0)
        with col2:
            area_tratada = st.number_input("🌾 Área tratada (ha)", min_value=0.0, format="%.2f", value=0.0, step=1.0)

        submitted = st.form_submit_button("📊 Calcular")

        if submitted:
            if vol_ha == 0 or area_tratada == 0:
                st.warning("⚠️ Preencha todos os campos com valores maiores que zero.")
            else:
                resultado = volume_calda(vol_ha, area_tratada)
                st.success(f"✅ O volume total da calda será de **{resultado:.2f} Litros**.")

elif opcao == "Dose total de produto":
    st.subheader("🧪 Dose total de produto (mL ou g)")

    with st.form("form_dose_produto"):
        col1, col2 = st.columns(2)
        with col1:
            dose_recomendada = st.number_input("📏 Dose recomendada (ml/ha ou g/ha)", min_value=0.0, format="%.2f", value=0.0, step=1.0)
        with col2:
            area_tratada = st.number_input("🌱 Área tratada (ha)", min_value=0.0, format="%.2f", value=0.0, step=1.0)

        submitted = st.form_submit_button("📊 Calcular")

        if submitted:
            if dose_recomendada == 0 or area_tratada == 0:
                st.warning("⚠️ Preencha todos os campos com valores maiores que zero.")
            else:
                resultado = dose_produto(dose_recomendada, area_tratada)
                st.success(f"✅ A dose total de produto é **{resultado:.2f} mL ou g**, dependendo da formulação.")

elif opcao == "Dose por tanque":
    st.subheader("🔄 Dose por tanque")
    st.markdown("💡 *Use este cálculo caso trabalhe com dose por pulverizador e não por área total.*")

    with st.form("form_dose_tanque"):
        col1, col2, col3 = st.columns(3)
        with col1:
            dose_recomendada = st.number_input("📏 Dose recomendada (L/ha ou g/ha)", min_value=0.0, format="%.2f", value=0.0, step=1.0)
        with col2:
            volume_tanque = st.number_input("🛢️ Volume do tanque (L)", min_value=0.0, format="%.2f", value=0.0, step=1.0)
        with col3:
            volume_aplicacao = st.number_input("💦 Volume de aplicação por ha (L/ha)", min_value=0.0, format="%.2f", value=0.0, step=1.0)

        submitted = st.form_submit_button("📊 Calcular")

        if submitted:
            if dose_recomendada == 0 or volume_tanque == 0 or volume_aplicacao == 0:
                st.warning("⚠️ Preencha todos os campos com valores maiores que zero.")
            else:
                resultado = dose_tanque(dose_recomendada, volume_tanque, volume_aplicacao)
                st.success(f"✅ A dose total no tanque é de **{resultado:.2f} mL ou g**, conforme a formulação.")

elif opcao == "Diluição do produto":
    st.subheader("💦 Cálculo de Diluição do Produto")

    with st.form("form_diluicao_produto"):
        col1, col2, col3 = st.columns(3)
        with col1:
            volume_produto = st.number_input("🧴 Volume do produto concentrado disponível (L)", min_value=0.0, format="%.3f", value=0.0, step=0.1)
        with col2:
            concentracao = st.number_input("⚗️ Concentração desejada na calda (fração decimal, ex: 0.1 para 10%)", min_value=0.0, max_value=1.0, format="%.3f", value=0.1, step=0.01)
        with col3:
            volume_calda = st.number_input("💧 Volume final da calda a preparar (L)", min_value=0.0, format="%.2f", value=0.0, step=0.1)

        submitted = st.form_submit_button("📊 Calcular")

        if submitted:
            if volume_produto == 0 or concentracao == 0 or volume_calda == 0:
                st.warning("⚠️ Preencha todos os campos com valores maiores que zero.")
            elif concentracao > 1:
                st.warning("⚠️ A concentração deve estar entre 0 e 1.")
            else:
                resultado = diluicao_produto(volume_produto, concentracao, volume_calda)
                st.success(f"✅ Volume de água necessário para diluir: **{resultado:.2f} Litros**.")

elif opcao == "Número de tanques necessários":
    st.subheader("🔢 Cálculo do Número de Tanques Necessários")

    with st.form("form_numero_tanques"):
        col1, col2, col3 = st.columns(3)
        with col1:
            area_total = st.number_input("🌾 Área total a ser tratada (ha)", min_value=0.0, format="%.2f", value=0.0, step=1.0)
        with col2:
            volume_por_ha = st.number_input("🚜 Volume de calda por hectare (L/ha)", min_value=0.0, format="%.2f", value=0.0, step=1.0)
        with col3:
            volume_tanque = st.number_input("🛢️ Volume do tanque (L)", min_value=0.0, format="%.2f", value=0.0, step=1.0)

        submitted = st.form_submit_button("📊 Calcular")

        if submitted:
            if area_total == 0 or volume_por_ha == 0 or volume_tanque == 0:
                st.warning("⚠️ Preencha todos os campos com valores maiores que zero.")
            else:
                resultado = numero_tanques(area_total, volume_por_ha, volume_tanque)
                st.success(f"✅ Número de tanques necessários: **{resultado} tanques**.")

elif opcao == "Tempo estimado de aplicação":
    st.subheader("⏱ Cálculo do Tempo Estimado de Aplicação")

    with st.form("form_tempo_aplicacao"):
        col1, col2, col3 = st.columns(3)
        with col1:
            area_total = st.number_input("🌾 Área total a ser tratada (ha)", min_value=0.0, format="%.2f", value=0.0, step=1.0)
        with col2:
            velocidade = st.number_input("🚜 Velocidade média do equipamento (km/h)", min_value=0.0, format="%.2f", value=5.0, step=0.1)
        with col3:
            largura = st.number_input("📏 Largura da barra de aplicação (m)", min_value=0.0, format="%.2f", value=10.0, step=0.1)

        submitted = st.form_submit_button("📊 Calcular")

        if submitted:
            if area_total == 0 or velocidade == 0 or largura == 0:
                st.warning("⚠️ Preencha todos os campos com valores maiores que zero.")
            else:
                resultado = tempo_aplicacao(area_total, velocidade, largura)
                st.success(f"✅ Tempo estimado de aplicação: **{resultado:.2f} horas**.")
