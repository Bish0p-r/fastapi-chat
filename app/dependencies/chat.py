from fastapi import Depends
from typing import Annotated

from app.services.chat import ChatServices, MessageServices, RMQManager
from app.repositories.chat import ChatRepository, MessageRepository


async def get_rmq_manager():
    manager = RMQManager()
    if not manager._is_ready:
        await manager.setup()
    return manager

GetWSChatManager = Annotated[RMQManager, Depends(get_rmq_manager)]


async def get_chat_services():
    return ChatServices(chat_repository=ChatRepository, message_repository=MessageRepository)


GetChatServices = Annotated[ChatServices, Depends(get_chat_services)]

