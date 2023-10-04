import asyncio
from typing import Awaitable

from fastapi.concurrency import run_in_threadpool
from passlib.context import CryptContext

# Initialize CryptContext
crypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    Hashing the plaintext password. Synchronous
    """
    return crypt_context.hash(password)


""" Hashing is an expensive process , in this case we run it in threadpool to free up the event loop"""


# this is done by wrapping the synchronous function into an async function and passing it to run_in_thread_pool function
async def async_hash_password(password: str) -> Awaitable[str]:
    """
    Hashing the plaintext password asynchronously.
    """
    return await run_in_threadpool(hash_password, password)


async def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify the plaintext password against a hashed one.
    """
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, crypt_context.verify, plain_password, hashed_password)
