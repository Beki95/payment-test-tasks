import uuid

import sqlalchemy
from sqlalchemy.orm import Session

from src.core.security import hashing_secret
from src.infra.db import (
    User,
    UserBalance,
)
from src.interfaces.repositories.alchemy.balance import IBalanceRepository
from src.interfaces.repositories.alchemy.users import IUsersRepository


class UserCreateService:

    def __init__(
        self, session: Session, repo: IUsersRepository, balance_repo: IBalanceRepository,
    ) -> None:
        self.session = session
        self.repo = repo
        self.balance_repo = balance_repo

    def execute(
        self, username: str, password: str, first_name: str, last_name: str,
    ) -> None:
        try:
            with self.session:
                password = hashing_secret(secret=password)
                user = User(
                    id=uuid.uuid4(),
                    username=username,
                    password=password,
                    first_name=first_name,
                    last_name=last_name,
                )
                self.repo.insert_user(instance=user)
                self.session.flush()

                balance = UserBalance(user_id=user.id)  # Default balance 100

                self.balance_repo.add_balance(instance=balance)
                self.session.commit()
        except sqlalchemy.exc.IntegrityError:
            self.session.rollback()
            print(f'User with username = {username} already exists')
        except Exception as err:
            self.session.rollback()
            print(err)
        else:
            print(f'Successful created id = {user.id}')
