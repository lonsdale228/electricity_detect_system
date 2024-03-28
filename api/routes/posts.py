from fastapi import APIRouter, Depends, HTTPException, status


router = APIRouter(tags=["posts"])

@router.post("/create", status_code=status.HTTP_201_CREATED, response_model=Post)
def create_post(post: Post, db: Session = Depends(get_db)):
    return post_create(db=db, post=post)
