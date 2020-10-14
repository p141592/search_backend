import logging
import httpx
from bson.objectid import ObjectId

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()


class AuthMixin:
    def check_user(self, email):
        return bool(self.CLIENT.users.find_one({'email': email}))

    def get_user_id(self, session_key):
        result = self.REDIS_CLIENT.get(f'crmt:session:{session_key}')
        if result:
            return result.decode("utf-8")

    def get_user(self, user_id):
        return self.CLIENT.users.find_one({'_id': ObjectId(user_id)})

    async def auth(self, api_key):
        """Проверка авторизации пользователя"""
        async with httpx.AsyncClient() as client:
            login_data = await self.get_user_data(api_key)
            logger.info(f"Данные логина {login_data}")
            r = await client.request(
                "POST",
                url,
                headers={
                    "api_key": api_key,
                    "content-type": "application/x-www-form-urlencoded",
                },
                data=login_data,
            )
            data = r.json().get("data")
            logger.info(f"AUTH RESPONSE: {data}")
            return data.get("session_id")

    async def get_user_data(self, api_key):
        data = await self.db.fetchrow("SELECT * FROM USERS WHERE api_key = $1", api_key)
        if not data:
            return await self.response(
                {"error": "api_key", "message": f"User {api_key} not found"}
            )

        return {
            "login": data.get("username"),
            "password": data.get("password"),
        }
