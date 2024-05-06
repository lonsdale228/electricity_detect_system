import os
import sys

from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from aiogram import types, F
import requests

from handlers.start import start
from keyboards.add_menu import keyboard_back
from loader import bot, dp
from bot_database.utils.utils import add_address_to_db


class AddAddress(StatesGroup):
    choosing_address = State()
    verifying_address = State()


@dp.message(StateFilter(AddAddress), F.text == "🔙Повернутися")
async def back_to_main_menu(message: types.Message, state: FSMContext):
    await state.clear()
    await start(message)


@dp.message(Command('add_address'), StateFilter(None))
async def add_address(message: types.Message, state: FSMContext):
    await message.answer("Введіть Вашу адресу у форматі 12.3456, 12.3456 ,\n"
                         "Або ж просто надішліть геолокацію за допомогою телеграм", reply_markup=keyboard_back)
    await state.set_state(AddAddress.choosing_address)


@dp.message(StateFilter(AddAddress.choosing_address), F.location)
async def get_address_location(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    latitude = message.location.latitude
    longitude = message.location.longitude
    await state.update_data(latitude=latitude, longitude=longitude)

    await message.answer_location(latitude=latitude, longitude=longitude)
    await bot.send_message(user_id, 'Чи корректно відображається Ваша адреса?', reply_markup=keyboard_back)
    await state.set_state(AddAddress.verifying_address)


# def resolve_short_url(short_url):
#     response = requests.get(short_url)
#     return response.url
# @dp.message(StateFilter(AddAddress.choosing_address), F.text.contains('https'))
# async def get_address_google(message: types.Message, state: FSMContext):
#     long_url = resolve_short_url(message.text.strip())
#     await message.answer(long_url)


@dp.message(StateFilter(AddAddress.choosing_address), F.text)
async def get_address_text(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    try:
        latitude = float(message.text[0].strip())
        longitude = float(message.text[1].strip())
        await state.update_data(latitude=latitude, longitude=longitude)
        await message.answer_location(latitude=latitude, longitude=longitude)
        await bot.send_message(user_id, 'Чи корректно відображається Ваша адреса?', reply_markup=keyboard_back)
        await state.set_state(AddAddress.verifying_address)
    except Exception:
        await message.reply("Введіть будь ласка корректні координати!", reply_markup=keyboard_back)


@dp.message(StateFilter(AddAddress.verifying_address))
async def verify_address(message: types.Message, state: FSMContext):
    data = await state.get_data()
    latitude = data['latitude']
    longitude = data['longitude']
    if message.text == "Так":
        await add_address_to_db(message.from_user.id, latitude, longitude)
        await state.clear()
        await message.answer('Ваша адреса була успішно додана до мапи!')
    if message.text == "Ні":
        await add_address(message, state)
