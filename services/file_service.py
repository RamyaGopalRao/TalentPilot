import os

from models import Resume, Education, Experience, Skill, JobListing

class FileService:
    @staticmethod
    def handle_uploaded_file(f):
        """
        Handles uploaded files by saving them to the 'media/uploads' directory.
        """
        upload_dir = os.path.join('media', 'uploads')
        upload_dir = os.path.join(os.path.dirname(os.getcwd()), 'media', 'uploads')

        print("Handling upload...")
        os.makedirs(upload_dir, exist_ok=True)
        file_path = os.path.join(upload_dir, f.name)

        with open(file_path, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
        print(f"File saved at: {file_path}")
        return file_path

    @staticmethod
    def mark_duplicates():
        """
        Identifies and marks duplicate resumes based on email and phone number.
        """
        duplicates = Resume.objects.values('email', 'phone').annotate(count=Count('id')).filter(count__gt=1)
        for duplicate in duplicates:
            duplicate_resumes = Resume.objects.filter(email=duplicate['email'], phone=duplicate['phone'])
            for resume in duplicate_resumes[1:]:
                resume.is_duplicate = True
                resume.save()

    @staticmethod
    def match_resumes_to_jobs():
        """
        Matches resumes to job listings based on required skills.
        """
        # Dictionary to store matching results
        matching_results = {}

        # Fetch all job listings
        job_listings = JobListing.objects.all()

        for job in job_listings:
            # Fetch required skills for the job
            job_skills = job.required_skills.values_list('name', flat=True)

            # Fetch all resumes
            resumes = Resume.objects.all()

            # List to store matching resumes for the current job
            matched_resumes = []

            for resume in resumes:
                # Convert resume.skills (TextField) into a list of skills
                resume_skills = resume.skills.split(',')

                # Check if any skill in the resume matches the required skills
                if any(skill.strip() in job_skills for skill in resume_skills):
                    matched_resumes.append({
                        'resume_id': resume.id,
                        'name': resume.name,
                        'email': resume.email,
                        'phone': resume.phone
                    })

            # Add job ID and matched resumes to results
            matching_results[job.id] = matched_resumes

        return matching_results
