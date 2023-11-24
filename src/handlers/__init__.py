"""Автоматически исполняемый файл, регистрирует обработчики сообщений

"""

from aiogram.dispatcher.filters import MediaGroupFilter


from src import dp, faq_keyboard
from .admin import *
from .user import *


def register_admin_handlers():
	"""Обработчики событий от админа"""
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
	
	dp.register_message_handler(edit_status, commands=['edit_status'])
	dp.register_message_handler(edit_status_person_id, state=EditStatusStates.to_admin)
	dp.register_message_handler(edit_status_end, state=EditStatusStates.person_id)


def register_user_handlers():
	"""Обработчики событий от пользователя"""
	dp.register_message_handler(start, commands=['start'])
	
	dp.register_message_handler(show_products, commands=['products'])
	
	dp.register_message_handler(connect_to_seller, commands=['связаться с продавцом'])
	dp.register_message_handler(answer, commands=faq_keyboard.get_faq().keys())
	dp.register_message_handler(start_adding_settings, commands=["моего вопроса нет в списке"])
	dp.register_message_handler(send_to_admin, state=FSMSendMessageToAdmin.message)
	
	
def register_all_handlers():
	register_user_handlers()
	register_admin_handlers()
	dp.register_message_handler(plug)  # заглушка


register_all_handlers()
