import datetime
import os
import zipfile
from io import BytesIO
from django.http import FileResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from api.models.compare_report_model import CompareReport

class CompareReportResumeDownload(APIView):

    def get(self, request):
        report_ids = request.query_params.get('report_ids', '')

        if not report_ids:
            return Response({"error": "No report IDs provided"}, status=status.HTTP_400_BAD_REQUEST)

        report_ids = [rid.strip() for rid in report_ids.split(",") if rid.strip().isdigit()]

        if len(report_ids) == 1:
            report_id = report_ids[0]
            try:
                report = CompareReport.objects.get(pk=report_id)
                file_path = report.resume.path

                file = open(file_path, 'rb')
                return FileResponse(file, as_attachment=True, filename=os.path.basename(file_path))

            except CompareReport.DoesNotExist:
                return Response({"error": "Report not found"}, status=status.HTTP_404_NOT_FOUND)

        # Create an in-memory ZIP file
        zip_buffer = BytesIO()

        # Create the ZIP file with the reports
        with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
            for report_id in report_ids:
                try:
                    report = CompareReport.objects.get(pk=report_id)
                    file_path = report.resume.path
                    zip_file.write(file_path, os.path.basename(file_path))
                except CompareReport.DoesNotExist:
                    continue

        # Reset buffer position to beginning
        zip_buffer.seek(0)

        # Create the response with the in-memory ZIP
        zip_filename = f"resumes_{datetime.date.today()}.zip"
        return FileResponse(
            zip_buffer,
            as_attachment=True,
            filename=zip_filename
        )