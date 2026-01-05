import random
import hashlib
from datetime import datetime, timedelta
import os

OTP_EXPIRY_MINUTES = int(os.getenv("OTP_EXPIRY_MINUTES", 10))
MAX_OTP_ATTEMPTS = int(os.getenv("MAX_OTP_ATTEMPTS", 5))


def generate_numeric_otp():
    return str(random.randint(100000, 999999))


def hash_otp(otp: str):
    return hashlib.sha256(otp.encode()).hexdigest()


def verify_otp(plain: str, hashed: str):
    return hashlib.sha256(plain.encode()).hexdigest() == hashed


def get_expiry_time():
    return datetime.utcnow() + timedelta(minutes=OTP_EXPIRY_MINUTES)
