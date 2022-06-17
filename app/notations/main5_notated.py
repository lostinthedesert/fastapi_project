# this lesson will look at retrieving individual posts using the post id. This will be a read only operation using http get.

from msilib.schema import Class
from random import randrange
from tkinter.font import BOLD
from typing import Optional
from fastapi import Body, FastAPI
from pydantic import BaseModel

app=FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int]= None

my_posts = [{"title":"title of post 1", "content":"content of post 1", "id":1}, {"title":"favorite food", "content":"I like pizza",
"id":2}]

# Here we are creating a function that will search our 'my_posts' list for a specific id. Note the syntax on the for loop. We are 
# narrowing the search down to 'p['id']' so the loop knows where to look for the value in question and then returning that entire
# list item when it finds a match.

def find_post(id):
    for p in my_posts:
        if p['id']==id:
            return p

@app.get("/") 
def root():
    return {"message": "this message will automatically reload :)"}

@app.get("/posts") 
def posts():
    return {"data":my_posts}

@app.post("/posts") 
def create_posts(post: Post):
    post_dict=post.dict()
    post_dict['id']=randrange(0, 99999999) 
    my_posts.append(post_dict)
    return {'data': post_dict}

# Here is our 'get_post' function. Notice our 'path parameter' in the first line now includes '{id}' in the existing '/posts' path.
# the curly brackets indicate it is a variable that the user will provide. Then in the next line we set the parameter as 'id' which
# will pass our user-entered 'id' into the function. We also specify the data type that 'id' must match, that is an integer. This is
# a FastAPI syntax that I'm not sure applies to regular python syntax. FastAPI will generate an error message if the user enters a 
# non-integer. This code also converts the user's 'id' value into an integer for future use.

# Next we assign a variable 'post' to our 'find_post' function and call the function using the user-entered 'id'. And finally
# we return the user the post they have requested using the 'id' provided. 

# So the 'id' is the important value here. It starts with the user, then goes to the path parameter where it is then fed into the 
# 'get_post' function and converted to an integer (by default all path parameters are strings), where it is then passed into the
# 'find_post' function, which then retruns the list entry that matches that id number and is printed back to the user.

@app.get("/posts/{id}")   #path parameter
def get_post(id: int): 
    post=find_post(id) 
    return({"post detail": post})



