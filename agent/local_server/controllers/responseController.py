from fastapi import APIRouter, Query
from typing import List, Optional
from agent.local_server.core.task_state import (
    task_records, task_lock, TaskStatus, TaskRecord
)

router = APIRouter()

@router.get("/lastResponses", response_model=List[TaskRecord])
async def get_last_responses(
    limit: Optional[int] = Query(100, description="Maximum number of task records to return"),
    status: Optional[TaskStatus] = Query(None, description="Filter by task status")
):
    """
    GET Endpoint to retrieve the last task responses.
    """
    async with task_lock:
        filtered_tasks = task_records.copy()
        if status:
            filtered_tasks = [task for task in filtered_tasks if task.status == status]
        sorted_tasks = sorted(filtered_tasks, key=lambda x: x.id, reverse=True)[:limit]
        return sorted_tasks


@router.get("/")
def read_root():
    return {
        "message": "AI Agent API with BrowserUse is running. Use the /run endpoint with a 'task' field in the POST request body or as a query parameter in a GET request to execute tasks."
    }
