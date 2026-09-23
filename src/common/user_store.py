from typing import Any

from src.common.database import user_db


def read_user_field(user: Any, field: str) -> Any:
    if isinstance(user, dict):
        return user[field]
    return getattr(user, field)


def find_user_by_email(email: str) -> Any | None:
    return next(
        (user for user in user_db if read_user_field(user, "email") == email),
        None,
    )


def find_user_by_id(user_id: int) -> Any | None:
    return next(
        (user for user in user_db if read_user_field(user, "user_id") == user_id),
        None,
    )
