from datetime import datetime

from beanie import Document, PydanticObjectId

from app.models.user import User


class Message(Document):
    chat_room_id: PydanticObjectId
    user: User
    message: str
    created_at: datetime = datetime.utcnow()

    class Settings:
        name = "messages"


class ChatRoom(Document):
    messages: list[Message] = []
    owner: User
    users: list[User]
    is_private: bool = False

    class Settings:
        name = "chatRooms"
