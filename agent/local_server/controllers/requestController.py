from fastapi import APIRouter
import logging
from agent.local_server.core.task_state import (
    TaskResponse,
    task_id_counter,
    task_lock,
)
from agent.local_server.core.task_executor import execute_task
import re

task_prompts = [f"../prompt/task{i}.md" for i in range(1, 17)]

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/run/{number}", response_model=TaskResponse)
async def run_task_get(number: int):
    global task_id_counter

    with open(task_prompts[number], "r", encoding="utf-8") as f:
        task = f.read()

    logger.info(f"Received task via GET: {task_prompts[number]}")

    async with task_lock:
        task_id_counter += 1
        current_task_id = task_id_counter

    result = await execute_task(current_task_id, task)
    print("여기까지왔구나.")
    print(result.results[0])
    return TaskResponse(result=result.results[0].model_dump_json())
