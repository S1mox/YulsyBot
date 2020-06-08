from vk_api.longpoll import VkLongPoll,VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

from datetime import datetime as time

import logging
import vk_api
import handlers
import config

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
longpoll = VkLongPoll(vk_session)

logging.info(f"{'-' * 20}\n{'Session was started': ^20}")
while True:                       # бесконечное прослушивание ответов с серверов VK
  for event in longpoll.listen():     # собирает события с прослушки
    logging.info(f"{event.type}; {event.from_chat}")

    if event.type == VkEventType.MESSAGE_NEW:      # если это новое сообщение, то =>
      handler = handlers.MessageHandler(vk_session)  # помощник для работы с сообщениями

      message = event.text.lower() # сохраняем сообщение пользователя

      if event.from_user and not event.from_me:         # для диалога с пользователями
        keyboard = create_keyboard() # клавиатура для пользователя

        if message == 'Начать':                        
          handler.send_message('user_id',event.user_id, "Давай начнем!", 0, keyboard) # при начале работы с ботессой
        elif message == 'кто твой создатель?': 
          handler.send_message('user_id',event.user_id, f"У меня {len(contributors)} создателя. Yul powered by {' and '.join(contributors)}", 0, keyboard) # пасхалОчка
        elif message == 'какой сегодня день?':
          handler.send_message('user_id',event.user_id, f'Сегодня: {time.now().strftime("%d.%m.%Y")}', 0, keyboard)
        elif message == 'как я?':
          handler.send_message('user_id',event.user_id, f'Я в норме!', 0, keyboard)
        elif message == 'помощь':
          handler.send_message('peer_id',event.user_id, f'Пока я только узнаю, чем я могу помочь, простиии 👉🏻👈🏻', 0, keyboard)
        else:
          # отправим эхо, если не распознали запроса пользователя
          handler.send_message('user_id', event.user_id, f"{event.text}", 0, keyboard)       
      elif event.from_chat and not event.from_me:                             # для чатов 
        handler.send_message('chat_id', event.chat_id, f"{event.text}")
      
      if not event.from_me:
        # сохранение сообщения пользователя в логи
        logging.info(f'TEXT: {message.encode("utf-8")}; TIME  : {str(time.strftime(time.now(), "%H:%M:%S"))}')

else:
  logging.info(f"\n{'-' * 20}\n{'Session was started': ^20}")