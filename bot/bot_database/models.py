import secrets
import uuid
from datetime import datetime

from sqlalchemy import Integer, DateTime, BigInteger, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column, Mapped, declarative_base, relationship

Base = declarative_base()


class Posts(Base):
    __tablename__ = "posts"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=lambda: str(uuid.uuid4()),
                                     index=True)
    title: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    api_key: Mapped[str] = mapped_column(default=lambda: str(secrets.token_urlsafe(16)))


class ApiUsers(Base):
    __tablename__ = "api_users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    api_key: Mapped[str] = mapped_column(default=lambda: str(secrets.token_urlsafe(16)))
    created_at = mapped_column(DateTime, default=lambda: datetime.now())
    last_usage = mapped_column(DateTime, default=None)
    tg_id = mapped_column(BigInteger, unique=True)

    addresses = relationship("Addresses", back_populates="api_user")


class Addresses(Base):
    __tablename__ = "addresses"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    is_private: Mapped[bool] = mapped_column()
    tg_id = mapped_column(BigInteger, ForeignKey('api_users.tg_id'), unique=False)
    electricity_status: Mapped[bool] = mapped_column()
    latitude: Mapped[float] = mapped_column()
    longitude: Mapped[float] = mapped_column()
    last_update: Mapped[datetime] = mapped_column(default=None)

    api_user = relationship("ApiUsers", back_populates="addresses")
