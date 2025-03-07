from rest_framework.views import APIView
from rest_framework.response import Response
from api.serializers.report_serializer import ReportSerializer
from api.models.report_model import Report
from comparator.compare import Compare

"""


@Author: IFD
@Date: 2025-03-05
"""
class CompareView(APIView):

    def post(self, request) -> Response:
        #Retrieve the job posting id and resume from the request data
        job_posting_id = request.data.get('job_posting_id')
        resume = request.data.get('resume')

        #Create a new report
        report = Report()

        #Create a new comparison
        comparison = Compare(job_posting_id, resume)

        #Compare the resume to the job posting
        comparison.compare()

        #Compare the resume to the job posting
        report.passed = comparison.passed
        report.score = comparison.score

        #Save the report
        report.save()

        #Return the report
        items = Report.objects.get(pk=report.id)
        serializer = ReportSerializer(items)
        return Response(serializer.data)