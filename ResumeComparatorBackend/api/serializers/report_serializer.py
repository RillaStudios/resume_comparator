from rest_framework import serializers
from api.models.report_model import Report

"""
Report serializer

This serializer is used to convert the report model to JSON format.

Author: IFD
Date: 2025-03-05
"""
class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = '__all__'