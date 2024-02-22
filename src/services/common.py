from datetime import (
    datetime,
    timedelta,
)

from fastapi import (
    Depends,
    Security,
)
from fastapi.security import APIKeyCookie
from starlette.requests import Request

from src.core import security
from src.infra.db import User
from src.infra.redis.models.blocked_id import BlockedIdModel
from src.interfaces.repositories.alchemy.users import IUsersRepository
from src.interfaces.repositories.redis._ip import IBlockedIPRepository
from src.services.exceptions import (
    AccessDeniedError,
    TokenExpiredOrNotValid,
    UserNotFoundError,
)

oauth2_scheme = APIKeyCookie(name='access_token')


async def get_current_user(
    token: str = Security(oauth2_scheme), user_repo: IUsersRepository = Depends()
) -> User:
    try:
        user_id = await security.decode_jwt_token(token)
        if user := await user_repo.get_user_by_id(user_id=user_id):
            return user
        raise UserNotFoundError
    except ValueError:
        raise TokenExpiredOrNotValid


class LockoutManager:

    def __init__(
        self, request: Request, blocked_cache_repo: IBlockedIPRepository, attempt: int = None
    ):
        self.attempt = attempt or 5  # By default, the number of unsuccessful attempts is 5
        self.blocked_cache_repo = blocked_cache_repo
        self.ip = self.get_ip(request=request)

    def get_ip(self, request: Request): return request.client.host  # noqa

    def get_time_in_unix_format(self, delta: timedelta = None) -> int:  # noqa
        now_in_unix = int(datetime.utcnow().timestamp())
        if delta:
            return now_in_unix + delta.total_seconds()
        return now_in_unix

    async def check_access(self):
        if not (
                data := await self.blocked_cache_repo.get_ip(self.ip)
        ):
            return

        if data.exp and data.exp > self.get_time_in_unix_format():
            raise AccessDeniedError

    async def failed_attempts(self):
        exp = None

        if ip_data := await self.blocked_cache_repo.get_ip(self.ip):
            ip_data: BlockedIdModel

            # Blocking for a certain period of time
            if ip_data.attempt < self.attempt: delta = None
            elif ip_data.attempt == self.attempt: delta = timedelta(seconds=15)
            elif ip_data.attempt == self.attempt + 1: delta = timedelta(minutes=1)
            else: delta = timedelta(minutes=5)

            if delta:
                exp = self.get_time_in_unix_format(delta=delta)
            attempt = ip_data.attempt
            attempt += 1
        else:
            attempt = 1
        blocked_data = BlockedIdModel(attempt=attempt, exp=exp)
        await self.blocked_cache_repo.set_ip(ip=self.ip, value=blocked_data)

        if attempt > self.attempt:
            raise AccessDeniedError

    async def open_access(self):
        await self.blocked_cache_repo.del_ip(ip=self.ip)
