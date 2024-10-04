import datetime

from pydantic import BaseModel, EmailStr, Field, model_validator

from backend.utils import get_password_hash


class UserRequest(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: str | None = None


class UserCreateRequest(UserRequest):
    active: bool = True
    pwd_modified_at: float = Field(default_factory=lambda: datetime.datetime.now())

    @model_validator(mode="after")
    def validator(cls, values: "UserCreateRequest") -> "UserCreateRequest":
        values.password = get_password_hash(values.password)
        return values


class UserResponse(BaseModel):
    username: str
    email: str
    full_name: str
    active: bool
    created_at: datetime.datetime
    modified_at: datetime.datetime
