import sqlalchemy
from sqlalchemy.orm import Session

from src.core.security import hashing_secret
from src.infra.db import User
from src.interfaces.repositories.users import IUsersRepository


class UserCreateService:

    def __init__(self, session: Session, repo: IUsersRepository) -> None:
        self.session = session
        self.repo = repo

    def execute(
        self, username: str, password: str, first_name: str, last_name: str,
    ) -> None:
        try:
            password = hashing_secret(secret=password)
            instance = User(
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
            )
            self.repo.insert_user(instance=instance)
            self.session.commit()
        except sqlalchemy.exc.IntegrityError:
            print(f'User with username = {username} already exists')
        except Exception as err:
            print(err)
        else:
            print(f'Successful created id = {instance.id}')
