from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.orm import Session
from typing import Dict, List
from datetime import datetime

import models
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Chat App Backend")

# Store active connections per room
class ConnectionManager:
    def __init__(self):
        self.rooms: Dict[str, List[WebSocket]] = {}

    async def connect(self, room: str, websocket: WebSocket):
        await websocket.accept()
        if room not in self.rooms:
            self.rooms[room] = []
        self.rooms[room].append(websocket)

    def disconnect(self, room: str, websocket: WebSocket):
        self.rooms[room].remove(websocket)

    async def broadcast(self, room: str, message: str):
        if room in self.rooms:
            for connection in self.rooms[room]:
                await connection.send_text(message)

manager = ConnectionManager()

@app.websocket("/ws/{room}/{username}")
async def websocket_endpoint(
    websocket: WebSocket,
    room: str,
    username: str,
    db: Session = Depends(get_db)
):
    await manager.connect(room, websocket)
    try:
        while True:
            data = await websocket.receive_text()

            # Save message to DB
            msg = models.Message(room=room, username=username, content=data)
            db.add(msg)
            db.commit()

            # Broadcast to all users in room
            await manager.broadcast(room, f"{username}: {data}")
    except WebSocketDisconnect:
        manager.disconnect(room, websocket)
        await manager.broadcast(room, f"{username} left the chat")

@app.get("/rooms/{room}/history")
def get_chat_history(room: str, db: Session = Depends(get_db)):
    messages = db.query(models.Message).filter(
        models.Message.room == room
    ).order_by(models.Message.timestamp).all()
    return [
        {
            "username": m.username,
            "content": m.content,
            "timestamp": m.timestamp
        } for m in messages
    ]

@app.get("/rooms")
def get_active_rooms():
    return {"active_rooms": list(manager.rooms.keys())}