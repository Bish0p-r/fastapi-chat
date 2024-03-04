from beanie import PydanticObjectId
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse

from app.models.user import User
from app.repositories.user import UserRepository


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

    async def partial_update(self, user_id: str, user_data: dict) -> User:
        return await self.repository.update(user_id=user_id, user_data=user_data)

    async def delete_profile(self, user_id: str) -> JSONResponse:
        await self.repository.delete_by_id(_id=user_id)
        return JSONResponse(status_code=200, content={"detail": "profile successfully deleted"})
