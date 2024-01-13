from fastapi import APIRouter, Response, Request, status
from fastapi.responses import JSONResponse

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
async def login(
        user_data: UserLoginSchema, auth_services: GetAuthServices, response: Response, request: Request
) -> Token:
    data = user_data.model_dump(mode='json')
    user_agent = request.headers.get("user-agent")
    access_token, refresh_token = await auth_services.login(user_data=data, user_agent=user_agent)
    response.set_cookie(key="chat_refresh_token", value=refresh_token, httponly=True)
    return Token(access_token=access_token, refresh_token=refresh_token)


@router.post("/logout")
async def logout(auth_services: GetAuthServices, response: Response, request: Request):
    token = request.cookies.get("chat_refresh_token")
    user_agent = request.headers.get("user-agent")
    await auth_services.logout(token=token, user_agent=user_agent)
    response.delete_cookie(key="chat_refresh_token")
    return {"message": "Successful logout"}


@router.post("/refresh")
async def refresh(auth_services: GetAuthServices, response: Response, request: Request) -> Token:
    token = request.cookies.get("chat_refresh_token")
    user_agent = request.headers.get("user-agent")
    access_token, refresh_token = await auth_services.refresh_tokens(token=token, user_agent=user_agent)
    response.set_cookie(key="chat_refresh_token", value=refresh_token, httponly=True)
    return Token(access_token=access_token, refresh_token=refresh_token)

@router.post("/logout-from-all-devices")
async def logout_from_all_devices(auth_services: GetAuthServices, user: GetCurrentUser, response: Response):
    await auth_services.logout_from_all_devices(user=user)
    response.delete_cookie(key="chat_refresh_token")
    return {"message": "Successful logout"}

@router.post("/test")
async def test(user: GetCurrentUser) -> User:
    return user

@router.get("/test")
async def test(request: Request):
    return request.headers
