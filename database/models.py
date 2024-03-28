import uuid

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
