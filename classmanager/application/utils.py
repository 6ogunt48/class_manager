import asyncio
from fastapi.concurrency import run_in_threadpool
from passlib.context import CryptContext
from typing import Awaitable

# Initialize CryptContext
crypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    Hash a plaintext password.
    """
    return crypt_context.hash(password)


async def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plaintext password against a hashed one.
    """
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, crypt_context.verify, plain_password, hashed_password)


async def async_hash_password(password: str) -> Awaitable[str]:
    """
    Hash a plaintext password asynchronously.
    """
    return await run_in_threadpool(hash_password, password)
