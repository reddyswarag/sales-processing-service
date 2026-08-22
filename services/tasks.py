from database import SessionLocal
from models import Job
from services.processor import process_csv, PermanentCSVError
import datetime

def run_csv_job(job_id: int, file_path: str):
    db = SessionLocal()
    job = None
    
    

    try:
        job = db.get(Job, job_id)
        if job is None:
            raise ValueError(f"job not found with job_id : {job_id}")
        job.result = None
        job.error = None
        job.status = "processing"
        job.started_at = datetime.datetime.now(datetime.UTC)
        job.current_attempt += 1
        db.commit()
        result = process_csv(file_path = file_path)
        job.result = result
        job.status = "completed"
        job.completed_at = datetime.datetime.now(datetime.UTC)
        db.commit()

        return result

    except PermanentCSVError as exc:
        db.rollback()

        if job is not None:
            job.status = "failed"
            job.result = None
            job.error = str(exc)
            job.completed_at = datetime.datetime.now(datetime.UTC)
            db.commit()
            return


    
    except Exception as exc:
        db.rollback()

        if job is not None:
            job.result = None
            job.error=str(exc)

            if job.current_attempt >= job.max_attempts:
                job.status = "failed"
                job.completed_at = datetime.datetime.now(datetime.UTC)
            else:
                job.status = "retrying"

            db.commit()

        raise

        
    finally:
        db.close()
        

