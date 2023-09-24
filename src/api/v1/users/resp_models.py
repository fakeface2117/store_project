import datetime
import uuid
from typing import Optional, Union

from pydantic import EmailStr

from src.core.config import Base


class CreateUserRequest(Base):
    name: str
    lastname: Union[str, None]
    surname: str
    country: str
    user_email: EmailStr
    consent_to_mailing: bool
    user_pass: str


class SelectUserResponse(Base):
    user_id: uuid.UUID
    name: str
    lastname: Optional[str]
    surname: str
    country: str
    user_email: str
    date_registration: datetime.datetime
    consent_to_mailing: bool


class UpdateUserRequest(Base):
    name: Optional[str]
    lastname: Optional[str]
    surname: Optional[str]
    country: Optional[str]
    user_email: Optional[str]
    consent_to_mailing: Optional[bool]


class UserIdResponse(Base):
    user_id: uuid.UUID


class SelectUserByEmailResponse(Base):
    user_id: uuid.UUID
    user_email: str
    hashed_password: str


class Token(Base):
    access_token: str
    token_type: str
