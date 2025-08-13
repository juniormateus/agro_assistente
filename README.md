# 🌱 Agroassistente

**Agroassistente** é um projeto de estudos com foco em desenvolvimento de aplicações para o setor agro.  
Foi criado como uma forma de colocar em prática diversos conceitos de programação, incluindo:

- Estruturação de código com funções e modularização em múltiplos arquivos
- Criação de interfaces interativas com [Streamlit](https://streamlit.io/)
- Consumo de **APIs públicas** (como Water API e NEWSAPI)
- Implementação de **web scraping** (Dados CEPEA)
- Manipulação de dados com **Pandas**
- Geração de **relatórios em PDF**
- Visualização de mapas com **Folium**
- Integração com **Google Earth Engine** para análise espacial
- Boas práticas de versionamento com Git e GitHub

---

## 🚀 Funcionalidades Atuais

- 💬 **Chat Agronômico**  
  Converse com um assistente virtual treinado para responder dúvidas sobre agricultura, manejo, épocas de plantio e muito mais.

- ⛅ **Previsão do Tempo**  
  Conectada à Water API, exibe a previsão do tempo atual e dos próximos dois dias, auxiliando no planejamento de atividades agrícolas.

- 📒 **Caderno de Campo Rápido**  
  Registre informações da lavoura, como cultura, talhão, atividades realizadas, produtos aplicados, clima, imagens e assinatura. Gere relatórios organizados em PDF.

- 📏 **Conversor de Medidas**  
  Ferramenta prática para converter unidades utilizadas no contexto rural (metros, hectares, litros, etc.).

- 💨 **Aplicação Inteligente de Defensivos**  
  Calculadora de volume de calda, dose por tanque e dose por hectare para uma aplicação mais eficiente.

- 🗺️ **Geoprocessamento com NDVI**  
  Permite o upload de arquivos KMZ ou desenho manual de áreas no mapa. A aplicação consulta o Google Earth Engine, calcula o NDVI e gera relatórios com imagens e valores médios.

- 📈 **Cotações Agrícolas e Pecuárias**  
  Exibe preços atualizados de milho, soja, boi gordo, bezerro, suíno, frango e leite, com dados regionais quando disponíveis.

- 📰 **Módulo de Notícias**  
  Agrega e exibe as principais manchetes do setor agrícola para manter o usuário sempre bem informado.

- 🗺️ Módulo de NDVI
Permite analisar áreas específicas e calcular o NDVI médio para monitoramento de vegetação, com base em dados históricos ou atuais.

- 🌾 Módulo MapBiomas
Realiza análises de uso e ocupação do solo, permitindo ao produtor entender a cobertura e mudanças na sua área de interesse.

- 💧 Módulo de Precipitação
Consulta dados de precipitação diária acumulada, fornecendo informações precisas sobre a quantidade de chuva em uma área e período específicos.

---

## 🧪 Funcionalidades em Desenvolvimento

- 📅 **Calendário Agronômico**  
  Sugestão de épocas ideais de plantio e colheita com base em localização e cultura selecionada.

- 🌾 **Planejamento de Plantio**  
  Calculadora da população ideal de plantas por hectare e quantidade de sementes necessária.

- 💧 **Adubação e Calagem**  
  Geração de recomendações técnicas a partir de análise de solo, cultura e produtividade esperada.

---

## 📦 Tecnologias e Bibliotecas Utilizadas

- [Python](https://www.python.org/)
- [Streamlit](https://streamlit.io/)
- [FPDF](https://pyfpdf.readthedocs.io/)
- [Pandas](https://pandas.pydata.org/)
- [Folium](https://python-visualization.github.io/folium/)
- [Google Earth Engine](https://earthengine.google.com/)
- [Requests](https://docs.python-requests.org/) (para APIs e scraping)
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) (web scraping)
- Fastapi

---

## 💻 Como Rodar Localmente

### Pré-requisitos

- Python 3.8 ou superior
- Git instalado

### Passos

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/agro_assistente.git
cd agroassistente

# Crie e ative o ambiente virtual
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate      # Windows

# Instale as dependências
pip install -r requirements.txt

# Rode o app
streamlit run Home.py
