from django.db import models
# Create your models here.

class Resume(models.Model):
    file = models.FileField(upload_to='resumes/')
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
