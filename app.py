import asyncio
import logging
from time import time
import redis.asyncio as redis
import uvicorn
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter

from starlette.middleware.base import BaseHTTPMiddleware

from api.routes.posts import router
from api.schemas.models import HealthResponse

from contextlib import asynccontextmanager

from database.connection import sessionmanager
from database.models import Base


@asynccontextmanager
async def lifespan(_: FastAPI):
    redis_connection = redis.from_url("redis://redis:6379", encoding="utf8")
    await FastAPILimiter.init(redis_connection)
    yield
    await FastAPILimiter.close()


app = FastAPI(lifespan=lifespan)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router=router, prefix="/posts")


@app.get("/", response_model=HealthResponse, dependencies=[Depends(RateLimiter(times=60, seconds=60))])
async def health():
    async with sessionmanager.connect() as connection:
        await connection.run_sync(Base.metadata.create_all)
    return HealthResponse(status="Ok")

# if __name__ == '__main__':
#
#     logging.basicConfig(level=logging.ERROR)
#     uvicorn.run(app, port=8000, host='0.0.0.0')
