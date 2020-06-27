from vk_api.longpoll import VkLongPoll, VkEventType

import vk_api
from googletrans import Translator

import requests
import json

import config

import logging


class MessageHandler:
  """ Класс работы с сообщениями """

  def __init__(self, vk_session):
    self.vk_session = vk_session
  
  def send_message(self, mtype, id, message = ' ', keyboard = None):
        """ Отправка сообщения из экземпляра MessageHandler
        
        keywords arguments:
        id -- id if receiver
        message -- message to receiver """
    
        if keyboard == None:
            self.vk_session.method('messages.send', values= {f"{mtype}":f'{id}', 'message': f"{message}", 'random_id':'0'})
        else:
            self.vk_session.method('messages.send', values= {f"{mtype}":f'{id}', 'message': f"{message}", 'random_id':'0', 'keyboard':f"{keyboard}"})

        logging.info(f"USER_ID: {id}; MESSAGE: {message.encode('utf-8')}")

class WeatherHandler:
    def __init__(self):
        """Конструктор создает шаблон ссылки для запроса"""
        super().__init__()
        self.link = f"http://api.openweathermap.org/data/2.5/weather?q=request&units=metric&APPID={config.WEATHER_TOKEN}"

    def GetWeather(self, city, country = None):
        """Получить погоду исходя из города (и страны) -> (dict('temperature':temp, 'condition':condition))
            
            keywords arguments:
            city -- город 
            country -- страна (необяз.)"""
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

class UserHandler:
    def __init__(self, vk_session):
        super().__init__()
        self.session = vk_session
    
    def GetUser(self, id):
        '''Возвращает JSON-объект с информацией о пользователе + город (id, название) -> JSON'''

        response = self.session.users.get(user_ids = id, fields = 'city')
        return response

class TranslateHandler:
    def __init__(self):
        super().__init__()
        self.translator = Translator()
    
    def Translate(self, dest = 'ru', text = ' '):
        result = self.translator.translate(text, dest=dest)
        logging.info(f"TRANSLATE {result.text} from {text} language {result.src}")
        return result.text