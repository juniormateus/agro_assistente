import streamlit as st
import ee
import geemap.foliumap as geemap
import pandas as pd
import geopandas as gpd
import plotly.express as px
import tempfile
import os
from openpyxl import load_workbook
from openpyxl.drawing.image import Image as XLImage
import matplotlib.pyplot as plt

# Configuração da página
st.set_page_config(layout='wide')

# Inicializa o Earth Engine
try:
    ee.Initialize()
except Exception as e:
    ee.Authenticate()
    ee.Initialize()

st.title("🌧️ Análise Temporal de Precipitação")

st.markdown("""
### Como usar esta ferramenta

1. Envie um arquivo GeoJSON contendo a área que deseja analisar.
2. Selecione a data inicial e a data final para o período de análise.
3. Clique no botão **Analisar** para buscar e processar os dados de precipitação.
4. Visualize o gráfico e a tabela com os dados diários de chuva.
5. Se desejar, baixe o relatório em Excel com os dados e o gráfico gerados.
            
**Fonte dos dados:** [UCSB CHG CHIRPS Daily](https://developers.google.com/earth-engine/datasets/catalog/UCSB-CHG_CHIRPS_DAILY)
""")

# Upload do GeoJSON
geojson_file = st.file_uploader("🌎 Envie o arquivo GeoJSON com sua área de interesse", type=["geojson"])

if geojson_file:
    # Lê e prepara a geometria
    gdf = gpd.read_file(geojson_file)
    gdf = gdf.to_crs(epsg=4326)
    coords = gdf.geometry.iloc[0].__geo_interface__['coordinates']
    geom_type = gdf.geometry.iloc[0].geom_type

    if geom_type == 'Polygon':
        geometry = ee.Geometry.Polygon(coords)
    elif geom_type == 'MultiPolygon':
        geometry = ee.Geometry.MultiPolygon(coords)
    else:
        st.error("⚠️ O GeoJSON precisa conter um polígono ou multipolígono.")
        st.stop()

    # Intervalo de datas lado a lado
    st.markdown("### 📅 Selecione o intervalo de datas")
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Data inicial", pd.to_datetime("2024-01-01"))
    with col2:
        end_date = st.date_input("Data final", pd.to_datetime("2024-12-31"))

    if start_date >= end_date:
        st.warning("⚠️ A data inicial deve ser menor que a final.")
        st.stop()

    # Botão para analisar
    if st.button("Analisar"):
        # Consulta à coleção CHIRPS
        chirps = ee.ImageCollection("UCSB-CHG/CHIRPS/DAILY") \
            .filterDate(str(start_date), str(end_date)) \
            .filterBounds(geometry)

        def extract_precip(img):
            stats = img.reduceRegion(
                reducer=ee.Reducer.mean(),
                geometry=geometry,
                scale=5000,
                maxPixels=1e13
            )
            return ee.Feature(None, {
                'date': img.date().format("YYYY-MM-dd"),
                'precip': stats.get('precipitation')
            })

        features = chirps.map(extract_precip).filter(ee.Filter.notNull(['precip']))

        try:
            dates = features.aggregate_array("date").getInfo()
            precips = features.aggregate_array("precip").getInfo()
        except Exception as e:
            st.error("❌ Erro ao buscar dados do Earth Engine.")
            st.stop()

        if not dates or not precips or len(dates) != len(precips):
            st.warning("⚠️ Nenhum dado de precipitação encontrado para o período e área selecionados.")
            st.stop()

        # Monta o DataFrame
        df = pd.DataFrame({"date": pd.to_datetime(dates), "precip": precips})

        # Precipitação acumulada
        total_precip = df["precip"].sum()

        # Gráfico de linha
        st.markdown("### 📈 Precipitação Diária")
        fig = px.line(df, x="date", y="precip", labels={"precip": "Precipitação (mm)", "date": "Data"})
        st.plotly_chart(fig)

        # Tabela com valores
        st.markdown("### 📋 Tabela de Valores Diários")
        st.dataframe(df)

        # Total acumulado
        st.success(f"💧 Precipitação acumulada: **{total_precip:.2f} mm**")

        # Exportação para Excel com gráfico
        st.markdown("### 📥 Baixar Excel com dados e gráfico")

        with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp:
            excel_path = tmp.name
            df.to_excel(excel_path, index=False, sheet_name="Precipitação")

            # Salva gráfico como imagem temporária
            img_path = tempfile.NamedTemporaryFile(delete=False, suffix=".png").name
            plt.figure(figsize=(8, 4))
            plt.plot(df["date"], df["precip"], color='blue')
            plt.title("Precipitação Diária")
            plt.xlabel("Data")
            plt.ylabel("mm")
            plt.grid(True)
            plt.tight_layout()
            plt.savefig(img_path, format="png")
            plt.close()

            # Insere imagem no Excel
            wb = load_workbook(excel_path)
            ws = wb["Precipitação"]
            img = XLImage(img_path)
            img.anchor = "E2"
            ws.add_image(img)
            wb.save(excel_path)

            # Download button
            with open(excel_path, "rb") as f:
                st.download_button(
                    label="📄 Baixar Excel",
                    data=f,
                    file_name="precipitacao_diaria.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

else:
    st.info("Envie um arquivo GeoJSON válido para continuar.")
