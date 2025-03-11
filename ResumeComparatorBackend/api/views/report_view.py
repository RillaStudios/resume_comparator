from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models.report_model import Report
from api.serializers.report_serializer import ReportSerializer

"""
A view for individual reports

This view allows for the retrieval, and deletion of individual reports.

@Author: IFD
@Date: 2025-03-05
"""
class ReportView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request) -> Response:
        """
        Create a report

        :param request:
        :return: The created report
        """
        file_serializer = ReportSerializer(data=request.data)

        if file_serializer.is_valid():

            file_serializer.save()

            return Response({"message": "File uploaded successfully!", "data": file_serializer.data}, status=201)
        else:
            return Response(file_serializer.errors, status=400)

    def get(self, request, uid: int = None) -> Response:
        """
        Get all reports

        :param uid:
        :param request:
        :return: A list of all reports
        """
        if uid is None:
            items = Report.objects.all()
            serializer = ReportSerializer(items, many=True)
            return Response(serializer.data)
        else:
            item = Report.objects.get(pk=uid)
            serializer = ReportSerializer(item)
            return Response(serializer.data)

    def delete(self, request, uid) -> Response:
        """
        Delete a report

        :param request:
        :param uid:
        :return: 204
        """
        item = Report.objects.get(pk=uid)
        item.delete()
        return Response(status=204)
