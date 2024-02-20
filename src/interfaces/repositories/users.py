from abc import (
    ABC,
    abstractmethod,
)

from src.infra.db import User


class IUsersRepository(ABC):

    @abstractmethod
    async def insert_user(self, instance: User):
        raise NotImplementedError
