from fastapi import APIRouter, Response, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.models.user import User
from app.schemas.auth import Token
from app.schemas.user import UserLoginSchema, UserCreateSchema
from app.dependencies.user import GetUserServices
from app.dependencies.auth import GetAuthServices
from app.dependencies.auth import GetCurrentUser


router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router.post("/registration")
async def registration(user_data: UserCreateSchema, user_services: GetUserServices) -> User:
    return await user_services.create_user(user_data=user_data.model_dump(mode='json'))


@router.post("/login")
async def login(user_data: UserLoginSchema, auth_services: GetAuthServices, response: Response, request: Request) -> Token:
    data = user_data.model_dump(mode='json')
    access_token, refresh_token = await auth_services.login(user_data=data)
    response.set_cookie(key="chat_refresh_token", value=refresh_token, httponly=True)
    request.state.device_id = 'asdasd'
    return Token(access_token=access_token, refresh_token=refresh_token)


@router.post("/logout")
async def logout(response: Response) -> None:
    response.delete_cookie(key="chat_access_token")


@router.post("/refresh")
async def refresh(auth_services: GetAuthServices, response: Response, request: Request) -> Token:
    access_token, refresh_token = await auth_services.refresh_tokens(token=request.cookies.get("chat_refresh_token"))
    response.set_cookie(key="chat_refresh_token", value=refresh_token, httponly=True)
    return Token(access_token=access_token, refresh_token=refresh_token)


@router.post("/test")
async def test(user: GetCurrentUser) -> User:
    return user

@router.get("/test")
async def test(request: Request):
    # request.state.device_id = 'asdasd'
    print(request.state.device_id)
    return request.headers
