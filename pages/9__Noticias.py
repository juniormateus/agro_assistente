import streamlit as st
import requests
from datetime import datetime

st.set_page_config(layout="wide")
st.title("📰 Notícias Recentes")

api_key = "3c542b01c1b44aadbbdc0475035633f1"

temas = {
    "Brasil": "brasil",
    "Agronegócio": "agronegócio",
    "Agricultura": "agricultura",
    "Clima": "clima",
    "Mercado": "mercado agrícola"
}

cols = st.columns(len(temas))
tema_selecionado = None
for idx, (nome, query) in enumerate(temas.items()):
    if cols[idx].button(nome):
        tema_selecionado = query

if not tema_selecionado:
    tema_selecionado = temas["Agronegócio"]

def buscar_noticias(termo):
    url = (
        "https://newsapi.org/v2/everything?"
        f"q={termo}&"
        "language=pt&"
        "sortBy=publishedAt&"
        "pageSize=9&"
        f"apiKey={api_key}"
    )
    resposta = requests.get(url)
    if resposta.status_code == 200:
        return resposta.json().get("articles", [])
    else:
        st.error(f"Erro ao buscar notícias: {resposta.status_code}")
        return []

noticias = buscar_noticias(tema_selecionado)

st.write(f"Mostrando notícias para: **{tema_selecionado.capitalize()}**")

if noticias:
    cols = st.columns(3)
    for idx, art in enumerate(noticias):
        with cols[idx % 3]:
            st.markdown(f"### [{art['title']}]({art['url']})")
            if art.get("urlToImage"):
                st.image(art["urlToImage"], use_container_width=True)
            st.write(art.get("description", ""))
            data_pub = art.get("publishedAt")
            if data_pub:
                data_fmt = datetime.fromisoformat(data_pub.replace("Z", "+00:00")).strftime("%d/%m/%Y %H:%M")
                st.write(f"Fonte: {art['source']['name']} | 📅 {data_fmt}")
            else:
                st.write(f"Fonte: {art['source']['name']}")
            st.markdown("---")
else:
    st.info("Nenhuma notícia encontrada.")