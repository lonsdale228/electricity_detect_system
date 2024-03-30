import logging
from time import time

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

from api.routes.posts import router
from api.schemas.models import HealthResponse

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

if __name__ == '__main__':
    logging.basicConfig(level=logging.ERROR)
    uvicorn.run(app, port=8000, host='0.0.0.0')