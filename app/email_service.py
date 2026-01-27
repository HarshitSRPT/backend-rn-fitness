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
Hi Enthusiast,

Your verification code for RN Fitness is:

{otp}

Confirm with us now and Start the journey.

This code expires in 10 minutes.
"""
    )
    SendGridAPIClient(SENDGRID_API_KEY).send(message)


def send_client_notification(submission):
    message = Mail(
        from_email=EMAIL_FROM,
        to_emails=CLIENT_EMAIL,
        subject="New Verified Lead",
        plain_text_content=f"""
New request received:

Name: {submission.name}
Email: {submission.email}
Service: {submission.service_type.value if submission.service_type else "Contact Form"}
Phone: {submission.contact_number}
Preferred Date: {submission.preferred_date}
Preferred Time: {submission.preferred_time}
Subject: {submission.subject}
Message:
{submission.message}
"""
    )
    SendGridAPIClient(SENDGRID_API_KEY).send(message)


def send_user_confirmation(submission):
    # Booking confirmation
    if submission.service_type:
        subject = "Your Booking Request is Confirmed – RN Fitness"
        body = f"""
Hi {submission.name},

Thank you for booking a session with RN Fitness.

Here are your submitted details:
Service: {submission.service_type.value}
Preferred Date: {submission.preferred_date}
Preferred Time: {submission.preferred_time}

Our team will contact you shortly to confirm your slot and guide you with the next steps.

Best regards,
RN Fitness Team
"""
    # Contact form confirmation
    else:
        subject = "We’ve Received Your Message – RN Fitness"
        body = f"""
Hi {submission.name},

Thank you for contacting RN Fitness.

We’ve received your message with the subject:
"{submission.subject}"

Our team will review your query and get back to you shortly.

Best regards,
RN Fitness Team
"""

    message = Mail(
        from_email=EMAIL_FROM,
        to_emails=submission.email,
        subject=subject,
        plain_text_content=body
    )

    SendGridAPIClient(SENDGRID_API_KEY).send(message)
