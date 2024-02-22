from abc import (
    ABC,
    abstractmethod,
)

from sqlalchemy import Transaction


class ITransactionsRepository(ABC):

    @abstractmethod
    async def add_transaction(self, instance: Transaction):
        raise NotImplementedError
