from os import getenv

from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage


bot = Bot(getenv('TOKEN'))
dp = Dispatcher(bot, storage=MemoryStorage())
ADMIN_ID = int(getenv('ADMIN_ID'))
