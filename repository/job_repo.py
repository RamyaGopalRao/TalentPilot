from sqlalchemy.orm import Session
from models import JobListing, Skill

class JobRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_job(self, job_data):
        job = JobListing(
            title=job_data.title,
            description=job_data.description,
            years_of_experience_required=job_data.years_of_experience_required
        )
        self.db.add(job)
        self.db.commit()
        self.db.refresh(job)
        return job
