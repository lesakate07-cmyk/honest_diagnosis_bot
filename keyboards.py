from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def answer_keyboard(options):
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=o)] for o in options],
        resize_keyboard=True
    )

def start_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Начать диагностику")]],
        resize_keyboard=True
    )

def offer_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Хочу на 3 дня")],
            [KeyboardButton(text="Пока подумаю")]
        ],
        resize_keyboard=True
    )
