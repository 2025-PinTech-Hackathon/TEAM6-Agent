from fastapi import APIRouter, Query
import logging
from agent.local_server.core.task_state import (
    TaskRequest, TaskResponse, task_id_counter, task_lock
)
from agent.local_server.core.task_executor import execute_task

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/run", response_model=TaskResponse)
async def run_task_post(request: TaskRequest):
    global task_id_counter
    task = request.task
    logger.info(f"Received task via POST: {task}")
    
    async with task_lock:
        task_id_counter += 1
        current_task_id = task_id_counter

    result = await execute_task(current_task_id, task)
    return TaskResponse(result=result)

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
    return TaskResponse(result=result)