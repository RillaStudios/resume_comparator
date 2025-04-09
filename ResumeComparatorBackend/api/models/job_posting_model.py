from django.db import models

"""
Job posting model

This model represents a job posting that can be created, read, updated, and deleted.

Attributes:

    title: The title of the job posting.
    company_name: The name of the company.
    company_desc: A description of the company.
    job_summary: A summary of the job posting.
    job_responsibilities: The responsibilities of the job.
    job_requirements_must_have: The must-have requirements for the job.
    job_requirements_nice_to_have: The nice-to-have requirements for the job.
    job_loc_city: The city where the job is located.
    job_loc_province: The province where the job is located.
    job_loc_country: The country where the job is located.
    job_loc_remote: A boolean indicating if the job is remote.
    job_salary_min: The minimum salary for the job.
    job_salary_max: The maximum salary for the job.
    job_salary_currency: The currency of the salary.
    job_salary_interval: The interval of the salary (e.g., hourly, monthly).
    job_employment_type: The type of employment (e.g., full-time, part-time).
    job_benefits: The benefits of the job.
    job_posting_date: The date the job was posted.
    job_closing_date: The date the job posting closes.
    job_contact_email: The email address for job applications.

@Author: IFD
@Date: 2025-03-05
"""
class JobPosting(models.Model):
    title = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)
    company_desc = models.TextField(null=True, blank=True)
    job_summary = models.TextField(null=True, blank=True)
    job_responsibilities = models.TextField(null=True, blank=True)
    job_requirements_must_have = models.TextField(null=True, blank=True)
    job_requirements_nice_to_have = models.TextField()
    job_loc_city = models.CharField(max_length=255, null=True, blank=True)
    job_loc_province = models.CharField(max_length=255, null=True, blank=True)
    job_loc_country = models.CharField(max_length=255, null=True, blank=True)
    job_loc_remote = models.BooleanField(default=False, null=True)
    job_salary_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    job_salary_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    job_salary_currency = models.CharField(max_length=10, null=True, blank=True)
    job_salary_interval = models.CharField(max_length=10, null=True, blank=True)
    job_employment_type = models.CharField(max_length=50, null=True, blank=True)
    job_benefits = models.TextField(null=True, blank=True)
    job_posting_date = models.DateTimeField(null=True, blank=True)
    job_closing_date = models.DateTimeField(null=True, blank=True)
    job_contact_email = models.EmailField(null=True, blank=True)


    """
    A method to convert a JobPosting object to a String representation.
    
    @Author: IFD
    @Date: 2025-04-09
    """
    def get_text(self):
        return (
            f"Job Posting ID: {self.id},\n"
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
            f"Benefits: {self.job_benefits},\n"
            f"Posted Date: {self.job_posting_date},\n"
            f"Application Deadline: {self.job_closing_date},\n"
            f"Contact Email: {self.job_contact_email}\n"
        )

    """
    A string representation of the job posting.

    @Author: IFD
    @Date: 2025-03-05
    """
    def __str__(self):
        return str(self.id)