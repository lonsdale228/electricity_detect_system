import asyncio
import logging

from aiogram import F
from sqlalchemy import select, delete

from database.connection import sessionmanager, get_session
from database.models import Base, ApiUsers, Addresses
from loader import bot, dp
from aiogram.types import Message
from aiogram.filters import Command
import aiohttp

URL = "http://web/posts/createe"
data = {
    "key": "1234"
}


async def get_my_status(tg_id: int):
    async with sessionmanager.session() as session:
        stmt = select(Addresses).where(Addresses.tg_id == tg_id).limit(1)
        result = await session.execute(stmt)

        result = result.scalar_one_or_none()

        if result is not None:
            return result


async def get_token(tg_id: int):
    db_user = ApiUsers(tg_id=tg_id)
    async with sessionmanager.session() as session:
        stmt = select(ApiUsers).where(ApiUsers.tg_id == tg_id)
        result = await session.execute(stmt)

        result = result.scalar_one_or_none()

        if result is not None:
            return result
        else:
            async with session:
                session.add(db_user)
                await session.commit()
                await session.refresh(db_user)
            return db_user


async def delete_usr(tg_id: int):
    async with sessionmanager.session() as session:
        stmt = select(ApiUsers).where(ApiUsers.tg_id == tg_id)
        result = await session.execute(stmt)

        result = result.scalar_one_or_none()
        if result is not None:
            stmt = delete(ApiUsers).where(ApiUsers.tg_id == tg_id)
            async with session:
                await session.execute(stmt)
                await session.commit()
                return True
        else:
            return False


@dp.message(Command("get_api_key"))
async def start_message(message: Message):
    user_id = message.from_user.id
    usr = await get_token(user_id)
    await message.answer(f'Your api key <code>{usr.api_key}</code> \nYour user_id: <code>{user_id}</code>')


@dp.message(Command("remove_my_data"))
async def delete_data(message: Message):
    user_id = message.from_user.id
    delete_status = await delete_usr(user_id)
    if delete_status:
        await message.answer(f'Your data was deleted!')
    else:
        await message.answer(f'Your data already deleted!')


@dp.message(Command("status"))
async def status(message: Message):
    user_id = message.from_user.id
    status = await get_my_status(user_id)

    if status.electricity_status:
        await message.answer('Світло увімкненно!')
    else:
        await message.answer('Світло вимкненно!')


@dp.message(F.location)
async def get_location(message: Message):
    await message.answer(f'{message.location.latitude}, {message.location.longitude}')

async def main():
    async with sessionmanager.connect() as connection:
        await connection.run_sync(Base.metadata.create_all)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
