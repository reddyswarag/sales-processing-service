from rq import Retry
from fastapi import FastAPI, HTTPException, Depends, UploadFile, File
from sqlalchemy.orm import Session
from database import get_db
from models import Job
from sqlalchemy import select
from schemas import JobUpdate, JobRequest, JobResponse
from pathlib import Path
import shutil 
from uuid import uuid4
from job_queue import csv_queue
from services.tasks import run_csv_job

app = FastAPI()

UPLOAD_DIR = Path("uploads")






@app.post("/jobs/upload" , status_code = 202)
def upload_csv(file : UploadFile = File(...), db: Session = Depends(get_db)):


    if not file.filename or not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="only .csv files are accepted")

    UPLOAD_DIR.mkdir(exist_ok=True)
    safe_filename=Path(file.filename).name
    stored_filename = f"{uuid4().hex}_{safe_filename}"
    file_path= UPLOAD_DIR/stored_filename
    with file_path.open("wb") as destination:
        shutil.copyfileobj(file.file, destination)

    new_job=Job(task= "upload_csv", status = "pending", file_path = str(file_path), result=None, error=None)
    db.add(new_job)
    db.commit()
    db.refresh(new_job)

    rq_job = csv_queue.enqueue(
        run_csv_job,
        new_job.job_id,
        new_job.file_path,
        job_id=f"csv-job-{new_job.job_id}",
        unique = True,
        retry = Retry(max=2, interval = [10,30])
    )

    return {
        "job_id" : new_job.job_id,
        "task" : new_job.task,
        "status": new_job.status,
        "filename" : safe_filename,
        "content_type" : file.content_type,
        "file_path" : str(file_path),
        "result" : new_job.result,
        "error": new_job.error,
        "rq_job_id" : rq_job.id
    }

@app.post("/jobs", response_model=JobResponse)
def create_job(job : JobRequest, db: Session=Depends(get_db)):
    new_job=Job(task = job.task, status = "pending")
    db.add(new_job)
    db.commit()
    db.refresh(new_job)
    return {
        "job_id":new_job.job_id,
        "task" : new_job.task,
        "status" : new_job.status
    }
    

@app.get("/jobs/{job_id}", response_model= JobResponse)
def get_job( 
    job_id : int, 
    db: Session= Depends(get_db)
):
    job=db.get(Job, job_id)

    if job is None:
        raise HTTPException(status_code=404,detail="not found !")
    return{
        "job_id": job.job_id,
        "task": job.task,
        "status":job.status,
        "result": job.result,
        "error" : job.error,
        "current_attempt" : job.current_attempt,
        "max_attempts" : job.max_attempts
    }

@app.get("/jobs", response_model= list[JobResponse])
def get_jobs( db: Session = Depends(get_db)):
    jobs = db.scalars(select(Job)).all()
    return[
        {
            "job_id": job.job_id,
            "task": job.task,
            "status": job.status,
            "result": job.result,
            "error" : job.error
        } 
        for job in jobs
    ]
    

@app.patch("/jobs/{job_id}", response_model=JobResponse)
def patch_job(job_id: int, jobupdate : JobUpdate, db : Session = Depends(get_db)):
    currjob=db.get(Job, job_id)
    if(currjob is not None):
        currjob.status=jobupdate.status
        db.commit()
        db.refresh(currjob)
        return currjob
    else:
        raise HTTPException(status_code=404,detail= "job not found")
    
@app.delete("/jobs/{job_id}")
def delete_job(job_id : int, db : Session = Depends(get_db)):
    job=db.get(Job, job_id)
    if job is None:
        raise HTTPException(status_code=404, detail = "job not found")
    else:
        db.delete(job)
        db.commit()
        return {"message" : "Deleted"}