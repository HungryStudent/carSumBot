from enum import Enum

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.utils import executor
from aiogram import Bot

import keyboards as kb
from config import *
from texts import *

stor = MemoryStorage()

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=stor)


class PriceTypes(Enum):
    netto = 1
    brutto = 2


class CalculateStates(StatesGroup):
    enter_netto = State()
    enter_brutto = State()
    enter_old = State()
    enter_size = State()
    enter_transit = State()


async def on_startup(_):
    pass


@dp.message_handler(state="*", commands='start')
async def start_message(message: Message, state: FSMContext):
    await state.finish()
    await message.answer(hello_text, reply_markup=kb.menu)


@dp.message_handler(text="Авто из Германии")
async def start_calculation(message: Message):
    await CalculateStates.enter_netto.set()
    await message.answer(netto_text, reply_markup=kb.skip_netto)


@dp.message_handler(lambda mes: mes.text in ["Авто из США", "Авто из ОАЭ"])
async def developed_countries(message: Message):
    await message.answer(developed_countries_text, reply_markup=kb.developed_countries)


@dp.message_handler(text="Пропустить", state=CalculateStates.enter_netto)
async def skip_netto(message: Message):
    await CalculateStates.next()
    await message.answer(brutto_text, reply_markup=ReplyKeyboardRemove())


@dp.message_handler(state=CalculateStates.enter_netto)
async def select_netto(message: Message, state: FSMContext):
    print(message.text)
    try:
        await state.update_data(price_type=PriceTypes.netto.value, price=int(message.text))
    except ValueError:
        await message.answer(int_error_text)
    await CalculateStates.enter_old.set()
    await message.answer(car_old_text, reply_markup=kb.car_old)


@dp.message_handler(state=CalculateStates.enter_brutto)
async def select_brutto(message: Message, state: FSMContext):
    try:
        await state.update_data(price_type=PriceTypes.brutto.value, price=int(message.text))
    except ValueError:
        await message.answer(int_error_text)
    await CalculateStates.enter_old.set()
    await message.answer(car_old_text, reply_markup=kb.car_old)


@dp.message_handler(lambda m: m.text in ["Авто до 3-х лет", "Авто от 3-х до 5-ти лет", "Электрокар"],
                    state=CalculateStates.enter_old)
async def select_car_old(message: Message, state: FSMContext):
    car_old_dict = {"Авто до 3-х лет": 1, "Авто от 3-х до 5-ти лет": 2, "Электрокар": 3}
    await state.update_data(car_old=car_old_dict[message.text])

    if car_old_dict[message.text] == 2:
        await CalculateStates.enter_size.set()
        await message.answer(size_text, reply_markup=ReplyKeyboardRemove())
    else:
        await CalculateStates.enter_transit.set()
        await message.answer(transit_text, reply_markup=kb.transit)


@dp.message_handler(state=CalculateStates.enter_size)
async def select_size(message: Message, state: FSMContext):
    try:
        await state.update_data(size=int(message.text))
    except ValueError:
        await message.answer(int_error_text)
    await CalculateStates.next()
    await message.answer(transit_text, reply_markup=kb.transit)


@dp.message_handler(state=CalculateStates.enter_transit)
async def select_transit(message: Message, state: FSMContext):
    transit_dict = {"До г.Брест (без пробега)": 1500, "До г.Брест (своим ходом)": 1200,
                    "До г.Москва (без пробега)": 2850, "До г.Москва (своим ходом)": 2500}
    await state.update_data(transit=message.text)

    data = await state.get_data()
    res = data["price"]
    if data["car_old"] == "1":
        res += data["price"] * 0.24
    elif data["car_old"] == "2":
        if 1001 < int(data["size"]) < 1500:
            res += int(data["size"]) * 1.7
        if 1501 < int(data["size"]) < 1800:
            res += int(data["size"]) * 2.5
        if 1801 < int(data["size"]) < 2300:
            res += int(data["size"]) * 2.7
        if 2301 < int(data["size"]) < 3000:
            res += int(data["size"]) * 3
        else:
            res += int(data["size"]) * 3.6
    elif data["car_old"] == "3":
        res += data["price"] * 0.075

    res += transit_dict[data["transit"]]
    res += data["price"] * 0.06 + 3600
    res *= 1.12
    await message.answer(res_text.format(res=int(res)), reply_markup=kb.res)


@dp.message_handler(text="Консультация")
async def help_message(message: Message):
    await message.answer(help_text, reply_markup=kb.help)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
