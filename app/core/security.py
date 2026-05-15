
from datetime import datetime, timedelta

import jwt
from pwdlib import PasswordHash

from app.core.config import settings


password_context = PasswordHash.recommended()

def hash_password(password: str) -> str:
    return password_context.hash(password=password)

def verify_password(plain_password:str, hashed_password:str) -> bool:
    return password_context.verify(plain_password, hashed_password)

def create_access_token(data:dict, minutes: int | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=minutes or settings.JWT_EXPIRES_MIN)
    to_encode.update(
        {"exp": expire}
    )
    return jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

def decode_token(token: str) -> dict:
    return jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
