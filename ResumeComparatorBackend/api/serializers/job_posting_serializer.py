from rest_framework import serializers
from api.models.job_posting_model import JobPosting

"""
Job posting serializer

This serializer is used to convert the report model to JSON format.

Author: IFD
Date: 2025-03-05
"""
class JobPostingSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobPosting
        fields = '__all__'