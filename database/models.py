import uuid

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import mapped_column, Mapped, DeclarativeBase, declarative_base

Base = declarative_base()


class Posts(Base):
    __tablename__ = "posts"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=lambda: str(uuid.uuid4()),
                                     index=True)
    title: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    api_key: Mapped[str] = mapped_column()
