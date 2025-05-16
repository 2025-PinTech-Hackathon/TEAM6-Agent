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
    print(result)
    return TaskResponse(
        result=(
            "Task 수행 성공! Task 실행 종료!"
            if is_task_success(result)
            else "Task 수행 실패! Task 실행 종료!"
        )
    )
