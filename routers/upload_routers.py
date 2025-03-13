from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from services.fileparser import process_resume, process_resumes_from_folder
from services.file_service import FileService
from database import get_db

router = APIRouter()

@router.post("/upload-resume/")
async def upload_single_resume(
    resume: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    try:
        file_path = FileService.handle_uploaded_file(resume)  # Save file
        process_resume(file_path, db)  # Process resume
        return {"message": f"Resume {resume.filename} uploaded and processed successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/upload-folder/")
async def upload_folder(
    folder: List[UploadFile] = File(...),
    db: Session = Depends(get_db)
):
    try:
        folder_path = "uploads/"  # Replace with your folder logic
        for file in folder:
            file_path = FileService.handle_uploaded_file(file)  # Save each file
            process_resume(file_path, db)  # Process each file
        return {"message": "All files in the folder uploaded and processed successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
