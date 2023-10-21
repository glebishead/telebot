"""Автоматически исполняемый файл, регистрирует обработчики сообщений

"""

from src import dp, bot
from .admin import *
from .user import *


def register_user_handlers():
	dp.register_message_handler(start, commands=['start'])
	
	# Обработчики событий от пользователя
	dp.register_message_handler(send_contacts, commands=['contacts'])
	dp.register_message_handler(show_products, commands=['show_products'])
	
	# оставить последним, это заглушка
	dp.register_message_handler(plug)


register_user_handlers()
