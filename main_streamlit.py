import streamlit as st
import plotly.express as px
from backend import WeatherAnalyzer

st.set_page_config(
    page_title="Bjørn-Magne Weather Forecast",
    page_icon="favicon.ico",
)

logo_path = "bmklogo1.png"
st.image(logo_path, width=100, output_format="PNG")

st.markdown("<h1 style='text-align: center; color: #1f4e79;'>Weather Forecast</h1>",
            unsafe_allow_html=True)

city_name = st.text_input("Enter a city name:", "Lurøy")
forecast_days = st.slider("How many days in advance do you want to see the weather forecast?",
                          min_value=1, max_value=5,
                          help="Select the number of forecasted days.")
option = st.selectbox("Select data to view",
                      ("Temperature", "Humidity", "Pressure", "Sky", "Wind"))

analyzer = WeatherAnalyzer(city_name, forecast_days, option)
dates, data_values = analyzer.get_data()

st.markdown(
    f"<h2 style='text-align: center; color: #1f4e79;'>{option} for the next {forecast_days} days in {city_name}:</h2>",
    unsafe_allow_html=True
)

if option in ['Temperature', 'Humidity', 'Pressure', 'Wind']:
    figure = px.line(x=dates, y=data_values, labels={
                    "x": "Date", "y": option}, height=400, width=600)
    st.plotly_chart(figure)

elif option == 'Sky':
    dates, sky_data = analyzer.get_data()
    num_columns = 5
    columns = st.columns(num_columns)
    for i, sky_condition in enumerate(sky_data):
        image_path = analyzer.get_image_path(sky_condition)
        columns[i % num_columns].image(image_path, width=100)
