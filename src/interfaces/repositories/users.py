from abc import (
    ABC,
    abstractmethod,
)

from src.infra.db import User


class IUsersRepository(ABC):

    @abstractmethod
    async def insert_user(self, instance: User):
        raise NotImplementedError

    @abstractmethod
    async def get_user_by_username(self, username: str):
        raise NotImplementedError
