import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import st_folium
from shapely.geometry import shape
from shapely.ops import unary_union
from fpdf import FPDF
import tempfile
import os
import requests
import simplekml

# Função para criar o KMZ a partir do GeoDataFrame
def create_kmz(gdf):
    kml = simplekml.Kml()
    for _, row in gdf.iterrows():
        geom = row.geometry
        if geom.geom_type == "Polygon":
            pol = kml.newpolygon(name="Área desenhada", outerboundaryis=list(geom.exterior.coords))
            pol.style.polystyle.color = simplekml.Color.changealphaint(100, simplekml.Color.green)
        elif geom.geom_type == "MultiPolygon":
            for part in geom.geoms:
                pol = kml.newpolygon(name="Área desenhada", outerboundaryis=list(part.exterior.coords))
                pol.style.polystyle.color = simplekml.Color.changealphaint(100, simplekml.Color.green)
    with tempfile.NamedTemporaryFile(suffix=".kmz", delete=False) as tmp:
        kml.savekmz(tmp.name)
        tmp.seek(0)
        kmz_data = tmp.read()
    os.remove(tmp.name)
    return kmz_data

# Função para criar imagem do mapa com área desenhada e basemap satélite com zoom out (buffer)
def create_map_image(geom):
    import matplotlib.pyplot as plt
    import contextily as ctx
    import geopandas as gpd

    gdf = gpd.GeoDataFrame(geometry=[geom], crs="EPSG:4326")
    gdf_webmerc = gdf.to_crs(epsg=3857)

    buffer_dist = 500  # metros para zoom out
    buffered_geom = gdf_webmerc.geometry.buffer(buffer_dist)

    fig, ax = plt.subplots(figsize=(6,6))
    buffered_geom.plot(ax=ax, alpha=0)  # invisível só para ajustar zoom
    gdf_webmerc.plot(ax=ax, alpha=0.5, edgecolor='red', facecolor='orange')

    minx, miny, maxx, maxy = buffered_geom.total_bounds
    ax.set_xlim(minx, maxx)
    ax.set_ylim(miny, maxy)

    ctx.add_basemap(ax, source=ctx.providers.Esri.WorldImagery)
    ax.axis('off')

    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp_img:
        fig.savefig(tmp_img.name, bbox_inches='tight', pad_inches=0)
        tmp_img.seek(0)
        img_bytes = tmp_img.read()

    plt.close(fig)
    os.remove(tmp_img.name)
    return img_bytes

# Função para criar PDF com dados, descrição e imagem
def create_pdf(area_ha, municipio, localidade, descricao="", image_bytes=None):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(0, 10, "Relatório da Área Desenhada", ln=True, align="C")
    pdf.ln(10)

    pdf.cell(0, 10, f"Área (ha): {area_ha:.2f}", ln=True)
    pdf.cell(0, 10, f"Município: {municipio}", ln=True)
    pdf.cell(0, 10, f"Localidade: {localidade if localidade else 'Não informada'}", ln=True)
    pdf.ln(10)

    if descricao:
        pdf.multi_cell(0, 10, f"Descrição / Inscrição da Área:\n{descricao}")
        pdf.ln(10)

    if image_bytes:
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp_img:
            tmp_img.write(image_bytes)
            tmp_img_path = tmp_img.name

        pdf.image(tmp_img_path, x=30, w=150)
        os.remove(tmp_img_path)

    pdf_bytes = bytes(pdf.output(dest='S'))
    return pdf_bytes

# Função para buscar município e localidade via Nominatim com campos expandidos
def reverse_geocode(lat, lon):
    url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lon}&zoom=10&addressdetails=1"
    try:
        response = requests.get(url, headers={'User-Agent': 'Agroassistente-App'})
        if response.status_code == 200:
            data = response.json()
            address = data.get("address", {})

            municipio = (
                address.get("city")
                or address.get("town")
                or address.get("municipality")
                or address.get("county")
                or "Não encontrado"
            )

            localidade = (
                address.get("suburb")
                or address.get("neighbourhood")
                or address.get("borough")
                or address.get("district")
                or address.get("quarter")
                or address.get("hamlet")
                or address.get("village")
                or ""
            )
            return municipio, localidade
        else:
            return "Não encontrado", ""
    except Exception:
        return "Não encontrado", ""

# --- Início da aplicação Streamlit ---

st.title("📐 Geoprocessamento e Análise de Área")

st.markdown("""
Desenhe a área de interesse no mapa ou faça upload de um arquivo KMZ.
Será calculada a área em hectares, e mostradas informações do município e localidade.
Você poderá exportar o arquivo KMZ com o polígono e um relatório PDF com as informações, descrição e imagem da área.
""")

basemap_option = st.radio(
    "Escolha o tipo de mapa base:",
    options=["Mapa com Labels (OpenStreetMap)", "Imagem de Satélite (Esri World Imagery)"]
)

uploaded_kmz = st.file_uploader("Upload de arquivo KMZ (opcional)", type=["kmz"])

geom = None
if uploaded_kmz:
    try:
        gdf = gpd.read_file(uploaded_kmz)
        geom = unary_union(gdf.geometry)
    except Exception as e:
        st.error(f"Erro ao ler KMZ: {e}")

st.subheader("Desenhe a área no mapa:")

m = folium.Map(location=[-23.5, -46.6], zoom_start=5)

if basemap_option == "Mapa com Labels (OpenStreetMap)":
    folium.TileLayer("OpenStreetMap").add_to(m)
else:
    folium.TileLayer(
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        attr="Esri",
        name="Esri Satellite",
        overlay=False,
        control=True
    ).add_to(m)

draw = folium.plugins.Draw(export=False)
draw.add_to(m)

output = st_folium(m, height=500, width=700, returned_objects=["all_drawings"])

if output and output.get("all_drawings") and output["all_drawings"]:
    try:
        geojson_draw = output["all_drawings"][0]["geometry"]
        geom = shape(geojson_draw)
    except Exception as e:
        st.error(f"Erro ao interpretar desenho: {e}")

if geom:
    gdf_geom = gpd.GeoDataFrame(geometry=[geom], crs="EPSG:4326")

    area_ha = gdf_geom.to_crs(epsg=5880).geometry.area.iloc[0] / 10000  # m² para hectares

    centroid = geom.centroid
    municipio, localidade = reverse_geocode(centroid.y, centroid.x)

    st.markdown(f"**Área Calculada:** {area_ha:.2f} hectares")
    st.markdown(f"**Município:** {municipio}")
    st.markdown(f"**Localidade:** {localidade if localidade else 'Não informada'}")

    # Campo para descrição
    descricao_area = st.text_area("📝 Descrição / Inscrição da Área", height=100)

    img_bytes = create_map_image(geom)
    kmz_bytes = create_kmz(gdf_geom)

    pdf_bytes = create_pdf(area_ha, municipio, localidade, descricao=descricao_area, image_bytes=img_bytes)

    col1, col2 = st.columns(2)
    with col1:
        st.download_button(
            label="📥 Baixar KMZ da Área",
            data=kmz_bytes,
            file_name="area_desenhada.kmz",
            mime="application/vnd.google-earth.kmz"
        )
    with col2:
        st.download_button(
            label="📥 Baixar PDF do Relatório",
            data=pdf_bytes,
            file_name="relatorio_area.pdf",
            mime="application/pdf"
        )
else:
    st.info("Desenhe uma área no mapa ou faça upload de um arquivo KMZ para iniciar.")
