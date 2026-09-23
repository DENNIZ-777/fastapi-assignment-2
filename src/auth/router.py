from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
import secrets
from typing import Annotated, Any

from fastapi import APIRouter, Cookie, Depends, Header, Response, status

from src.auth.schemas import LoginRequest, TokenResponse
from src.common.custom_exception import InvalidAccountException, InvalidTokenException
from src.common.database import blocked_token_db, session_db
from src.common.security import create_jwt, decode_token, parse_bearer_token, verify_password
from src.common.user_store import find_user_by_email, find_user_by_id, read_user_field

auth_router = APIRouter(prefix="/auth", tags=["auth"])

SHORT_SESSION_LIFESPAN = 15
LONG_SESSION_LIFESPAN = 24 * 60


@dataclass(frozen=True)
class RefreshCredentials:
    token: str
    user_id: int
    expiration: int


def _get_user_id(payload: dict[str, object]) -> int:
    try:
        user_id = int(payload["sub"])
    except (KeyError, TypeError, ValueError) as exc:
        raise InvalidTokenException() from exc

    if find_user_by_id(user_id) is None:
        raise InvalidTokenException()
    return user_id


def _create_token_pair(user_id: int) -> TokenResponse:
    return TokenResponse(
        access_token=create_jwt(user_id, SHORT_SESSION_LIFESPAN, "access"),
        refresh_token=create_jwt(user_id, LONG_SESSION_LIFESPAN, "refresh"),
    )


def _authenticate_user(request: LoginRequest) -> Any:
    user = find_user_by_email(str(request.email))
    if user is None or not verify_password(
        request.password,
        read_user_field(user, "hashed_password"),
    ):
        raise InvalidAccountException()
    return user


def _get_refresh_credentials(
    authorization: Annotated[str | None, Header()] = None,
) -> RefreshCredentials:
    token = parse_bearer_token(authorization)
    if token in blocked_token_db:
        raise InvalidTokenException()

    payload = decode_token(token, expected_type="refresh")
    user_id = _get_user_id(payload)
    expiration = payload["exp"]
    if not isinstance(expiration, int):
        raise InvalidTokenException()
    return RefreshCredentials(token, user_id, expiration)


@auth_router.post("/token", response_model=TokenResponse)
def create_token(request: LoginRequest) -> TokenResponse:
    user = _authenticate_user(request)
    return _create_token_pair(read_user_field(user, "user_id"))


@auth_router.post("/token/refresh", response_model=TokenResponse)
def refresh_token(
    credentials: Annotated[RefreshCredentials, Depends(_get_refresh_credentials)],
) -> TokenResponse:
    tokens = _create_token_pair(credentials.user_id)
    blocked_token_db[credentials.token] = credentials.expiration
    return tokens


@auth_router.delete("/token", status_code=status.HTTP_204_NO_CONTENT)
def delete_token(
    credentials: Annotated[RefreshCredentials, Depends(_get_refresh_credentials)],
) -> Response:
    blocked_token_db[credentials.token] = credentials.expiration
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@auth_router.post("/session")
def create_session(request: LoginRequest) -> Response:
    user = _authenticate_user(request)
    sid = secrets.token_urlsafe(32)
    while sid in session_db:
        sid = secrets.token_urlsafe(32)

    expires_at = datetime.now(timezone.utc) + timedelta(minutes=LONG_SESSION_LIFESPAN)
    session_db[sid] = (read_user_field(user, "user_id"), expires_at)

    response = Response(status_code=status.HTTP_200_OK)
    response.set_cookie(
        key="sid",
        value=sid,
        max_age=LONG_SESSION_LIFESPAN * 60,
        httponly=True,
        samesite="lax",
    )
    return response


@auth_router.delete("/session", status_code=status.HTTP_204_NO_CONTENT)
def delete_session(
    sid: Annotated[str | None, Cookie()] = None,
) -> Response:
    response = Response(status_code=status.HTTP_204_NO_CONTENT)
    if sid is not None:
        session_db.pop(sid, None)
        response.delete_cookie(key="sid")
    return response
