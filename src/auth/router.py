from fastapi import APIRouter
from fastapi import Depends, Cookie

from src.common.database import blocked_token_db, session_db, user_db

auth_router = APIRouter(prefix="/auth", tags=["auth"])

SHORT_SESSION_LIFESPAN = 15
LONG_SESSION_LIFESPAN = 24 * 60

@auth_router.post("/token")
def create_token():
    pass


@auth_router.post("/token/refresh")
def refresh_token():
    pass


@auth_router.delete("/token")
def delete_token():
    pass


@auth_router.post("/session")
def create_session():
    pass


@auth_router.delete("/session")
def delete_session():
    pass
