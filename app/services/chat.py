from beanie import PydanticObjectId
from fastapi import HTTPException, status

from app.models.user import User
from app.models.chat import ChatRoom, Message
from app.repositories.chat import ChatRepository, MessageRepository


class ChatServices:
    def __init__(self, repository: type[ChatRepository]):
        self.repository = repository

    async def get_available_chats(self):
        return await self.repository.get_list()

    async def create_chat_room(self, user: User):
        return await self.repository.create(**{"owner": user, "users": [user]})


class MessageServices:
    def __init__(self, repository: type[MessageRepository]):
        self.repository = repository

    async def get_last_messages(self):
        return await self.repository.get_list()