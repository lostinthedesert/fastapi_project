# this will look at 'status codes'. when the user sends an invalid requests we want FastAPI to send back a default message specific
# to that particular error. Note: status codes are not just sent for errors, they are sent for any http request including successfully
# executed ones. We are importing 'Response', 'status', and 'HTTPException' from FastAPI for this lesson.

from msilib.schema import Class
from random import randrange
from tkinter.font import BOLD
from turtle import pos
from typing import Optional
from fastapi import Body, FastAPI, Response, status, HTTPException
from pydantic import BaseModel


app=FastAPI()

# create Post class with pydantic library
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int]= None

#create database for user's posts
my_posts = [{"title":"title of post 1", "content":"content of post 1", "id":1}, {"title":"favorite food", "content":"I like pizza",
"id":2}]

# create function for finding posts using 'id'
def find_post(id):
    for p in my_posts:
        if p['id']==id:
            return p

# create root path using FastAPI
@app.get("/") 
def root():
    return {"message": "this message will automatically reload :)"}

# create /posts path read only
@app.get("/posts") 
def posts():
    return {"data":my_posts}

# Here is our first example of a status code. See that it is included in the decorator parameter after the path name. 'status_code'
# is the variable created to store the value of the status function that we imported and the method is '.HTTP_201_CREATED'. the 
# status function generates a drop down menu in VS Code that we can select our desired status code from. Now when the user successfully
# creates a new post, this status code will be sent.

# create /posts path for user created posts
@app.post("/posts", status_code=status.HTTP_201_CREATED) 
def create_posts(post: Post):
    post_dict=post.dict()
    post_dict['id']=randrange(0, 99999999) 
    my_posts.append(post_dict)
    return {'data': post_dict}

# Here's our next example. Here we'll use an if statement to determine when the user has entered an invalid id. Note the syntax 'if not
# post' which basically translates to if the find_post function fails to return anything, therefore leaving the 'post' variable 
# undefined, do the following.... Next we call the HTTPException function that we imported using the 'raise' command and pass the 
# parameter 'status_code=status.HTTP_404_NOT_FOUND, just like we did for the 'create_post' path above, and then a second parameter
# that we assigned the variable 'detail' and set equal to a string that will tell the user their given id was not found.

# create 'id' path parameter to read stored posts
@app.get("/posts/{id}")   
def get_post(id: int):     
    post=find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{id} not found") 
    return({"post detail": post})



