from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional

# CREATE POSTS
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode=True

# CREATE USERS
class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode=True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Here are some new validation schemas for tokens. These will help us validate that the user is submitting the correct data types
# in regard to the values extracted from their tokens.

# VERIFY TOKENS
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str]=None