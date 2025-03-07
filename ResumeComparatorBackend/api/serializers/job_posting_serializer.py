from rest_framework import serializers
from api.models.report_model import Report

"""
Job Posting serializer

This serializer is used to convert the job posting model to JSON format.

Author: IFD
Date: 2025-03-05
"""
class JobPostingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = '__all__'