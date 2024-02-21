from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession


def get_session() -> AsyncSession:
    raise NotImplementedError


def redis_stub() -> Redis:
    raise NotImplementedError
