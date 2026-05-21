from typing import List, Optional

from pydantic import BaseModel


class UserData(BaseModel):

    id: int

    email: str

    first_name: str

    last_name: str

    avatar: str


class SupportData(BaseModel):

    url: str

    text: str


class UsersListResponse(BaseModel):

    page: int

    per_page: int

    total: int

    total_pages: int

    data: List[UserData]

    support: SupportData


class SingleUserResponse(BaseModel):

    data: UserData

    support: SupportData


class CreateUserResponse(BaseModel):

    name: str

    job: str

    id: Optional[str] = None

    createdAt: Optional[str] = None