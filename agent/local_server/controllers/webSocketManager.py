from fastapi import WebSocket
from typing import List

class WebSocketManager:
    def __init__(self):
        self.connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.connections.remove(websocket)

    async def send_to_all(self, message: dict):
        for conn in self.connections:
            await conn.send_json(message)

websocket_manager = WebSocketManager()
