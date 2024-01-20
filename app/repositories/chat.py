import pymongo
from beanie import PydanticObjectId

from app.models.chat import ChatRoom, Message
from app.common.base.repository import BaseRepository

class ChatRepository(BaseRepository):
    collection: ChatRoom = ChatRoom


class MessageRepository(BaseRepository):
    collection: Message = Message

    @classmethod
    async def get_chat_messages(cls, chat_id: PydanticObjectId) -> list[collection]:
        return await cls.collection.find_many(cls.collection.chat_room_id == chat_id).sort("created_at").to_list()
