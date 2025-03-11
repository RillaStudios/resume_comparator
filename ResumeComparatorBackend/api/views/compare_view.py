from django.core.files.storage import default_storage
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from api.serializers.report_serializer import ReportSerializer
from api.models.report_model import Report
from comparator.compare import Compare

"""
A view to compare a resume to a job posting.
It will take a resume file and a job ID, compare the 
resume to the job posting, and return a report. It contains
a single post method that handles the comparison. Errors are
returned if the file is not uploaded, the file is not a .pdf or .docx,
the file size is too large, or the job ID is missing.

Attributes:
    APIView: A Django REST framework class for handling API requests.

@Author: IFD
@Date: 2025-03-05
"""
class CompareView(APIView):

    def post(self, request) -> Response:

        # Check if resume file is uploaded
        if 'resume' not in request.FILES:
            return Response({"error": "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST)

        # Check if file is .pdf or .docx
        if not request.FILES['resume'].name.endswith('.pdf') or not request.FILES['resume'].name.endswith('.docx'):
            return Response({"error": "File must be .docx or pdf"}, status=status.HTTP_409_CONFLICT)

        # Check if file size is less than 50MB
        if request.FILES['resume'].size > 50 * 1024 * 1024:
            return Response({"error": "File size too large. Max size is 50MB"}, status=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE)

        # Get resume file and job ID
        resume_file = request.FILES['resume']
        job_id = request.data.get('jobId')

        # Check if job ID is provided
        if not job_id:
            return Response({"error": "Job ID is missing"}, status=status.HTTP_400_BAD_REQUEST)

        # Define file path relative to MEDIA_ROOT
        file_path = f"resumes/{resume_file.name}"

        # Save file using Django's default storage
        saved_path = default_storage.save(file_path, resume_file)

        #Create a new comparison report
        report = Compare(job_id, saved_path).compare_and_gen_report()

        #Save the report to the database
        report.save()

        #Return the report
        items = Report.objects.get(pk=report.id)
        serializer = ReportSerializer(items)
        return Response(serializer.data)