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
from app.email_service import send_otp_email, send_client_notification

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

    db.add(EmailVerification(
        email=data.email,
        otp_hash=hash_otp(otp),
        expires_at=get_expiry_time()
    ))

    db.add(FormSubmission(
        name=data.name,
        email=data.email,
        service_type=data.service_type,
        contact_number=data.contact_number,
        preferred_date=data.preferred_date,
        preferred_time=data.preferred_time,
        subject=data.subject,
        message=data.message,
        ip_address=request.client.host
    ))

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
    return {"status": "verified"}
