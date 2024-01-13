from beanie import PydanticObjectId

from app.models.user import User


class UserRepository:
    collection: User = User

    @classmethod
    async def get_list(cls) -> list[collection]:
        return await cls.collection.find_all().to_list()

    @classmethod
    async def get_by_kwargs(cls, **kwargs) -> collection:
        return await cls.collection.find_one(kwargs)

    @classmethod
    async def create(cls, **data) -> collection:
        instance = cls.collection(**data)
        await instance.create()
        return instance

    @classmethod
    async def update(cls, user_id: str, user_data: dict) -> collection:
        instance = await cls.collection.find_one(cls.collection.id == user_id)
        await instance.set(user_data)
        return instance

    @classmethod
    async def delete(cls, user_id: str) -> None:
        pass
