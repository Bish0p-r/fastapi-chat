from datetime import datetime, timedelta

from beanie import Document, PydanticObjectId

from app.models.user import User


class Message(Document):
    chat_room_id: PydanticObjectId
    user: User
    message: str
    created_at: timedelta = datetime.utcnow()

    class Settings:
        name = "messages"


class ChatRoom(Document):
    messages: list[Message] = None
    owner: User
    users: list[User]

    class Settings:
        name = "chatRooms"
