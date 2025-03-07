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

    def get(self, request, uid) -> Response:
        """
        Get a report

        :param request:
        :param uid:
        :return: The report
        """
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
