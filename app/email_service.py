import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
EMAIL_FROM = os.getenv("EMAIL_FROM")
CLIENT_EMAIL = os.getenv("CLIENT_EMAIL")


def send_otp_email(to_email: str, otp: str):
    message = Mail(
        from_email=EMAIL_FROM,
        to_emails=to_email,
        subject="Verify your request",
        plain_text_content=f"""
Your verification code is:

{otp}

This code expires in 10 minutes.
"""
    )

    sg = SendGridAPIClient(SENDGRID_API_KEY)
    sg.send(message)


def send_client_notification(submission):
    message = Mail(
        from_email=EMAIL_FROM,
        to_emails=CLIENT_EMAIL,
        subject="New Verified Lead",
        plain_text_content=f"""
Name: {submission.name}
Email: {submission.email}
Service: {submission.service_type}

Subject: {submission.subject}
Message:
{submission.message}
"""
    )
    SendGridAPIClient(SENDGRID_API_KEY).send(message)
