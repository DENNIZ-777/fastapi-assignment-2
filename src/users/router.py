from typing import Annotated, Any

from fastapi import (
    APIRouter,
    Depends,
    status
)

from src.auth.dependencies import get_current_user
from src.common.custom_exception import EmailAlreadyExistsException
from src.common.database import user_db
from src.common.security import hash_password
from src.common.user_store import find_user_by_email, read_user_field
from src.users.schemas import CreateUserRequest, User, UserResponse

user_router = APIRouter(prefix="/users", tags=["users"])

@user_router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_user(request: CreateUserRequest) -> UserResponse:
    if find_user_by_email(str(request.email)) is not None:
        raise EmailAlreadyExistsException()

    user_id = max(
        (read_user_field(user, "user_id") for user in user_db),
        default=0,
    ) + 1
    user = User(
        user_id=user_id,
        email=request.email,
        hashed_password=hash_password(request.password),
        name=request.name,
        phone_number=request.phone_number,
        height=request.height,
        bio=request.bio,
    )
    user_db.append(user)
    return UserResponse.model_validate(user, from_attributes=True)

@user_router.get("/me", response_model=UserResponse)
def get_user_info(
    user: Annotated[Any, Depends(get_current_user)],
) -> UserResponse:
    return UserResponse.model_validate(
        user,
        from_attributes=not isinstance(user, dict),
    )
