from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
# from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from api.schemas.models import Post
from api.utils.post_crud import post_create
from database.connection import get_session, AsyncSession

router = APIRouter(tags=["posts"])


@router.post("/create", status_code=status.HTTP_201_CREATED, response_model=Post)
async def create_post(post: Post, session: AsyncSession):
    print("Post received!")
    return await post_create(session=session, post=post)
