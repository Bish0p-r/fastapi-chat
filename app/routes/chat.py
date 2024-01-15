from beanie import PydanticObjectId
from pprint import pprint
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Request, Depends
from fastapi.security import HTTPAuthorizationCredentials
from starlette.templating import Jinja2Templates

from app.dependencies.auth import GetCurrentUser
from app.dependencies.chat import GetChatServices
from app.dependencies.auth import get_current_user_from_token_ws, GetAuthServices


router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)

templates = Jinja2Templates(directory="app/templates")


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()


@router.get("/{room_id}")
async def connect_to_chat_room(room_id: PydanticObjectId, user: GetCurrentUser, request: Request):
    # pprint(request.headers)
    token = request.headers.get("authorization")
    return templates.TemplateResponse(
        "chat.html",
        {"user": user, "room_id": room_id, "request": request, "token1": str(token)}
    )


@router.post("/")
async def create_chat_room(user: GetCurrentUser, chat_services: GetChatServices):
    return await chat_services.create_chat_room(user=user)

async def test_dep(token):
    print(token)
    return token


@router.websocket("/ws/{room_id}")
async def websocket_chat_room(
        room_id: str,
        websocket: WebSocket,
        token: str,
        auth_services: GetAuthServices
):
    # print(user)
    # print(websocket.headers)
    print(websocket.cookies)
    # TODO: добавить аунтефикацию по токену в куки
    user = await get_current_user_from_token_ws(token=token, websocket=websocket, auth_services=auth_services)
    # print(user)
    await manager.connect(websocket)
    await manager.broadcast(f"Client #{room_id} joined the chat")
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast(f"Client #{room_id} says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{room_id} left the chat")