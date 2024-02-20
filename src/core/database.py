from typing import (
    AsyncGenerator,
    Callable,
)

from sqlalchemy import (
    create_engine,
    orm,
)
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
)

from src.core.settings import settings
from src.interfaces.db import get_session


def async_session(url: str) -> Callable[[AsyncGenerator], None]:
    engine = create_async_engine(
        url, pool_pre_ping=True, future=True,
    )
    factory = orm.sessionmaker(
        engine, class_=AsyncSession, autoflush=False, expire_on_commit=False,
    )

    async def wrapp() -> AsyncGenerator[AsyncSession, None]:  # noqa
        async with factory() as session:
            yield session

    return wrapp


def sync_session(url: str) -> orm.scoped_session:
    engine = create_engine(
        url, pool_pre_ping=True, future=True,
    )
    factory = orm.sessionmaker(
        engine, autoflush=False, expire_on_commit=False,
    )
    return orm.scoped_session(factory)


sync_session_impl = sync_session(settings.POSTGRES_URI.replace('+asyncpg', ''))
async_session_impl = get_session, async_session(settings.POSTGRES_URI)
