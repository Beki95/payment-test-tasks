from datetime import timedelta

from pydantic import ValidationError

from src.infra.redis.common import BaseRedisClient
from src.infra.redis.models.blocked_id import BlockedIdModel
from src.interfaces.repositories.redis._ip import IBlockedIPRepository


class BlockedIPRepository(BaseRedisClient, IBlockedIPRepository):

    async def get_ip(self, ip: str) -> BlockedIdModel | None:
        try:
            data = await self.get(name=ip)
            return BlockedIdModel.parse_raw(data)
        except ValidationError:
            return

    async def set_ip(
        self, ip: str, value: BlockedIdModel, ex: int | timedelta = None,
    ) -> None:
        await self.set(name=ip, value=value.json(), ex=ex)

    async def del_ip(self, ip: str) -> None:
        await self.delete(key=ip)
