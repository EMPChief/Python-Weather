from flask import Flask, render_template, request, jsonify
import csv
import glob
from itertools import islice
import pandas as pd

    
class WeatherAPP:
    def __init__(self):
        self.app = Flask('WeatherAPP')
        self.data_path = 'weather_historic_data/'
        self.load_dictionary_data()
        self.routes()

    def load_dictionary_data(self):
        with open('dictionary.json', 'r') as f:
            csv_reader = csv.DictReader(f)
            self.dictionary_data = list(csv_reader)

    def run(self):
        self.app.run(host='0.0.0.0', port=3000, debug=True)

    def routes(self):
        @self.app.route('/')
        def index():
            return render_template('index.html')

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
            df = pd.read_csv(
                filename,
                skiprows=20,
                parse_dates=['    DATE'],
            )

            temperature = df.loc[df['    DATE'] == date].squeeze()['   TG'] / 10
            
            return {
                "station": station,
                "date": date,
                "temperature": temperature,
            }


if __name__ == '__main__':
    weather_app = WeatherAPP()
    weather_app.run()

