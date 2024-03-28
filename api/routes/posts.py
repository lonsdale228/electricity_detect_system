from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from api.schemas.models import Post
from api.utils.post_crud import post_create
from database.connection import get_db


router = APIRouter(tags=["posts"])


@router.post("/create", status_code=status.HTTP_201_CREATED, response_model=Post)
def create_post(post: Post, db: Session = Depends(get_db)):
    print("Post received!")
    return post_create(db=db, post=post)
