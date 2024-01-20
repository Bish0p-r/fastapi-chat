from collections import defaultdict
from typing import Dict

from aio_pika import ExchangeType, connect, Message as pika_Message
from aio_pika.abc import AbstractIncomingMessage
from beanie import PydanticObjectId
from fastapi import HTTPException, status, WebSocket, WebSocketDisconnect
import aio_pika

from app.models.user import User
from app.models.chat import ChatRoom, Message
from app.repositories.chat import ChatRepository, MessageRepository
from app.config import settings


class ChatManager:
    _clients: Dict[str, set[WebSocket]] = defaultdict(set)

    def __init__(self, ws: WebSocket, sender, room_id: str, repository, user):
        self.ws = ws
        self.sender = sender
        self.room_id = room_id
        self._clients[room_id].add(ws)
        self.message_repository = repository
        self.user = user

    @classmethod
    async def send(cls, message: str, key: str):
        for ws in cls._clients[key]:
            await ws.send_text(message)

    async def response(self):
        await self.ws.accept()
        #TODO: send recent messages
        try:
            while True:
                print(self._clients)
                message = await self.ws.receive_text()
                await self.message_repository.create(message=message, chat_room_id=self.room_id, user=self.user)
                await self.sender.send(message, room_id=self.room_id)
        except WebSocketDisconnect:
            self._clients[self.room_id].remove(self.ws)


class RMQManager:
    _instance = None
    _is_ready = False
    _chat_manger = ChatManager

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    async def setup(self):
        connection = await connect(settings.RABBITMQ_URI)
        channel = await connection.channel()
        exchange = await channel.declare_exchange('wschat', ExchangeType.FANOUT, durable=True)
        queue = await channel.declare_queue(exclusive=True)

        await queue.bind(exchange)
        await queue.consume(self.on_message)

        self.exchange = exchange
        self._is_ready = True

    async def on_message(self, message: AbstractIncomingMessage):
        room_id = message.headers.get('room_id')

        async with message.process():
            await self._chat_manger.send(message.body.decode(), key=room_id)

    async def send(self, message: str, routing_key='', room_id='123'):
        msg = pika_Message(message.encode())
        msg.headers['room_id'] = room_id
        await self.exchange.publish(msg, routing_key=routing_key)


class ChatServices:
    _chat_manger = ChatManager

    def __init__(self, chat_repository: type[ChatRepository], message_repository: type[MessageRepository]):
        self.repository = chat_repository
        self.message_repository = message_repository

    async def get_available_chats(self):
        return await self.repository.get_list()

    async def create_chat_room(self, user: User):
        return await self.repository.create(**{"owner": user, "users": [user]})

    async def start_chat(self, ws: WebSocket, manager: RMQManager, room_id: str, user: User):
        chat_manager = self._chat_manger(
            ws=ws, sender=manager, room_id=room_id, user=user, repository=self.message_repository
        )
        await chat_manager.response()


class MessageServices:
    def __init__(self, repository: type[MessageRepository]):
        self.repository = repository

    async def get_messages(self, room_id: PydanticObjectId):
        return await self.repository.get_chat_messages(chat_id=room_id)


