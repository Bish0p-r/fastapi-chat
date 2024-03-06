from cashews import cache
from fastapi import APIRouter, Request, Response, status

from app.common.base.schemas import JsonResponseSchema
from app.dependencies.auth import GetAuthServices, GetCurrentUserFromCookie
from app.models.user import User
from app.schemas.auth import Token
from app.schemas.user import UserCreateSchema, UserLoginSchema

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router.post("/registration", status_code=status.HTTP_201_CREATED, response_model=User)
@cache.invalidate("list:users")
async def registration(user_data: UserCreateSchema, auth_services: GetAuthServices):
    return await auth_services.create_user(user_data=user_data.model_dump(mode="json"))


@router.post("/login", response_model=Token)
async def login(
    user_data: UserLoginSchema,
    auth_services: GetAuthServices,
    response: Response,
    request: Request,
):
    data = user_data.model_dump(mode="json")
    user_agent = request.headers.get("user-agent")
    access_token, refresh_token = await auth_services.login(response=response, user_data=data, user_agent=user_agent)
    return {"access_token": access_token, "refresh_token": refresh_token}


@router.post("/logout", response_model=JsonResponseSchema)
async def logout(response: Response, request: Request, auth_services: GetAuthServices):
    token = request.cookies.get("chat_refresh_token")
    user_agent = request.headers.get("user-agent")
    await auth_services.logout(response=response, token=token, user_agent=user_agent)
    return {"detail": "successful logout"}


@router.post("/refresh", response_model=Token)
async def refresh(auth_services: GetAuthServices, response: Response, request: Request):
    token = request.cookies.get("chat_refresh_token")
    user_agent = request.headers.get("user-agent")
    access_token, refresh_token = await auth_services.refresh_tokens(
        response=response, token=token, user_agent=user_agent
    )
    return {"access_token": access_token, "refresh_token": refresh_token}


@router.post("/logout-from-all-devices", response_model=JsonResponseSchema)
async def logout_from_all_devices(auth_services: GetAuthServices, user: GetCurrentUserFromCookie, response: Response):
    await auth_services.logout_from_all_devices(response=response, user=user)
    return {"detail": "successful logout from all devices"}
