from datetime import datetime, timezone
from typing import Annotated, Any

from fastapi import Cookie, Header

from src.common.custom_exception import (
    InvalidSessionException,
    InvalidTokenException,
    UnauthenticatedException,
)
from src.common.database import session_db
from src.common.security import decode_token, parse_bearer_token
from src.common.user_store import find_user_by_id


def _get_token_user(authorization: str) -> Any:
    token = parse_bearer_token(authorization)
    payload = decode_token(token, expected_type="access")
    try:
        user_id = int(payload["sub"])
    except (KeyError, TypeError, ValueError) as exc:
        raise InvalidTokenException() from exc

    user = find_user_by_id(user_id)
    if user is None:
        raise InvalidTokenException()
    return user


def _get_session_user(sid: str) -> Any:
    session = session_db.get(sid)
    if session is None:
        raise InvalidSessionException()

    user_id, expires_at = session
    if datetime.now(timezone.utc) >= expires_at:
        session_db.pop(sid, None)
        raise InvalidSessionException()

    user = find_user_by_id(user_id)
    if user is None:
        raise InvalidSessionException()
    return user


def get_current_user(
    sid: Annotated[str | None, Cookie()] = None,
    authorization: Annotated[str | None, Header()] = None,
) -> Any:
    if sid is not None:
        return _get_session_user(sid)
    if authorization is not None:
        return _get_token_user(authorization)
    raise UnauthenticatedException()
