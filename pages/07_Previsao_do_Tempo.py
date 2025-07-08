import streamlit as st
import requests

st.set_page_config(layout="wide")
st.title("🌤️ Previsão do Tempo Agrícola (WeatherAPI)")

api_key = "650b9cde70eb461489823326252906"

cidade = st.text_input("Digite o nome da cidade:")

if st.button("Consultar Previsão") and cidade:
    url = f"http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={cidade}&days=3&lang=pt"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        st.subheader(f"📍 Previsão para {data['location']['name']}, {data['location']['region']}")

        cols = st.columns(3)
        alertas = []

        for idx, dia in enumerate(data["forecast"]["forecastday"]):
            temp_min = dia["day"]["mintemp_c"]
            temp_max = dia["day"]["maxtemp_c"]

            # Adiciona alertas
            if temp_min < 0:
                alertas.append(f"⚠️ Alerta de geada em {dia['date']}! Temperatura mínima: {temp_min}°C")
            if temp_max > 30:
                alertas.append(f"🔥 Alerta de calor intenso em {dia['date']}! Temperatura máxima: {temp_max}°C")

            with cols[idx]:
                date = dia["date"]
                condition = dia["day"]["condition"]["text"]
                icon_url = "http:" + dia["day"]["condition"]["icon"]
                chance_of_rain = dia["day"].get("daily_chance_of_rain", "N/A")
                humidity = dia["day"]["avghumidity"]
                wind_kph = dia["day"]["maxwind_kph"]

                st.markdown(f"### {date}")
                st.image(icon_url, width=80)
                st.write(f"🌡️ {temp_min}°C - {temp_max}°C")
                st.write(f"🌧️ Chuva: {chance_of_rain}%")
                st.write(f"💧 Umidade: {humidity}%")
                st.write(f"💨 Vento: {wind_kph} km/h")
                st.write(f"🌤️ {condition}")

        # Mostrar alertas, se houver
        if alertas:
            st.markdown("---")
            st.subheader("🚨 Alertas climáticos:")
            for alerta in alertas:
                st.warning(alerta)

    elif response.status_code == 400:
        st.error("Cidade não encontrada. Verifique o nome digitado.")
    elif response.status_code == 401:
        st.error("Chave da API inválida ou não autorizada.")
    else:
        st.error(f"Erro ao consultar a API: {response.status_code}")
