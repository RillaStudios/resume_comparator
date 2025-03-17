import json
import os

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
        base_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base_dir, 'data', 'job_postings.json')
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

        for job_posting in job_postings:
            if job_posting['id'] == job_posting_id:
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

        return self

    def to_json(self):
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

    def get_by_id(self, job_posting_id):
        return self.create_from_json(job_posting_id)

    def __str__(self):
        return json.dumps(self.to_json(), indent=4)