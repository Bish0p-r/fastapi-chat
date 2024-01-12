from app.models.auth import RefreshToken

class AuthRepository:
    collection: RefreshToken = RefreshToken

    @classmethod
    async def get_by_kwargs(cls, **kwargs) -> RefreshToken:
        return await cls.collection.get(**kwargs)

    @classmethod
    async def get_by_refresh_token(cls, refresh_token: str) -> RefreshToken:
        return await cls.collection.find_one(cls.collection.refresh_token == refresh_token)

    @classmethod
    async def create(cls, **data: dict) -> RefreshToken:
        instance = cls.collection(**data)
        await instance.create()
        return instance

    @classmethod
    async def delete(cls, **kwargs):
        await cls.collection.find(**kwargs).delete()

    @classmethod
    async def delete_by_id(cls, id):
        await cls.collection.find(cls.collection.id == id).delete()


