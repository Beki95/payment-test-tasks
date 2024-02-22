from datetime import (
    datetime,
    timedelta,
)
from typing import Final
from uuid import UUID

from jose import (
    ExpiredSignatureError,
    JWTError,
    jwt,
)
from jose.exceptions import JWTClaimsError
from passlib.context import CryptContext

from src.core.settings import settings

pwd_context: Final = CryptContext(
    schemes=['bcrypt'], deprecated='auto',
)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def hashing_secret(secret: str) -> str:
    return pwd_context.hash(secret=secret)


async def create_jwt_token(user_id: UUID, scopes: list | None):
    claims = dict(
        sub=user_id.__str__(),
        scopes=scopes,
        exp=datetime.utcnow() + timedelta(minutes=settings.EXPIRE_MINUTES)
    )
    return jwt.encode(
        claims=claims, key=settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )


async def decode_jwt_token(jwt_token: str) -> dict:
    try:
        payload = jwt.decode(
            jwt_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        user_id = payload.get("sub")
        if user_id is None:
            raise ValueError('Invalid token')

    except (JWTError, JWTClaimsError, ExpiredSignatureError) as e:
        raise ValueError(e)

    return user_id
