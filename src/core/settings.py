from os import environ

from dotenv import load_dotenv
from pydantic.v1 import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    POSTGRES_URI = environ.get('POSTGRES_URI')
    SECRET_KEY = environ.get('SECRET_KEY')


settings = Settings()
