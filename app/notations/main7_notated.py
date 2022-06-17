# this will complete the CRUD tutuorial as we look at how to update a post. We will be using the put request meaning that the user
# must provide all of the post content in order to update it, even if they only want to update one part of the post. So in our
# case 'title' and 'content' must be provided even if they only want to update the title, for example. 

# for our hypothetical we want to replace post id 1 with a new title. 

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

# create function to find posts by id
def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id']==id:
            return i

# create root path using FastAPI
@app.get("/") 
def root():
    return {"message": "this message will automatically reload :)"}

# create /posts path read only
@app.get("/posts") 
def posts():
    return {"data":my_posts}

# create /posts path for user created posts
@app.post("/posts", status_code=status.HTTP_201_CREATED) 
def create_posts(post: Post):
    post_dict=post.dict()
    post_dict['id']=randrange(0, 99999999) 
    my_posts.append(post_dict)
    return {'data': post_dict}

# create 'id' path parameter to read stored posts
@app.get("/posts/{id}")   
def get_post(id: int):     
    post=find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{id} not found")   
    return({"post detail": post})

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)   
def delete_post(id: int): 
    index = find_index_post(id)
    if index==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{id} not found")
    my_posts.pop(index)   
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# For our update code we are using a .put request and then the exact same code we used for creating a new post. Essentially what we
# are doing is grabbing an existing post and replacing it with a new post but keeping the id the same. We will recycle our 'find_index_
# post(id)' function that we used in 'delete_post'. We are also recycling the 'post: Post' code in the 'update_post' parameter.

# Once we have the index number associated with the post id submitted by the user, we want to convert our 'post' values into a dictionary
# like we did when creating a post, then we want to add an 'id' value to the 'post' dictionary (because remember that key is not
# included in the orginal Post(BaseModel) class) and assign it the value provided by the user. Then finally we want to replace the 
# existing 'my_post' value at our given index with our new 'post' dictionary (which now includes the addition of an id). And return
# the user's updates to them.

# So on the front end, the user is providing new values in the body of the interface. They can update any available field but they must
# also provide the other fields (even if they are unchanged) from the original post. This version of the code does not prefill or 
# automatically provide existing values that are not entered by the user.

# Also note the efficiency of python to create a new key within 'post_dict' AND assign that key a value in one line of code:
# post_dict['id']=id. Also note that when referencing the desired 'my_posts' entry, square brackets are used to pass the 'index'
# value, not parentheses.

# Update a post
@app.put("/posts/{id}", status_code=status.HTTP_202_ACCEPTED)   
def update_post(id: int, post: Post): 
    index = find_index_post(id)
    if index==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{id} not found")
    post_dict=post.dict()
    post_dict['id']=id
    my_posts[index]=post_dict
    return{'message':post_dict}
