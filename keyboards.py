from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from config import admin_username

menu = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1).add(KeyboardButton('Авто из Германии'),
                                                                  KeyboardButton('Авто из США'),
                                                                  KeyboardButton('Авто из ОАЭ'),
                                                                  KeyboardButton('Консультация'))

skip_netto = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1).add(KeyboardButton('Пропустить'))

car_old = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1).add(KeyboardButton('Авто до 3-х лет'),
                                                                     KeyboardButton('Авто от 3-х до 5-ти лет'),
                                                                     KeyboardButton('Электрокар'))

help = InlineKeyboardMarkup(row_width=1).add(
    InlineKeyboardButton(text="Задать вопрос", url=f"https://t.me/{admin_username}"))
developed_countries = InlineKeyboardMarkup(row_width=1).add(
    InlineKeyboardButton(text="Запросить расчёт", url=f"https://t.me/{admin_username}"))

transit = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1).add(KeyboardButton('До г.Брест (без пробега)'),
                                                                     KeyboardButton('До г.Брест (своим ходом)'),
                                                                     KeyboardButton('До г.Москва (без пробега)'),
                                                                     KeyboardButton('До г.Москва (своим ходом)'))

res = InlineKeyboardMarkup(resize_keyboard=True, row_width=1).add(
    InlineKeyboardButton('Рассчитать ещё', callback_data="reset"),
    InlineKeyboardButton('Заказать', url=f"https://t.me/{admin_username}"),
    InlineKeyboardButton('Задать вопрос', url=f"https://t.me/{admin_username}"))
