from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from repository.job_repo import JobRepository
from services.job_service import JobService
from schema import JobListingCreate
from database import get_db

router = APIRouter()

@router.post("/jobs/")
def create_job(job: JobListingCreate, db: Session = Depends(get_db)):
    repo = JobRepository(db)
    return repo.create_job(job)
@router.get("/match-resumes-to-jobs/")
def match_resumes_to_jobs():
    matching_results = JobService.match_resumes_to_jobs()
    return {"matching_results": matching_results}