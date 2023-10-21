"""Обработчики сообщений от админа/ов, комманд администратора/ов

"""

from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram_media_group import media_group_handler

from src import bot


class AddProductStates(StatesGroup):
	name = State()
	category = State()
	description = State()
	media = State()
	price = State()
	quantity = State()


async def add_product(message: Message) -> None:
	await bot.send_message(message.from_id, 'Введите название товара')
	await AddProductStates.name.set()


async def add_product_name(message: Message, state=FSMContext) -> None:
	async with state.proxy() as data:
		data['name'] = message.text
	await bot.send_message(message.from_id, 'Введите категории товара')
	await AddProductStates.next()


async def add_product_category(message: Message, state=FSMContext) -> None:
	async with state.proxy() as data:
		data['category'] = message.text
	await bot.send_message(message.from_id, 'Введите описание товара')
	await AddProductStates.next()


async def add_product_description(message: Message, state=FSMContext) -> None:
	async with state.proxy() as data:
		data['description'] = message.text
	await bot.send_message(message.from_id, 'Прикрепите к сообщению фото и/или видео товара')
	await AddProductStates.next()


@media_group_handler
async def add_product_media_group(messages: list[Message], state=FSMContext) -> None:
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


async def add_product_media(message: Message, state=FSMContext) -> None:
	async with state.proxy() as data:
		if message.photo:
			data['images'] = [message.photo[-1].file_id]
		elif message.video:
			data['videos'] = [message.video['file_id']]
	await bot.send_message(message.from_id, 'Введите цену товара')
	await AddProductStates.next()


async def add_product_price(message: Message, state=FSMContext) -> None:
	async with state.proxy() as data:
		data['price'] = int(message.text)
	await bot.send_message(message.from_id, 'Введите доступное на данный момент количество единиц товара')
	await AddProductStates.next()


async def add_product_quantity(message: Message, state=FSMContext) -> None:
	async with state.proxy() as data:
		data['quantity'] = message.text
		if 'images' not in data.keys():
			data['images'] = ''
		if 'videos' not in data.keys():
			data['videos'] = ''
	
	name = data['name']
	category = data['category']
	description = data['description']
	images = ' - '.join(data['images'])
	videos = ' - '.join(data['videos'])
	price = data['price']
	quantity = data['quantity']
	
	await bot.send_message(message.from_id, 'Вы добавили товар успешно!')
	await bot.send_message(message.from_id, f'Название: {name}\n'
	                                        f'Категории: {category}\n'
	                                        f'Описание: {description}\n'
	                                        f'Изображения (id): {images}\n'
	                                        f'Видео (id): {videos}\n'
	                                        f'Цена: {price}\n'
	                                        f'Количество: {quantity}\n')
	await state.finish()


async def add_product_cancel(message: Message, state=FSMContext) -> None:
	if await state.get_state() is None:
		return
	await bot.send_message(message.from_id, 'Добавление товара прекращено')
	await state.finish()
