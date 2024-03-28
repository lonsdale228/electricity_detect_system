from fastapi import APIRouter, Depends, HTTPException, status

from api.schemas.models import Post
from api.utils.post_crud import post_create
from database.connection import get_session

router = APIRouter(tags=["posts"])


@router.post("/create", status_code=status.HTTP_201_CREATED, response_model=Post)
async def create_post(post: Post, session=Depends(get_session)):
    return await post_create(session=session, post=post)
