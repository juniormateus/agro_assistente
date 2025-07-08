import streamlit as st

st.set_page_config(
    page_title="Agroassistente 🌱",
    layout="wide",
    page_icon="🌱"
)

st.title("Agroassistente 🌱")
st.write(
    "Bem-vindo ao Agroassistente, um projeto open source pensado para facilitar o dia a dia do profissional e do produtor rural!\n\n"
    "Aqui você encontra uma série de ferramentas inteligentes e práticas para apoiar suas decisões no campo."
)

st.markdown("---")

st.header("Funcionalidades atuais")

st.markdown("""
- 💬 **Chat Agronômico**  
  Converse com um assistente virtual treinado para responder dúvidas sobre agricultura, manejo, épocas de plantio e muito mais. Ideal para produtores, técnicos e estudantes do setor agro.

- ⛅ **Previsão do Tempo**  
  Conectado à API da Water API, oferece a previsão do tempo para o dia atual e os próximos dois dias, ajudando no planejamento das atividades.

- 📒 **Caderno de Campo Rápido**  
  Registre facilmente dados importantes como cultura, talhão, atividades, insumos aplicados, condições climáticas, fotos e assinatura, e gere relatórios em PDF para controle e documentação.

- 📏 **Conversor de Medidas**  
  Ferramenta prática para converter unidades.

- 💨 **Aplicação Inteligente de Defensivos**  
  Calcule o volume de calda, dose de produto e dose por tanque para uma aplicação mais eficiente e econômica.

- 🗺️ **Geoprocessamento**  
  Faça o upload de arquivos KMZ ou desenhe manualmente uma área para obter parâmetros precisos de área e exportar relatórios em PDF ou KMZ com os dados e imagens.

- 📰 **Módulo de Notícias**  
  Fique atualizado com as principais notícias da área agrícola para tomar decisões mais informadas.
""")

st.markdown("---")

st.header("Futuras aplicações de desenvolvimento")

st.markdown("""
- 📅 **Calendário Agronômico**  *(em desenvolvimento)*  
  Informe sua localização e escolha a cultura para receber as melhores épocas de plantio e colheita.

- 🌾 **Planejamento de Plantio**  *(em desenvolvimento)*  
  Calcule a população ideal de plantas por hectare e a quantidade de sementes necessária para sua área.

- 💧 **Adubação e Calagem**  *(em desenvolvimento)*  
  Insira os dados da análise de solo, cultura e produtividade esperada para receber recomendações específicas de adubação e calagem.

- 📈 **Módulos de Cotações**  *(em desenvolvimento)*  
  Inclui cotação pecuária e cotação agricultura.
""")

st.markdown("---")
st.caption("Desenvolvido com 💚 para produtores e técnicos do agro")
