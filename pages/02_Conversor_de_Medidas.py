# pages/02_🌡️_Conversor_de_Unidades.py

import streamlit as st
from core.conversor import (
    converter_volume,
    converter_peso,
    converter_area,
    converter_temperatura
)

st.set_page_config(page_title="Conversor de Unidades", page_icon="🔄")

st.title("🔄 Conversor de Unidades")
st.write("Converta unidades comuns no meio agrícola de forma prática!")

tipo = st.selectbox("📦 Qual tipo de unidade você quer converter?", [
    "Volume",
    "Peso/Massa",
    "Área",
    "Temperatura"
])

valor = st.number_input("Digite o valor a ser convertido:", min_value=0.0, format="%.4f")

if tipo == "Volume":
    opcoes = {
        "Mililitros (ml)": "ml",
        "Litros (l)": "l",
        "Metros cúbicos (m³)": "m3",
        "Galão (EUA)": "gal_us",
        "Galão (UK)": "gal_uk"
    }

    de = st.selectbox("De:", opcoes.keys())
    para = st.selectbox("Para:", opcoes.keys())

    if st.button("Converter"):
        resultado = converter_volume(valor, opcoes[de], opcoes[para])
        st.success(f"✅ {valor:.2f} {de} = {resultado:.2f} {para}")

elif tipo == "Peso/Massa":
    opcoes = {
        "Gramas (g)": "g",
        "Quilogramas (kg)": "kg",
        "Toneladas (t)": "t",
        "Arroba (15kg)": "arroba",
        "Saca de 60kg": "saca60",
        "Libras (lb)": "lb"
    }

    de = st.selectbox("De:", opcoes.keys())
    para = st.selectbox("Para:", opcoes.keys())

    if st.button("Converter"):
        resultado = converter_peso(valor, opcoes[de], opcoes[para])
        st.success(f"✅ {valor:.2f} {de} = {resultado:.2f} {para}")

elif tipo == "Área":
    opcoes = {
        "Metros quadrados (m²)": "m2",
        "Hectares (ha)": "ha",
        "Alqueire Paulista (~2,42 ha)": "alqueire_sp",
        "Alqueire Mineiro (~4,84 ha)": "alqueire_mg",
        "Acre": "acre"
    }

    de = st.selectbox("De:", opcoes.keys())
    para = st.selectbox("Para:", opcoes.keys())

    if st.button("Converter"):
        resultado = converter_area(valor, opcoes[de], opcoes[para])
        st.success(f"✅ {valor:.2f} {de} = {resultado:.2f} {para}")

elif tipo == "Temperatura":
    opcoes = {
        "Celsius (°C)": "c",
        "Fahrenheit (°F)": "f"
    }

    de = st.selectbox("De:", opcoes.keys())
    para = st.selectbox("Para:", opcoes.keys())

    if st.button("Converter"):
        resultado = converter_temperatura(valor, opcoes[de], opcoes[para])
        st.success(f"🌡️ {valor:.2f}°{de.upper()} = {resultado:.2f}°{para.upper()}")
