from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database URL
# Replace the SQLite URL with your database's URL (e.g., PostgreSQL, MySQL)
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"  # Example SQLite database
# For PostgreSQL: "postgresql://user:password@localhost/dbname"
# For MySQL: "mysql+pymysql://user:password@localhost/dbname"

# Create the database engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}  # For SQLite only
)

# Session Local for database interaction
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for ORM models
Base = declarative_base()

# Dependency for accessing the database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
