from django.core.mail import EmailMessage
import logging
from django.http import JsonResponse
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from rest_framework.decorators import api_view
from .utils import send_success_email
from api.models.compare_report_model import CompareReport

"""
Email view for sending candidate emails and emailing reports to 

@Author: Michael Tamatey
@Date: 2025-04-14
"""
logger = logging.getLogger(__name__)
@api_view(['POST'])
def send_candidate_email(request):
    try:
        data = request.data

        applicant_name = data.get('applicant_name')
        applicant_email = data.get('applicant_email')
       
        
        # Check for missing fields
        if not (applicant_name and applicant_email):
            return JsonResponse({'error': _('Missing required fields.')}, status=400)

        # Validate email format
        try:
            validate_email(applicant_email)
        except ValidationError:
            return JsonResponse({'error': _('Invalid email format.')}, status=400)
        
        
        # Send success email
        send_success_email(applicant_email, applicant_name)

        return JsonResponse({
            'message': _('Email sent successfully.')
        })

    except Exception as e:
        logger.error(f"🔥 ERROR: {e}")
        return JsonResponse({'error': str(e)}, status=500)
 

"""
    Send email with selected reports to the specified email address.
    This function retrieves the selected reports based on the provided IDs,

    compiles their details into a formatted string, and sends it as an email.
    It also attaches the resumes of the selected reports to the email.
        :return: JsonResponse indicating success or failure of the email sending process.
        :rtype: JsonResponse

        @Author: Michael Tamatey  
        @Date: 2025-04-14
        """

@api_view(['POST'])
def send_selected_reports(request):
    # Extracting selected report IDs and recipient email from the JSON request
    selected_report_ids = request.data.get('report_ids', [])
    recipient_email = request.data.get('email')

    if not selected_report_ids or not recipient_email:
        return JsonResponse({'error': 'No reports selected or missing email'}, status=400)

    reports = CompareReport.objects.filter(id__in=selected_report_ids)
    if not reports:
        return JsonResponse({'error': 'No reports found with provided IDs'}, status=404)

    report_details = ""
    for report in reports:
        report_details += f"Report for {report.applicant_name} - Job ID: {report.job_id}\n"
        report_details += f"Score: {report.score}\n"
        report_details += f"Created At: {report.created_at.strftime('%Y-%m-%d %H:%M:%S')}\n"
        report_details += f"Passing: {report.passing}\n"
        report_details += f"Failing: {report.failing}\n"
        report_details += f"Description: {report.report_text}\n"
        report_details += f"Resume: {report.resume.url if report.resume else 'No file available'}\n\n"

    email = EmailMessage(
        subject="Selected Candidate Reports",
        body=report_details,
        from_email='noreply.resumecomparator@gmail.com',
        to=[recipient_email]
    )

    for report in reports:
        if report.resume and hasattr(report.resume, 'path'):
            try:
                with open(report.resume.path, 'rb') as f:
                    email.attach(report.resume.name, f.read(), 'application/octet-stream')
            except Exception as e:
                logger.error(f"Could not attach resume for report ID {report.id}: {str(e)}")

    try:
        email.send()
        return JsonResponse({'message': 'Email sent successfully'}, status=200)
    except Exception as e:
        logger.error(f"Email sending failed: {e}")
        return JsonResponse({'error': str(e)}, status=500)