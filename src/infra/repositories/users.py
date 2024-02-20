from sqlalchemy import select

from src.infra.db import User
from src.infra.repositories.common import CommonRepository
from src.interfaces.repositories.users import (
    IUsersRepository,
)


class UserRepository(CommonRepository, IUsersRepository):

    def insert_user(self, instance: User) -> User:
        return self.insert(instance=instance)

    async def get_user_by_username(self, username: str):
        query = (
            select(User)
            .where(User.username == username)
        )
        result = await self.session.execute(query)
        return result.scalars().first()
