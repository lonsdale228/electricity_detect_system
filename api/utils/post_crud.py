from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from api.schemas.models import Post
from database.models import Posts


async def post_create(session: AsyncSession, post: Post):
    db_user = Posts(api_key=post.api_key, title=post.title, description=post.description)

    async with session:
        session.add(db_user)
        await session.commit()
        await session.refresh(db_user)
    return db_user


async def get_all_users(session: AsyncSession):
    async with session:
        stmt = select(Posts).limit(100)
        result = await session.execute(stmt)
        return result.scalars().all()
