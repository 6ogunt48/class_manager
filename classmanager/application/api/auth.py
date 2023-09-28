import os
from datetime import datetime, timedelta
from typing import Optional

import jwt
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from starlette import status

from application.db.app_models import User, UserRole
from application.pydantic import (LoginResponse, UserCreate,
                                  UserCreateResponse, UserLogin)
from application.utils import async_hash_password, verify_password

router = APIRouter()

SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = "HS256"


def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=40)) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_jwt_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.PyJWTError:
        return None


@router.post("/register-user/", status_code=status.HTTP_201_CREATED, response_model=UserCreateResponse)
async def register_user(user_data: UserCreate) -> UserCreateResponse:
    user_exists = await User.filter(email=user_data.email).first()
    if user_exists:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
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


@router.post("/login/", status_code=status.HTTP_200_OK, response_model=LoginResponse)
async def login(user_data: UserLogin) -> LoginResponse:
    user = await User.filter(username=user_data.username).first()
    if not user or not await verify_password(user_data.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")

    access_token = create_access_token(data={"username": user.username})

    response = JSONResponse(content={"message": "Authentication Successful"})
    response.set_cookie(key="access_token", value=access_token, httponly=True)
    return LoginResponse(message="Authentication Successful", access_token=access_token)

"""
write test for login endpoint
write test for logout endpoint
implement logout endpoint
write test to change passwird endpoint
implment change password endpoint
"""
