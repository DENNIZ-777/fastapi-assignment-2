import os
import secrets
from datetime import datetime, timedelta, timezone

import jwt
from jwt.exceptions import InvalidTokenError as PyJWTInvalidTokenError
from pwdlib import PasswordHash

from src.common.custom_exception import (
    BadAuthorizationHeaderException,
    InvalidTokenException,
    UnauthenticatedException,
)

JWT_ALGORITHM = "HS256"
# Production deployments should set JWT_SECRET_KEY. Local runs get a process-scoped temporary key.
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY") or secrets.token_hex(32)
password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    try:
        return password_hash.verify(password, hashed_password)
    except ValueError:
        return False


def create_token(user_id: int, lifespan_minutes: int) -> str:
    expiration = datetime.now(timezone.utc) + timedelta(minutes=lifespan_minutes)
    return jwt.encode(
        {"sub": str(user_id), "exp": expiration},
        JWT_SECRET_KEY,
        algorithm=JWT_ALGORITHM,
    )


def decode_token(token: str) -> dict[str, object]:
    try:
        payload = jwt.decode(
            token,
            JWT_SECRET_KEY,
            algorithms=[JWT_ALGORITHM],
            options={"require": ["sub", "exp"]},
        )
        if not isinstance(payload.get("sub"), str):
            raise InvalidTokenException()
        return payload
    except PyJWTInvalidTokenError as exc:
        raise InvalidTokenException() from exc


def parse_bearer_token(authorization: str | None) -> str:
    if authorization is None:
        raise UnauthenticatedException()

    parts = authorization.split(" ")
    if len(parts) != 2 or parts[0] != "Bearer" or not parts[1]:
        raise BadAuthorizationHeaderException()
    return parts[1]
