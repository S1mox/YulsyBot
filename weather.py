import requests
import config
import json
import logging

logging.basicConfig(filename="weather.log", filemode='w', level=logging.INFO)

class WeatherHandler:
    def __init__(self):
        super().__init__()
        self.link = f"http://api.openweathermap.org/data/2.5/weather?q=request&units=metric&APPID={config.WEATHER_TOKEN}"

    def GetWeather(self, city, country = None):
        request = city + (f",{country}" if country != None else '')
        temp_link = self.link.replace("request", request)

        try:
            res = requests.get(temp_link)
            weather = res.json()
            
            condition = weather['weather'][0]['description']
            temperature = weather['main']['temp']

            return {'temperature':temperature, 'condition':condition}

        except Exception as e:
            print("Exception (find):",e)
            logging.error(temp_link)
            logging.critical(weather)

# Tests
# handler = WeatherHandler()

# print(handler.GetWeather('Homel'))

# link_generate
# link = f"http://api.openweathermap.org/data/2.5/find?q=request&type=like&APPID={config.WEATHER_TOKEN}"
# request = 'Homel,BY'
# temp_link = link.replace("request", request)
# print(temp_link)