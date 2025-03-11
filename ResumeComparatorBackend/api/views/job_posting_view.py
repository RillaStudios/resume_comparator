from rest_framework.views import APIView
from rest_framework.response import Response

from api.job_posting.job_posting import JobPosting

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
            job_posting = JobPosting().create_from_json(uid)

            return Response(job_posting.to_json())
        else:
            """
            Get all job postings

            :param uid:
            :param request:
            :return: Job postings
            """
            job_posting = JobPosting().create_from_json(None)

            return Response(job_posting)