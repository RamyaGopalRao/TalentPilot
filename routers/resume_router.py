from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from repository.resume_repo import ResumeRepository
from schema import ResumeCreate
from database import get_db

router = APIRouter()

@router.post("/resumes/")
def create_resume(resume: ResumeCreate, db: Session = Depends(get_db)):
    repo = ResumeRepository(db)
    return repo.create_resume(resume)

@router.get("/resumes/")
def get_resumes(db: Session = Depends(get_db)):
    repo = ResumeRepository(db)
    return repo.get_resumes()
