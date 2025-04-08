from django.core.mail import send_mail

def send_success_email(applicant_email, applicant_name, job_id):
    subject = f"Application Status for Job ID {job_id}"
    message = (
        f"Hi {applicant_name},\n\n"
        f"Congratulations! You've passed our screening for the job position with ID: {job_id}.\n"
        f"We'll be in touch with the next steps soon.\n\n"
        f"Best regards,\nRecruitment Team"
    )
    send_mail(subject, message, None, [applicant_email])