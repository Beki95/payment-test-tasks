from src.infra.db import User
from src.infra.repositories.common import CommonRepository
from src.interfaces.repositories.users import (
    IUsersRepository,
)


class UserRepository(CommonRepository, IUsersRepository):

    def insert_user(self, instance: User) -> User:
        return self.insert(instance=instance)
