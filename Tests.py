import vk_api

from vk_api.longpoll import VkLongPoll, VkEventType

import handlers
import requests
import config
######### Tests ###########

temp_session = vk_api.VkApi(token=config.VK_TOKEN)
session = temp_session.get_api()
longpoll = VkLongPoll(temp_session)

print(session.users.get(users_id=307841071))
# userH = handlers.UserHandler(temp_session)
# print(userH.GetUser("307841071"))


### Weather ###
# handler = WeatherHandler()

# print(handler.GetWeather('Homel'))

# link_generate
# link = f"http://api.openweathermap.org/data/2.5/find?q=request&type=like&APPID={config.WEATHER_TOKEN}"
# request = 'Homel,BY'
# temp_link = link.replace("request", request)
# print(temp_link)


### User ###