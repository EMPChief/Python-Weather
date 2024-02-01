from flask import Flask, render_template, request, jsonify
import csv
import json  # Import the json module
import pandas as pd

class WeatherAPP:
    def __init__(self):
        self.app = Flask('WeatherAPP')
        self.data_path = 'weather_historic_data/'
        self.load_dictionary_data()
        self.routes()

    def load_dictionary_data(self):
        with open('dictionary.json', 'r') as f:
            self.dictionary_data = json.load(f)
            if not isinstance(self.dictionary_data, list):
                raise ValueError("The 'entries' key is missing or not a list in dictionary.json")

    def run(self):
        self.app.run(host='0.0.0.0', port=3000, debug=True)

    def routes(self):
        @self.app.route('/')
        def index():
            st_filename = "weather_historic_data/stations.txt"
            stations = pd.read_csv(st_filename, skiprows=17)
            stations = stations[['STAID', 'STANAME                                 ']]
            context = stations
            return render_template('index.html', data=context.to_html())

        @self.app.route("/api/dic/<word>")
        def get_dictionary(word):
            result = {
                'error': 'Word not found in the database!'
            }
            for entry in self.dictionary_data:
                if entry.get("word") == word:
                    result = entry
                    break
            return jsonify(result)

        @self.app.route("/api/weather/<station>/<date>")
        def get_weather(station, date):
            filename = "weather_historic_data/TG_STAID" + str(station).zfill(6) + ".txt"
            dataframe = pd.read_csv(
                filename,
                skiprows=20,
                parse_dates=['    DATE'],
            )

            temperature = dataframe.loc[dataframe['    DATE'] == date].squeeze()['   TG'] / 10
            temperature_celsius = dataframe.loc[dataframe['    DATE'] == date].squeeze()['   TG'] / 10
            temperature_fahrenheit = (temperature_celsius * 9/5) + 32
            return {
                "station": station,
                "date": date,
                "temperature": temperature,
                "temperature_celsius": temperature_celsius,
                "temperature_fahrenheit": temperature_fahrenheit,
            }
        @self.app.route("/api/weather/<station>")
        def get_all_weather_data(station):
            filename = "weather_historic_data/TG_STAID" + str(station).zfill(6) + ".txt"
            dataframe = pd.read_csv(
                filename,
                skiprows=20,
                parse_dates=['    DATE'],
            )
            result = dataframe.to_dict(orient='records')
            return result
        
        @self.app.route("/api/years/weather/<station>/<year>")
        def annually_weather_data(station, year):
            filename = "weather_historic_data/TG_STAID" + str(station).zfill(6) + ".txt"
            dataframe = pd.read_csv(
                filename,
                skiprows=20,
                parse_dates=['    DATE'],
            )
            dataframe['year'] = dataframe['    DATE'].dt.year
            filtered_data = dataframe[dataframe['year'] == int(year)].to_dict(orient='records')
            
            return jsonify(filtered_data)

if __name__ == '__main__':
    weather_app = WeatherAPP()
    weather_app.run()
