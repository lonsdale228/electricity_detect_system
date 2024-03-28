import uuid

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID

from database.connection import Base, engine


class Posts(Base):
    __tablename__ = "posts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    title = Column(String)
    description = Column(String)
    api_key = Column(String)


Base.metadata.create_all(engine)
