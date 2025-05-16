# agent/local_server/core/task_state.py

import asyncio
from datetime import datetime
from enum import Enum
from typing import Optional, List
from pydantic import BaseModel

class TaskStatus(str, Enum):
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

class TaskRequest(BaseModel):
    task: str

class TaskResponse(BaseModel):
    result: str

class TaskRecord(BaseModel):
    id: int
    task: str
    status: TaskStatus
    start_time: datetime
    end_time: Optional[datetime] = None
    duration: Optional[float] = None
    result: Optional[str] = None
    error: Optional[str] = None

# 전역 상태
task_records: List[TaskRecord] = []
task_id_counter: int = 0
task_lock = asyncio.Lock()
