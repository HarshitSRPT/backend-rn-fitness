from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from app.database import SessionLocal
from app.models import FormSubmission, EmailVerification
from app.schemas import FormStartRequest, OTPVerifyRequest
from app.otp_service import (
    generate_numeric_otp, hash_otp, verify_otp,
    get_expiry_time, MAX_OTP_ATTEMPTS
)
from app.email_service import send_otp_email, send_client_notification, send_user_confirmation

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/forms/start")
def start_form(data: FormStartRequest, request: Request, db: Session = Depends(get_db)):
    otp = generate_numeric_otp()

    # Always create new OTP
    db.add(EmailVerification(
        email=data.email,
        otp_hash=hash_otp(otp),
        expires_at=get_expiry_time()
    ))

    # Look for existing pending submission
    submission = db.query(FormSubmission)\
        .filter(FormSubmission.email == data.email, FormSubmission.status == "pending")\
        .first()

    if submission:
        # Update instead of insert (resend flow)
        submission.name = data.name
        submission.contact_number = data.contact_number
        submission.service_type = data.service_type
        submission.preferred_date = data.preferred_date
        submission.preferred_time = data.preferred_time
        submission.subject = data.subject
        submission.message = data.message
        submission.ip_address = request.client.host
    else:
        # First-time submit
        submission = FormSubmission(
            name=data.name,
            email=data.email,
            contact_number=data.contact_number,
            service_type=data.service_type,
            preferred_date=data.preferred_date,
            preferred_time=data.preferred_time,
            subject=data.subject,
            message=data.message,
            ip_address=request.client.host
        )
        db.add(submission)

    db.commit()
    send_otp_email(data.email, otp)

    return {"status": "otp_sent"}

@router.post("/forms/verify")
def verify_form(data: OTPVerifyRequest, db: Session = Depends(get_db)):
    record = db.query(EmailVerification)\
        .filter(EmailVerification.email == data.email)\
        .order_by(EmailVerification.created_at.desc())\
        .first()

    if not record or record.expires_at < datetime.utcnow():
        raise HTTPException(400, "OTP expired")

    if record.attempt_count >= MAX_OTP_ATTEMPTS:
        raise HTTPException(400, "Too many attempts")

    if not verify_otp(data.otp, record.otp_hash):
        record.attempt_count += 1
        db.commit()
        raise HTTPException(400, "Invalid OTP")

    submission = db.query(FormSubmission)\
        .filter(FormSubmission.email == data.email, FormSubmission.status == "pending")\
        .first()

    if not submission:
        raise HTTPException(400, "No pending submission")

    submission.status = "verified"
    submission.verified_at = datetime.utcnow()
    db.commit()

    send_client_notification(submission)
    send_user_confirmation(submission)
    return {"status": "verified"}
