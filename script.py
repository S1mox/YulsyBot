from vk_api.longpoll import VkLongPoll,VkEventType
from datetime import datetime as time

import vk_api
import config

vk_session = vk_api.VkApi(token=config.VK_TOKEN)
longpoll = VkLongPoll(vk_session)

print("Module was started")
while True:
  for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
      print(f'TEXT: {event.text}')
      print(f'TIME: {str(time.strftime(time.now(), "%H:%M:%S"))}')