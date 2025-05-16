from fastapi import FastAPI, WebSocket
import uvicorn

app = FastAPI()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"메시지 받음: {data}")


if __name__ == "__main__":
    uvicorn.run("test_server:app", host="0.0.0.0", port=8888, reload=True)
