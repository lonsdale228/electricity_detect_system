from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
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


async def get_all_addresses(session: AsyncSession, limit: int = 10, offset: int = 0):
    async with session:
        stmt = select(Addresses)
        result = await session.execute(stmt)
        return result.scalars().all()
