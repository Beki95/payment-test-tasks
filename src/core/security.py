from typing import Final

from passlib.context import CryptContext

pwd_context: Final = CryptContext(
    schemes=['bcrypt'], deprecated='auto',
)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def hashing_secret(secret: str) -> str:
    return pwd_context.hash(secret=secret)
