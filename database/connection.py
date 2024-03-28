from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession, async_scoped_session

from database.models import Base

# SQLALCHEMY_DATABASE_URL = config("DATABASE_URL")
SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://postgres:1111@localhost:5432/electricity"

engine = create_async_engine(SQLALCHEMY_DATABASE_URL)


async def get_session_maker():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    return async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_session() -> AsyncSession:
    session_maker = await get_session_maker()
    async with session_maker() as session:
        yield session
