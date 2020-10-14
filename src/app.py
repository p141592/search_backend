import logging

from starlette.requests import Request
from starlette.responses import UJSONResponse

from auth import AuthMixin
from resources import ResourceMixin
from search import SearchEngine

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()


class ASGIApplication(AuthMixin, ResourceMixin, SearchEngine):
    TARGET_SERVER = "/"

    def __init__(self, scope):
        assert scope["type"] == "http"
        self.scope = scope
        self.receive = None
        self.send = None

    async def __call__(self, receive, send):
        self.receive = receive
        self.send = send
        self.redis = await self.redis()
        self.db = await self.db()

        request = Request(self.scope, self.receive)

        if request.url.path == "/ping":
            return await self.response({"message": "pong"})

        user_key = request.headers.get("api_key")
        if not user_key:
            return await self.response(
                {"error": "api_key", "message": "User key should not be 'None'"}
            )

        data = await self.search(request)
        logger.info(f"RESPONSE BODY: {data}")
        return await self.response(data)

    async def response(self, data):
        response = UJSONResponse(data)
        return await response(self.scope, self.receive, self.send)
