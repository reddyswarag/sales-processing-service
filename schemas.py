from pydantic import BaseModel, ConfigDict
from enum import Enum

class JobRequest(BaseModel):
    task : str

class JobStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    RETRYING = "retrying"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class JobResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    job_id : int
    task : str | None
    status : JobStatus | None
    result : dict |None
    error : str | None
    current_attempt : int
    max_attempts : int