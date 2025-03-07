from django.db import models

"""
Job Posting model

This model represents a job posting that can be read.

Attributes:

    title (CharField): The title of the job posting.
    description (TextField): The description of the job posting.
    created_at (DateTimeField): The date and time the job posting was created.
    company (CharField): The company that created the job posting.
    location (CharField): The location of the job posting.
    salary (CharField): The salary of the job posting.
    remote (BooleanField): Whether the job posting is remote.
    
@Author: IFD
@Date: 2025-03-05
"""

class JobPosting(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    company = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    salary = models.CharField(max_length=100)
    remote = models.BooleanField(default=False)

    """
    A string representation of the job posting.
    
    Returns:
        str: The title of the job posting.
    """
    def __str__(self):
        return self.title