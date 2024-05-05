from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str


class ApiUser(BaseModel):
    tg_id: int


class Post(BaseModel):
    id: Optional[UUID] = Field(None, description="Who sends the error message.")
    api_key: Optional[str] = Field(None, description="Enter valid api key...")

    class Config:
        from_attributes = True


class Address(BaseModel):
    id: int = Field(None, description="Who sends the error")
    latitude: float = Field(None, description="")
    longitude: float = Field(None, description="")
    electricity_status: bool = Field(None)

    class Config:
        from_attributes = True


class Delete(BaseModel):
    id: UUID = Field()
    api_key: str = Field(None, description="Enter valid api key...")

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
