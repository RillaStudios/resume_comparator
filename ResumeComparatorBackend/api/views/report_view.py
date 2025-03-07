from rest_framework.views import APIView
from rest_framework.response import Response
from api.models.report_model import Report
from api.serializers.report_serializer import ReportSerializer

"""
A view for all reports

This view allows for the retrieval and deletion of all reports.

@Author: IFD
@Date: 2025-03-05
"""
class ReportsView(APIView):

    def get(self, request) -> Response:
        """
        Get all reports

        :param request:
        :return: A list of all reports
        """
        items = Report.objects.all()
        serializer = ReportSerializer(items, many=True)
        return Response(serializer.data)

    def delete(self, request) -> Response:
        """
        Delete all reports

        :param request:
        :return: A 204 response
        """

        items = Report.objects.all()
        items.delete()
        return Response(status=204)