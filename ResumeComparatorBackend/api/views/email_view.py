import json
from django.http import JsonResponse
from rest_framework.decorators import api_view
from .utils import send_success_email
from api.models.compare_report_model import CompareReport

@api_view(['POST', 'GET'])
def send_candidate_email(request):
    try:
        data = request.data

        applicant_name = data.get('applicant_name')
        applicant_email = data.get('applicant_email')
        job_id = data.get('job_id')

        if not (applicant_name and applicant_email and job_id):
            return JsonResponse({'error': 'Missing required fields.'}, status=400)

        try:
            job = CompareReport.objects.get(id=job_id)
        except CompareReport.DoesNotExist:
            return JsonResponse({'error': 'Invalid job ID.'}, status=404)

        send_success_email(applicant_email, applicant_name, job_id)
        return JsonResponse({'message': 'Email sent successfully.'})

    except Exception as e:
        print("🔥 ERROR:", e)
        return JsonResponse({'error': str(e)}, status=500)