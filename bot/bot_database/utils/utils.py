from sqlalchemy import select

from bot_database.connection import sessionmanager
from bot_database.models import Addresses


async def add_address_to_db(tg_id: int, latitude: float, longitude: float):
    async with sessionmanager.session() as session:
        session.add(Addresses(longitude=longitude, latitude=latitude, is_private=False, electricity_status=True, tg_id=tg_id))
        await session.commit()