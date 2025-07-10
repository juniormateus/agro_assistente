import streamlit as st
from fpdf import FPDF
import datetime
import tempfile

st.set_page_config(layout="wide")
st.title("📒 Caderno de Campo")

# Texto das instruções para o módulo
instrucoes_caderno = """
Este módulo permite o registro prático e organizado das atividades realizadas no campo. Você pode registrar:

- Data da atividade
- Cultura trabalhada
- Talhão ou área específica
- Tipo de atividade (plantio, pulverização, colheita, etc.)
- Produto ou insumo utilizado
- Condições climáticas durante a atividade
- Equipamento utilizado
- Observações gerais e importantes do dia a dia

Além disso, você pode anexar uma foto da atividade e adicionar uma assinatura (nome ou imagem) para validar o registro.

Após preencher os dados, é possível gerar um resumo da atividade e baixar um arquivo PDF para manter um histórico físico ou digital das operações no campo.

Use este caderno para facilitar o monitoramento, planejamento e a organização das informações no seu trabalho agrícola.
"""

def criar_pdf(data, cultura, talhao, atividade, produto, obs, condicoes, equipamento, assinante, assinatura_img_bytes, imagem_atividade_bytes):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Caderno de Campo - Registro Rápido", ln=True, align="C")
    pdf.ln(10)

    pdf.cell(0, 10, f"Data: {data.strftime('%d/%m/%Y')}", ln=True)
    pdf.cell(0, 10, f"Cultura: {cultura}", ln=True)
    pdf.cell(0, 10, f"Talhão ou Área: {talhao}", ln=True)
    pdf.cell(0, 10, f"Atividade: {atividade}", ln=True)
    pdf.cell(0, 10, f"Produto/Insumo: {produto if produto else 'Não informado'}", ln=True)
    pdf.cell(0, 10, f"Condições Climáticas: {condicoes if condicoes else 'Não informado'}", ln=True)
    pdf.cell(0, 10, f"Equipamento: {equipamento if equipamento else 'Não informado'}", ln=True)
    pdf.ln(5)
    pdf.multi_cell(0, 10, f"Observações: {obs if obs else 'Nenhuma'}")

    # Foto da atividade
    if imagem_atividade_bytes:
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp_img:
            tmp_img.write(imagem_atividade_bytes)
            tmp_img.flush()
            pdf.ln(10)
            pdf.cell(0, 10, "Foto da Atividade:", ln=True)
            pdf.image(tmp_img.name, w=150)

    pdf.ln(20)

    # Assinatura (imagem ou texto), centralizada
    if assinatura_img_bytes:
        with tempfile.NamedTemporaryFile(suffix=".png", delete=True) as tmp_sign:
            tmp_sign.write(assinatura_img_bytes)
            tmp_sign.flush()
            x_center = (210 - 60) / 2  # Centraliza imagem (A4 width = 210mm)
            pdf.cell(0, 10, "Assinatura:", ln=True, align='C')
            pdf.image(tmp_sign.name, x=x_center, w=60)
    elif assinante:
        pdf.cell(0, 10, "", ln=True)
        pdf.cell(0, 10, "Assinatura:", ln=True, align='C')
        pdf.set_font("Arial", style='I', size=12)
        pdf.cell(0, 10, assinante, ln=True, align='C')

    return pdf.output(dest='S').encode("latin-1")


# Criar as abas com ordem corrigida
tab1, tab2 = st.tabs(["Registro de Atividades", "Instruções"])

with tab1:
    # Inputs do usuário
    data = st.date_input("Data da atividade", value=datetime.date.today())
    cultura = st.text_input("Cultura", placeholder="Ex: Soja, Milho, Café")
    talhao = st.text_input("Talhão ou área", placeholder="Ex: Talhão 1, Lavoura sul")
    atividade = st.selectbox(
        "Tipo de atividade",
        ["Plantio", "Pulverização", "Adubação", "Calagem", "Colheita", "Outra"]
    )
    produto = st.text_input("Produto/insumo aplicado (opcional)", placeholder="Nome do defensivo, adubo etc.")
    condicoes = st.text_input("Condições climáticas (opcional)", placeholder="Ex: Ensolarado, vento fraco")
    equipamento = st.text_input("Equipamento utilizado (opcional)", placeholder="Ex: Pulverizador Costal")
    obs = st.text_area("Observações gerais", placeholder="Ex: Aplicação feita no fim da tarde, com vento fraco.")

    # Upload de imagem da atividade
    imagem_atividade = st.file_uploader("Anexar foto da atividade (opcional)", type=["png", "jpg", "jpeg"])

    # Assinatura opcional
    usar_assinatura = st.checkbox("Adicionar assinatura")
    assinante = ""
    assinatura_img_bytes = None
    if usar_assinatura:
        assinante = st.text_input("Nome para assinatura")
        assinatura_img = st.file_uploader("Ou envie imagem da assinatura (opcional)", type=["png", "jpg", "jpeg"])
        if assinatura_img is not None:
            assinatura_img_bytes = assinatura_img.read()

    if st.button("📄 Gerar Resumo da Atividade"):
        resumo = f"""
Data: {data.strftime('%d/%m/%Y')}
Cultura: {cultura}
Talhão/Área: {talhao}
Atividade: {atividade}
Produto/Insumo: {produto if produto else 'Não informado'}
Condições Climáticas: {condicoes if condicoes else 'Não informado'}
Equipamento: {equipamento if equipamento else 'Não informado'}
Observações: {obs if obs else 'Nenhuma'}
"""
        if usar_assinatura:
            resumo += f"\n✍️ Assinatura: {assinante if assinante else 'Imagem anexada' if assinatura_img_bytes else 'Nenhuma'}"

        st.success("Resumo da atividade gerado:")
        st.code(resumo)

        pdf_bytes = criar_pdf(
            data, cultura, talhao, atividade, produto, obs, condicoes, equipamento,
            assinante, assinatura_img_bytes, imagem_atividade.read() if imagem_atividade else None
        )

        st.download_button(
            label="📥 Baixar PDF do Caderno de Campo",
            data=pdf_bytes,
            file_name=f"caderno_campo_{data.strftime('%Y%m%d')}.pdf",
            mime="application/pdf"
        )

with tab2:
    st.markdown(instrucoes_caderno)
