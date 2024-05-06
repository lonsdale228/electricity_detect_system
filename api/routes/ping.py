from fastapi import APIRouter, Depends
from fastapi import status

from api.utils.post_crud import check_api_key_exists, ping_status_to_db
from database.connection import get_session

ping_router = APIRouter(tags=["ping"])


@ping_router.get("/ping_status", status_code=status.HTTP_201_CREATED)
async def ping_status(api_key, electricity_status: bool, address_id: int = -1, session=Depends(get_session)):
    if await check_api_key_exists(session, api_key):
        await ping_status_to_db(api_key=api_key, electricity_status=electricity_status, address_id=address_id, session=session)
        return status.HTTP_200_OK
    else:
        return status.HTTP_401_UNAUTHORIZED
