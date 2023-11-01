"""Обработчики сообщений от пользователя, пользовательских комманд

"""

from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from src import bot
from data.methods.insert_into_users import insert_into_users
from src import keyboards, dp


class FSMSendMessageToAdmin(StatesGroup):
    message = State()


async def start(message: Message):
    with open(f'static/stickers/StartSticker.tgs') as sticker:
        await bot.send_sticker(message.from_id, sticker)
    await insert_into_users(message.from_id)
    await message.reply('Hello')


async def send_contacts(message: Message):
    await bot.send_message('Контакты: ---')


async def show_products(message: Message):
    await bot.send_message('Товары: ---')


@dp.message_handler(commands=['связаться с продавцом'])
async def connect_to_seller(message: Message):
    await bot.send_message(message.from_user.id, "Выберите категорию вопроса", reply_markup=keyboards.faq_keyboard())


@dp.message_handler(commands=keyboards.faq.keys())
async def answer(message: Message):
    answer_text = "Пока нет ответов на вопросы"
    # answer_text = faq[message.txt]
    # todo: раскоментировать, если есть faq и удалить первое определение answer_text
    await bot.send_message(message.from_user.id, answer_text)


@dp.message_handler(commands=["моего вопроса нет в списке"], state=None)
async def start_adding_settings(message: Message):
    await FSMSendMessageToAdmin.message.set()
    await bot.send_message(message.from_user.id, "Напишите свой вопрос(/cancel для отмены)")

@dp.message_handler(state=FSMSendMessageToAdmin.message)
async def send_to_admin(message: Message, state: FSMContext):
    text = message.text
    if is_banned(text):
        await bot.send_message(message.from_user.id, "Сообщение не отправлено, так как содержит оскорбления")
        return
    await bot.send_message(message.from_user.id, text)

async def plug(message: Message):
    print(f"___Unresolved___\nMessage from: {message['from']}\nchat: {message['chat']}\ntext: {message.text}\n___")


def is_banned(text):
    # todo: фильтр плохих слов чтобы не кибербуллили админов
    return False
