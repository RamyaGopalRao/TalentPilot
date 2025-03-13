import os
import json
from concurrent.futures import ThreadPoolExecutor
from PyPDF2 import PdfReader
from docx import Document
from sqlalchemy.orm import Session
from openai import OpenAI
from models import Resume, Education, Experience


# Directory to save uploaded files
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Extract text from a file
def extract_text(file_path: str) -> str:
    text = ""
    if file_path.endswith('.pdf'):  # Process PDF files
        try:
            with open(file_path, 'rb') as file:
                reader = PdfReader(file)
                for page in reader.pages:
                    text += page.extract_text()
        except Exception as e:
            raise Exception(f"Error reading PDF file: {e}")
    elif file_path.endswith('.docx') or file_path.endswith('.doc'):  # Process Word files
        try:
            doc = Document(file_path)
            for paragraph in doc.paragraphs:
                text += paragraph.text + '\n'
        except Exception as e:
            raise Exception(f"Error reading Word file: {e}")
    else:
        raise Exception("Unsupported file format. Please provide .pdf or .docx files.")
    return text


# Parse resume using OpenAI
def parse_resume(file_path: str, user_message: str) -> dict:
    client = OpenAI(api_key="your_openai_api_key")  # Replace with actual API key

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        store=True,
        messages=[
            {"role": "user", "content": user_message}
        ]
    )
    bottext = completion.choices[0].message.content.strip()

    # Extract JSON-like content
    start_index = bottext.find("{")
    end_index = bottext.rfind("}") + 1
    if start_index != -1 and end_index != -1:
        json_text = bottext[start_index:end_index]
        try:
            return json.loads(json_text)
        except json.JSONDecodeError:
            raise Exception("Failed to parse resume JSON.")
    raise Exception("No valid JSON found in response.")


# Process a single resume
def process_resume(file_path: str, db: Session):
    # Extract text from the resume
    resume_text = extract_text(file_path)

    # Prepare message for parsing
    user_message = f"""Extract key details: Name, Email, Phone, Skills, Education, Experience.
    Resume Text: {resume_text}"""

    # Parse resume using OpenAI
    try:
        resume_dict = parse_resume(file_path, user_message)
    except Exception as e:
        raise Exception(f"Failed to parse resume: {e}")

    # Check for duplicates
    existing_resume = db.query(Resume).filter(
        Resume.email == resume_dict['email'],
        Resume.phone == resume_dict['phone']
    ).first()
    if existing_resume:
        existing_resume.is_duplicate = True
        db.commit()
    else:
        # Save Resume and associated details
        resume = Resume(
            name=resume_dict['name'],
            email=resume_dict['email'],
            phone=resume_dict['phone'],
            skills=", ".join(resume_dict['skills']),
            years=resume_dict.get('years', 0)
        )
        db.add(resume)
        db.commit()

        # Save Education
        for edu in resume_dict['education']:
            db.add(Education(
                resume_id=resume.id,
                degree=edu['degree'],
                field=edu['specialization'],
                institution=edu['institution'],
                year=edu['year']
            ))
        # Save Experience
        for exp in resume_dict['experience']:
            db.add(Experience(
                resume_id=resume.id,
                position=exp['position'],
                company=exp['company'],
                duration=exp['years']
            ))
        db.commit()


# Process multiple resumes from a folder
def process_resumes_from_folder(folder_path: str, db: Session):
    file_paths = [
        os.path.join(folder_path, f) for f in os.listdir(folder_path)
        if f.endswith(('.pdf', '.docx'))
    ]
    with ThreadPoolExecutor(max_workers=5) as executor:
        for file_path in file_paths:
            executor.submit(process_resume, file_path, db)
