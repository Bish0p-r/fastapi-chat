from typing import Annotated

from fastapi import Depends

from app.repositories.user import UserRepository
from app.services.user import UserServices


async def get_user_services():
    return UserServices(UserRepository)


GetUserServices = Annotated[UserServices, Depends(get_user_services)]
