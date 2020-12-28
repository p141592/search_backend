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

    async def list(self, limit=100, offset=0, order_by="okved_code"):
        return await self.connect.fetch(
            """SELECT * FROM full_company LIMIT $1 OFFSET $2""", limit, offset
        )

    async def get(self, pk):
        return await self.connect.fetchrow(
            """
            SELECT 
                *
            FROM full_company
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

    async def get_categories(self, query):
        if query:
            return await self.connect.fetch(
                """
                SELECT name, code
                FROM okved
                ORDER BY name <-> $1 LIMIT 10;
                """, query
            )
        return await self.connect.fetch(
            "SELECT * FROM okved ORDER BY code"
        )

    async def get_regions(self, query):
        if query:
            return await self.connect.fetch(
                """
                SELECT city FROM cities ORDER BY city <-> $1 LIMIT 10
                """, query
            )
        return await self.connect.fetch("SELECT distinct(city) FROM address Group By city")
