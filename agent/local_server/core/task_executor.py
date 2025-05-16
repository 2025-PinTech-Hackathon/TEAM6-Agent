import os
from dotenv import load_dotenv
import logging
import traceback
from datetime import datetime
from agent.local_server.core.task_state import task_records, task_lock, TaskRecord, TaskStatus
from browser_use.browser.browser import Browser, BrowserConfig
from browser_use import Agent
#from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import SecretStr
from agent.local_server.core.task_utils import get_chrome_path
from pathlib import Path

logger = logging.getLogger(__name__)

# .env 상대 경로 자동 탐지
load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent.parent / ".env")

# Verify the OpenAI API key is loaded
api_key = os.getenv("GEMINI_API_KEY") #OPENAI_API_KEY
if not api_key:
    raise ValueError(
        "GEMINI_API_KEY not found in .env file. Make sure your .env file is set up correctly."
    )

async def execute_task(task_id: int, task: str):
    """
    Background task to execute the AI agent.
    Initializes a new browser instance for each task to ensure isolation.
    """
    global task_records
    browser = None  # Initialize browser instance for this task
    try:
        logger.info(f"Starting background task ID {task_id}: {task}")
        
        # Create and add the task record with status 'running'
        async with task_lock:
            task_record = TaskRecord(
                id=task_id,
                task=task,
                status=TaskStatus.RUNNING,
                start_time=datetime.utcnow()
            )
            task_records.append(task_record)

        # Initialize a new browser instance for this task
        logger.info(f"Task ID {task_id}: Initializing new browser instance.")
        browser = Browser(
            config=BrowserConfig(
                chrome_instance_path=get_chrome_path(),  # Update if different
                disable_security=True,
                headless=False,  # Set to True for headless mode
                # Removed 'remote_debugging_port' as it caused issues
            )
        )
        logger.info(f"Task ID {task_id}: Browser initialized successfully.")
        
        # Initialize and run the Agent with the new browser instance
        agent = Agent(
            task=task,
            llm=ChatGoogleGenerativeAI(model='gemini-2.0-flash-exp', api_key=SecretStr(api_key)),  #ChatOpenAI(model="gpt-4o", api_key=api_key),
            browser=browser
        )
        logger.info(f"Task ID {task_id}: Agent initialized. Running task.")
        result = await agent.run()
        result_str = str(result)
        logger.info(f"Task ID {task_id}: Agent.run() completed successfully.")
        
        # Update the task record with status 'completed'
        async with task_lock:
            for record in task_records:
                if record.id == task_id:
                    record.status = TaskStatus.COMPLETED
                    record.end_time = datetime.utcnow()
                    record.duration = (record.end_time - record.start_time).total_seconds()
                    record.result = result
                    break
                
        return result_str

    except Exception as e:
        logger.error(f"Error in background task ID {task_id}: {e}")
        logger.error(traceback.format_exc())
        
        # Update the task record with status 'failed'
        async with task_lock:
            for record in task_records:
                if record.id == task_id:
                    record.status = TaskStatus.FAILED
                    record.end_time = datetime.utcnow()
                    record.duration = (record.end_time - record.start_time).total_seconds()
                    record.error = str(e)
                    break
    finally:
        # Ensure that the browser is closed in case of failure or success
        if browser:
            try:
                logger.info(f"Task ID {task_id}: Closing browser instance.")
                await browser.close()
                logger.info(f"Task ID {task_id}: Browser instance closed successfully.")
            except Exception as close_e:
                logger.error(f"Task ID {task_id}: Error closing browser: {close_e}")
                logger.error(traceback.format_exc())
