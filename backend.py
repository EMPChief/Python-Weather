import os
import requests
import dotenv

dotenv.load_dotenv()

API_KEY = os.getenv("API_KEY")


class WeatherAnalyzer:
    def __init__(self, city_name, forecast_days=1, option=None):
        self.city_name = city_name
        self.forecast_days = forecast_days
        self.option = option

    def get_data(self):
        url = f"http://api.openweathermap.org/data/2.5/forecast?q={self.city_name}&appid={API_KEY}"
        data = requests.get(url).json()
        filtered_data = data["list"]
        nr_values = 8 * self.forecast_days
        filtered_data = filtered_data[:nr_values]

        if self.option:
            return self.filter_data(filtered_data)
        else:
            return filtered_data

    def filter_data(self, data):
        if self.option == "Temperature":
            return self.filter_temperature(data)
        elif self.option == "Pressure":
            return self.filter_pressure(data)
        elif self.option == "Humidity":
            return self.filter_humidity(data)
        elif self.option == "Sky":
            return self.filter_sky(data)
        elif self.option == "Wind":
            return self.filter_wind(data)
        else:
            return data

    def filter_temperature(self, data):
        return [entry["dt_txt"] for entry in data], [entry["main"]["temp"] for entry in data]

    def filter_pressure(self, data):
        return [entry["dt_txt"] for entry in data], [entry["main"]["pressure"] for entry in data]

    def filter_humidity(self, data):
        return [entry["dt_txt"] for entry in data], [entry["main"]["humidity"] for entry in data]

    def filter_sky(self, data):
        return [entry["dt_txt"] for entry in data], [entry["weather"][0]['main'] for entry in data]

    def filter_wind(self, data):
        return [entry["dt_txt"] for entry in data], [entry["wind"]["speed"] for entry in data]


if __name__ == "__main__":
    analyzer = WeatherAnalyzer(city_name="bergen", forecast_days=4, option="Sky")
    dates, data_values = analyzer.get_data()
    print(dates, data_values)
