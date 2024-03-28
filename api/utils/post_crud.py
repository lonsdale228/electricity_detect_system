from uuid import UUID

from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from sqlalchemy.orm import Session
from starlette import schemas

from api.schemas.models import Post
from database.models import Posts


async def post_create(session, post: Post):
    db_user = Posts(api_key=post.api_key, title=post.title, description=post.description)

    async with session.begin() as session:
        session.add(db_user)
        print("boba")
        await session.commit()
        await session.refresh(db_user)
    return db_user
