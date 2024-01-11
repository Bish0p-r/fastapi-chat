from fastapi import Depends

from app.services.auth import AuthServices
from app.services.user import UserServices
from app.repositories.user import UserRepository


async def get_user_services():
    return UserServices(UserRepository)

GetUserServices = Depends(get_user_services)

async def get_auth_services():
    return AuthServices(UserRepository)

GetAuthServices = Depends(get_auth_services)
