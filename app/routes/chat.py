from typing import Annotated

from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, Request, WebSocket
from fastapi.responses import HTMLResponse
from starlette.templating import Jinja2Templates

from app.dependencies.auth import (
    GetCurrentUser,
    GetCurrentUserFromCookie,
    GetCurrentUserWS,
)
from app.dependencies.chat import GetChatServices, GetMessageServices, GetWSChatManager
from app.dependencies.user import GetUserServices
from app.models.chat import Message
from app.schemas.chat import ChatSchema
from app.schemas.user import UserIdSchema

router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)

templates = Jinja2Templates(directory="app/templates")


@router.get("/")
async def get_available_chats(chat_services: GetChatServices) -> list[ChatSchema]:
    return await chat_services.get_available_chats()


@router.get("/")
async def get_my_chats(chat_services: GetChatServices) -> list[ChatSchema]:
    return await chat_services.get_available_chats()


@router.post("/")
async def create_chat_room(user: GetCurrentUser, chat_services: GetChatServices):
    return await chat_services.create_chat_room(user=user)


@router.get("/{room_id}/messages")
async def get_chat_messages(
    chat_services: GetChatServices,
    message_services: GetMessageServices,
    room_id: PydanticObjectId,
    user: GetCurrentUserFromCookie,
) -> list[Message]:
    await chat_services.is_user_have_permission(user_id=user.id, room_id=room_id)
    return await message_services.get_messages(room_id=room_id)


@router.post("/{room_id}")
async def add_user_to_chat(
    chat_services: GetChatServices,
    user_services: GetUserServices,
    room_id: PydanticObjectId,
    invited_user_id: Annotated[UserIdSchema, Depends()],
    user: GetCurrentUserFromCookie,
) -> ChatSchema:
    invited_user = await user_services.get_user_by_id(user_id=invited_user_id.id)
    return await chat_services.add_user_to_chat(invited_user, user.id, room_id)


@router.get("/{room_id}")
async def connect_to_chat_room(
    chat_services: GetChatServices, room_id: PydanticObjectId, user: GetCurrentUserFromCookie, request: Request
) -> HTMLResponse:
    await chat_services.is_user_have_permission(user_id=user.id, room_id=room_id)
    return templates.TemplateResponse("chat.html", {"user": user, "room_id": room_id, "request": request})


@router.websocket("/ws/{room_id}")
async def chat(
    ws: WebSocket,
    room_id: str,
    manager: GetWSChatManager,
    user: GetCurrentUserWS,
    chat_services: GetChatServices,
):
    await chat_services.start_chat(ws=ws, manager=manager, room_id=room_id, user=user)
