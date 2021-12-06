import os
from pydantic import BaseSettings
from dotenv import load_dotenv

load_dotenv(verbose=True)


class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URL: str = os.getenv('DATABASE_URL', '')

    class Config:
        env_file = '.env'


settings = Settings()
