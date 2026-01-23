import uuid
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Integer,Date, Time
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from .database import Base
from app.schemas import ServiceType
from sqlalchemy import Enum as PgEnum


class Service(Base):
    __tablename__ = "services"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, server_default=func.now())


class FormSubmission(Base):
    __tablename__ = "form_submissions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    email = Column(String(150), nullable=False)
    contact_number=Column(String, nullable=True)
    preferred_date = Column(Date, nullable=True)
    preferred_time = Column(Time, nullable=True)
    service_type = Column(
        PgEnum(
            ServiceType,
            name="service_type_enum",
            values_callable=lambda enum: [e.value for e in enum]  # <-- important
        ),
        nullable=True
    )
    subject = Column(String(200))
    message = Column(Text, nullable=False)

    status = Column(String(20), default="pending")
    verified_at = Column(DateTime)
    ip_address = Column(String(45))

    created_at = Column(DateTime, server_default=func.now())


class EmailVerification(Base):
    __tablename__ = "email_verifications"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(150), nullable=False)
    otp_hash = Column(String(255), nullable=False)
    expires_at = Column(DateTime, nullable=False)
    attempt_count = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())
