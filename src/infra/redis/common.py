from typing import (
    Any,
    TypeVar,
)

import pydantic
from redis.asyncio import Redis
from redis.typing import (
    EncodableT,
    KeyT,
)

T = TypeVar("T", bound=pydantic.BaseModel)


class BaseRedisClient:

    def __init__(self, session: Redis):
        self.session = session

    async def get(self, name: KeyT, dto: T = None) -> str | T | None:
        try:
            data = await self.session.get(name=name)
            if dto:
                return dto.parse_obj(data)
            return data
        except (ValueError, TypeError):
            return None

    async def set(
        self,
        name: KeyT,
        value: EncodableT,
        **kwargs: Any,
    ) -> None:
        await self.session.set(
            name=name, value=value, **kwargs,
        )

    async def delete(self, key):
        await self.session.delete(key)

    async def update(self, key, value):
        ...
