import streamlit as st
import pandas as pd
import json
import io
from core.analise_solo import calcular_saturacao_bases, calcular_ctc
from core.calagem import calcular_necessidade_calagem
from core.adubacao import recomendar_n, recomendar_p, recomendar_k
from core.utils import validar_parametros_entrada, formatar_resultados

# Carrega dados de culturas
@st.cache_data
def carregar_culturas(caminho="data/culturas.json"):
    with open(caminho, "r") as f:
        return json.load(f)

# Gera arquivo Excel com os dados
def gerar_excel_resultado(dados_entrada, resultados):
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        pd.DataFrame([dados_entrada]).to_excel(writer, sheet_name="Entrada", index=False)
        pd.DataFrame([resultados]).to_excel(writer, sheet_name="Recomendação", index=False)
    buffer.seek(0)
    return buffer

# App principal
def main():
    st.set_page_config(page_title="AgroAssist", layout="wide")
    st.title("🌱 Agro Assistente — Recomendação Agronômica")

    culturas = carregar_culturas()

    col1, col2 = st.columns(2)
    with col1:
        cultura = st.selectbox("🧬 Selecione a cultura", list(culturas.keys()))
    with col2:
        produtividade = st.number_input("🎯 Produtividade esperada (kg/ha)", min_value=0, value=100, step=1)

    st.markdown("### 🧪 Análise de Solo")
    with st.form("formulario"):
        ca = st.number_input("Cálcio (Ca²⁺ - cmolc/dm³)", min_value=0.0, format="%.2f", value=2.0)
        mg = st.number_input("Magnésio (Mg²⁺ - cmolc/dm³)", min_value=0.0, format="%.2f", value=0.8)
        k = st.number_input("Potássio (K⁺ - cmolc/dm³)", min_value=0.0, format="%.2f", value=0.2)
        al = st.number_input("Alumínio (Al³⁺ - cmolc/dm³)", min_value=0.0, format="%.2f", value=1.2)
        p = st.number_input("Fósforo (P - mg/dm³)", min_value=0.0, format="%.2f", value=8.0)
        prnt_percent = st.number_input("PRNT do calcário (%)", min_value=0.0, max_value=100.0, value=80.0, step=1.0)

        submitted = st.form_submit_button("📊 Calcular Recomendação")

    if submitted:
        try:
            validar_parametros_entrada(ca=ca, mg=mg, k=k, al=al, p_mehlich=p, produtividade=produtividade, prnt=prnt_percent / 100)
        except Exception as e:
            st.error(f"Erro nos dados de entrada: {e}")
            return

        dados_cultura = culturas[cultura]

        # Cálculos principais
        v_atual = calcular_saturacao_bases(ca, mg, k, al)
        ctc = calcular_ctc(ca, mg, k, al)
        calagem = calcular_necessidade_calagem(dados_cultura["v_percent_desejado"], v_atual, ctc, prnt_percent / 100)
        n = recomendar_n(produtividade, dados_cultura["n_por_produtividade"])
        p2o5 = recomendar_p(p, dados_cultura["faixas_p_mehlich"])
        k2o = recomendar_k(ca, mg, k, dados_cultura["faixas_sat_k"])

        resultados = formatar_resultados(calagem, n, p2o5, k2o)
        dados_entrada = {
            "Cultura": cultura,
            "Ca": ca, "Mg": mg, "K": k, "Al": al, "P": p,
            "PRNT (%)": prnt_percent,
            "Produtividade (kg/ha)": produtividade,
            "CTC": round(ctc, 2),
            "V atual (%)": round(v_atual, 2)
        }

        st.success("✅ Recomendação gerada com sucesso!")

        st.markdown("### 📋 Resultado da Recomendação")

        col1, col2 = st.columns(2)
        with col1:
            st.success(f"🌾 Calagem: **{resultados['calagem_t_ha']:.2f} t/ha**")
            st.info(f"🧪 Nitrogênio (N): **{resultados['nitrogenio_kg_ha']} kg/ha**")
        with col2:
            st.info(f"🟡 Fósforo (P₂O₅): **{resultados['fosforo_p2o5_kg_ha']} kg/ha**")
            st.info(f"🟠 Potássio (K₂O): **{resultados['potassio_k2o_kg_ha']} kg/ha**")

        st.markdown("### 📥 Baixar resultado (.xlsx)")
        excel_bytes = gerar_excel_resultado(dados_entrada, resultados)
        st.download_button(
            label="⬇️ Baixar Planilha",
            data=excel_bytes,
            file_name="recomendacao_agronomica.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

        st.markdown("---")
        st.caption("🔒 Pronto para integração com IA interpretativa (OpenAI) — em breve disponível!")

if __name__ == "__main__":
    main()
