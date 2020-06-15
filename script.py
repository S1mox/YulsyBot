from vk_api.longpoll import VkLongPoll,VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

from datetime import datetime as time

import logging
import vk_api
import handlers
import config
import random

contributors = ['Seamo', 'Nyalen']    # Developers
logging.basicConfig(filename="Yul.log", filemode='w',level=logging.INFO)

def create_keyboard():
  """ Создание клавиатуры в диалоге с пользователем """
  keyboard = VkKeyboard(one_time=False)

  keyboard.add_button('Помощь', color=VkKeyboardColor.DEFAULT)
  keyboard.add_button('Как я?', color=VkKeyboardColor.POSITIVE)

  keyboard.add_line()
  keyboard.add_button('Какой сегодня день?', color=VkKeyboardColor.POSITIVE)

  return keyboard.get_keyboard()

vk_session = vk_api.VkApi(token=config.VK_TOKEN)
session_api = vk_session.get_api()
longpoll = VkLongPoll(vk_session)

logging.info(f"{'-' * 20}\n{'Session was started': ^20}")
while True:                       # бесконечное прослушивание ответов с серверов VK
  for event in longpoll.listen():     # собирает события с прослушки
    if event.type == VkEventType.MESSAGE_NEW:      # если это новое сообщение, то =>
      handler = handlers.MessageHandler(vk_session)  # помощник для работы с сообщениями
      message = event.text.lower() # сохраняем сообщение пользователя
      command_string = message.split(' ')

      if event.from_user and not event.from_me:         # для диалога с пользователями
        try:
          keyboard = create_keyboard() # клавиатура для пользователя

          logging.info(f"{command_string}:{len(command_string)}")

          if message == 'Начать':                        
            handler.send_message(mtype='user_id', id=event.peer_id, message="Давай начнем!",keyboard=keyboard) # при начале работы с ботессой
          elif message == 'кто твой создатель?': 
            handler.send_message(mtype='user_id', id=event.peer_id, message=f"У меня {len(contributors)} создателя. Yul powered by {' and '.join(contributors)}",keyboard=keyboard) # пасхалОчка
          elif message == 'какой сегодня день?':
            handler.send_message(mtype='user_id', id=event.peer_id, message=f'Сегодня: {time.now().strftime("%d.%m.%Y")}',keyboard=keyboard)
          elif message == 'как я?':
            handler.send_message(mtype='user_id', id=event.peer_id, message=f'Я в норме!',keyboard=keyboard)
          elif message == 'помощь':
            handler.send_message(mtype='user_id', id=event.peer_id, message=f'Поиграй со мной:\n/flip - Подбрашивание монетки\n/weather [City] - Узнать погоду в городе [City]\n/random [a-b] - Случайное число от a до b',keyboard=keyboard)
          elif message == '/flip':
            userHandler = handlers.UserHandler(session_api)
            user = userHandler.GetUser(event.user_id)
            handler.send_message(mtype='user_id', id=event.peer_id, message=f"Вы подбросили монету: {'Решка' if round(random.random()) == 1 else 'Орел'}", keyboard=keyboard)
          elif command_string[0] == '/random' and len(command_string) == 2:
            rng = command_string[1].split('-')
            handler.send_message(mtype='user_id', id=event.peer_id, message=f"Вы загадали случайное число от {rng[0]} до {rng[1]}: {random.randint(int(rng[0]), int(rng[1]) + 1)}", keyboard=keyboard)
          elif command_string[0] == '/weather' and len(command_string) == 2:
            try:
              weatherHandler = handlers.WeatherHandler()

              response = weatherHandler.GetWeather(command_string[1])

              handler.send_message(mtype='user_id', id=event.peer_id, message=f"Погода в вашем городе: {response['temperature']}°C , {response['condition']}", keyboard=keyboard)
            except Exception as X:
              logging.error(f"{X}")
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
else:
  logging.info(f"\n{'-' * 20}\n{'Session was started': ^20}")