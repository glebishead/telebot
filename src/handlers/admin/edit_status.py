"""Обработчики сообщений от админа/ов, комманд администратора/ов
с добавлением товара в базу данных

"""

from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from src import bot
from .is_admin import is_admin
from data.methods import edit_users


class EditStatusStates(StatesGroup):
	person_id = State()
	to_admin = State()


async def edit_status(message: Message):
	if not await is_admin(message.from_user.id):
		await bot.send_message(message.from_user.id, "Вы не являетесь администратором, поэтому функция недоступна")
		return
	await bot.send_message(message.from_id, 'Введите telegram id пользователя, статус которого хотите изменить')
	await EditStatusStates.person_id.set()


async def edit_status_person_id(message: Message, state=FSMContext):
	async with state.proxy() as data:
		data['person_id'] = message.text
	await bot.send_message(message.from_id, f'Введите новый статус пользователя {message.text}\n'
	                                        f'0 - Пользователь\n'
	                                        f'1 - Администратор\n')
	await EditStatusStates.next()


async def edit_status_end(message: Message, state=FSMContext):
	async with state.proxy() as data:
		data['status'] = message.text
		await edit_users(data['person_id'], data['status'])
	await bot.send_message(message.from_id, f'Статус пользователя успешно изменён')
	await state.finish()
