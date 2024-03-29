import uuid

from sqlalchemy import Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column, Mapped, declarative_base

Base = declarative_base()


class Posts(Base):
    __tablename__ = "posts"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=lambda: str(uuid.uuid4()),
                                     index=True)
    title: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    api_key: Mapped[str] = mapped_column()


class ApiUsers(Base):
    __tablename__ = "api_users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    api_key: Mapped[str] = mapped_column()


class Addresses(Base):
    __tablename__ = "Addresses"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    is_private: Mapped[bool] = mapped_column()
