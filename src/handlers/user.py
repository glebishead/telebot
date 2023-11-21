"""Обработчики сообщений от пользователя, пользовательских комманд

"""

from aiogram.types import Message, MediaGroup
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from src import bot, faq_keyboard, ADMIN_ID
from data.methods import insert_into_users, select_from_products


class FSMSendMessageToAdmin(StatesGroup):
    message = State()


async def start(message: Message):
    try:
        await insert_into_users(message.from_id)
    except ValueError as ve:
        print(ve)
    await message.answer('Здоров, братиш, на связи <b>Celestial</b>\n\n'
                         'У меня все товары высшего сорта, даже для тебя что-то да найдётся, пиши '
                         '/products чтобы ознакомиться с <b>товарами</b>', parse_mode='html')


async def show_products(message: Message):
    try:
        products = [*map(lambda x: x, await select_from_products())]
        for product in products:
            product_id, key, game_name, description, categories, images, videos, price, is_sold = product
            caption = f'Ключ от игры {game_name}\n\n'\
                      f'{description}\n'\
                      f'Категории {categories}\n'\
                      f'по цене {price}\n'
            
            if not is_sold:
                main_image, *images = images.split(' - ')  # 'images' and 'videos' are strings of separated id
                main_video, *videos = videos.split(' - ')
                
                if images or videos or (main_video and main_image):
                    media = MediaGroup()
                    
                    if main_image and main_video:
                        media.attach_photo(main_image, caption=caption)
                        media.attach_video(main_video)
                    elif main_image:
                        media.attach_photo(main_image, caption=caption)
                    elif main_video:
                        media.attach_video(main_video, caption=caption)
                        
                    for image_id in images:
                        media.attach_photo(image_id)
                    for video_id in videos:
                        media.attach_video(video_id)
                    
                    await message.answer_media_group(media)
                    
                elif main_image:
                    await message.answer_photo(main_image, caption=caption)
                    
                elif main_video:
                    await message.answer_video(main_video, caption=caption)
                else:
                    await message.answer(caption)
    except Exception as e:
        print(e)


async def connect_to_seller(message: Message):
    await bot.send_message(message.from_user.id, "Выберите категорию вопроса", reply_markup=faq_keyboard.faq_keyboard())


async def answer(message: Message):
    answer_text = faq_keyboard.get_faq()[message.text]
    await bot.send_message(message.from_user.id, answer_text)


async def start_adding_settings(message: Message):
    await FSMSendMessageToAdmin.message.set()
    cancel_b = KeyboardButton("/cancel")
    cancel_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(cancel_b)
    await bot.send_message(message.from_user.id, "Напишите свой вопрос(/cancel для отмены)", reply_markup=cancel_kb)


async def send_to_admin(message: Message, state: FSMContext):
    text = message.text
    if is_banned(text):
        await bot.send_message(message.from_user.id, "Сообщение не отправлено, так как содержит оскорбления")
        return
    await bot.send_message(ADMIN_ID, text)
    await state.finish()


async def plug(message: Message):
    print(f"___Unresolved___\nMessage from: {message['from']}\nchat: {message['chat']}\ntext: {message.text}\n___")


def is_banned(text):
    return False
