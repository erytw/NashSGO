from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup,\
    KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

register = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Регистрация")]
    ],
    resize_keyboard=True
)

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Ближайшее Д/з")],
        [KeyboardButton(text="Оценки за день")],
        [KeyboardButton(text="Оценки за 7 дней")],
        [KeyboardButton(text="Данные школы"),
         KeyboardButton(text="Перерегистрация")]
    ],
    resize_keyboard=True
)

call_main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Меню")]
    ],
    resize_keyboard=True
)

remove = ReplyKeyboardRemove()
