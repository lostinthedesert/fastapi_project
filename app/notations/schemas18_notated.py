# new schemas.PostOut to assist in our vote counter.

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

# so our new class PostOut inherits BaseModel instead of PostBase because look at the first value: 'Post' is type Post. That means it is inheriting class Post from above which already inherits PostBase (which in turn inherited BaseModel). We also had to add 'votes' to the schema beccause when we query the JOINed tables it returns the data to us with a new column: votes. Since that variable doesn't exists in our other schemas python doesn't know what to do with it, hence the need for a new schema. This is a good reminder that our schema models can have variables whose data type is another schema class. so in this example Post:Post.

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
