from typing import Dict, List

from fastapi import WebSocket, WebSocketDisconnect
from security import verify_token
from db_models import User, Product, Chathistory
from database_connection import get_db
from sqlalchemy.orm import Session
from chatbot_service import chatbot_service

import json
from datetime import datetime


class ConnectionManager:

    def __init__(self):
        self.active_connections: Dict[int, WebSocket] = {}

    async def connect(self, websocket: WebSocket, user_id: int):
        await websocket.accept()
        self.active_connections[user_id] = websocket
        print(f"User {user_id} connected")

    def disconnect(self, user_id: int):
        if user_id in self.active_connections:
            del self.active_connections[user_id]

        print(f"User {user_id} disconnected")

    async def send_message(self, message: dict, user_id: int):
        if user_id in self.active_connections:
            websocket = self.active_connections[user_id]
            await websocket.send_json(message)

    async def send_text(self, message: str, user_id: int):
        if user_id in self.active_connections:
            websocket = self.active_connections[user_id]
            await websocket.send_text(message)


manager = ConnectionManager()


async def authenticate_websocket(token: str) -> int:

    user_id = verify_token(token)

    if user_id:
        return user_id
    else:
        raise Exception("Invalid or expired token")


async def load_chat_history(
    user_id: int,
    db: Session,
    limit: int
) -> List[dict]:

    chat_history = (
        db.query(Chathistory)
        .filter(Chathistory.user_id == user_id)
        .order_by(Chathistory.timestamp.desc())
        .limit(limit)
        .all()
    )
    #new added
    if not chat_history:
        return None
    #till here
    chat_history.reverse()

    chat_messages = []

    for message in chat_history:

        message_data = {
            "sender": "user" if message.sender == "user" else "assistant",
            "message": message.message,
            "timestamp": message.timestamp.isoformat()
        }

        chat_messages.append(message_data)

    return chat_messages


async def save_message_to_db(
    user_id: int,
    message: str,
    sender: str,
    db: Session
):

    chat_history = Chathistory(
        user_id=user_id,
        message=message,
        sender=sender
    )

    db.add(chat_history)
    db.commit()
    db.refresh(chat_history)

    return chat_history


async def handle_chat_websocket(
    websocket: WebSocket,
    token: str
):

    db: Session = next(get_db())

    try:

        # Authenticate user
        user_id = await authenticate_websocket(token)

        # Get user from database
        user = (
            db.query(User)
            .filter(User.user_id == user_id)
            .first()
        )

        if not user:

            await websocket.close(
                code=1008,
                reason="Invalid user"
            )

            return

        # Connect user
        await manager.connect(websocket, user_id)

        # Load previous chat history
        chat_history = await load_chat_history(
            user_id,
            db,
            10
        )

        if chat_history:

            history_message = {
                "type": "history",
                "message": chat_history
            }

            await manager.send_message(
                history_message,
                user_id
            )

        else:

            welcome_text = (
                f"Hi {user.full_name}, "
                f"welcome to {chatbot_service.company_name}. "
                f"I am {chatbot_service.bot_name}. "
                f"How can I help you today?"
            )

            welcome_message = {
                "type": "message",
                "message": welcome_text,
                "sender": "assistant",
                "timestamp": datetime.now().isoformat()
            }

            await manager.send_message(
                welcome_message,
                user_id
            )

        # Keep receiving messages
        while True:

            data = await websocket.receive_text()

            message_data = json.loads(data)

            message = message_data["message"].strip()

            if not message:
                continue

            # Save user's message
            await save_message_to_db(
                user_id,
                message,
                "user",
                db
            )

            # Get products from database
            products = db.query(Product).all()

            # Get recent chat history
            chat_history = (
                db.query(Chathistory)
                .filter(Chathistory.user_id == user_id)
                .order_by(Chathistory.timestamp.desc())
                .limit(10)
                .all()
            )

            chat_history.reverse()

            # Get response from chatbot
            response = chatbot_service.chat(
                user.full_name,
                message,
                products,
                chat_history
            )

            # Save assistant response
            await save_message_to_db(
                user_id,
                response,
                "assistant",
                db
            )

            # Send response to client
            response_message = {
                "type": "message",
                "message": response,
                "sender": "assistant",
                "timestamp": datetime.now().isoformat()
            }

            await manager.send_message(
                response_message,
                user_id
            )

    except WebSocketDisconnect:

        manager.disconnect(user_id)

    except Exception as e:

        print(f"Error: {e}")
        try:
            await websocket.close(code=1008,reason="Error")
        except:
            pass
        if user_id:
            manager.disconnect(user_id)

    finally:

        db.close()