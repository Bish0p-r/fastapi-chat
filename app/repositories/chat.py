import pymongo
from beanie import PydanticObjectId

from app.models.chat import ChatRoom, Message
from app.common.base.repository import BaseRepository

class ChatRepository(BaseRepository):
    collection: ChatRoom = ChatRoom


class MessageRepository(BaseRepository):
    collection: Message = Message

    async def get_chat_messages(self, chat_id: PydanticObjectId | str) -> list[Message]:
        return await self.collection.find_all(chat_room_id=chat_id).sort("-created_at").to_list()
