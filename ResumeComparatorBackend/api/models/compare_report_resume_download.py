import datetime
import os
import zipfile

from django.http import FileResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models.compare_report_model import CompareReport

"""
A view for downloading resumes from reports

This view allows for the downloading of resumes from reports.

@Author: IFD
@Date: 2025-03-25
"""
class CompareReportResumeDownload(APIView):

    """
    Download a resume from a report

    This method allows for the downloading of a resume from a report.

    :param request: The request object.
    :return: The response object.

    @Author: IFD
    @Date: 2025-03-25
    """
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

                return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=os.path.basename(file_path))

            except CompareReport.DoesNotExist:
                return Response({"error": "Report not found"}, status=status.HTTP_404_NOT_FOUND)

        # Download multiple reports as a ZIP
        zip_filename = f"resumes_{datetime.date.today()}.zip"
        zip_filepath = os.path.join("/tmp", zip_filename)

        with zipfile.ZipFile(zip_filepath, 'w') as zip_file:
            for report_id in report_ids:
                try:
                    report = CompareReport.objects.get(pk=report_id)
                    file_path = report.resume.path
                    zip_file.write(file_path, os.path.basename(file_path))
                except CompareReport.DoesNotExist:
                    continue

        # Return the ZIP file
        response = FileResponse(open(zip_filepath, 'rb'), as_attachment=True, filename=zip_filename)
        os.remove(zip_filepath)  # Delete temp file after sending

        return response