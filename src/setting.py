from pydantic import BaseSettings


class Settings(BaseSettings):
    REDIS_HOST: str
    REDIS_POST: int = 6379
    REDIS_DB: int = 0
    CACHE_DATA_ALIVE: int = 5 * 60  # seconds
    CACHE_AUTH_ALIVE: int = 30 * 60  # seconds
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    DB_HOST: str = "0.0.0.0"
    DB_PORT: int = 5432


settings = Settings()
