from enum import Enum

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.utils import executor
from aiogram import Bot

import keyboards as kb
from config import TOKEN
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


@dp.message_handler(text=kb.country1)
async def start_calculation(message: Message):
    await CalculateStates.enter_netto.set()
    await message.answer(netto_text, reply_markup=kb.skip_netto)


@dp.message_handler(lambda mes: mes.text in [kb.country2, kb.country3])
async def developed_countries(message: Message):
    await message.answer(developed_countries_text, reply_markup=kb.developed_countries)


@dp.message_handler(text=kb.skip_netto_text, state=CalculateStates.enter_netto)
async def skip_netto(message: Message):
    await CalculateStates.next()
    await message.answer(brutto_text, reply_markup=ReplyKeyboardRemove())


@dp.message_handler(state=CalculateStates.enter_netto)
async def select_netto(message: Message, state: FSMContext):
    try:
        await state.update_data(price_type=PriceTypes.netto.value, price=int(message.text))
    except ValueError:
        await message.answer(int_error_text)
        return
    await CalculateStates.enter_old.set()
    await message.answer(car_old_text, reply_markup=kb.car_old)


@dp.message_handler(state=CalculateStates.enter_brutto)
async def select_brutto(message: Message, state: FSMContext):
    try:
        await state.update_data(price_type=PriceTypes.brutto.value, price=int(message.text))
    except ValueError:
        await message.answer(int_error_text)
        return
    await CalculateStates.enter_old.set()
    await message.answer(car_old_text, reply_markup=kb.car_old)


@dp.message_handler(lambda m: m.text in [kb.young_car, kb.old_car, kb.electric_car],
                    state=CalculateStates.enter_old)
async def select_car_old(message: Message, state: FSMContext):
    car_old_dict = {kb.young_car: 1, kb.old_car: 2, kb.electric_car: 3}
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
    transit_dict = {kb.brest_no_mileage: 1500, kb.brest_with_mileage: 1200,
                    kb.moscow_no_mileage: 2850, kb.moscow_with_mileage: 2200}
    await state.update_data(transit=message.text)

    data = await state.get_data()
    res = data["price"]
    if data["car_old"] == 1:
        res += data["price"] * 0.24
    elif data["car_old"] == 2:
        if 1001 < data["size"] < 1500:
            res += data["size"] * 1.7/2
        elif 1501 < data["size"] < 1800:
            res += data["size"] * 2.5/2
        elif 1801 < data["size"] < 2300:
            res += data["size"] * 2.7/2
            print(data["size"] * 2.7 / 2)
        elif 2301 < data["size"] < 3000:
            res += data["size"] * 3/2
        else:
            res += data["size"] * 3.6/2
    elif data["car_old"] == 3:
        res += data["price"] * 0.075

    res += transit_dict[data["transit"]]
    res += data["price"] * 0.06 + 3100
    res *= 1.02
    res *= 1.1
    await message.answer(res_text.format(res=int(res)), reply_markup=kb.res)
    await state.finish()


@dp.callback_query_handler(text="reset")
async def func(call: CallbackQuery):
    await call.message.answer(hello_text, reply_markup=kb.menu)
    await call.answer()


@dp.message_handler(text=kb.consultation)
async def help_message(message: Message):
    await message.answer(help_text, reply_markup=kb.help)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
