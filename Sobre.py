import streamlit as st

def main():
    st.set_page_config(
        page_title="Agroassistente 🌱",
        page_icon="🌱",
        layout="wide"
    )

    # Título principal
    st.title("Agroassistente 🌱")
    
    st.markdown(
        """
        **Bem-vindo ao Agroassistente, um projeto open source pensado para facilitar o dia a dia do profissional e do produtor rural!**

        Aqui você encontra uma série de ferramentas inteligentes e práticas para apoiar suas decisões no campo.
        """
    )

    st.markdown("---")
    st.header("Funcionalidades atuais:")
    
    # Usando colunas para melhorar a visualização
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("⛅ Previsão do Tempo")
        st.write(
            "Conectado à API da Water API, oferece a previsão do tempo para o dia atual e os próximos dois dias, ajudando no planejamento das atividades."
        )
        st.subheader("📒 Caderno de Campo Rápido")
        st.write(
            "Registre facilmente dados importantes como cultura, talhão, atividades, insumos aplicados, condições climáticas, fotos e assinatura, e gere relatórios em PDF para controle e documentação."
        )
        st.subheader("📏 Conversor de Medidas")
        st.write("Ferramenta prática para converter unidades.")
        st.subheader("📅 Calendário Agronômico (Em desenvolvimento)")
        st.write(
            "Informe sua localização e escolha a cultura para receber as melhores épocas de plantio e colheita."
        )
        st.subheader("🌾 Planejamento de Plantio (Em desenvolvimento)")
        st.write(
            "Calcule a população ideal de plantas por hectare e a quantidade de sementes necessária para sua área."
        )
    
    with col2:
        st.subheader("💧 Adubação e Calagem (Em desenvolvimento)")
        st.write(
            "Insira os dados da análise de solo, cultura e produtividade esperada para receber recomendações específicas de adubação e calagem."
        )
        st.subheader("💨 Aplicação Inteligente de Defensivos")
        st.write(
            "Calcule o volume de calda, dose de produto e dose por tanque para uma aplicação mais eficiente e econômica."
        )
        st.subheader("🗺️ Geoprocessamento")
        st.write(
            "Faça o upload de arquivos KMZ ou desenhe manualmente uma área para obter parâmetros precisos de área e exportar relatórios em PDF ou KMZ com os dados e imagens."
        )
        st.subheader("📰 Módulo de Notícias")
        st.write(
            "Fique atualizado com as principais notícias da área agrícola para tomar decisões mais informadas."
        )

if __name__ == "__main__":
    main()