from rest_framework import serializers
from api.models.compare_report_model import CompareReport

"""
Report serializer

This serializer is used to convert the report model to JSON format.

Author: IFD
Date: 2025-03-05
"""
class CompareReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompareReport
        fields = '__all__'