import os
from dotenv import load_dotenv
import logging
import traceback
from datetime import datetime, UTC
from agent.local_server.core.task_state import (
    task_records,
    task_lock,
    TaskRecord,
    TaskStatus,
)
from browser_use.browser.browser import Browser, BrowserConfig
from browser_use import Agent

# from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import SecretStr
from agent.local_server.core.task_utils import get_chrome_path
from pathlib import Path
from agent.local_server.core.task_hook import send_result_to_client
import json
from agent.local_server.controllers.webSocketManager import websocket_manager


logger = logging.getLogger(__name__)

# .env 상대 경로 자동 탐지
load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent.parent / ".env")

# 전역 브라우저 인스턴스
browser_instance = None

# Verify the OpenAI API key is loaded
api_key = os.getenv("GEMINI_API_KEY")  # OPENAI_API_KEY
if not api_key:
    raise ValueError(
        "GEMINI_API_KEY not found in .env file. Make sure your .env file is set up correctly."
    )


async def test_start(agent):
    print("==============owowowowowowowowowowo=======================")


async def test_end(agent):
    print("==============iiiiiiiiiiiiiiiiiiiiiiiiiiii=======================")


async def send_result_to_client(agent):
    print("==============iiiiiiiiiiiiiiiiiiiiiiiiiiii=======================")

    history = agent.state.history
    print(history)
    print(history.action_results()[-1])

    print("==============ow123123owowowowowo=======================")

    await websocket_manager.send_to_all(history.action_results()[-1].model_dump())
    print("==============owowowowowowowowowowo=======================")


async def execute_task(task_id: int, task: str):
    """
    Background task to execute the AI agent.
    Initializes a new browser instance for each task to ensure isolation.
    """
    global task_records, browser_instance
    try:
        logger.info(f"Starting background task ID {task_id}: {task}")

        # Create and add the task record with status 'running'
        async with task_lock:
            task_record = TaskRecord(
                id=task_id,
                task=task,
                status=TaskStatus.RUNNING,
                start_time=datetime.now(UTC),
            )
            task_records.append(task_record)

        # Initialize a new browser instance for this task
        logger.info(f"Task ID {task_id}: Initializing new browser instance.")

        # 브라우저 인스턴스 초기화 (없을 때만 생성)
        if browser_instance is None:
            logger.info(f"Task ID {task_id}: Initializing shared browser instance.")
            browser_instance = Browser(
                config=BrowserConfig(
                    chrome_instance_path=get_chrome_path(),
                    cdp_url="http://127.0.0.1:9222",
                    disable_security=True,
                    headless=False,
                    keep_alive=True,
                ),
            )
            logger.info("Shared browser instance created.")

        # Agent 실행
        agent = Agent(
            task=task,
            llm=ChatGoogleGenerativeAI(
                model="gemini-2.0-flash-exp", api_key=SecretStr(api_key)
            ),
            browser=browser_instance,
        )
        logger.info(f"Task ID {task_id}: Agent initialized. Running task.")
        result = await agent.run(
            on_step_end=send_result_to_client, on_step_start=test_start
        )
        logger.info(f"Task ID {task_id}: Agent.run() completed successfully.")

        # Update the task record with status 'completed'
        async with task_lock:
            for record in task_records:
                if record.id == task_id:
                    record.status = TaskStatus.COMPLETED
                    record.end_time = datetime.now(UTC)
                    record.duration = (
                        record.end_time - record.start_time
                    ).total_seconds()
                    record.result = result
                    break

        return result

    except Exception as e:
        logger.error(f"Error in background task ID {task_id}: {e}")
        logger.error(traceback.format_exc())

        # Update the task record with status 'failed'
        async with task_lock:
            for record in task_records:
                if record.id == task_id:
                    record.status = TaskStatus.FAILED
                    record.end_time = datetime.now(UTC)
                    record.duration = (
                        record.end_time - record.start_time
                    ).total_seconds()
                    record.error = str(e)
                    break
