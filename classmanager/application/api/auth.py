import logging
import os
from datetime import datetime, timedelta
from typing import Optional

import jwt
from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from starlette import status

from application.db.app_models import User, UserRole
from application.pydantic import (LoginResponse, PasswordChange,
                                  PasswordChangeResponse, UserCreate,
                                  UserCreateResponse)
from application.utils import async_hash_password, verify_password

router = APIRouter()

SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login/")
logger = logging.getLogger("uvicorn")


def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=40)) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_token


def decode_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.PyJWTError:
        return None


@router.post("/register-user/", status_code=status.HTTP_201_CREATED, response_model=UserCreateResponse)
async def register_user(user_data: UserCreate) -> UserCreateResponse:
    """ role student or teacher """
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
async def login(response: Response, user_data: OAuth2PasswordRequestForm = Depends()) -> LoginResponse:
    user = await User.filter(username=user_data.username).first()
    if not user or not await verify_password(user_data.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")

    access_token = create_access_token(data={"username": user.username})

    response.set_cookie(key="access_token", value=access_token, httponly=True, secure=True)
    return {"message": "Authentication Successful", "access_token": access_token}


@router.post("/change-password/", status_code=status.HTTP_200_OK, response_model=PasswordChangeResponse)
async def change_password(user_data: PasswordChange) -> PasswordChangeResponse:
    user = await User.filter(username=user_data.username).first()
    if not user or not await verify_password(user_data.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or old password")

    new_hashed_password = await async_hash_password(user_data.new_password)
    user.password_hash = new_hashed_password
    await user.save()
    return PasswordChangeResponse(message="Password changed successfully")


async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    logger.info(f"Token received: {token}")
    payload = decode_token(token)

    if payload is None:
        logger.error("User not authenticated: payload is None")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not authenticated")
    username = payload.get("username")
    user = await User.filter(username=username).first()
    if not user:
        logger.error(f"no user found with user name : {username}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not authenticated")
    return user
