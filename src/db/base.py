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
                a.raw_object,
                co.okved_code
            FROM company c
            JOIN address a on c.inn = a.company_inn
            JOIN contact c2 on c.inn = c2.company_inn
            JOIN companies_okved co on c.inn = co.company_inn
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
