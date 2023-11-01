"""Обработчики сообщений от админа/ов, комманд администратора/ов
с переадресовкой сообщения всем пользователям

"""

from aiogram.types import Message, MediaGroup
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import ChatNotFound
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram_media_group import media_group_handler

from src import bot
from data.methods import select_from_users
from .add_product import is_admin


class ShowEveryoneStates(StatesGroup):
	show = State()


async def send_all_start(message: Message):
	if not is_admin(message.from_user.id):
		await bot.send_message(message.from_user.id, "Вы не являетесь администратором, поэтому функция недоступна")
		return
	await message.reply('Ваше следующее сообщение отправится всем пользователям бота')
	await ShowEveryoneStates.show.set()


async def send_all_end(message: Message, state: FSMContext):
	persons = [*await select_from_users()]
	for person in persons:
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
	