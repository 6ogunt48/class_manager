from fastapi import APIRouter, Depends

from application.config import Settings, get_settings

router = APIRouter()


# ping route for checking service and configuration status and current environment
@router.get("/ping")
async def pong(settings: Settings = Depends(get_settings)) -> dict:
    return {
        "ping": "pong!",
        "environment": settings.environment,
        "testing": settings.testing,
    }
