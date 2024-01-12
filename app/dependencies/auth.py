from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from typing import Annotated

from app.models.user import User
from app.repositories.user import UserRepository
from app.services.auth import AuthServices
from app.repositories.auth import AuthRepository
from app.common.exceptions import InvalidTokenException


async def get_auth_services():
    return AuthServices(user_repository=UserRepository, auth_repository=AuthRepository)

GetAuthServices = Annotated[AuthServices, Depends(get_auth_services)]


# http_bearer = HTTPBearer()
http_bearer = Annotated[HTTPAuthorizationCredentials, Depends(HTTPBearer())]

async def get_user_from_token(auth_services: GetAuthServices, token: http_bearer) -> User:
    access_token = token.credentials
    user = await auth_services.get_user_from_token(token=access_token)
    if user is None:
        raise InvalidTokenException
    return user


GetCurrentUser = Annotated[User, Depends(get_user_from_token)]
