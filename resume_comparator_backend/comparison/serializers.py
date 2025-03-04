from rest_framework import serializers
from .models import Resume

class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = ['id', 'name', 'email', 'phone', 'summary', 'experience', 'education', 'skills', 'projects', 'certifications', 'languages', 'interests', 'references']