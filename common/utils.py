from datetime import datetime, timedelta, timezone
from django.conf import settings

import bcrypt
import jwt


def hash_password(raw_password: str) -> str:
    password_bytes = raw_password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode("utf-8")


def check_password(raw_password: str, password_hash: str) -> bool:
    return bcrypt.checkpw(raw_password.encode("utf-8"), password_hash.encode("utf-8"))


def generate_access_token(user_id: int, expires_minute: int = 60) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "user_id": user_id,
        "type": "access",
        "iat": now,
        "exp": now + timedelta(minutes=expires_minute),
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")


def decode_access_token(token: str) -> bool:
    return jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
