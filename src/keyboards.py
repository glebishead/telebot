from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

faq = {}  # todo: фунцкия получения часто задавыемых вопросов

def faq_keyboard():
    button1 = KeyboardButton("моего вопроса нет в списке")

    result_kb = ReplyKeyboardMarkup(resize_keyboard=True)
    result_kb.row(button1)
    for question in faq.keys():
        button = KeyboardButton(question)
        result_kb.row(button)
    return result_kb
