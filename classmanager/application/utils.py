from passlib.context import CryptContext

# chose hashing algorithm
crypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return crypt_context.hash(password)
