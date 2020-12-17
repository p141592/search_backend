import logging

from pydantic import BaseSettings


class Settings(BaseSettings):
    """Настройки приложения"""
    LOGGING_LEVEL = logging.DEBUG


settings = Settings()
