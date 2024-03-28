from sqlalchemy.ext.asyncio import AsyncSession

from api.schemas.models import Post
from database.models import Posts


async def post_create(session: AsyncSession, post: Post):
    db_user = Posts(api_key=post.api_key, title=post.title, description=post.description)

    async with session:
        session.add(db_user)
        await session.commit()
        await session.refresh(db_user)
    return db_user
