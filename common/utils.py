from datetime import datetime, timedelta, timezone
from django.conf import settings

import bcrypt
import jwt


def hash_password(raw_password: str) -> str:
    password_bytes = raw_password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(salt, password_bytes)
    return hashed.decode("utf-8")


def check_password(raw_password: str, password_hash: str) -> bool:
    return bcrypt.checkpw(raw_password.encode("utf-8"), password_hash.encode("utf-8"))
