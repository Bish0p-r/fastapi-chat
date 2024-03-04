from beanie import PydanticObjectId
from fastapi import APIRouter, WebSocket, Request
from starlette.templating import Jinja2Templates


from app.dependencies.auth import GetCurrentUser
from app.dependencies.chat import GetChatServices, GetWSChatManager, GetMessageServices
from app.dependencies.auth import GetCurrentUserWS, GetCurrentUserFromCookie
from app.models.chat import Message
from app.schemas.chat import ChatSchema


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


@router.get("/messages/{room_id}")
async def get_chat_messages(
        message_services: GetMessageServices, room_id: PydanticObjectId, user: GetCurrentUserFromCookie
) -> list[Message]:
    # TODO: permission check
    return await message_services.get_messages(room_id=room_id)


@router.get("/{room_id}")
async def connect_to_chat_room(room_id: str, user: GetCurrentUserFromCookie, request: Request):
    return templates.TemplateResponse(
        "chat.html",
        {"user": user, "room_id": room_id, "request": request}
    )


@router.websocket('/ws/{room_id}')
async def chat(
        ws: WebSocket, room_id: str, manager: GetWSChatManager, user: GetCurrentUserWS, chat_services: GetChatServices
):
    await chat_services.start_chat(ws=ws, manager=manager, room_id=room_id, user=user)
