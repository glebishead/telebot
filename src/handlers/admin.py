"""Обработчики сообщений от админа/ов, комманд администратора/ов

"""

from aiogram.types import Message, MediaGroup
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.exceptions import ChatNotFound
from aiogram_media_group import media_group_handler

from src import bot, ADMIN_ID
from data.methods import select_from_users, insert_into_products, describe_products


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


class ShowEveryoneStates(StatesGroup):
	show = State()


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
	await insert_into_products(1, key, name, description, categories, images, videos, price)
	await bot.send_message(message.from_id, f'Название: {name}\n'
	                                        f'Ключ: {key}\n'
	                                        f'Категории: {categories}\n'
	                                        f'Описание: {description}\n'
	                                        f'Изображения (id): {images}\n'
	                                        f'Видео (id): {videos}\n'
	                                        f'Цена: {price}\n')
	await state.finish()
	

async def add_product_cancel(message: Message, state=FSMContext):
	if await state.get_state() is None:
		return
	await bot.send_message(message.from_id, 'Добавление товара прекращено')
	await state.finish()


async def send_all_start(message: Message):
	if not is_admin(message.from_user.id):
		await bot.send_message(message.from_user.id, "Вы не являетесь администратором, поэтому функция недоступна")
		return
	await message.reply('Ваше следующее сообщение отправится всем пользователям бота')
	await ShowEveryoneStates.show.set()


async def send_all_end(message: Message, state: FSMContext):
	persons = [*await select_from_users()]
	for person in persons:
		# id, name, register_date, status = person
		# когда бд изменится закомменить код ниже, выше раскомментить
		id, register_date, status = person
		try:
			await message.copy_to(id)
		except ChatNotFound:
			print(f"Person with id {id} not found")
	await message.reply('Это сообщение было отправлено всем пользователям')
	await state.finish()


async def send_all_cancel(message: Message, state=FSMContext):
	if await state.get_state() is None:
		return
	await bot.send_message(message.from_id, 'Пересылка следующего сообщения отключена')
	await state.finish()


@media_group_handler
async def send_all_media_group_end(messages: list[Message], state: FSMContext):
	persons = [*await select_from_users()]
	for person in persons:
		# id, name, register_date, status = person
		# когда бд изменится закомменить код ниже, выше раскомментить
		id, register_date, status = person
		try:
			media = MediaGroup()
			for j in range(len(messages)):
				media.attach_photo(messages[j]['photo'][1]['file_id'], caption=messages[0].text)
			await bot.send_media_group(id, media=media)
		except ChatNotFound:
			print(f"Person with id {id} not found")
	await messages[0].reply('Это сообщение было отправлено всем пользователям')
	await state.finish()
