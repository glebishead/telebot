"""Обработчики сообщений от пользователя, пользовательских комманд

"""


from aiogram.types import Message

from src import bot
from data.methods.insert_into_users import insert_into_users


async def start(message: Message):
	with open(f'static/stickers/StartSticker.tgs') as sticker:
		await bot.send_sticker(message.from_id, sticker)
	await insert_into_users(message.from_id)
	await message.reply('Hello')


async def send_contacts(message: Message):
	await bot.send_message('Контакты: ---')


async def show_products(message: Message):
	await bot.send_message('Товары: ---')


async def plug(message: Message):
	print(f"___Unresolved___\nMessage from: {message['from']}\nchat: {message['chat']}\ntext: {message.text}\n___")
