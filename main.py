from flask import Flask, render_template, request, jsonify
import pandas as pd
import json
class WeatherAPP:
    def __init__(self):
        self.app = Flask('WeatherAPP')
        self.load_data()
    
    def load_data(self):
        with open('data.json', 'r') as f:
            self.weather_data = json.load(f)
    
    def run(self):
        self.app.run(host='0.0.0.0', port=3000, debug=True)
    
    def routes(self):
        @self.app.route('/')
        def index():
            return render_template('index.html')


        @self.app.route("/weather/<station>/<date>")
        def get_weather(station, date):
            result = {
                "error":"Data not found!"
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