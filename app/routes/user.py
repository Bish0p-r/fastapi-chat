from fastapi import APIRouter
from app.config import settings
from app.models.user import UserCreateSchema, User, UserLoginSchema


router = APIRouter(
    prefix="/auth",
    tags=["user"],
)


@router.post("/login")
async def login(user_data: UserLoginSchema):
    return None


@router.post("/registration")
async def registration(user_data: UserCreateSchema) -> User:
    usr = User(**user_data.model_dump(mode='json'), hashed_password=user_data.password)
    await usr.create()
    return usr