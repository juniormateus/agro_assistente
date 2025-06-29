# Agroassistente 🌱

**Projeto Open Source para auxiliar profissionais e produtores rurais com ferramentas digitais práticas e inteligentes.**

---

## Sobre o Agroassistente

O Agroassistente é uma aplicação web desenvolvida para facilitar o manejo agrícola por meio de módulos que oferecem desde previsão do tempo até análises geoespaciais e planejamento agronômico. A ideia é centralizar ferramentas úteis em um só lugar, tornando o dia a dia no campo mais eficiente e fundamentado em dados.

---

## Funcionalidades atuais

- **Previsão do Tempo**  
  Consulta a previsão do dia atual e dos próximos dois dias via API da Water API.

- **Caderno de Campo Rápido**  
  Registro de atividades diárias com informações como cultura, talhão, insumos aplicados, fotos e assinatura, com geração de PDF.

- **Conversor de Medidas**  
  Conversão de unidades comuns na área agronômica.

- **Calendário Agronômico**  
  Indicação da época ideal de plantio e colheita para culturas, com base na localização do usuário.

- **Planejamento de Plantio**  
  Cálculo da população de plantas por hectare e quantidade de sementes.

- **Adubação e Calagem**  
  Recomendações específicas baseadas na tonalidade do solo, cultura e produtividade esperada.

- **Aplicação Inteligente de Defensivos**  
  Cálculo de volume de calda, dose de produto e dose por tanque para aplicação eficiente.

- **Geoprocessamento**  
  Upload ou desenho manual de áreas para análise de parâmetros, com exportação em KMZ ou PDF.

- **Módulo de Notícias**  
  Atualizações sobre notícias relevantes para o setor agrícola.

---

## Tecnologias utilizadas

- [Streamlit](https://streamlit.io/) - Interface web
- Python 3.x
- APIs externas (Water API para previsão do tempo)
- Bibliotecas diversas para geoprocessamento e geração de PDFs

---

## Como rodar o projeto localmente

1. Clone o repositório:

   ```bash
   git clone https://github.com/seu_usuario/agroassistente.git
   cd agroassistente