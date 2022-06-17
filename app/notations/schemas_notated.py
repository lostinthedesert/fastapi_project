# Here we have created a module to handle our old 'Post' class that is the pydantic model for our user's posts. We'll import
# this to the main.py file and remove the old code from that file to clean things up a bit. Notice we changed the name of the 'Post'
# class to 'PostBase' but all the values are the same. We've also created some new related classes: PostCreate and Post which both
# 'extend' the PostBase object by passing it as an argument (as a result inheriting those values into the lower classes).

# This is going to allow us to designate different pydantic models depending on what actions our app is performing. Say for example,
# we only want to return the title and content to a user when they update a post but not the 'created_at' and 'published' values,
# here we can create a class that only defines those two values and then refer to that class in the 'response_model' variable
# of our path parameter. We can also force the user to enter certain values in order to send post/update requests in the same way.

from datetime import datetime
from pydantic import BaseModel


# PostBase class with pydantic library schema BaseModel
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

# CLASS FOR CREATING NEW POSTS
class PostCreate(PostBase):
    pass

# Just want to point out the 'class Config' code here. This is a required code and is found on the fastapi docs page. Basically,
# if we don't use this code sqlalchemy can't squeeze the data into this model because it's not a dictionary. This code allows the data
# to pass from the database into our pydantic model.

# CLASS FOR RETURNING POSTS TO USERS
class Post(PostBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode=True
