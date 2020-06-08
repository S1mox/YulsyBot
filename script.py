from vk_api.longpoll import VkLongPoll,VkEventType
from datetime import datetime as time

import vk_api
import config

contributors = ['Seamo', 'Nyalen']

vk_session = vk_api.VkApi(token=config.VK_TOKEN)
longpoll = VkLongPoll(vk_session)

print("Module was started")
while True:                       # бесконечное прослушивание ответов с серверов VK
  for event in longpoll.listen():     # собирает события с прослушки
    if event.type == VkEventType.MESSAGE_NEW:      # если это новое сообщение, то =>
      if event.from_user and not event.from_me:
        
        if event.text == 'Начать':                        # при начале работы с ботессой
          vk_session.method('messages.send', values= {'user_id':f'{event.user_id}', 'message': f"Давай начнем!", 'random_id':'0'})
        elif event.text.lower() == 'кто твой создатель?': # пасхалОчка
          vk_session.method('messages.send', values= {'user_id':f'{event.user_id}', 'message': f"У меня {len(contributors)} создателя. Yul powered by {' and '.join(contributors)}", 'random_id':'0'})
        else:
          # отправим эхо, если не распознали запроса пользователя
          vk_session.method('messages.send', values= {'user_id':f'{event.user_id}', 'message': f'{event.text}', 'random_id':'0'})
        
        # сохранение сообщения пользователя в логи
        print(f'TEXT: {event.text}')
        print(f'TIME: {str(time.strftime(time.now(), "%H:%M:%S"))}')