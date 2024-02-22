from abc import (
    ABC,
    abstractmethod,
)
from uuid import UUID

from src.infra.db import UserBalance


class IBalanceRepository(ABC):

    @abstractmethod
    def add_balance(self, instance: UserBalance) -> None:
        raise NotImplementedError

    @abstractmethod
    async def withdraw_funds(self, user_id: UUID, amount: float) -> None:
        raise NotImplementedError
