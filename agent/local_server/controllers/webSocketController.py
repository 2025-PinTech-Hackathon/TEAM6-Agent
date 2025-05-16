from fastapi import APIRouter, WebSocket
from agent.local_server.controllers.webSocketManager import websocket_manager

router = APIRouter()

@router.websocket("/ws/agent")
async def websocket_endpoint(websocket: WebSocket):
    await websocket_manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except:
        websocket_manager.disconnect(websocket)
