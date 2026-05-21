from pydantic import BaseModel

from typing import Optional


class CreateUserRequest(BaseModel):

    name: str

    job: str


class UpdateUserRequest(BaseModel):

    name: Optional[str] = None

    job: Optional[str] = None


class LoginRequest(BaseModel):

    email: str

    password: str


class RegisterRequest(BaseModel):

    email: str

    password: str