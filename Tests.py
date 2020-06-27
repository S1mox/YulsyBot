import vk_api

from vk_api.longpoll import VkLongPoll, VkEventType

import handlers
import requests
import config
import time

######### Tests ###########

temp_session = vk_api.VkApi(token=config.VK_TOKEN)
session = temp_session.get_api()
longpoll = VkLongPoll(temp_session)

# Рассылка сообщения
# handler = handlers.MessageHandler(temp_session)
# while True:
#     handler.send_message("user_id", "190862881", "Че с деньгами?", None)

### Weather ###
# handler = WeatherHandler()
# print(handler.GetWeather('Homel'))

### User ###
# print(session.users.get(user_ids = 307841071, fields = 'city'))