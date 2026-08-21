from pydantic import BaseModel, ConfigDict

class JobRequest(BaseModel):
    task : str

class JobUpdate(BaseModel):
    status : str

class JobResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    job_id : int
    task : str | None
    status : str | None
    result : dict |None
    error : str | None
    current_attempt : int
    max_attempts : int