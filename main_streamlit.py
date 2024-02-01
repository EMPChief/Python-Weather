import streamlit as st
import plotly.express as px

st.set_page_config(
    page_title="Bjørn-Magne Weather Forecast",
    page_icon="favicon.ico",
)

logo_path = "bmklogo1.png"
st.image(logo_path, width=100, output_format="PNG")

st.markdown("<h1 style='text-align: center; color: #1f4e79;'>Weather Forecast</h1>",
            unsafe_allow_html=True)

city_name = st.text_input("Enter a city name:", "Bergen")
forecast_days = st.slider("How many days in advance do you want to see the weather forecast?",
                          min_value=1, max_value=5,
                          help="Select the number of forecasted days.")
option = st.selectbox("Select data to view",
                      ("Temperature", "Humidity", "Wind Speed", "Sky"))

def get_weather_data(days):
    dates = ["2022-10-25", "2022-11-25", "2022-12-25"]
    temperatures = [10, 11, 15]
    temperatures = [days * temp for temp in temperatures]
    return dates, temperatures

dates, data_values = get_weather_data(forecast_days)

st.markdown(
    f"<h2 style='text-align: center; color: #1f4e79;'>{option} for the next {forecast_days} days in {city_name}:</h2>",
    unsafe_allow_html=True
)

figure = px.line(x=dates, y=data_values, labels={
                 "x": "Date", "y": option}, height=600, width=1000)
st.plotly_chart(figure)
