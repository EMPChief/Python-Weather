from flask import Flask, render_template, request, jsonify
import json

"""
WeatherAPP class that initializes a Flask app, loads weather and dictionary data, 
defines routes and runs the Flask app.

Provides a REST API for retrieving weather data by station and date, and dictionary
definitions by word. Renders an index page.
"""


class WeatherAPP:
    def __init__(self):
        self.app = Flask('WeatherAPP')
        self.load_data()

    def load_data(self):
        with open('data.json', 'r') as f:
            self.weather_data = json.load(f)
        self.load_dictionary_data()

    def load_dictionary_data(self):
        with open('dictionary.json', 'r') as f:
            self.dictionary_data = json.load(f)

    def run(self):
        self.app.run(host='0.0.0.0', port=3000, debug=True)

    def routes(self):
        @self.app.route('/')
        def index():
            return render_template('index.html')

        @self.app.route("/api/dic/<word>")
        def get_dictionary(word):
            result = {
                'error': 'Word not found in database!'
            }
            for entry in self.dictionary_data.get("entries", []):
                if entry.get("word") == word:
                    result = entry
                    break
            return jsonify(result)

        @self.app.route("/api/weather/<station>/<date>")
        def get_weather(station, date):
            result = {
                "error": "Data not found!"
            }
            for entry in self.weather_data.get("weatherData", []):
                if entry.get("station") == station and entry["date"] == date:
                    result = entry
                    break
            return jsonify(result)


if __name__ == '__main__':
    weather_app = WeatherAPP()
    weather_app.routes()
    weather_app.run()
