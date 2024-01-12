import uuid
from datetime import datetime, timedelta

from fastapi import Response, HTTPException, status
from jose import jwt, JWTError, ExpiredSignatureError
from beanie import PydanticObjectId

from app.config import settings
from app.repositories.user import UserRepository
from app.repositories.auth import AuthRepository
from app.common.utils import verify_password
from app.models.user import User
from app.common.exceptions import InvalidTokenException, ExpiredTokenException


class AuthServices:
    def __init__(self, user_repository: type[UserRepository], auth_repository: type[AuthRepository]):
        self.auth_repository = auth_repository
        self.user_repository = user_repository

    @staticmethod
    async def __create_device_id() -> str:
        return str(uuid.uuid4())

    @staticmethod
    async def create_token(data: dict, expire_in: timedelta = timedelta(minutes=settings.ACCESS_TOKEN_EXP_MINUTES)) -> str:
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

    async def create_refresh_token(self, data, user_id: str, device_id: str) -> str:
        refresh_token = await self.create_token(data=data, expire_in=timedelta(days=settings.REFRESH_TOKEN_EXP_DAYS))
        token_data = {"user_id": user_id, "device_id": device_id, "refresh_token": refresh_token}
        await self.auth_repository.create(**token_data)
        return refresh_token

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

    async def login(self, user_data: dict):
        user = await self.user_repository.get_by_kwargs(email=user_data["email"])

        if not user or not verify_password(user_data["password"], user.hashed_password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")

        device_id = await self.__create_device_id()
        access_token = await self.create_token(
            data={"sub": str(user.id),"device_id": device_id, "type": "access-token"}
        )
        refresh_data = {"sub": str(user.id),"device_id": device_id, "type": "refresh-token"}
        refresh_token = await self.create_refresh_token(data=refresh_data, user_id=str(user.id), device_id=device_id)
        return access_token, refresh_token

    async def refresh_tokens(self, token: str):
        existed_token = await self.auth_repository.get_by_refresh_token(refresh_token=token)
        if existed_token is None:
            raise InvalidTokenException

        payload = await self.decode_token(token)
        if payload.get("device_id") != existed_token.device_id:
            raise InvalidTokenException

        await self.auth_repository.delete_by_id(id=existed_token.id)

        access_token = await self.create_token(
            data={"sub": existed_token.user_id, "device_id": existed_token.device_id, "type": "access-token"}
        )
        refresh_data = {"sub": existed_token.user_id, "device_id": existed_token.device_id, "type": "refresh-token"}
        refresh_token = await self.create_refresh_token(
            data=refresh_data, user_id=existed_token.user_id, device_id=existed_token.device_id
        )
        return access_token, refresh_token
