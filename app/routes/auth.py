from fastapi import APIRouter

from app.models.user import UserCreateSchema, User, UserLoginSchema
from app.dependencies.user import GetUserServices, GetAuthServices
from app.services.auth import AuthServices
from app.services.user import UserServices


router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router.post("/login")
async def login(user_data: UserLoginSchema, auth_services: AuthServices = GetAuthServices):
    return None


@router.post("/registration")
async def registration(user_data: UserCreateSchema, user_services: UserServices = GetUserServices) -> User:
    return await user_services.create_user(user_data=user_data.model_dump(mode='json'))


@router.post("/refresh")
async def refresh_token(auth_services: AuthServices = GetAuthServices):
    return None
