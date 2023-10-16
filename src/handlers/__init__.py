"""Автоматически исполняемый файл, регистрирует обработчики сообщений

"""

from src import dp
from .admin import *
from .user import *


def register_user_handlers():
	dp.register_message_handler(start, commands=['start'])
	dp.register_message_handler(echo)


register_user_handlers()
