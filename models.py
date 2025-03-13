from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

# Intermediate table for Many-to-Many relationship between JobListing and Skills
job_skills = Table(
    'job_skills', Base.metadata,
    Column('job_id', Integer, ForeignKey('joblisting.id')),
    Column('skill_id', Integer, ForeignKey('skill.id'))
)

class Skill(Base):
    __tablename__ = "skill"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)

class Resume(Base):
    __tablename__ = "resume"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    phone = Column(String(20), nullable=False)
    skills = Column(Text, nullable=False)  # Skills can be stored as a comma-separated string
    years = Column(Integer, nullable=False)
    is_duplicate = Column(Boolean, default=False)

class Education(Base):
    __tablename__ = "education"
    id = Column(Integer, primary_key=True, index=True)
    resume_id = Column(Integer, ForeignKey("resume.id"), nullable=False)
    degree = Column(String(100), nullable=False)
    field = Column(String(100), nullable=False)
    institution = Column(String(200), nullable=False)
    year = Column(String(4), nullable=False)

class Experience(Base):
    __tablename__ = "experience"
    id = Column(Integer, primary_key=True, index=True)
    resume_id = Column(Integer, ForeignKey("resume.id"), nullable=False)
    position = Column(String(100), nullable=False)
    company = Column(String(100), nullable=False)
    duration = Column(String(50), nullable=False)

class JobListing(Base):
    __tablename__ = "joblisting"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    specifications = Column(Text, nullable=True)
    years_of_experience_required = Column(Integer, default=0)
    required_skills = relationship("Skill", secondary=job_skills, backref="job_listings")
