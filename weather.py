import requests
import json
import config

class WeatherHandler:
    def __init__(self):
        super().__init__()
        self.link = f"http://api.openweathermap.org/data/2.5/find?q=(CITY, CONTRY)&type=like&APPID={config.WEATHER_TOKEN}"
    def GetWeather(self, city, country = None):
        temp_link = self.link.replace('CITY', city).replace("COUNTY", country)
        try:
            res = requests.get(temp_link)
            weather = res.json()