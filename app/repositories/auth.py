from datetime import datetime

from app.models.auth import RefreshToken
from app.common.base.repository import BaseRepository

class AuthRepository(BaseRepository):
    collection: RefreshToken = RefreshToken

    @classmethod
    async def get_by_refresh_token(cls, refresh_token: str) -> collection:
        return await cls.collection.find_one(cls.collection.refresh_token == refresh_token)

    @classmethod
    async def delete(cls, **kwargs) -> None:
        await cls.collection.find(**kwargs).delete()

    @classmethod
    async def delete_by_agent_and_id(cls, user_id, user_agent) -> None:
        await cls.collection.find_all(cls.collection.id == user_id).find_many(cls.collection.user_agent == user_agent).delete()

    @classmethod
    async def delete_expired_tokens(cls) -> None:
        await cls.collection.find_many(cls.collection.expires_at < datetime.now()).delete()
