import json
import logging
from django.http import JsonResponse
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from rest_framework.decorators import api_view
from .utils import send_success_email
from api.models.compare_report_model import CompareReport

logger = logging.getLogger(__name__)

@api_view(['POST'])
def send_candidate_email(request):
    try:
        data = request.data

        applicant_name = data.get('applicant_name')
        applicant_email = data.get('applicant_email')
        job_id = data.get('job_id')

        # Check for missing fields
        if not (applicant_name and applicant_email and job_id):
            return JsonResponse({'error': _('Missing required fields.')}, status=400)

        # Validate email format
        try:
            validate_email(applicant_email)
        except ValidationError:
            return JsonResponse({'error': _('Invalid email format.')}, status=400)

        # Check if job exists
        try:
            job = CompareReport.objects.get(id=job_id)
        except CompareReport.DoesNotExist:
            return JsonResponse({'error': _('Invalid job ID.')}, status=404)

        # Send success email
        send_success_email(applicant_email, applicant_name, job_id)

        return JsonResponse({
            'message': _('Email sent successfully.'),
            'title': job.title  
        })

    except Exception as e:
        logger.error(f"🔥 ERROR: {e}")
        return JsonResponse({'error': str(e)}, status=500)
   