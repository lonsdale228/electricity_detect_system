from loader import dp
from aiogram.types import Message
from aiogram.filters import Command


@dp.message(Command("start"))
async def start(message: Message):
    await message.answer("Привіт! \n"
                         "Для створення APi ключу, введіть команду: \n"
                         "/get_api_key \n"
                         "Для додання своєї адреси, введіть: \n"
                         "/add_address")