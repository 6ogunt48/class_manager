from pydantic import BaseModel, EmailStr, Field, field_validator
from typing_extensions import Literal

from application.db.app_models import UserRole


class UserCreate(BaseModel):
    first_name: str = Field(..., min_length=2, max_length=50)
    last_name: str = Field(..., min_length=2, max_length=50)
    username: str = Field(..., min_length=8, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=50)
    role: Literal[UserRole.STUDENT, UserRole.TEACHER]

    @field_validator("password")
    @classmethod
    def validate_password(cls, password: str) -> str:
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not any(char.isupper() for char in password):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(char.islower() for char in password):
            raise ValueError("password must contain at least one lower case letter")
        if not any(char in "!@#$%^&*()_+" for char in password):
            raise ValueError("Password must contain at least one symbol")
        if not any(char.isdigit() for char in password):
            raise ValueError("Password must contain at least one digit")
        return password

    @field_validator("username")
    @classmethod
    def validate(cls, username: str) -> str:
        if len(username) < 8:
            raise ValueError("Username must be at least 8 characters long")
        if not any(char.isupper for char in username):
            raise ValueError("Username must contain one upper case letter")
        if not any(char.islower() for char in username):
            raise ValueError("Username must contain one lower case")
        return username


class UserCreateResponse(BaseModel):
    message: str


class LoginResponse(BaseModel):
    message: str


class PasswordChange(BaseModel):
    username: str
    password: str
    new_password: str


class PasswordChangeResponse(BaseModel):
    message: str


class CreateCourse(BaseModel):
    course_code: str = Field(..., min_length=2, max_length=6)
    title: str = Field(..., min_length=2, max_length=100)
    description: str = Field(None, max_length=500)


class CreateCourseResponse(BaseModel):
    message: str
