from datetime import datetime, timedelta

from fastapi import Response, HTTPException, status
from jose import jwt, JWTError
from beanie import PydanticObjectId

from app.config import settings
from app.repositories.user import UserRepository
from app.repositories.auth import AuthRepository
from app.common.utils import verify_password
from app.models.user import User
from app.common.exceptions import InvalidTokenException


class AuthServices:
    def __init__(self, user_repository: type[UserRepository], auth_repository: type[AuthRepository]):
        self.auth_repository = auth_repository
        self.user_repository = user_repository

    @staticmethod
    async def create_token(data: dict, expire_in: timedelta = timedelta(minutes=30)) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + expire_in
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt

    @staticmethod
    async def decode_token(token: str) -> dict:
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        except JWTError:
            raise InvalidTokenException

        expire: str = payload.get("exp")
        if not expire or int(expire) < datetime.utcnow().timestamp():
            raise InvalidTokenException

        return payload

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

        return await self.create_token(data={"sub": str(user.id), "type": "access-token"})

    async def ping(self):
        return 'pong'
