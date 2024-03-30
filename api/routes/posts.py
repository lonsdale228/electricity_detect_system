from fastapi import APIRouter, Depends, HTTPException, status

from api.schemas.models import Post
from api.utils.post_crud import post_create, get_all_users
from database.connection import get_session

router = APIRouter(tags=["posts"])


@router.post("/create", status_code=status.HTTP_201_CREATED, response_model=Post)
async def create_post(post: Post, session=Depends(get_session)):
    return await post_create(session=session, post=post)


@router.get("/get_all_userss", status_code=status.HTTP_201_CREATED, response_model=list[Post])
async def get_users(skip: int = 0, limit: int = 10, session=Depends(get_session)):
    if limit > 100 or limit <= 0: limit = 1
    return await get_all_users(offset=skip, limit=limit, session=session)
