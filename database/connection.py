from decouple import config
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession

engine = create_async_engine(config("DATABASE_URL"), echo=True)
