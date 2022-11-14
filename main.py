from enum import Enum

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.utils import executor
from aiogram import Bot

import keyboards as kb
from config import *

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
    await message.answer(developed_countries_text)


@dp.message_handler(text="Пропустить", state=CalculateStates.enter_netto)
async def skip_netto(message: Message):
    await CalculateStates.next()
    await message.answer(brutto_text, reply_markup=ReplyKeyboardRemove())


@dp.message_handler(state=CalculateStates.enter_netto)
async def select_netto(message: Message, state: FSMContext):
    try:
        await state.update_data(price_type=PriceTypes.netto.value, price=int(message.text))
    except ValueError:
        await message.answer(price_error_text)
    await CalculateStates.enter_old.set()
    await message.answer(car_old_text, reply_markup=kb.car_old)


@dp.message_handler(state=CalculateStates.enter_brutto)
async def select_brutto(message: Message, state: FSMContext):
    try:
        await state.update_data(price_type=PriceTypes.brutto.value, price=int(message.text))
    except ValueError:
        await message.answer(price_error_text)
    await CalculateStates.enter_old.set()
    await message.answer(car_old_text, reply_markup=kb.car_old)


@dp.message_handler(lambda m: m.text in ["Авто до 3-х лет", "Авто от 3-х до 5-ти лет", "Электрокар"],
                    state=CalculateStates.enter_old)
async def select_car_old(message: Message, state: FSMContext):
    car_old_dict = {"Авто до 3-х лет": 1, "Авто от 3-х до 5-ти лет": 2, "Электрокар": 3}
    await state.update_data(price_type=PriceTypes.brutto.value, price=car_old_dict[message.text])


@dp.message_handler(text="Консультация")
async def help_message(message: Message):
    await message.answer(help_text, reply_markup=kb.help)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
