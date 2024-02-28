from datetime import datetime
from typing import Optional, Annotated

from fastapi import Depends
from pydantic import EmailStr, Field, BaseModel, ConfigDict, field_validator

from app.database import Session
from app.exceptions.exception import UserExc

from app.models import User


class UserBase(BaseModel):
    email: EmailStr

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    email: EmailStr

    password: str

    # @field_validator("email")
    # @classmethod
    # def validate_email_taken(cls, email_user):
    #     from app.routers.crud.base import get_sync_filter_row
    #
    #     with Session() as session:
    #         user = get_sync_filter_row(session, User, email=email_user)
    #     if user:
    #         raise UserExc.http400()
    #     return email_user


class UserOut(UserBase):
    id: int
    created_at: datetime


class UserInPost(UserBase):
    created_at: datetime


class PostBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: str
    content: str
    published: Optional[bool] = True
    id: int
    created_at: datetime
    owner_id: int
    owner: UserInPost


class PostCreate(BaseModel):
    title: str
    content: str


class PostOut(BaseModel):
    Post: PostBase
    votes: int


class LoginUser(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None


class VoteIn(BaseModel):
    post_id: int
    dir: Annotated[int, Field(le=1, ge=0)]


class VoteBase(BaseModel):
    post_id: int
    user_id: int
