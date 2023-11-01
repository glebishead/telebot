"""Обработчики сообщений от админа/ов, комманд администратора/ов
с добавлением товара в базу данных

"""

from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram_media_group import media_group_handler

from src import bot, ADMIN_ID
from data.methods import insert_into_products


def is_admin(userid):
	# todo: admin_list
	return userid == ADMIN_ID


class AddProductStates(StatesGroup):
	name = State()
	description = State()
	categories = State()
	key = State()
	media = State()
	price = State()


async def add_product(message: Message):
	if not is_admin(message.from_user.id):
		await bot.send_message(message.from_user.id, "Вы не являетесь администратором, поэтому функция недоступна")
		return
	await bot.send_message(message.from_id, 'Введите название товара')
	await AddProductStates.name.set()


async def add_product_name(message: Message, state=FSMContext):
	async with state.proxy() as data:
		data['name'] = message.text
	await bot.send_message(message.from_id, 'Введите описание товара')
	await AddProductStates.next()


async def add_product_description(message: Message, state=FSMContext):
	async with state.proxy() as data:
		data['description'] = message.text
	await bot.send_message(message.from_id, 'Введите категории товара')
	await AddProductStates.next()


async def add_product_categories(message: Message, state=FSMContext):
	async with state.proxy() as data:
		data['categories'] = message.text
	await bot.send_message(message.from_id, 'Введите ключ steam')
	await AddProductStates.next()

	
async def add_product_key(message: Message, state=FSMContext):
	async with state.proxy() as data:
		data['key'] = message.text
	await bot.send_message(message.from_id, 'Прикрепите к сообщению фото и/или видео товара')
	await AddProductStates.next()


@media_group_handler
async def add_product_media_group(messages: list[Message], state=FSMContext):
	"""В телеграмме фото и видео имеют уникальный file_id,
	который можно отправить и сохранить в базу данных
	
	"""
	async with state.proxy() as data:
		for message in messages:
			if 'images' not in data.keys() and message.photo:
				data['images'] = [message.photo[-1].file_id]
			elif 'videos' not in data.keys() and message.video:
				data['videos'] = [message.video['file_id']]
			elif 'images' in data.keys() and message.photo:
				data['images'].append(message.photo[-1].file_id)
			elif 'videos' in data.keys() and message.video:
				data['videos'].append(message.video['file_id'])
	await bot.send_message(message.from_id, 'Введите цену товара')
	await AddProductStates.next()


async def add_product_media(message: Message, state=FSMContext):
	async with state.proxy() as data:
		if message.photo:
			data['images'] = [message.photo[-1].file_id]
		elif message.video:
			data['videos'] = [message.video['file_id']]
	await bot.send_message(message.from_id, 'Введите цену товара')
	await AddProductStates.next()


async def add_product_price(message: Message, state=FSMContext):
	async with state.proxy() as data:
		data['price'] = int(message.text)
		if 'images' not in data.keys():
			data['images'] = ''
		if 'videos' not in data.keys():
			data['videos'] = ''
	
	name = data['name']
	description = data['description']
	categories = data['categories']
	key = data['key']
	images = ' - '.join(data['images'])
	videos = ' - '.join(data['videos'])
	price = data['price']
	
	await bot.send_message(message.from_id, 'Вы добавили товар успешно!')
	await insert_into_products(key, name, description, categories, images, videos, price)
	await state.finish()
	

async def add_product_cancel(message: Message, state=FSMContext):
	if await state.get_state() is None:
		return
	await bot.send_message(message.from_id, 'Добавление товара прекращено')
	await state.finish()
