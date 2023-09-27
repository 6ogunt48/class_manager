import logging

from fastapi import FastAPI

from application.api import auth, ping
from application.db.database_config import init_db

log = logging.getLogger("uvicorn")


def create_application() -> FastAPI:
    application = FastAPI()
    application.include_router(ping.router, prefix="/env", tags=["env"])
    application.include_router(auth.router, prefix="/auth", tags=["Auth"])

    return application


app = create_application()


@app.on_event("startup")
async def startup_event():
    log.info("Starting up....................")
    init_db(app)


@app.on_event("shutdown")
async def shutdown_event():
    log.info("Shutting down..................")

