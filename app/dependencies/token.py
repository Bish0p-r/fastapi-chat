from typing import Annotated

from fastapi import Depends

from app.repositories.token import JWTTokenRepository
from app.repositories.user import UserRepository
from app.services.token import JWTTokenServices


async def get_jwt_token_services() -> JWTTokenServices:
    return JWTTokenServices(user_repository=UserRepository, token_repository=JWTTokenRepository)

GetTokenServices = Annotated[JWTTokenServices, Depends(get_jwt_token_services)]


