from fastapi import Depends
from typing import Annotated

from app.services.chat import ChatServices
from app.repositories.chat import ChatRepository


async def get_chat_services():
    return ChatServices(repository=ChatRepository)

GetChatServices = Annotated[ChatServices, Depends(get_chat_services)]
