# TalentPilot

**TalentPilot** is an AI-driven resume parsing and job shortlisting application built with **FastAPI** and **OpenAI**. It simplifies the recruitment process by allowing users to upload resumes (single or multiple), extracting essential information using AI, and matching candidates to job listings based on skills and experience.

---

## Features
1. **Resume Upload**:
   - Upload single resumes or bulk resumes (folder).
   - Supports `.pdf` and `.docx` formats.
2. **Multiprocessing**:
   - Processes multiple resumes in parallel for bulk uploads.
3. **Text Extraction**:
   - Utilizes `PyPDF2` for PDFs and `python-docx` for Word documents.
4. **AI Parsing**:
   - Sends extracted text to OpenAI's API for structured parsing of:
     - Name, Email, Phone
     - Skills
     - Education (degree, specialization, institution, year)
     - Experience (position, company, duration)
5. **Database Operations**:
   - Stores parsed resume data in the database, ensuring duplicate detection.
6. **Job Matching**:
   - Matches job listings to resumes based on required skillsets.
7. **Skill and Job Management**:
   - Add and manage skillsets, job listings, and experiences.

---

## Architecture Overview

### Workflow
1. **Upload**:
   - User uploads a single resume or a folder of resumes.
   - Files are saved to the `uploads` directory for processing.

2. **Resume Processing**:
   - For a single file, text is extracted and sent to OpenAI's API.
   - For multiple files, multiprocessing is employed for concurrent processing.

3. **AI Integration**:
   - OpenAI extracts structured resume details and sends them back in JSON format.

4. **Database Operations**:
   - Data is saved in models like `Resume`, `Education`, `Experience`, and `Skill`.
   - Duplicate resumes are flagged based on email and phone.

5. **Job Matching**:
   - Skillsets and experiences from job listings are compared against resumes.
   - Matching resumes are retrieved for each job listing.

---

### Architecture Diagram

```plaintext
+----------------------------+        +----------------------------+        +-----------------------------+
|        User Uploads        | ---->  |      File Handler          | ---->  |       Resume Processor       |
| (Single/Multiple Resumes)  |        | (Save Files, Multiprocessing)|      |  (Extract Text, AI Parsing)  |
+----------------------------+        +----------------------------+        +-----------------------------+
                                                                                 |
                                                                                 v
+----------------------------+        +----------------------------+        +-----------------------------+
|    Database Operations     | <---- |      Parsed Resume Data     | ----> |  Job Matching Engine         |
| (Save, Flag Duplicates)    |        |   (OpenAI Processed JSON)   |        | (Skill & Experience Matching)|
+----------------------------+        +----------------------------+        +-----------------------------+
