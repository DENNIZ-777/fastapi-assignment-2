from fastapi import APIRouter
from fastapi import Depends, Cookie

from common.database import blocked_token_db, session_db, user_db

auth_router = APIRouter(prefix="/auth", tags=["auth"])

SHORT_SESSION_LIFESPAN = 15
LONG_SESSION_LIFESPAN = 24 * 60

@auth_router.post("/token")


@auth_router.post("/token/refresh")


@auth_router.delete("/token")


@auth_router.post("/session")


@auth_router.delete("/session")
