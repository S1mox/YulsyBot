from vk_api.longpoll import VkLongPoll,VkEventType

from datetime import datetime as time
import vk_api

class MessageHandler:
  def __init__(self, vk_session, session_api):
    self.vk_session = vk_session
    self.session_api = session_api
  
  def send_message(self, user_id, message = ' ', random_id = '0', keyboard = None):
    self.vk_session.method('messages.send', values= {'user_id':f'{user_id}', 'message': f"{message}", 'random_id':{random_id}, 'keyboard':f"{keyboard}"})