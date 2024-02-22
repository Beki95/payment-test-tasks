from typing import TypeVar

from fastapi import (
    Depends,
    FastAPI,
)

from src.core.database import (
    async_session_impl,
    redis_session_impl,
)
from src.infra.db.repositories.balance import BalanceRepository
from src.infra.db.repositories.transactions import TransactionsRepository
from src.infra.db.repositories.users import UserRepository
from src.infra.redis._ip import BlockedIPRepository
from src.interfaces.db import (
    get_session,
    redis_stub,
)
from src.interfaces.repositories.alchemy.balance import IBalanceRepository
from src.interfaces.repositories.alchemy.transactions import ITransactionsRepository
from src.interfaces.repositories.alchemy.users import IUsersRepository
from src.interfaces.repositories.redis._ip import IBlockedIPRepository

T = TypeVar('T')


def override_repo(repo: T):
    def wrap(session: get_session = Depends()): return repo(session)

    return wrap


def override_cache_repo(repo: T):
    def wrap(session: redis_stub = Depends()): return repo(session)

    return wrap


def register_dependencies(app: FastAPI):
    app.dependency_overrides.setdefault(
        *async_session_impl
    )
    app.dependency_overrides.setdefault(
        *redis_session_impl
    )
    app.dependency_overrides.setdefault(
        *(IUsersRepository, override_repo(UserRepository))
    )
    app.dependency_overrides.setdefault(
        *(ITransactionsRepository, override_repo(TransactionsRepository))
    )
    app.dependency_overrides.setdefault(
        *(IBalanceRepository, override_repo(BalanceRepository))
    )
    app.dependency_overrides.setdefault(
        *(IBlockedIPRepository, override_cache_repo(BlockedIPRepository))
    )
