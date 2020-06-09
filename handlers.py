from vk_api.longpoll import VkLongPoll,VkEventType

import vk_api

class MessageHandler:
  """ Класс работы с сообщениями """

  def __init__(self, vk_session):
    self.vk_session = vk_session
  
  def send_message(self, message_type, id, message = ' ', random_id = '0', keyboard = None):
      """Отправка сообщения из экземпляра MessageHandler
        
        keywords arguments:
        message_type -- type of message ('chat_id', 'user_id', 'peer_id'
        id -- id if receiver"""
      self.vk_session.method('messages.send', values= {f"{message_type}":f'{id}', 'message': f"{message}", 'random_id':{random_id}, 'keyboard':f"{keyboard}"})

