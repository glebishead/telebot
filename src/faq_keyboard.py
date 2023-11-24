from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from data.methods.select_id_from_faq import select_from_faq

Q_COUNT = 3


def get_faq():
    res = {}
    for qid in range(1, Q_COUNT + 1):
        question, answer = select_from_faq(qid)
        res[question] = answer
    return res


def faq_keyboard():
    button0 = KeyboardButton("моего вопроса нет в списке")

    result_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for question in get_faq().keys():
        button = KeyboardButton(question)
        result_kb.row(button)

    result_kb.row(button0)
    return result_kb
