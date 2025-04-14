from django.core.mail import send_mail
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from datetime import datetime
from django.utils import timezone
from django.utils.http import base36_to_int


"""
Email utility function

@Author: Michael Tamatey
@Date: 2025-03-05
"""
def send_success_email(applicant_email, applicant_name, job_id):
    subject = f"Application Status for Job ID {job_id}"
    message = (
        f"Hi {applicant_name},\n\n"
        f"Congratulations! You've passed our screening for the job position with ID: {job_id}.\n"
        f"We'll be in touch with the next steps soon.\n\n"
        f"Best regards,\nRecruitment Team"
    )
    send_mail(subject, message, None, [applicant_email])


"""
Password Reset Token Generator (expires in 10 minutes)

@Author: Michael Tamatey
@Date: 2025-03-05
"""
class TenMinuteTokenGenerator(PasswordResetTokenGenerator):
    def _make_timestamp(self, user):
        return super()._make_timestamp(user)

    def check_token(self, user, token):
        # Step 1: Check if the token is valid (basic check)
        if not super().check_token(user, token):
            return False

        # Step 2: Try to retrieve the timestamp from the token
        try:
            ts_b36 = token.split('-')[1]
            ts = self._parse_timestamp(ts_b36)  # Parse timestamp from base36
        except Exception:
            return False

        # Step 3: Calculate token age
        now_ts = self._num_seconds(timezone.now())
        token_age = now_ts - ts

        # Step 4: Token must be within 10 minutes (600 seconds)
        return token_age <= 600  # 10 minutes

    def _parse_timestamp(self, ts_b36):
        # Convert the timestamp from base36
        return datetime.fromtimestamp(base36_to_int(ts_b36))

    def _num_seconds(self, dt):
        # Return the number of seconds since the epoch
        return int(dt.timestamp())