"""Исполняемый файл проекта"""


from logging import basicConfig, INFO

from aiogram.utils import executor

from src.handlers import dp


if __name__ == '__main__':
	basicConfig(level=INFO)
	executor.start_polling(dp, skip_updates=True)
