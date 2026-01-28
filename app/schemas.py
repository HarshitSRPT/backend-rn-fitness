from pydantic import BaseModel, EmailStr, field_validator, model_validator
from uuid import UUID
from datetime import date, time, datetime
from typing import Optional
import re
from enum import Enum

class FormStartRequest(BaseModel):
    name: str
    email: EmailStr
    contact_number: Optional[str] = None
    preferred_date: Optional[date] = None
    preferred_time: Optional[time] = None
    service_type: Optional["ServiceType"] = None
    subject: str | None = None
    message: str
    @field_validator("contact_number")
    @classmethod
    def validate_phone(cls, v):
        if v and not re.fullmatch(r"\+?\d{8,15}", v):
            raise ValueError("Invalid phone number")
        return v

    @field_validator("preferred_date")
    @classmethod
    def validate_date(cls, v):
        if v and v < date.today():
            raise ValueError("Preferred date must be today or later")
        return v

    @field_validator("preferred_time")
    @classmethod
    def validate_time(cls, v, info):
        d = info.data.get("preferred_date")
        if v and d == date.today():
            if datetime.combine(d, v) <= datetime.now():
                raise ValueError("Preferred time must be in the future")
        return v
    
    @model_validator(mode="after")
    def validate_date_time_pair(self):
        if (self.preferred_date is None) != (self.preferred_time is None):
            raise ValueError(
                "preferred_date and preferred_time must be provided together"
            )
        return self

class ServiceType(str, Enum):
    personal_training = "Personal Training"
    group_classes = "Group Classes"
    nutrition_coaching = "Nutrition Coaching"
    online_coaching = "Online Coaching"
    gym_training = "In-person Gym Training"
    doctor_consultations = "Doctor Consultations"

class OTPVerifyRequest(BaseModel):
    email: EmailStr
    otp: str
