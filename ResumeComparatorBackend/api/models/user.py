from django.contrib.auth.models import AbstractUser
from django.db import models


"""
User Model

This model is used to register a user with a role and hashed password.

Author: Michael Tamatey
Date: 2025-03-05
"""
class User(AbstractUser):
    RECRUITER = 'RECRUITER'
    DIRECTOR = 'DIRECTOR'
    ROLE_CHOICES = [
        (RECRUITER, 'Recruiter'),
        (DIRECTOR, 'Director'),
    ]

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    address = models.CharField(max_length=255)
    role = models.CharField(
        max_length=9,
        choices=ROLE_CHOICES,
        default=RECRUITER,
    )

    def __str__(self):
        return f"{self.username} ({self.role})"