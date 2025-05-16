from fastapi import APIRouter, Query
import logging
from agent.local_server.core.task_state import (
    TaskRequest, TaskResponse, task_id_counter, task_lock
)
from agent.local_server.core.task_executor import execute_task
import re

router = APIRouter()
logger = logging.getLogger(__name__)

def is_task_success(result_str: str | None) -> int:
    if not result_str or "AgentHistoryList" not in result_str:
        return 0

    try:
        matches = re.findall(r"ActionResult\(.*?\)", result_str)
        if not matches:
            return 0

        last = matches[-1]

        is_done = "is_done=True" in last
        success = "success=True" in last

        return 1 if is_done and success else 0

    except Exception as e:
        print("❌ parsing error in is_task_success:", e)
        return 0

@router.post("/run", response_model=TaskResponse)
async def run_task_post(request: TaskRequest):
    global task_id_counter
    task = request.task
    logger.info(f"Received task via POST: {task}")
    
    async with task_lock:
        task_id_counter += 1
        current_task_id = task_id_counter

    result = await execute_task(current_task_id, task)
    return TaskResponse(
        result="Task 수행 성공! Task 실행 종료!" if is_task_success(result) else "Task 수행 실패! Task 실행 종료!"
    )


@router.get("/run", response_model=TaskResponse)
async def run_task_get(
    task: str = Query(..., description="The task description for the AI agent.")
):
    global task_id_counter
    logger.info(f"Received task via GET: {task}")
    
    async with task_lock:
        task_id_counter += 1
        current_task_id = task_id_counter

    result = await execute_task(current_task_id, task)
    return TaskResponse(
        result="Task 수행 성공! Task 실행 종료!" if is_task_success(result) else "Task 수행 실패! Task 실행 종료!"
    )