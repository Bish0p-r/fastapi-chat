from beanie import PydanticObjectId
from fastapi import HTTPException, status

from app.models.user import User
from app.repositories.user import UserRepository
from app.common.utils import get_hash_password, verify_password


class UserServices:
    def __init__(self, repository: type[UserRepository]):
        self.repository = repository

    async def get_users(self) -> list[User]:
        return await self.repository.get_list()

    async def get_user_by_id(self, user_id: PydanticObjectId) -> User:
        user = await self.repository.get_by_kwargs(_id=user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user

    async def get_user_by_email(self, user_email: str) -> User:
        return await self.repository.get_by_kwargs(email=user_email)

    async def create_user(self, user_data: dict) -> User:
        user = await self.get_user_by_email(user_data.get('email'))
        if user:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User with this email already exists")
        hashed_password = get_hash_password(user_data.get('password'))
        return await self.repository.create(**user_data, hashed_password=hashed_password)

    async def partial_update(self, user_id: str, user_data: dict) -> User:
        return await self.repository.update(user_id=user_id, user_data=user_data)

    async def delete_profile(self, user_id: str) -> None:
        await self.repository.delete_by_id(_id=user_id)
