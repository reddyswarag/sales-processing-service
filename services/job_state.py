from schemas import JobStatus

VALID_TRANSITIONS ={
    JobStatus.PENDING : {JobStatus.PROCESSING,JobStatus.CANCELLED},
    JobStatus.PROCESSING : {JobStatus.COMPLETED, JobStatus.RETRYING, JobStatus.FAILED},
    JobStatus.RETRYING : {JobStatus.PROCESSING, JobStatus.CANCELLED},
    JobStatus.COMPLETED : set(),
    JobStatus.FAILED : set(),
    JobStatus.CANCELLED : set(),
}

def can_transition(current_status : JobStatus, new_status : JobStatus) -> bool:
    return new_status in VALID_TRANSITIONS[current_status]
