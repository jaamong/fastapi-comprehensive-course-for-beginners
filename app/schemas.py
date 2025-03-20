from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass  # same thing as PostBase


class PostResponse(PostBase):
    id: int
    created_at: datetime

    # class Config: 최신 버전에서는 필요없음
    #     orm_mode = True


class UserBase(BaseModel):
    email: str
    password: str


class UserCreate(UserBase):
    email: EmailStr


class UserResponse(BaseModel):
    id: int
    email: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: Optional[str] = None
