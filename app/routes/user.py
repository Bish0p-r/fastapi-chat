from beanie import PydanticObjectId
from fastapi import APIRouter

from app.models.user import UserCreateSchema, User, UserLoginSchema
from app.dependencies.user import GetUserServices
from app.services.user import UserServices


router = APIRouter(
    prefix="/auth",
    tags=["user"],
)


@router.post("/login")
async def login(user_data: UserLoginSchema):
    return None


@router.post("/registration")
async def registration(user_data: UserCreateSchema, user_services: UserServices = GetUserServices) -> User:
    return await user_services.create_user(user_data=user_data.model_dump(mode='json'))


@router.get("/list")
async def get_users(user_services: UserServices = GetUserServices) -> list[User]:
    return await user_services.get_users()

@router.get("/{user_id}")
async def get_user(user_id: PydanticObjectId, user_services: UserServices = GetUserServices) -> User:
    return await user_services.get_user_by_id(user_id=user_id)
