from vk_api.longpoll import VkLongPoll,VkEventType

import vk_api
import logging

class MessageHandler:
  """ Класс работы с сообщениями """

  def __init__(self, vk_session):
    self.vk_session = vk_session
  
  def send_message(self, id, message = ' ', keyboard = None):
      """Отправка сообщения из экземпляра MessageHandler
        
        keywords arguments:
        id -- id if receiver
        message -- message to recever"""
      self.vk_session.messages.send(peer_id=id, message=message, random_id='0', keyboard = keyboard)

