import logging.config
import time

import uvicorn
from pydantic import BaseModel
from starlette.applications import Starlette
from starlette.exceptions import HTTPException
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import UJSONResponse, JSONResponse
from starlette.routing import Route
from starlette.types import ASGIApp, Scope, Receive, Send

from db.base import DB
from logs import LOGGING_CONFIG
from setting import settings

logging.basicConfig(level=logging.DEBUG)
logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger()


async def http_exception(request, exc):
    return JSONResponse({"detail": exc.detail}, status_code=exc.status_code)


exception_handlers = {HTTPException: http_exception}


async def list(request):
    limit = int(request.query_params.get("limit", 100))
    offset = int(request.query_params.get("offset", 0))
    group = request.query_params.get("group", "okved_code")
    data = await DB(request.scope["pool"]).list(limit, offset, group)
    return UJSONResponse({"results": [dict(**i) for i in data]})


async def search(request):
    query = request.query_params.get("q")
    if not query:
        return await list(request)

    objects = [{"pk": "7d41ab1e-ffdf-473e-8a77-05e98e5251ad"}, {"pk": "7d41ab1e-ffdf-473e-8a77-05e98e5251ad"}]
    return UJSONResponse({
                "query": query,
                "count": 0,
                "limit": 100,
                "offset": 0,
                "order_by": "",
                "filters": [],
                "results": objects
            }
        )


async def detail(request):
    data = await DB(request.scope["pool"]).get(request.path_params['pk'])
    return UJSONResponse(dict(**data))


async def categories(request):
    query = request.query_params.get("q")
    data = await DB(request.scope["pool"]).get_categories(query)
    return UJSONResponse(dict(catefories=[dict(**i) for i in data]))


async def regions(request):
    query = request.query_params.get("q")
    data = await DB(request.scope["pool"]).get_regions(query)
    return UJSONResponse(dict(regions=[dict(**i) for i in data]))


class DBMiddleware:
    DB_POOL = None

    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if not self.DB_POOL:
            self.DB_POOL = await DB.create_pool()
        async with self.DB_POOL.acquire() as connection:
            async with connection.transaction():
                scope["pool"] = connection
                await self.app(scope, receive, send)


class TimeMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        _start = time.time()
        await self.app(scope, receive, send)
        logger.warning(f"= Время запроса: {_start - time.time()}")


middleware = [
    Middleware(DBMiddleware),
    Middleware(CORSMiddleware, allow_origins=['*'])
]


async def db_close():
    await DBMiddleware.DB_POOL.close()


app = Starlette(
    debug=True,
    middleware=middleware,
    on_shutdown=[db_close],
    exception_handlers=exception_handlers,
    routes=[
        Route('/', search),
        Route('/{pk:int}', detail),
        Route("/categories", categories),
        Route("/regions", regions)
    ]
)


if __name__ == "__main__":
    uvicorn.run(
        "src.app:app",
        host="0.0.0.0",
        port=8000,
        log_config=LOGGING_CONFIG,
        log_level=settings.LOGGING_LEVEL,
        reload=True
    )
