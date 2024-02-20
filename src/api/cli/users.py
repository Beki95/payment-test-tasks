import click
from faker import Faker

fake = Faker()


@click.command()
@click.option('--username', prompt='Your username', required=True)
@click.option('--password', prompt='Your password', required=True)
@click.option('--firstname', required=False, default=fake.first_name)
@click.option('--lastname', required=False, default=fake.last_name)
def insert_user(username: str, password: str, firstname: str, lastname: str) -> None:
    ...
