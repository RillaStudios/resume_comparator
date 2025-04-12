from django.db import models

"""
Job posting model

This model represents a job posting that can be created, read, updated, and deleted.

Attributes:

    title: The title of the job posting.
    company_name: The name of the company.
    company_desc: A description of the company.
    summary: A summary of the job posting.
    responsibilities: The responsibilities of the job.
    skills_qual_required: The required skills and qualifications for the job.
    skills_qual_nice_to_have: The nice-to-have skills and qualifications for the job.
    address: The address of the job location.
    city: The city of the job location.
    prov_state: The province or state of the job location.
    country: The country of the job location.
    zip_postal_code: The postal code of the job location.
    remote: A boolean indicating if the job is remote.
    salary_min: The minimum salary for the job.
    salary_max: The maximum salary for the job.
    salary_currency_type: The currency type for the salary.
    salary_interval: The interval for the salary (e.g., hourly, monthly).
    employment_type: The type of employment (e.g., full-time, part-time).
    benefits: The benefits offered with the job.
    posting_date: The date the job was posted.
    closing_date: The date the job posting closes.
    contact_name: The name of the contact person for the job posting.
    contact_email: The email of the contact person for the job posting.

@Author: IFD
@Date: 2025-03-05
"""
class JobPosting(models.Model):
    title = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)
    company_desc = models.TextField(null=True, blank=True)
    summary = models.TextField(null=True, blank=True)
    responsibilities = models.TextField(null=True, blank=True)
    skills_qual_required = models.TextField(null=True, blank=True)
    skills_qual_nice_to_have = models.TextField()
    address = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    prov_state = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    zip_postal_code = models.CharField(max_length=20, null=True, blank=True)
    remote = models.BooleanField(default=False, null=True)
    salary_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    salary_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    salary_currency_type = models.CharField(max_length=10, null=True, blank=True)
    salary_interval = models.CharField(max_length=10, null=True, blank=True)
    employment_type = models.CharField(max_length=50, null=True, blank=True)
    benefits = models.TextField(null=True, blank=True)
    posting_date = models.DateTimeField(null=True, blank=True)
    closing_date = models.DateTimeField(null=True, blank=True)
    contact_name = models.CharField(max_length=255, null=True, blank=True)
    contact_email = models.EmailField(null=True, blank=True)


    """
    A method to convert a JobPosting object to a String representation.
    
    @Author: IFD
    @Date: 2025-04-09
    """
    def get_text(self):
        return (
            f"Job Posting ID: {self.id}\n"
            f"Title: {self.title}\n"
            f"Company Name: {self.company_name}\n"
            f"Company Description: {self.company_desc}\n"
            f"Job Summary: {self.summary}\n"
            f"Job Responsibilities: {self.responsibilities}\n"
            f"Job Requirements (Must Have): {self.skills_qual_required}\n"
            f"Job Requirements (Nice to Have): {self.skills_qual_nice_to_have}\n"
            f"Location: {self.address}, {self.city}, {self.prov_state}, {self.country}, {self.zip_postal_code}\n"
            f"Remote: {self.remote}\n"
            f"Salary Min: {self.salary_min}\n"
            f"Salary Max: {self.salary_max}\n"
            f"Salary Currency Type: {self.salary_currency_type}\n"
            f"Salary Interval: {self.salary_interval}\n"
            f"Employment Type: {self.employment_type}\n"
            f"Benefits: {self.benefits}\n"
            f"Posted Date: {self.posting_date}\n"
            f"Contact Name: {self.contact_name}\n"
            f"Contact Email: {self.contact_email}"
        )

    """
    A string representation of the job posting.

    @Author: IFD
    @Date: 2025-03-05
    """
    def __str__(self):
        return str(self.id)