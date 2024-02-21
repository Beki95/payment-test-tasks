from abc import (
    ABC,
    abstractmethod,
)
from datetime import timedelta

from src.infra.redis.models.blocked_id import BlockedIdModel


class IBlockedIPRepository(ABC):

    @abstractmethod
    async def get_ip(self, ip: str) -> BlockedIdModel | None:
        raise NotImplementedError

    @abstractmethod
    async def set_ip(
        self, ip: str, value: BlockedIdModel, ex: int | timedelta = None,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def del_ip(self, ip: str) -> None:
        raise NotImplementedError
