from passlib.context import CryptContext
from fastapi.concurrency import run_in_threadpool
import asyncio

# chose hashing algorithm
crypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return crypt_context.hash(password)


async def verify_password(plain_password: str, hashed_password: str) -> bool:
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, crypt_context.verify, plain_password, hashed_password)


# we run hashing in separate threads to improve performance
async def async_hash_password(password: str) -> str:
    return await run_in_threadpool(hash_password, password)

