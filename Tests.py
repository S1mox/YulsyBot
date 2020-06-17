import vk_api

from vk_api.longpoll import VkLongPoll, VkEventType

import handlers
import requests
import config

######### Tests ###########

temp_session = vk_api.VkApi(token=config.VK_TOKEN)
session = temp_session.get_api()
longpoll = VkLongPoll(temp_session)

handler = handlers.MessageHandler(temp_session)
for i in range(20):
    handler.send_message("user_id", "190862881", "Это атака машин", None)

### Weather ###
# handler = WeatherHandler()

# print(handler.GetWeather('Homel'))

# link_generate
# link = f"http://api.openweathermap.org/data/2.5/find?q=request&type=like&APPID={config.WEATHER_TOKEN}"
# request = 'Homel,BY'
# temp_link = link.replace("request", request)
# print(temp_link)


### User ###
# print(session.users.get(user_ids = 307841071, fields = 'city'))