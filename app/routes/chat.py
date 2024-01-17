from fastapi import APIRouter, WebSocket, Request
from starlette.templating import Jinja2Templates


from app.dependencies.auth import GetCurrentUser
from app.dependencies.chat import GetChatServices, GetWSChatManager
from app.dependencies.auth import GetCurrentUserWS, GetCurrentUserFromCookie


router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)

templates = Jinja2Templates(directory="app/templates")



@router.post("/")
async def create_chat_room(user: GetCurrentUser, chat_services: GetChatServices):
    return await chat_services.create_chat_room(user=user)


@router.get("/{room_id}")
async def connect_to_chat_room(room_id: str, user: GetCurrentUserFromCookie, request: Request):
    return templates.TemplateResponse(
        "chat.html",
        {"user": user, "room_id": room_id, "request": request}
    )


@router.websocket('/ws/{room_id}')
async def chat(ws: WebSocket, room_id: str, manager: GetWSChatManager, user: GetCurrentUserWS, chat_services: GetChatServices):
    await chat_services.start_chat(ws=ws, manager=manager, room_id=room_id, user=user)
    # await WSChat(ws, manager, room_id).response()
