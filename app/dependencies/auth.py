from fastapi import Depends, Request, status, HTTPException, WebSocket
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from typing import Annotated

from app.dependencies.token import get_jwt_token_services, GetTokenServices
from app.models.user import User
from app.repositories.user import UserRepository
from app.services.auth import AuthServices
from app.common.exceptions import InvalidTokenException


async def get_auth_services():
    return AuthServices(
        user_repository=UserRepository,
        token_services= await get_jwt_token_services()
    )

GetAuthServices = Annotated[AuthServices, Depends(get_auth_services)]

http_bearer = Annotated[HTTPAuthorizationCredentials, Depends(HTTPBearer())]


async def get_current_user_from_token(token_services: GetTokenServices, token: http_bearer, request: Request) -> User:
    access_token = token.credentials
    user = await token_services.get_user_from_token(token=access_token)
    payload = await token_services.decode_token(token=access_token)
    user_agent = request.headers.get("user-agent")

    if user is None or payload.get("user_agent") is None or user_agent != payload.get("user_agent"):
        raise InvalidTokenException
    return user

GetCurrentUser = Annotated[User, Depends(get_current_user_from_token)]


async def get_current_user_from_token_ws(token_services: GetTokenServices, websocket: WebSocket) -> User:
    access_token = websocket.cookies.get("chat_access_token")
    if access_token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    user = await token_services.get_user_from_token(token=access_token)
    payload = await token_services.decode_token(token=access_token)
    user_agent = websocket.headers.get("user-agent")

    if user is None or payload.get("user_agent") is None or user_agent != payload.get("user_agent"):
        raise InvalidTokenException
    return user

GetCurrentUserWS = Annotated[User, Depends(get_current_user_from_token_ws)]


async def get_current_user_from_cookie(token_services: GetTokenServices, request: Request) -> User:
    access_token = request.cookies.get("chat_access_token")
    if access_token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    user = await token_services.get_user_from_token(token=access_token)
    payload = await token_services.decode_token(token=access_token)
    user_agent = request.headers.get("user-agent")

    if user is None or payload.get("user_agent") is None or user_agent != payload.get("user_agent"):
        raise InvalidTokenException
    return user

GetCurrentUserFromCookie = Annotated[User, Depends(get_current_user_from_cookie)]