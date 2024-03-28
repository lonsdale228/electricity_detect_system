from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str


class Post(BaseModel):
    id: Optional[UUID] = Field(None, description="Who sends the error message.")
    title: str
    description: str
    api_key: str

    class Config:
        from_attributes = True



# class DeletePostResponse(BaseModel):
#     detail: str
#
#
# class UpdatePost(BaseModel):
#     id: UUID
#     title: str
#     description: str
#     api_key: str
#
#     class Config:
#         orm_mode = True