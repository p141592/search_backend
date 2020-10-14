import logging

import httpx
from httpx import Headers

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()


class SearchEngine:
    async def search(self, user_key, request):
        # Set auth cache
        access_key = await self.redis.get(user_key)
        if not access_key:
            access_key = await self.auth(user_key)
            logger.info(
                f"user_key: {user_key} "
                f"access_key: {access_key}"
            )
        ###

        headers = (tuple(["session_id", access_key]), *request.headers.items())
        logger.info(f"HEADERS: {headers}")
        logger.info(f"QUERY PARAMS: {request.query_params}")
        data = await request.body()
        logger.info(f"DATA: {data}")

        async with httpx.AsyncClient() as client:
            url = self.TARGET_SERVER + request.url.path
            r = await client.request(
                request.method,
                url,
                headers=Headers(headers),
                data=data,
                params=dict(**request.query_params),
            )

        return r.json()
