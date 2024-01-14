from beanie import PydanticObjectId

class BaseRepository:
    collection = None

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
    async def delete_by_id(cls, _id: PydanticObjectId | str) -> None:
         await cls.collection.find(cls.collection.id == _id).delete()