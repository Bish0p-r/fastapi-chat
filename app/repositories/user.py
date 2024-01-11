from app.models.user import User


class UserRepository:
    collection: User = User

    async def get_by_id(self, user_id: str):
        pass

    async def get_by_email(self, user_email: str):
        pass

    async def create(self, data):
        pass

    async def update(self, user_id: str, data):
        pass

    async def delete(self, user_id: str):
        pass