import uuid

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID

from database.connection import Base, engine


class ApiUsers(Base):
    __tablename__ = 'api_users'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    api_key = Column(String)


Base.metadata.create_all(engine)
