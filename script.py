from vk_api.longpoll import VkLongPoll,VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

from datetime import datetime as time

import logging
import vk_api
import handlers
import config
import random

contributors = ['Seamo', 'Nyalen'] # Developers
logging.basicConfig(filename="Yul.log", filemode='a', level=logging.INFO)

def create_keyboard():
    """Создание клавиатуры в диалоге с пользователем """
    keyboard = VkKeyboard(one_time=True)

    keyboard.add_button('Помощь', color=VkKeyboardColor.DEFAULT)

    return keyboard.get_keyboard()

vk_session = vk_api.VkApi(token=config.VK_TOKEN)
session_api = vk_session.get_api()
longpoll = VkLongPoll(vk_session)

handler = handlers.MessageHandler(vk_session)  # помощник для работы с сообщениями
userHandler = handlers.UserHandler(session_api)
weatherHandler = handlers.WeatherHandler()
translateHandler = handlers.TranslateHandler()

logging.info(f"\n{'-' * 20}\n{'Session was started': ^20}")
logging.info(f"{time.now().strftime('%Y:%m:%d')}")

help_msg = f'Поиграй со мной >.<:\
  \n/flip - Подбрашивание монетки\
  \n/weather [City] - Узнать погоду в городе [City]\
  \n/random [a-b] - Случайное число от a до b\
  \n/translate [lang = ru: кодировка языка] [text] - Перевод текста на lang'

while True:                       # бесконечное прослушивание ответов с серверов VK
  for event in longpoll.listen():     # собирает события с прослушки
    if event.type == VkEventType.MESSAGE_NEW:      # если это новое сообщение, то =>
      message = event.text.lower()  # сохраняем сообщение пользователя
      command_string = message.split(' ')

      if event.from_user and not event.from_me:     # для диалога с пользователями
        try:
          keyboard = create_keyboard() # клавиатура для пользователя

          logging.info(f"{command_string}:{len(command_string)}")

          if message == 'начать':                        
            handler.send_message(mtype='user_id', id=event.peer_id, message="Давай начнем!",keyboard=keyboard) # при начале работы с ботессой
          
          elif message == 'кто твой создатель?': 
            handler.send_message(mtype='user_id', id=event.peer_id, message=f"У меня {len(contributors)} создателя. Yul powered by {' and '.join(contributors)}",keyboard=keyboard) # пасхалОчка
          
          elif message == 'какой сегодня день?':
            handler.send_message(mtype='user_id', id=event.peer_id, message=f'Сегодня: {time.now().strftime("%d.%m.%Y")}',keyboard=keyboard)
          
          elif message == 'как я?':
            handler.send_message(mtype='user_id', id=event.peer_id, message=f'Я в норме!',keyboard=keyboard)
          
          elif message == 'помощь':
            handler.send_message(mtype='user_id', id=event.peer_id, message=help_msg,keyboard=keyboard)
                    
          elif message == '/flip':
            user = userHandler.GetUser(event.user_id)
            handler.send_message(mtype='user_id', id=event.peer_id, message=f"Вы подбросили монету: {'Решка' if round(random.random()) == 1 else 'Орел'}", keyboard=keyboard)
          
          elif command_string[0] == '/random' and len(command_string) == 2:
            rng = command_string[1].split('-')
            handler.send_message(mtype='user_id', id=event.peer_id, message=f"Вы загадали случайное число от {rng[0]} до {rng[1]}: {random.randint(int(rng[0]), int(rng[1]) + 1)}", keyboard=keyboard)
          
          elif command_string[0] == '/weather' and len(command_string) == 2:
            try:
              response = weatherHandler.GetWeather(command_string[1])

              handler.send_message(mtype='user_id', id=event.peer_id, message=f"Погода в вашем городе: {response['temperature']}°C , {translateHandler.Translate(text=response['condition'])}", keyboard=keyboard)
            except Exception as X:
              logging.error(f"{X}")

          elif command_string[0] == '/translate' and len(command_string) > 1:
            handler.send_message(mtype='user_id', id=event.peer_id, message=f"{translateHandler.Translate(text=command_string[1]) if len(command_string) < 3 else translateHandler.Translate(command_string[1], ' '.join(command_string[2:]))}", keyboard=keyboard)
          
          else:
            # отправим эхо, если не распознали запроса пользователя
            handler.send_message(mtype='user_id', id=event.peer_id, message=f"{event.text}",keyboard=keyboard) 
        
        except:
          handler.send_message(mtype='user_id', id=event.peer_id, message=f"Прости, я тебя не понимаю. >.<")
      
      elif event.from_chat and not event.from_me:                             # для чатов 
        handler.send_message(mtype='chat_id', id=event.peer_id, message=f"{event.text}")
      
      if not event.from_me:
        # сохранение сообщения пользователя в логи
        logging.info(f'TEXT: {message.encode("utf-8")}; TIME  : {str(time.strftime(time.now(), "%H:%M:%S"))};')
  
logging.info(f"\n{'-' * 20}\n{'Session was ended': ^20}")