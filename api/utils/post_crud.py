from uuid import UUID

from sqlalchemy.orm import Session
from starlette import schemas

from api.schemas.models import Post
from database.models import Posts


def post_create(db: Session, post: Post):
    db_user = Posts(api_key=post.api_key, title=post.title, description=post.description)
    db.add(db_user)
    print("boba")
    db.commit()
    db.refresh(db_user)
    return db_user
