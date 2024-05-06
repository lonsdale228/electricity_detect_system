import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, join
from api.schemas.models import Post, ApiUser
from database.models import Posts, ApiUsers, Addresses


async def create_api_user(session: AsyncSession, api_user: ApiUser):
    db_user = ApiUsers(tg_id=api_user.tg_id)

    async with session:
        stmt = select(ApiUsers).where(ApiUsers.tg_id == api_user.tg_id)
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


async def post_create(session: AsyncSession, post: Post):
    db_user = Posts(title="", description="")

    async with session:
        session.add(db_user)
        await session.commit()
        await session.refresh(db_user)
    return db_user


async def get_all_users(session: AsyncSession, limit: int = 10, offset: int = 0):
    async with session:
        stmt = select(Posts).offset(offset).limit(limit)
        result = await session.execute(stmt)
        return result.scalars().all()


async def check_api_key_exists(session: AsyncSession, api_key: str):
    async with session:
        stmt = select(ApiUsers).where(ApiUsers.api_key == api_key)
        result = await session.execute(stmt)
        return result.one_or_none()


async def get_all_addresses(session: AsyncSession, limit: int = 10, offset: int = 0):
    async with session:
        stmt = select(Addresses)
        result = await session.execute(stmt)
        return result.scalars().all()


async def get_my_address(session: AsyncSession, tg_id: int):
    async with session:
        stmt = select(Addresses).where(Addresses.tg_id == tg_id)
        result = await session.execute(stmt)
        return result.scalars().all()


async def get_uniq_address(session: AsyncSession, api_key, user_id: int = 0):
    if await check_api_key_exists(session, api_key):
        async with session:
            stmt = select(Addresses).where(ApiUsers.id == user_id).limit(1)
            result = await session.execute(stmt)
            return result.scalars().all()
    else:
        print("API key not exist!")


async def ping_status_to_db(session: AsyncSession, electricity_status: bool, address_id: int, api_key):
    async with session.begin():
        stmt = select(ApiUsers).where(ApiUsers.api_key == api_key)
        result = await session.execute(stmt)
        user = result.scalars().first()

        if user:
            if address_id == -1:
                await session.execute(
                    update(Addresses)
                    .where(Addresses.tg_id == user.tg_id)
                    .values(last_update=datetime.datetime.now(), electricity_status=electricity_status)
                )
            else:
                await session.execute(
                    update(Addresses)
                    .where(Addresses.tg_id == user.tg_id)
                    .where(Addresses.id == address_id)
                    .values(last_update=datetime.datetime.now(), electricity_status=electricity_status)
                )
            await session.commit()
        else:
            print("No user found with the provided API key")
