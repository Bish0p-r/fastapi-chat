from datetime import timedelta

from beanie import PydanticObjectId
from pydantic import BaseModel

from app.schemas.user import UserSchema


class MessageSchema(BaseModel):
    chat_room_id: PydanticObjectId
    user: UserSchema
    message: str
    created_at: timedelta


class ChatSchema(BaseModel):
    id: PydanticObjectId
    messages: list[MessageSchema] = []
    owner: UserSchema
    users: list[UserSchema]
    is_private: bool = False


class ChatCreateSchema(BaseModel):
    is_private: bool = False
