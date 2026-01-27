import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
EMAIL_FROM = os.getenv("EMAIL_FROM")
CLIENT_EMAIL = os.getenv("CLIENT_EMAIL")

LOGO_URL = "https://res.cloudinary.com/dvgtugqlm/image/upload/v1769537286/logo_n6sfxq.png"


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
""",
        html_content=f"""
<html>
<body>
    <div style="text-align:center;">
        <img src="{LOGO_URL}" alt="RN Fitness Logo" style="max-width:150px; margin-bottom:20px;" />
    </div>
    <p>Hi Enthusiast,</p>
    <p>Your verification code for RN Fitness is:</p>
    <h2>{otp}</h2>
    <p>Confirm with us now and start the journey.</p>
    <p>This code expires in 10 minutes.</p>
</body>
</html>
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
""",
        html_content=f"""
<html>
<body>
    <div style="text-align:center;">
        <img src="{LOGO_URL}" alt="RN Fitness Logo" style="max-width:150px; margin-bottom:20px;" />
    </div>
    <p><strong>New request received:</strong></p>
    <p>Name: {submission.name}</p>
    <p>Email: {submission.email}</p>
    <p>Service: {submission.service_type.value if submission.service_type else "Contact Form"}</p>
    <p>Phone: {submission.contact_number}</p>
    <p>Preferred Date: {submission.preferred_date}</p>
    <p>Preferred Time: {submission.preferred_time}</p>
    <p>Subject: {submission.subject}</p>
    <p>Message:<br>{submission.message}</p>
</body>
</html>
"""
    )
    SendGridAPIClient(SENDGRID_API_KEY).send(message)


def send_user_confirmation(submission):
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
        html_body = f"""
<p>Hi {submission.name},</p>
<p>Thank you for booking a session with RN Fitness.</p>
<p><strong>Service:</strong> {submission.service_type.value}</p>
<p><strong>Date:</strong> {submission.preferred_date}</p>
<p><strong>Time:</strong> {submission.preferred_time}</p>
<p>Our team will contact you shortly.</p>
"""
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
        html_body = f"""
<p>Hi {submission.name},</p>
<p>Thank you for contacting RN Fitness.</p>
<p>We’ve received your message with the subject:</p>
<p><em>{submission.subject}</em></p>
<p>Our team will get back to you shortly.</p>
"""

    message = Mail(
        from_email=EMAIL_FROM,
        to_emails=submission.email,
        subject=subject,
        plain_text_content=body,
        html_content=f"""
<html>
<body>
    <div style="text-align:center;">
        <img src="{LOGO_URL}" alt="RN Fitness Logo" style="max-width:150px; margin-bottom:20px;" />
    </div>
    {html_body}
</body>
</html>
"""
    )

    SendGridAPIClient(SENDGRID_API_KEY).send(message)
