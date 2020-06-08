from vk_api.longpoll import VkLongPoll,VkEventType

import vk_api

class MessageHandler:
  def __init__(self, vk_session):
    self.vk_session = vk_session
  
  def send_message(self, message_type, id, message = ' ', random_id = '0', keyboard = None):
      self.vk_session.method('messages.send', values= {f"{message_type}":f'{id}', 'message': f"{message}", 'random_id':{random_id}, 'keyboard':f"{keyboard}"})

