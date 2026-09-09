import jwt
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException
from pwdlib import PasswordHash

from auth.schemas import UserRole


password_hash = PasswordHash.recommended()

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD_HASH = password_hash.hash("admin123")

SECRET_KEY = "sih2026-backend-secret-key-2026x"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(
    password: str,
    hashed_password: str
) -> bool:
    return password_hash.verify(
        password,
        hashed_password
    )


def authenticate_user(
    username: str,
    password: str
) -> UserRole | None:
    if username != ADMIN_USERNAME:
        return None

    if not verify_password(
        password,
        ADMIN_PASSWORD_HASH
    ):
        return None

    return UserRole.ADMIN


def create_access_token(
    username: str,
    role: UserRole
) -> str:
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": username,
        "role": role.value,
        "exp": expire
    }

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


def verify_access_token(token: str) -> dict | None:
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        return payload
    except jwt.InvalidTokenError:
        return None


def require_authentication(authorization: str) -> dict:
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication credentials"
        )

    token = authorization.split(" ", 1)[1]

    payload = verify_access_token(token)

    if payload is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    return payload