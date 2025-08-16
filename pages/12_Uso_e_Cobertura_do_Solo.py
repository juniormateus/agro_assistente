import streamlit as st
import ee
import geemap.foliumap as geemap
import geopandas as gpd
import pandas as pd
import plotly.express as px
import plotly.io as pio
import tempfile
import os
from openpyxl import Workbook
from openpyxl.drawing.image import Image as XLImage
from core.palete_biome import paleta_cores, paleta_nome, dicionario_classes

# Configuração da página
st.set_page_config(layout='wide')

# Inicializar o Earth Engine
ee.Initialize()

@st.cache_data
def carregar_imagem_mapbiomas(ano):
    image = ee.Image('projects/mapbiomas-public/assets/brazil/lulc/collection9/mapbiomas_collection90_integration_v1') \
             .select(f'classification_{ano}')
    return image

def calcular_estatisticas_area(image, geojson_fc):
    regiao = geojson_fc.geometry()
    area_image = ee.Image.pixelArea().divide(1e4).rename('area').addBands(image)
    stats = area_image.reduceRegion(
        reducer=ee.Reducer.sum().group(groupField=1, groupName='class'),
        geometry=regiao,
        scale=30,
        maxPixels=1e13
    )
    return stats.getInfo()

def ler_geojson_como_fc(uploaded_file):
    if uploaded_file is not None:
        gdf = gpd.read_file(uploaded_file)
        geojson = gdf.__geo_interface__
        feature_collection = ee.FeatureCollection(geojson)
        return feature_collection
    return None

def converter_para_dataframe(stats):
    area_data = []
    for group in stats.get('groups', []):
        class_value = group['class']
        class_name = dicionario_classes.get(class_value, str(class_value))
        area_ha = group['sum']
        area_data.append({
            'class': class_name,
            'area_ha': round(area_ha, 2)
        })
    df = pd.DataFrame(area_data)
    return df

def gerar_excel_completo(df, fig_pie, fig_bar):
    wb = Workbook()
    ws = wb.active
    ws.title = "Estatísticas"

    ws.append(['Classe', 'Área (ha)'])
    for idx, row in df.iterrows():
        ws.append([row['class'], row['area_ha']])

    pie_fd, pie_path = tempfile.mkstemp(suffix='.png')
    bar_fd, bar_path = tempfile.mkstemp(suffix='.png')

    os.close(pie_fd)
    os.close(bar_fd)

    pio.write_image(fig_pie, pie_path, format='png', scale=2)
    pio.write_image(fig_bar, bar_path, format='png', scale=2)

    ws2 = wb.create_sheet(title="Gráficos")
    img_pie = XLImage(pie_path)
    img_bar = XLImage(bar_path)

    img_pie.width, img_pie.height = 480, 360
    img_bar.width, img_bar.height = 480, 360

    ws2.add_image(img_pie, "A1")
    ws2.add_image(img_bar, "A20")

    tmp_excel_fd, tmp_excel_path = tempfile.mkstemp(suffix='.xlsx')
    os.close(tmp_excel_fd)
    wb.save(tmp_excel_path)

    os.remove(pie_path)
    os.remove(bar_path)

    return tmp_excel_path

st.title('🗺️ Análise de Uso e Cobertura do Solo (MapBiomas)')

st.markdown("""
### Como usar esta ferramenta

1. Escolha o ano desejado utilizando o controle deslizante no topo da página.
2. Na aba **Dados**, envie um arquivo GeoJSON com a área que deseja analisar.
3. Acesse a aba **Estatísticas** para visualizar a distribuição de uso e cobertura do solo por classe.
4. Veja os gráficos gerados (pizza e barras) para entender a proporção das classes.
5. Se quiser, baixe um relatório em Excel contendo os dados e os gráficos.
6. Na aba **Mapa**, visualize a classificação de uso do solo na sua área de estudo para o ano selecionado.

**Fonte dos dados:** [MapBiomas - Coleção 9](https://mapbiomas.org/colecoes-mapbiomas?cama_set_language=pt-BR)
""")

# Slider para seleção do ano com tooltip simples
ano_selecionado = st.slider(
    'Selecione o ano:', 
    min_value=1985, max_value=2022, value=2022, step=1,
    format="%d"
)

# Carregar imagem MapBiomas uma vez por ano selecionado
image_mapbiomas = carregar_imagem_mapbiomas(ano_selecionado)

# Criar mapa base (sem adicionar camadas ainda)
m = geemap.Map(center=[-14.2, -51.9], zoom=4)
m.add_basemap("SATELLITE")

# Abas para organizar a interface
tab_dados, tab_estatisticas, tab_mapa = st.tabs(["Dados", "Estatísticas", "Mapa"])

with tab_dados:
    uploaded_file = st.file_uploader('🌎 Envie o arquivo GeoJSON com sua área de interesse', type='geojson')
    if uploaded_file:
        st.success("Arquivo GeoJSON carregado. Agora vá para a aba 'Estatísticas' para ver os resultados.")

with tab_estatisticas:
    if uploaded_file is None:
        st.warning("Por favor, faça upload do arquivo GeoJSON na aba 'Dados' para continuar.")
    else:
        with st.spinner("Calculando estatísticas..."):
            geojson_fc = ler_geojson_como_fc(uploaded_file)
            if geojson_fc is None:
                st.error("Erro ao ler o arquivo GeoJSON.")
            else:
                stats = calcular_estatisticas_area(image_mapbiomas, geojson_fc)
                stats_df = converter_para_dataframe(stats)
                if stats_df.empty:
                    st.warning("Nenhuma estatística disponível para a área selecionada.")
                else:
                    st.dataframe(stats_df)

                    stats_df['color'] = stats_df['class'].map(paleta_nome)

                    fig_pie = px.pie(stats_df, names='class', values='area_ha', color='class',
                                     color_discrete_map=paleta_nome,
                                     title='Distribuição de áreas por classe')
                    fig_bar = px.bar(stats_df, x='class', y='area_ha',
                                     labels={'class': 'Classe', 'area_ha': 'Área (ha)'},
                                     title='Distribuição de Áreas por Classe',
                                     color='class', color_discrete_map=paleta_nome)

                    col1, col2 = st.columns(2)
                    with col1:
                        st.plotly_chart(fig_pie, use_container_width=True)
                    with col2:
                        st.plotly_chart(fig_bar, use_container_width=True)

                    if st.button("Exportar relatório Excel (.xlsx)"):
                        caminho_arquivo = gerar_excel_completo(stats_df, fig_pie, fig_bar)
                        with open(caminho_arquivo, 'rb') as f:
                            st.download_button(
                                label="Clique aqui para baixar o relatório",
                                data=f,
                                file_name=f'relatorio_uso_cobertura_{ano_selecionado}.xlsx',
                                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                            )

with tab_mapa:
    st.write(f"Visualização do uso e cobertura do solo para o ano {ano_selecionado}:")
    m.layers = []  # limpar camadas antigas para evitar duplicação
    m.addLayer(image_mapbiomas, {'palette': list(paleta_cores.values()), 'min': 0, 'max': 62}, f'Uso do Solo {ano_selecionado}')
    if uploaded_file is not None:
        geojson_fc = ler_geojson_como_fc(uploaded_file)
        if geojson_fc:
            m.centerObject(geojson_fc, 12)
            m.addLayer(geojson_fc, {}, "GeoJSON Layer")
    m.to_streamlit(height=600)
