import logging

import aioredis
import asyncpg

from setting import settings

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()


REDIS = None
SECURITY_STORE = None
MOGODB_USER_STORE = None


class ResourceMixin:
    @staticmethod
    async def redis():
        global REDIS
        if not REDIS:
            logger.info("CONNECT TO REDIS")
            REDIS = await aioredis.create_redis_pool(
                f"redis://{settings.REDIS_HOST}:{settings.REDIS_POST}",
                db=settings.REDIS_DB,
            )
        return REDIS

    @staticmethod
    async def db():
        global SECURITY_STORE
        if not SECURITY_STORE:
            logger.info("CONNECT TO DB")
            SECURITY_STORE = await asyncpg.connect(
                user=settings.DB_USER,
                password=settings.DB_PASSWORD,
                database=settings.DB_NAME,
                host=settings.DB_HOST,
                port=settings.DB_PORT,
            )
        return SECURITY_STORE

    @staticmethod
    async def mongodb():
        global MOGODB_USER_STORE
        if not MOGODB_USER_STORE:
            logger.info("CONNECT TO USER STORE")
            MOGODB_USER_STORE = await asyncpg.connect(
                user=settings.DB_USER,
                password=settings.DB_PASSWORD,
                database=settings.DB_NAME,
                host=settings.DB_HOST,
                port=settings.DB_PORT,
            )
        return MOGODB_USER_STORE
