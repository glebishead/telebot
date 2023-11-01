"""Автоматически исполняемый файл, регистрирует обработчики сообщений

"""

from aiogram.dispatcher.filters import MediaGroupFilter


from .admin import *
from .user import *


def register_user_handlers():
	dp.register_message_handler(start, commands=['start'])
	
	# Обработчики событий от пользователя
	dp.register_message_handler(send_contacts, commands=['contacts'])
	dp.register_message_handler(show_products, commands=['show_products'])
	
	# Обработчики событий от админа
	dp.register_message_handler(add_product, commands=['add_product'])
	dp.register_message_handler(add_product_cancel, commands=['cancel'], state=AddProductStates.states)
	
	dp.register_message_handler(add_product_name, state=AddProductStates.name)
	dp.register_message_handler(add_product_description, state=AddProductStates.description)
	dp.register_message_handler(add_product_categories, state=AddProductStates.categories)
	dp.register_message_handler(add_product_key, state=AddProductStates.key)
	dp.register_message_handler(add_product_media_group, MediaGroupFilter(is_media_group=True),
	                            content_types=['photo', 'video'], state=AddProductStates.media)
	dp.register_message_handler(add_product_media, content_types=['photo', 'video'], state=AddProductStates.media)
	dp.register_message_handler(add_product_price, state=AddProductStates.price)
	
	dp.register_message_handler(send_all_start, commands=['send_all'])
	dp.register_message_handler(send_all_cancel, commands=['cancel'], state=ShowEveryoneStates.show)
	dp.register_message_handler(send_all_media_group_end, MediaGroupFilter(is_media_group=True),
	                            content_types=['photo', 'video'], state=ShowEveryoneStates.show)
	dp.register_message_handler(send_all_end, content_types=['photo', 'video', 'sticker', 'text'],
	                            state=ShowEveryoneStates.show)
	
	# оставить последним, это заглушка
	dp.register_message_handler(plug)


register_user_handlers()
