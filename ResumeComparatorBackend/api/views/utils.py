from django.core.mail import send_mail


"""
Email utility function

@Author: Michael Tamatey
@Date: 2025-03-05
"""
def send_success_email(applicant_email, applicant_name):
    subject = "CGI Job Application Status Update"
    message = (
        f"Hi {applicant_name},\n\n"
        f"Congratulations!\n\n"
        f"We're excited to let you know that your resume has successfully passed our screening process for the job position.\n\n"
        f"Here’s what that means:\n"
        f"Your qualifications closely match the job requirements.\n"
        f"Your resume demonstrated strong alignment with the role's responsibilities.\n\n"
        f"What’s next?\n"
        f"The next step in the hiring process is an interview with our recruitment team. "
        f"You will receive a follow-up email shortly with the interview details, including scheduling and format.\n\n"
        f"In the meantime, feel free to reach out if you have any questions.\n\n"
        f"Best regards,\n"
        f"Recruitment Team\n"
        f"CGI Talent Acquisition"
    )
    send_mail(subject, message, None, [applicant_email])