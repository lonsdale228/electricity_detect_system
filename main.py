import asyncio

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes.posts import router
from api.schemas.models import HealthResponse
from database.connection import async_engine
from database.models import Base

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router=router, prefix="/posts")


@app.get("/", response_model=HealthResponse)
async def health():
    return HealthResponse(status="Ok")


async def main():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


if __name__ == '__main__':
    asyncio.run(main())
    uvicorn.run(app, port=8000, host='0.0.0.0')
