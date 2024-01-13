from datetime import datetime, timedelta

from fastapi import HTTPException, status
from jose import jwt, JWTError, ExpiredSignatureError
from beanie import PydanticObjectId

from app.config import settings
from app.repositories.user import UserRepository
from app.repositories.auth import AuthRepository
from app.common.utils import verify_password
from app.models.user import User
from app.models.auth import RefreshToken
from app.common.exceptions import InvalidTokenException, ExpiredTokenException


class AuthServices:
    def __init__(self, user_repository: type[UserRepository], auth_repository: type[AuthRepository]):
        self.auth_repository = auth_repository
        self.user_repository = user_repository

    @staticmethod
    async def create_token(data: dict, expire_in: timedelta) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + expire_in
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt

    @staticmethod
    async def decode_token(token: str) -> dict:
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        except ExpiredSignatureError:
            raise ExpiredTokenException
        except JWTError:
            raise InvalidTokenException
        return payload

    async def validate_refresh_token(self, token: str, user_agent: str) -> RefreshToken:
        existed_token = await self.auth_repository.get_by_refresh_token(refresh_token=token)
        if existed_token is None:
            raise InvalidTokenException

        payload = await self.decode_token(token)
        if payload.get("user_agent") != user_agent or payload.get("type") != "refresh-token":
            raise InvalidTokenException
        return existed_token

    async def create_access_token(
            self,
            data: dict,
            expire_in: timedelta = timedelta(minutes=settings.ACCESS_TOKEN_EXP_MINUTES)
    ):
        data = data.copy()
        data.update({"type": "access-token"})
        return await self.create_token(data, expire_in=expire_in)

    async def create_refresh_token(
            self,
            data: dict,
            expire_in=timedelta(days=settings.REFRESH_TOKEN_EXP_DAYS)
    ) -> str:
        data = data.copy()
        data.update({"type": "refresh-token"})
        user_id = data.get("sub")
        user_agent = data.get("user_agent")
        refresh_token = await self.create_token(data=data, expire_in=expire_in)
        token_data = {"user_id": user_id, "user_agent": user_agent, "refresh_token": refresh_token}
        await self.auth_repository.create(**token_data)
        return refresh_token

    async def issue_tokens_for_user(self, token_data:dict) -> tuple[str, str]:
        return await self.create_access_token(data=token_data), await self.create_refresh_token(data=token_data)

    async def get_user_from_token(self, token: str) -> User:
        payload = await self.decode_token(token)
        data = {}
        sub = payload.get("sub")
        if sub is None:
            raise InvalidTokenException

        if payload.get("type") == "access-token":
            data["_id"] = PydanticObjectId(sub)
        elif payload.get("type") == "email-verification-token":
            data["email"] = sub
        else:
            raise InvalidTokenException
        return await self.user_repository.get_by_kwargs(**data)

    async def login(self, user_data: dict, user_agent: str) -> tuple[str, str]:
        user = await self.user_repository.get_by_kwargs(email=user_data["email"])
        if not user or not verify_password(user_data["password"], user.hashed_password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")

        await self.auth_repository.delete_by_agent_and_id(user_id=user.id, user_agent=user_agent)
        data = {"sub": str(user.id),"user_agent": user_agent}
        return await self.issue_tokens_for_user(token_data=data)

    async def logout(self, token: str, user_agent: str) -> None:
        existed_token = await self.validate_refresh_token(token=token, user_agent=user_agent)
        await self.auth_repository.delete_by_id(_id=existed_token.id)

    async def refresh_tokens(self, token: str, user_agent:str) -> tuple[str, str]:
        existed_token = await self.validate_refresh_token(token=token, user_agent=user_agent)
        await self.auth_repository.delete_by_id(_id=existed_token.id)
        data = {"sub": existed_token.user_id, "user_agent": existed_token.user_agent}
        return await self.issue_tokens_for_user(token_data=data)

    async def logout_from_all_devices(self, user) -> None:
        await self.auth_repository.delete(**{"user_id": user.id})
