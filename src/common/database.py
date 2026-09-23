from datetime import datetime
from typing import Any


user_db: list[Any] = []
session_db: dict[str, tuple[int, datetime]] = {}
blocked_token_db: dict[str, datetime] = {}
