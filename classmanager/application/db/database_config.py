import os

from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

TORTOISE_ORM = {
    "connections": {"default": os.environ.get("DATABASE_URL")},
    "apps": {
        "models": {
            "models": ["application.db.app_models", "aerich.models"],
            "default_connection": "default",
        },
    },
}


def init_db(application: FastAPI) -> None:
    register_tortoise(
        application,
        db_url=os.environ.get("DATABASE_URL"),
        modules={"models": ["application.db.app_models"]},
        generate_schemas=False,
        add_exception_handlers=True,
    )
