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
    
    def get(self, request, uid=None):
        if uid is not None:
            """
            Get all job postings

            :param uid:
            :param request:
            :return: Job postings
            """

            # Get a single job posting by primary key (uid)
            job_posting = JobPosting.objects.get(pk=uid)
            serializer = JobPostingSerializer(job_posting)
            return Response(serializer.data)
        else:
            """
            Get all job postings

            :param uid:
            :param request:
            :return: Job postings
            """

            # Get all job postings
            job_postings = JobPosting.objects.all()
            serializer = JobPostingSerializer(job_postings, many=True)
            return Response(serializer.data)


    def post(self, request):
        """
        Create a new job posting

        :param request:
        :return: Job posting

        @Author: IFD
        @Date: 2025-04-09
        """
        serializer = JobPostingSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)

    def patch(self, request):
        """
        Update a job posting

        :param request:
        :return: Job posting

        @Author: IFD
        @Date: 2025-04-09
        """
        uid = request.data.get('id')

        if not uid:
            return Response({"error": "Job posting ID is required."}, status=400)

        try:
            job_posting = JobPosting.objects.get(pk=uid)

        except JobPosting.DoesNotExist:
            return Response({"error": "Job posting not found."}, status=404)

        serializer = JobPostingSerializer(job_posting, data=request.data, partial=True)

        if serializer.is_valid():

            serializer.save()

            return Response(serializer.data, status=200)

        return Response(serializer.errors, status=400)

    def delete(self, request):
        """
        Delete a job posting

        :param request:
        :return: Job posting

        @Author: IFD
        @Date: 2025-04-09
        """
        uid = request.data.get('id')

        if not uid:
            return Response({"error": "Job posting ID is required."}, status=400)

        try:
            job_posting = JobPosting.objects.get(pk=uid)
            job_posting.delete()

            return Response({"message": "Job posting deleted successfully."}, status=204)

        except JobPosting.DoesNotExist:
            return Response({"error": "Job posting not found."}, status=404)