from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

generation_text_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text = "/quote")
        ],
        [
            KeyboardButton(text = "/news")
        ],
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)