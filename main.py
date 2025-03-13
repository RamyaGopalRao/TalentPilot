from fastapi import FastAPI
from routers import resume_router,job_routers,upload_routers
import uvicorn

app = FastAPI()

# Include routers
app.include_router(resume_router.router, prefix="/api", tags=["Resumes"])
app.include_router(job_routers.router, prefix="/api", tags=["Jobs"])
app.include_router(upload_routers.router, prefix="/api", tags=["Uploads"])

if __name__ == "__main__":
    uvicorn.run(app, port=8000)
