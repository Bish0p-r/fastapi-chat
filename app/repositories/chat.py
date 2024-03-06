from beanie import PydanticObjectId
from beanie.operators import ElemMatch

from app.common.base.repository import BaseRepository
from app.models.chat import ChatRoom, Message
from app.models.user import User


class ChatRepository(BaseRepository):
    collection: ChatRoom = ChatRoom

    @classmethod
    async def get_rooms_list(cls, is_private: bool = False) -> list[collection]:
        return await cls.collection.find_all(cls.collection.is_private == is_private).to_list()

    @classmethod
    async def get_user_chats(cls, user: User) -> list[collection]:
        return await cls.collection.find_many(ElemMatch(cls.collection.users, _id=user.id)).to_list()

    @classmethod
    async def delete_user_from_chat(cls, room_id: PydanticObjectId, user: User):
        instance = await cls.collection.find_one(cls.collection.id == room_id)
        instance.users = [u for u in instance.users if u.id != user.id]
        await instance.save()
        return instance

    @classmethod
    async def add_user_to_chat_room(cls, room_id: str, user: User) -> collection:
        instance = await cls.collection.find_one(cls.collection.id == room_id)
        if user not in instance.users:
            instance.users.append(user)
            await instance.save()
        return instance


class MessageRepository(BaseRepository):
    collection: Message = Message

    @classmethod
    async def get_chat_messages(cls, chat_id: PydanticObjectId) -> list[collection]:
        return await cls.collection.find_many(cls.collection.chat_room_id == chat_id).sort("created_at").to_list()
