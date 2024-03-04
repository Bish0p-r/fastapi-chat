import pymongo
from beanie import PydanticObjectId

from app.models.chat import ChatRoom, Message
from app.common.base.repository import BaseRepository

class ChatRepository(BaseRepository):
    collection: ChatRoom = ChatRoom

    @classmethod
    async def get_rooms_list(cls, is_private: bool = False) -> list[collection]:
        return await cls.collection.find_all(cls.collection.is_private == is_private).to_list()


class MessageRepository(BaseRepository):
    collection: Message = Message

    @classmethod
    async def get_chat_messages(cls, chat_id: PydanticObjectId) -> list[collection]:
        return await cls.collection.find_many(cls.collection.chat_room_id == chat_id).sort("created_at").to_list()
