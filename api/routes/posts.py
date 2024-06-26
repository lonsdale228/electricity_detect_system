from fastapi import APIRouter, Depends, HTTPException, status

from api.schemas.models import Post, ApiUser, Address
from api.utils.post_crud import post_create, get_all_users, create_api_user, get_all_addresses, check_api_key_exists, \
    get_uniq_address
from database.connection import get_session

router = APIRouter(tags=["gets"])


# @router.post("/createe", status_code=status.HTTP_201_CREATED)
# async def create_user(api_user: ApiUser, session=Depends(get_session)):
#     create = await create_api_user(session, api_user=api_user)
#     return create.api_key
#
#
# @router.post("/create", status_code=status.HTTP_201_CREATED)
# async def create_post(post: Post, session=Depends(get_session)):
#     if post.key == "1234":
#
#         create = await post_create(session=session, post=post)
#         return create.id, create.api_key
#     else:
#         return status.HTTP_401_UNAUTHORIZED


@router.get("/get_all_users", status_code=status.HTTP_201_CREATED, response_model=list[Post])
async def get_users(skip: int = 0, limit: int = 10, session=Depends(get_session)):
    if limit > 100 or limit <= 0: limit = 1
    if skip < 0: skip = 0
    return await get_all_users(offset=skip, limit=limit, session=session)


@router.get("/get_all_addresses", status_code=status.HTTP_201_CREATED, response_model=list[Address])
async def get_addresses(api_key, skip: int = 0, limit: int = 10, session=Depends(get_session)):
    if await check_api_key_exists(session, api_key):
        return await get_all_addresses(offset=skip, limit=limit, session=session)
    else:
        return status.HTTP_401_UNAUTHORIZED


@router.get("/get_uniq_address", status_code=status.HTTP_201_CREATED, response_model=list[Address])
async def get_uniq(api_key, user_id: int, session=Depends(get_session)):
    if await check_api_key_exists(session, api_key):
        return await get_uniq_address(api_key=api_key, user_id=user_id, session=session)
    else:
        return status.HTTP_401_UNAUTHORIZED
