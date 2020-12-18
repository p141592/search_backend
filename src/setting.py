import logging

from pydantic import BaseSettings


class Settings(BaseSettings):
    """Настройки приложения"""
    LOGGING_LEVEL = logging.DEBUG
    DB_DSN: str = "postgres://postgres:postgres@0.0.0.0:5432/postgres"
    DB_POOL_MIN: int = 1
    DB_POOL_MAX: int = 5


settings = Settings()
