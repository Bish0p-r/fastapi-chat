from fastapi import Response

from app.common.exceptions import (
    EmailAlreadyExistsException,
    IncorrectEmailOrPasswordException,
)
from app.common.utils import get_hash_password, verify_password
from app.models.user import User
from app.repositories.user import UserRepository
from app.services.token import JWTTokenServices


class AuthServices:
    def __init__(self, user_repository: type[UserRepository], token_services: JWTTokenServices) -> None:
        self.user_repository = user_repository
        self.token_services = token_services

    @staticmethod
    async def set_tokens_to_cookie(response: Response, access_token: str, refresh_token: str) -> None:
        response.set_cookie(key="chat_access_token", value=access_token, httponly=True)
        response.set_cookie(key="chat_refresh_token", value=refresh_token, httponly=True)

    @staticmethod
    async def delete_tokens_from_cookie(response: Response) -> None:
        response.delete_cookie(key="chat_access_token")
        response.delete_cookie(key="chat_refresh_token")

    async def create_user(self, user_data: dict) -> User:
        user = await self.user_repository.get_by_kwargs(email=user_data.get("email"))
        if user:
            raise EmailAlreadyExistsException
        hashed_password = get_hash_password(user_data.get("password"))
        return await self.user_repository.create(**user_data, hashed_password=hashed_password)

    async def login(self, response: Response, user_data: dict, user_agent: str) -> tuple[str, str]:
        user = await self.user_repository.get_by_kwargs(email=user_data["email"])
        if not user or not verify_password(user_data["password"], user.hashed_password):
            raise IncorrectEmailOrPasswordException
        await self.token_services.delete_token_after_login(user_id=user.id, user_agent=user_agent)
        data = {"sub": str(user.id), "user_agent": user_agent}
        access_token, refresh_token = await self.token_services.issue_tokens_for_user(token_data=data)
        await self.set_tokens_to_cookie(response=response, access_token=access_token, refresh_token=refresh_token)
        return access_token, refresh_token

    async def logout(self, response: Response, token: str, user_agent: str) -> None:
        existed_token = await self.token_services.validate_refresh_token(token=token, user_agent=user_agent)
        await self.token_services.delete_token_by_id(_id=existed_token.id)
        await self.delete_tokens_from_cookie(response=response)

    async def refresh_tokens(self, response: Response, token: str, user_agent: str) -> tuple[str, str]:
        existed_token = await self.token_services.validate_refresh_token(token=token, user_agent=user_agent)
        await self.token_services.delete_token_by_id(_id=existed_token.id)
        data = {"sub": existed_token.user_id, "user_agent": existed_token.user_agent}
        access_token, refresh_token = await self.token_services.issue_tokens_for_user(token_data=data)
        await self.set_tokens_to_cookie(response=response, access_token=access_token, refresh_token=refresh_token)
        return access_token, refresh_token

    async def logout_from_all_devices(self, response: Response, user: User) -> None:
        await self.token_services.delete_all_user_tokens(user_id=user.id)
        await self.delete_tokens_from_cookie(response=response)
