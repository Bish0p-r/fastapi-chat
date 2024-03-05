from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from app.config import settings
from app.models.auth import RefreshToken
from app.models.chat import ChatRoom, Message
from app.models.user import User


async def init_db():
    client = AsyncIOMotorClient(settings.MONGODB_CONN_STRING)

    await init_beanie(
        database=client[settings.MONGODB_NAME],
        document_models=[User, RefreshToken, ChatRoom, Message],
    )
