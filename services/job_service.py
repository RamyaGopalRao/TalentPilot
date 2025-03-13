from models import Resume, JobListing


class JobService:
    @staticmethod
    def match_resumes_to_jobs():
        """
        Matches resumes to job listings based on required skills.

        Returns:
            dict: A dictionary containing job IDs and their matched resumes.
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
