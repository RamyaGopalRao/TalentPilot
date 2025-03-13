from sqlalchemy.orm import Session
from models import Resume

class ResumeRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_resume(self, resume_data):
        resume = Resume(**resume_data.dict())
        self.db.add(resume)
        self.db.commit()
        self.db.refresh(resume)
        return resume

    def get_resumes(self):
        return self.db.query(Resume).all()
