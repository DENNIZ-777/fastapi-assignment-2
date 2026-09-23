import re

from pydantic import BaseModel, EmailStr, field_validator
from pydantic_core import PydanticCustomError

class CreateUserRequest(BaseModel):
    name: str
    email: EmailStr
    password: str
    phone_number: str
    bio: str | None = None
    height: float

    @field_validator('password', mode='after')
    @classmethod
    def validate_password(cls, v: str) -> str:
        if len(v) < 8 or len(v) > 20:
            raise PydanticCustomError("invalid_password", "INVALID PASSWORD")
        return v
    
    @field_validator('phone_number', mode='after')
    @classmethod
    def validate_phone_number(cls, v: str) -> str:
        if re.fullmatch(r"010-\d{4}-\d{4}", v) is None:
            raise PydanticCustomError("invalid_phone_number", "INVALID PHONE NUMBER")
        return v

    @field_validator('bio', mode='after')
    @classmethod
    def validate_bio(cls, v: str | None) -> str | None:
        if v is not None and len(v) > 500:
            raise PydanticCustomError("bio_too_long", "BIO TOO LONG")
        return v


class User(BaseModel):
    user_id: int
    email: EmailStr
    hashed_password: str
    name: str
    phone_number: str
    height: float
    bio: str | None = None

class UserResponse(BaseModel):
    user_id: int
    name: str
    email: EmailStr
    phone_number: str
    bio: str | None = None
    height: float
