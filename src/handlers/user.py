"""Обработчики сообщений от пользователя, пользовательских комманд

"""


from aiogram.types import Message


async def start(message: Message):
	await message.reply('Hello')


async def echo(message: Message):
	await message.reply(message.text)
