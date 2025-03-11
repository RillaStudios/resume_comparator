from django.db import models

"""
Report model

This model represents a report that can be created, read, and deleted.

Attributes:

    applicant_name (CharField): The name of the report.
    description (TextField): The description of the report.
    created_at (DateTimeField): The date and time the report was created.
   
@Author: IFD
@Date: 2025-03-05
"""
class Report(models.Model):
    applicant_resume = models.FileField(upload_to='resumes/')
    created_at = models.DateTimeField(auto_now_add=True)

    """
    A string representation of the report.
    
    Returns:
        str: The name and id of the report.
        
    @Author: IFD
    @Date: 2025-03-05
    """
    def __str__(self):
        return str(self.id)