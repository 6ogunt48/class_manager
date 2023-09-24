import os
from fastapi import Depends, FastAPI
from tortoise.contrib.fastapi import register_tortoise
from application.config import Settings, get_settings
from application.api import ping


def create_application() -> FastAPI:
    app = FastAPI()
    app.include_router(ping.router, prefix="/env", tags=["env"])
    return app


app = create_application()
