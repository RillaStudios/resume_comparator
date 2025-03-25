from django.core.files.storage import default_storage
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from api.models.compare_report_model import CompareReport
from api.serializers.compare_report_serializer import CompareReportSerializer
from comparator.compare import Compare

"""
A view for individual reports

This view allows for the retrieval, and deletion of individual reports.

@Author: IFD
@Date: 2025-03-05
"""
class CompareReportView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request) -> Response:
        """
        Create a new report

        :param request:
        :return: A new report

        Author: IFD
        Date: 2025-03-05
        """

        # Check if resume file(s) are uploaded
        if 'resume' not in request.FILES:
            return Response({"error": "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST)

        # Check if job ID is provided
        if not 'jobId' in request.data:
            return Response({"error": "Job ID is missing"}, status=status.HTTP_400_BAD_REQUEST)

        job_id = request.data.get('jobId')
        reports = []

        for resume_file in request.FILES.getlist('resume'):

            # Check if file size is less than 50MB
            if resume_file.size > 50 * 1024 * 1024:
                return Response({"error": "File size too large. Max size is 50MB"},
                                status=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE)

            #Convert word document to pdf (if necessary)
            #if resume_file.name.endswith('.docx') or resume_file.name.endswith('.doc'):
                # Due to Pythons rather absurdity of not being able to convert a simple docx to pdf
                # We will use pandoc (possibly) to convert the docx to pdf, this will be in a later version.
                # For now, we will just throw an error
                #
                # Also note that we need it to be converted to PDF as pdfplumber only works with PDFs
                # and all the docx reading packages perform rather poorly with the various formats of docx
                #
                # print('is a docx')
                # resume_file = DocxConverter(resume_file).convert_docx_to_pdf()
                #return Response({"error": "Only PDFs are supported at the moment"},
                  #              status=status.HTTP_400_BAD_REQUEST)

            # Define file path relative to MEDIA_ROOT

            file_path = f"resumes/{resume_file.name}"

            # Save the file using Django's default storage
            saved_path = default_storage.save(file_path, resume_file)

            # Create the report, passing the relative file path
            report = Compare(job_id, saved_path).compare_and_gen_report()

            #Save the report to the database
            report.save()
            reports.append(report)

        # Return the report(s)
        if len(reports) == 1:
            serializer = CompareReportSerializer(reports[0])
        else:
            serializer = CompareReportSerializer(reports, many=True)

        return Response(serializer.data)

    def get(self, request, uid: int = None) -> Response:
        """
        Get all reports

        :param uid:
        :param request:
        :return: A list of all reports
        """
        if uid is None:
            items = CompareReport.objects.all()
            serializer = CompareReportSerializer(items, many=True)
            return Response(serializer.data)
        else:
            item = CompareReport.objects.get(pk=uid)
            serializer = CompareReportSerializer(item)
            return Response(serializer.data)

    def delete(self, request, uid) -> Response:
        """
        Delete a report

        :param request:
        :param uid:
        :return: 204
        """
        item = CompareReport.objects.get(pk=uid)
        item.delete()
        return Response(status=204)
