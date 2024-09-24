from datetime import datetime, timezone

from passlib.context import CryptContext

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_text(plain_text):
    return bcrypt_context.hash(plain_text)


def compare_hashed_text(plain_text, hashed_text):
    return bcrypt_context.verify(plain_text, hashed_text)


def get_current_utc_time():
    return datetime.now(timezone.utc)
