"""Исполняемый файл проекта

"""
import asyncio
import os
from logging import basicConfig, INFO

from aiogram import Bot
from aiogram.types import Message
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage


async def start(message: Message):
	await message.reply('Hello')


async def echo(message: Message):
	await message.reply(message.text)


def register_user_handlers():
	dp.register_message_handler(start, commands=['start'])
	dp.register_message_handler(echo)


if __name__ == '__main__':
	basicConfig(level=INFO)
	
	bot = Bot(os.getenv('TOKEN'))
	dp = Dispatcher(bot, storage=MemoryStorage())
	ADMIN_ID = int(os.getenv('ADMIN_ID'))
	
	register_user_handlers()
	executor.start_polling(dp, skip_updates=True)
