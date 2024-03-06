from beanie import PydanticObjectId
from cashews import cache
from fastapi import APIRouter

from app.common.base.schemas import JsonResponseSchema
from app.config import settings
from app.dependencies.auth import GetCurrentUser, GetCurrentUserFromCookie
from app.dependencies.user import GetUserServices
from app.models.user import User
from app.schemas.user import UserUpdateSchema

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get("/")
@cache(ttl=settings.CACHE_TTL, key="list:users")
async def user_list(user_services: GetUserServices) -> list[User]:
    return await user_services.get_users()


@router.get("/me")
@cache(ttl=settings.CACHE_TTL, key="user_retrieve:{user.id}")
async def user_my_profile(user: GetCurrentUserFromCookie) -> User:
    return user


@router.get("/{user_id}")
@cache(ttl=settings.CACHE_TTL, key="user_retrieve:{user_id}")
async def user_retrieve(user_id: PydanticObjectId, user_services: GetUserServices) -> User:
    return await user_services.get_user_by_id(user_id=user_id)


@router.patch("/me")
@cache.invalidate("list:users")
@cache.invalidate("user_retrieve:{user.id}")
async def user_update(user: GetCurrentUser, user_data: UserUpdateSchema, user_services: GetUserServices) -> User:
    return await user_services.partial_update(user_id=user.id, user_data=user_data)


@router.delete("/me", response_model=JsonResponseSchema)
@cache.invalidate("list:users")
@cache.invalidate("user_retrieve:{user.id}")
async def user_delete(user: GetCurrentUser, user_services: GetUserServices):
    return await user_services.delete_profile(user_id=user.id)
