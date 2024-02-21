import click
from faker import Faker

from src.core.database import sync_session_impl
from src.infra.db.repositories.users import UserRepository
from src.services.users import UserCreateService

fake = Faker()


@click.command()
@click.option('--username', prompt='Your username', required=True)
@click.option('--password', prompt='Your password', required=True)
@click.option('--first_name', required=False, default=fake.first_name)
@click.option('--last_name', required=False, default=fake.last_name)
def insert_user(username: str, password: str, first_name: str, last_name: str) -> None:
    session = sync_session_impl()
    repo = UserRepository(session=session)
    service = UserCreateService(repo=repo, session=session)
    service.execute(
        username=username,
        password=password,
        first_name=first_name,
        last_name=last_name,
    )
