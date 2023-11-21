"""Обработчики сообщений от админа/ов, комманд администратора/ов
с переадресовкой сообщения всем пользователям

"""

from aiogram.types import Message, MediaGroup
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import ChatNotFound
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram_media_group import media_group_handler

from src import bot
from .is_admin import is_admin
from data.methods import select_from_users


class ShowEveryoneStates(StatesGroup):
	show = State()


async def send_all_start(message: Message):
	if not await is_admin(message.from_user.id):
		await bot.send_message(message.from_user.id, "Вы не являетесь администратором, поэтому функция недоступна")
		return
	await message.reply('Ваше следующее сообщение отправится всем пользователям бота')
	await ShowEveryoneStates.show.set()


async def send_all_end(message: Message, state: FSMContext):
	persons = [*await select_from_users()]
	for person in persons:
		person_id, register_date, status = person
		try:
			await message.copy_to(person_id)
		except ChatNotFound:
			print(f"Person with id {id} not found")
	await message.reply('Это сообщение было отправлено всем пользователям')
	await state.finish()


@media_group_handler
async def send_all_media_group_end(messages: list[Message], state: FSMContext):
	persons = [*await select_from_users()]
	for person in persons:
		person_id, register_date, status = person
		try:
			media = MediaGroup()
			main_message, *messages = messages
			
			if 'photo' in main_message.iter_keys():
				media.attach_photo(main_message['photo'][1]['file_id'], caption=main_message.caption)
			if 'video' in main_message.iter_keys():
				media.attach_video(main_message['video']['file_id'], caption=main_message.caption)
				
			for message in messages:
				if 'photo' in message.iter_keys():
					media.attach_photo(message['photo'][1]['file_id'])
				if 'video' in message.iter_keys():
					media.attach_video(message['video']['file_id'])
				
			await bot.send_media_group(person_id, media=media)
		except ChatNotFound:
			print(f"Person with id {id} not found")
	await messages[0].reply('Это сообщение было отправлено всем пользователям')
	await state.finish()


async def send_all_cancel(message: Message, state=FSMContext):
	if await state.get_state() is None:
		return
	await bot.send_message(message.from_id, 'Пересылка следующего сообщения отключена')
	await state.finish()