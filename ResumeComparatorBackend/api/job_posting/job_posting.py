import json
import os
from DjangoApp import settings

"""
A class to represent a job posting.

Author: IFD
Date: 2025-03-17
"""
class JobPosting:

    def __init__(self, uid: int = 0, title: str = "", company_name: str = "", company_desc: str = "", job_summary: str = "",
                 job_responsibilities: list[str] = None, job_requirements_must_have: list[str] = None, job_requirements_nice_to_have: list[str] = None,
                 job_loc_city: str = "", job_loc_province: str = "", job_loc_country: str = "", job_loc_remote: bool = False, job_salary_min: float = 0.0,
                 job_salary_max: float = 0.0, job_salary_currency: str = "", job_salary_interval: str = "", job_employment_type: str = "", benefits: list[str] = None,
                 job_posting_date: str = "", job_closing_date: str = "", job_contact_email: str = ""):

        self.job_posting_id = uid
        self.title = title
        self.company_name = company_name
        self.company_desc = company_desc
        self.job_summary = job_summary
        self.job_responsibilities = job_responsibilities
        self.job_requirements_must_have = job_requirements_must_have
        self.job_requirements_nice_to_have = job_requirements_nice_to_have
        self.job_loc_city = job_loc_city
        self.job_loc_province = job_loc_province
        self.job_loc_country = job_loc_country
        self.job_loc_remote = job_loc_remote
        self.job_salary_min = job_salary_min
        self.job_salary_max = job_salary_max
        self.job_salary_currency = job_salary_currency
        self.job_salary_interval = job_salary_interval
        self.job_employment_type = job_employment_type
        self.benefits = benefits
        self.job_posting_date = job_posting_date
        self.job_closing_date = job_closing_date
        self.job_contact_email = job_contact_email

    def create_from_json(self, job_posting_id=None):
        """
        A method to create a JobPosting object from a JSON file.

        :param job_posting_id: The ID of the job posting to retrieve. If None, all job postings are returned.
        :return: A list of JobPosting objects or a single JobPosting object.

        Author: IFD
        Date: 2025-03-17
        """
        file_path = os.path.join(settings.BASE_DIR, 'api', 'job_posting', 'data', 'job_postings.json')

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"No such file or directory: '{file_path}'")

        with open(file_path, 'r') as file:
            job_postings = json.load(file)['job-postings']

        if job_posting_id is None:
            return [
                JobPosting(
                    uid=job_posting['id'],
                    title=job_posting['title'],
                    company_name=job_posting['company']['name'],
                    company_desc=job_posting['company']['description'],
                    job_summary=job_posting['job_description']['summary'],
                    job_responsibilities=job_posting['job_description']['responsibilities'],
                    job_requirements_must_have=job_posting['job_description']['requirements']['must_have'],
                    job_requirements_nice_to_have=job_posting['job_description']['requirements']['nice_to_have'],
                    job_loc_city=job_posting['location']['city'],
                    job_loc_province=job_posting['location']['province'],
                    job_loc_country=job_posting['location']['country'],
                    job_loc_remote=job_posting['location']['remote'],
                    job_salary_min=job_posting['salary']['min'],
                    job_salary_max=job_posting['salary']['max'],
                    job_salary_currency=job_posting['salary']['currency'],
                    job_salary_interval=job_posting['salary']['period'],
                    job_employment_type=job_posting['employment_type'],
                    benefits=job_posting['benefits'],
                    job_posting_date=job_posting['posted_date'],
                    job_closing_date=job_posting['application_deadline'],
                    job_contact_email=job_posting['contact_email']
                ).to_json()
                for job_posting in job_postings
            ]

        job_posting_id = int(job_posting_id)
        found = False

        for job_posting in job_postings:
            if job_posting['id'] == job_posting_id:
                found = True
                self.job_posting_id = job_posting['id']
                self.title = job_posting['title']
                self.company_name = job_posting['company']['name']
                self.company_desc = job_posting['company']['description']
                self.job_summary = job_posting['job_description']['summary']
                self.job_responsibilities = job_posting['job_description']['responsibilities']
                self.job_requirements_must_have = job_posting['job_description']['requirements']['must_have']
                self.job_requirements_nice_to_have = job_posting['job_description']['requirements']['nice_to_have']
                self.job_loc_city = job_posting['location']['city']
                self.job_loc_province = job_posting['location']['province']
                self.job_loc_country = job_posting['location']['country']
                self.job_loc_remote = job_posting['location']['remote']
                self.job_salary_min = job_posting['salary']['min']
                self.job_salary_max = job_posting['salary']['max']
                self.job_salary_currency = job_posting['salary']['currency']
                self.job_salary_interval = job_posting['salary']['period']
                self.job_employment_type = job_posting['employment_type']
                self.benefits = job_posting['benefits']
                self.job_posting_date = job_posting['posted_date']
                self.job_closing_date = job_posting['application_deadline']
                self.job_contact_email = job_posting['contact_email']
                break

        if not found:
            # Debug info to help understand what's happening
            available_ids = [jp['id'] for jp in job_postings]
            raise ValueError(f"No job posting found with ID: {job_posting_id}. Available IDs: {available_ids}")

        return self

    def to_json(self):
        """
        A method to convert a JobPosting object to a JSON object.

        :return: A JSON object representing the JobPosting object.

        Author: IFD
        Date: 2025-03-17
        """
        return {
            "id": self.job_posting_id,
            "title": self.title,
            "company": {
                "name": self.company_name,
                "description": self.company_desc
            },
            "job_description": {
                "summary": self.job_summary,
                "responsibilities": self.job_responsibilities,
                "requirements": {
                    "must_have": self.job_requirements_must_have,
                    "nice_to_have": self.job_requirements_nice_to_have
                }
            },
            "location": {
                "city": self.job_loc_city,
                "province": self.job_loc_province,
                "country": self.job_loc_country,
                "remote": self.job_loc_remote
            },
            "salary": {
                "min": self.job_salary_min,
                "max": self.job_salary_max,
                "currency": self.job_salary_currency,
                "period": self.job_salary_interval
            },
            "employment_type": self.job_employment_type,
            "benefits": self.benefits,
            "posted_date": self.job_posting_date,
            "application_deadline": self.job_closing_date,
            "contact_email": self.job_contact_email
        }

    def get_text(self):
        return (
            f"Job Posting ID: {self.job_posting_id},\n"
            f"Title: {self.title},\n"
            f"Company Name: {self.company_name},\n"
            f"Job Summary: {self.job_summary},\n"
            f"Job Responsibilities: {self.job_responsibilities},\n"
            f"Job Requirements (Must Have): {self.job_requirements_must_have},\n"
            f"Job Requirements (Nice to Have): {self.job_requirements_nice_to_have},\n"
            f"Location: {self.job_loc_city}, {self.job_loc_province}, {self.job_loc_country},\n"
            f"Remote: {self.job_loc_remote},\n"
            f"Salary Min: {self.job_salary_min} {self.job_salary_currency},\n"
            f"Salary Max: {self.job_salary_max} {self.job_salary_currency},\n"
            f"Salary Interval: {self.job_salary_interval},\n"
            f"Employment Type: {self.job_employment_type},\n"
            f"Benefits: {self.benefits},\n"
            f"Posted Date: {self.job_posting_date},\n"
            f"Application Deadline: {self.job_closing_date},\n"
            f"Contact Email: {self.job_contact_email}\n"
        )
