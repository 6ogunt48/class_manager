import os
from application.db.database_config import init_db
import logging
from fastapi import Depends, FastAPI
from tortoise.contrib.fastapi import register_tortoise
from application.config import Settings, get_settings
from application.api import ping

log = logging.getLogger("uvicorn")


def create_application() -> FastAPI:
    application = FastAPI()
    application.include_router(ping.router, prefix="/env", tags=["env"])

    return application


app = create_application()


@app.on_event("startup")
async def startup_event():
    log.info("Starting up....................")
    init_db(app)


@app.on_event("shutdown")
async def shutdown_event():
    log.info("Shutting down..................")
