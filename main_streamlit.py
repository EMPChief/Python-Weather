import streamlit as st
import plotly.express as px
from backend import WeatherAnalyzer
import requests

class WeatherApp:
    def __init__(self):
        st.set_page_config(
            page_title="Bjørn-Magne Weather Forecast",
            page_icon="favicon.ico",
        )

        self.logo_path = "bmklogo1.png"
        self.display_logo_and_title()

        self.city_name = st.sidebar.text_input("Enter a city name:", "Bergen")
        self.forecast_days = st.sidebar.slider("How many days in advance do you want to see the weather forecast?",
                                               min_value=1, max_value=5,
                                               help="Select the number of forecasted days.")
        self.option = st.sidebar.selectbox("Select data to view",
                                           ("Temperature", "Humidity", "Pressure", "Sky", "Wind"))
        self.analyzer = None

    def display_logo_and_title(self):
        st.image(self.logo_path, width=100, output_format="PNG")
        st.markdown("<h1 style='text-align: center; color: #1f4e79;'>Weather Forecast</h1>",
                    unsafe_allow_html=True)

    def run(self):
        try:
            self.analyzer = WeatherAnalyzer(self.city_name, self.forecast_days, self.option)
            dates, data_values = self.analyzer.get_data()

            self.display_header()

            if self.option in ['Temperature', 'Humidity', 'Pressure', 'Wind']:
                self.display_line_chart(dates, data_values)

            elif self.option == 'Sky':
                dates, sky_data = self.analyzer.get_data()
                self.display_sky_images(dates, sky_data)

        except requests.exceptions.RequestException as e:
            st.error(f"Error fetching weather data: {str(e)}")
        except KeyError as e:
            st.error(f"A city by this name does not exist: {str(e)}")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

    def display_header(self):
        st.markdown(
            f"<h2 style='text-align: center; color: #1f4e79;'>{self.option} for the next {self.forecast_days} days in {self.city_name}:</h2>",
            unsafe_allow_html=True
        )

    def display_line_chart(self, dates, data_values):
        figure = px.line(x=dates, y=data_values, labels={"x": "Date", "y": self.option}, height=400, width=600)
        st.plotly_chart(figure)

    def display_sky_images(self, dates, sky_data):
        num_columns = 5
        columns = st.columns(num_columns)
        for i, sky_condition in enumerate(sky_data):
            image_path = self.analyzer.get_image_path(sky_condition)
            columns[i % num_columns].image(image_path, width=100)

if __name__ == "__main__":
    weather_app = WeatherApp()
    weather_app.run()
