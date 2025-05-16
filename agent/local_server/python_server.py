# main.py

# Important Instructions:
# 1. Close any existing Chrome instances.
# 2. Start Chrome with remote debugging enabled:
#    /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222
# 3. Run the FastAPI server:
#    uvicorn main:app --host 127.0.0.1 --port 8888 --reload --workers 1
# make sure you set OPENAI_API_KEY=yourOpenAIKeyHere to .env file

import os

os.environ["PYDANTIC_V1_COMPAT_MODE"] = "true"
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from fastapi import FastAPI, WebSocket
import logging
from fastapi.middleware.cors import CORSMiddleware
from agent.local_server.controllers import (
    requestController,
)  # 라우터 import
from fastapi.responses import Response


# ----------------------------
# Configure Logging
# ----------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ----------------------------
# Initialize FastAPI App
# ----------------------------
app = FastAPI(title="AI Agent API with BrowserUse", version="1.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*"
    ],  # For development: allow all origins. In production, specify exact origins.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 라우터 등록
app.include_router(requestController.router)
# app.include_router(webSocketController.router)

# For executable.
# ----------------------------
# Entry Point
# ----------------------------
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "python_server:app", host="127.0.0.1", port=8888, reload=False, workers=1
    )
