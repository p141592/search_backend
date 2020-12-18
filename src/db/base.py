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
        return await self.connect.fetchrow(
            """
            SELECT 
                c.inn, 
                c.ogrn, 
                c.name as company_name, 
                c2.name as contact_name, 
                c2.position, 
                a.city, 
                a.index, 
                a.raw_object 
            FROM company c
            JOIN address a on c.inn = a.company_inn
            JOIN contact c2 on c.inn = c2.company_inn
            WHERE inn = $1
            """,
            str(pk)
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
