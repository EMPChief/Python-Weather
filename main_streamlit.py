import streamlit as st
import plotly.express as px
from backend import get_data
st.set_page_config(
    page_title="Bjørn-Magne Weather Forecast",
    page_icon="favicon.ico",
)
logo_path = "bmklogo1.png"
st.image(logo_path, width=100, output_format="PNG")

st.markdown("<h1 style='text-align: center; color: #1f4e79;'>Weather Forecast</h1>",
            unsafe_allow_html=True)

city_name = st.text_input("Enter a city name:", "Lurøy, NO")
forecast_days = st.slider("How many days in advance do you want to see the weather forecast?",
                          min_value=1, max_value=5,
                          help="Select the number of forecasted days.")
option = st.selectbox("Select data to view",
                      ("Temperature", "Humidity", "Pressure", "Sky", "Wind"))


dates, data_values = get_data(city_name, forecast_days, option)


st.markdown(
    f"<h2 style='text-align: center; color: #1f4e79;'>{option} for the next {forecast_days} days in {city_name}:</h2>",
    unsafe_allow_html=True
)

figure = px.line(x=dates, y=data_values, labels={
                 "x": "Date", "y": option}, height=600, width=1000)
st.plotly_chart(figure)
