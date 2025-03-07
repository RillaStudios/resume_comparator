from rest_framework.views import APIView
from rest_framework.response import Response
from api.models.job_posting_model import JobPosting
from api.serializers.job_posting_serializer import JobPostingSerializer

"""
A view for all job postings
This view allows for the retrieval of all job postings.

@Author: IFD
@Date: 2025-03-05
"""
class JobPostingView(APIView):

    def get(self, request) -> Response:
        """
        Get all job postings

        :param request:
        :return: Job postings
        """
        items = JobPosting.objects.all()
        serializer = JobPostingSerializer(items, many=True)
        return Response(serializer.data)