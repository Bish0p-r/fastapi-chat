from app.common.base.repository import BaseRepository
from app.models.user import User


class UserRepository(BaseRepository):
    collection: User = User

    @classmethod
    async def update(cls, user_id: str, user_data: dict) -> collection:
        instance = await cls.collection.find_one(cls.collection.id == user_id)
        await instance.set(user_data)
        return instance
