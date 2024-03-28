from decouple import config
from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession, async_scoped_session
from sqlalchemy.orm import sessionmaker, scoped_session
from asyncio import current_task
from typing import Annotated, AsyncIterator

# SQLALCHEMY_DATABASE_URL = config("DATABASE_URL")
SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://postgres:1111@localhost:5432/electricity"

async_engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,
    echo=True,
)
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    autoflush=False,
    future=True,
)


async def get_session() -> AsyncIterator[async_sessionmaker]:
    try:
        yield AsyncSessionLocal
    except SQLAlchemyError as e:
        print(e)


AsyncSession = Annotated[async_sessionmaker, Depends(get_session)]
