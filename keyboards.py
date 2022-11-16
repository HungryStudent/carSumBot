from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from texts import admin_username

country1 = 'Авто из Германии'
country2 = 'Авто из США'
country3 = 'Авто из ОАЭ'
consultation = 'Консультация'

skip_netto_text = 'Пропустить'

young_car = 'Авто до 3-х лет'
old_car = 'Авто от 3-х до 5-ти лет'
electric_car = "Электрокар"

ask = "Задать вопрос"
request_calculation = "Запросить расчёт"

brest_no_mileage = 'До г.Брест (без пробега)'
brest_with_mileage = 'До г.Брест (своим ходом)'
moscow_no_mileage = 'До г.Москва (без пробега)'
moscow_with_mileage = 'До г.Москва (своим ходом)'


reset_calculation = "Рассчитать ещё"
buy = 'Заказать'
menu = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1).add(KeyboardButton(country1),
                                                                  KeyboardButton(country2),
                                                                  KeyboardButton(country3),
                                                                  KeyboardButton(consultation))

skip_netto = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1).add(KeyboardButton(skip_netto_text))

car_old = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1).add(KeyboardButton(young_car),
                                                                     KeyboardButton(old_car),
                                                                     KeyboardButton(electric_car))

help = InlineKeyboardMarkup(row_width=1).add(
    InlineKeyboardButton(text=ask, url=f"https://t.me/{admin_username}"))
developed_countries = InlineKeyboardMarkup(row_width=1).add(
    InlineKeyboardButton(text=request_calculation, url=f"https://t.me/{admin_username}"))

transit = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1).add(KeyboardButton(brest_no_mileage),
                                                                     KeyboardButton(brest_with_mileage),
                                                                     KeyboardButton(moscow_no_mileage),
                                                                     KeyboardButton(moscow_with_mileage))

res = InlineKeyboardMarkup(resize_keyboard=True, row_width=1).add(
    InlineKeyboardButton(reset_calculation, callback_data="reset"),
    InlineKeyboardButton(buy, url=f"https://t.me/{admin_username}"),
    InlineKeyboardButton(ask, url=f"https://t.me/{admin_username}"))
