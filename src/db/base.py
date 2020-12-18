import asyncpg

from setting import settings


class DB:
    @staticmethod
    async def create_pool(dsn=settings.DB_DSN, min_size=settings.DB_POOL_MIN, max_size=settings.DB_POOL_MAX):
        return await asyncpg.create_pool(dsn, min_size=min_size, max_size=max_size, statement_cache_size=0)

    @staticmethod
    async def statistics(db):
        return await db.fetch("select * from pg_stat_activity where datname=$1", db._con._params.database)

    def __init__(self, connect):
        self.connect = connect

    async def get(self, pk):
        return await self.connect.fetchraw(
            """
            # Здесь должен быть запрос для получения одного объекта
            """
        )

    async def search(self, query):
        return await self.connect.fetch(
            """
            # 
            """
        )

    async def create_index(self):
        await self.connect.fetch("CREATE EXTENSION IF not exists rum")
        return await self.connect.fetch("CREATE INDEX rumidx ON company USING rum (a rum_tsvector_ops)"
        )
