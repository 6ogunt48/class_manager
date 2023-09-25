from fastapi import APIRouter, HTTPException
from fastapi.concurrency import run_in_threadpool
from starlette import status

from application.db.app_models import User, UserRole
from application.pydantic import UserCreate, UserCreateResponse
from application.utils import hash_password

router = APIRouter()


# we run hashing in separate threads to improve performance
async def async_hash_password(password: str) -> str:
    return await run_in_threadpool(hash_password, password)


@router.post(
    "/register-user/",
    status_code=status.HTTP_201_CREATED,
    response_model=UserCreateResponse,
)
async def register_user(user_data: UserCreate) -> UserCreateResponse:
    user_exists = await User.filter(email=user_data.email).first()
    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )
    hashed_password = await async_hash_password(user_data.password)
    await User.create(
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        username=user_data.username,
        email=user_data.email,
        password_hash=hashed_password,
        role=UserRole[user_data.role.upper()],
    )
    return UserCreateResponse(message="Registration successful")
