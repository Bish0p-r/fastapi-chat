from fastapi import Depends
from typing import Annotated

from app.services.user import UserServices
from app.repositories.user import UserRepository


async def get_user_services():
    return UserServices(UserRepository)

GetUserServices = Annotated[UserServices, Depends(get_user_services)]

