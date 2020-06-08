from vk_api.longpoll import VkLongPoll,VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from datetime import datetime as time

import vk_api
import handlers
import config

contributors = ['Seamo', 'Nyalen']    # Developers

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

print(f"{'-' * 20}\n{'Session was started': ^20}")
while True:                       # бесконечное прослушивание ответов с серверов VK
  for event in longpoll.listen():     # собирает события с прослушки
    if event.type == VkEventType.MESSAGE_NEW:      # если это новое сообщение, то =>
      handler = handlers.MessageHandler(vk_session, session_api)  # помощник для работы с сообщениями

      if event.from_user and not event.from_me:
        keyboard = create_keyboard() # клавиатура для пользователя
        message = event.text.lower() # сохраняем сообщение пользователя

        if message == 'Начать':                        
          handler.send_message(event.user_id, "Давай начнем!", 0, keyboard) # при начале работы с ботессой
        elif message == 'кто твой создатель?': 
          handler.send_message(event.user_id, f"У меня {len(contributors)} создателя. Yul powered by {' and '.join(contributors)}", 0, keyboard) # пасхалОчка
        elif message == 'какой сегодня день?':
          handler.send_message(event.user_id, f'Сегодня: {str(time.date)}', random_id=0, keyboard = keyboard)
        elif message == 'как я?':
          handler.send_message(event.user_id, f'Я в норме!', random_id=0, keyboard = keyboard)
        elif message == 'помощь':
          handler.send_message(event.user_id, f'Пока я только узнаю, чем я могу помочь, простии 👉🏻👈🏻', random_id=0, keyboard = keyboard)
        else:
          # отправим эхо, если не распознали запроса пользователя
          handler.send_message(event.user_id, f"{event.text}", 0, keyboard)
        
        # сохранение сообщения пользователя в логи
        print(f'TEXT: {event.text}')
        print(f'TIME: {str(time.strftime(time.now(), "%H:%M:%S"))}')
else:
  print(f"\n{'-' * 20}\n{'Session was started': ^20}")