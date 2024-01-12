from fastapi import APIRouter

from app.models.user import User
from app.schemas.auth import Token
from app.schemas.user import UserLoginSchema, UserCreateSchema
from app.dependencies.user import GetUserServices, GetAuthServices


router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router.post("/login")
async def login(user_data: UserLoginSchema, auth_services: GetAuthServices) -> Token:
    return None


@router.post("/registration")
async def registration(user_data: UserCreateSchema, user_services: GetUserServices) -> User:
    return await user_services.create_user(user_data=user_data.model_dump(mode='json'))


@router.post("/refresh")
async def refresh_token(auth_services: GetAuthServices):
    return None
