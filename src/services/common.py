from fastapi import (
    Security,
)
from fastapi.security import APIKeyCookie

from src.core import security
from src.services.exceptions import TokenExpiredOrNotValid

oauth2_scheme = APIKeyCookie(name='access_token')


async def get_current_user(token: str = Security(oauth2_scheme)):  # -> user_id
    try:
        payload = await security.decode_jwt_token(token)
    except ValueError:
        raise TokenExpiredOrNotValid()
    return payload
