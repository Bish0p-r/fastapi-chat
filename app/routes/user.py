from beanie import PydanticObjectId
from fastapi import APIRouter

from app.models.user import User
from app.schemas.user import UserUpdateSchema
from app.dependencies.user import GetUserServices
from app.dependencies.auth import GetCurrentUser


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get("/")
async def get_users(user_services: GetUserServices) -> list[User]:
    return await user_services.get_users()


@router.get("/me")
async def get_my_profile(user: GetCurrentUser):
    return user


@router.patch("/me")
async def update_my_profile(user: GetCurrentUser, user_data: UserUpdateSchema, user_services: GetUserServices) -> User:
    return await user_services.partial_update(user_id=user.id, user_data=user_data)


@router.delete("/me")
async def delete_my_profile(user: GetCurrentUser, user_services: GetUserServices):
    await user_services.delete_profile(user_id=user.id)
    return {"message": "Profile successfully deleted"}


@router.get("/{user_id}")
async def get_user(user_id: PydanticObjectId, user_services: GetUserServices) -> User:
    return await user_services.get_user_by_id(user_id=user_id)

