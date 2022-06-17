from datetime import datetime
from pydantic import BaseModel, EmailStr, conint
from typing import Optional

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode=True 

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
    owner_id: int
    owner: UserResponse

    class Config:
        orm_mode=True

class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        orm_mode=True

# CREATE USERS
class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

# VERIFY TOKENS
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str]=None

# VOTE SCHEMA
class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)
