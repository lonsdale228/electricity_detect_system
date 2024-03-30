import asyncio
import logging

from loader import bot, dp
from aiogram.types import Message
from aiogram.filters import Command
import aiohttp

URL = "http://web/posts/createe"
data = {
    "key": "1234"
}


async def get_token(tg_id: int):
    async with aiohttp.ClientSession() as session:
        json = data
        json["tg_id"] = tg_id
        async with session.post(URL, json=json) as response:
            answer = await response.json()
            logging.critical(answer)
            return answer


@dp.message(Command("get_api_key"))
async def start_message(message: Message):
    user_id = message.from_user.id
    api_key = await get_token(user_id)
    await message.answer(f'Your api key <code>{api_key}</code>, \nYour user_id: <code>{user_id}</code>')


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
