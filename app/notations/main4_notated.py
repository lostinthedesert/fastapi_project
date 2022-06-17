# We are going to look at CRUD and some functionality to achieving that. CRUD = Create, Read, Update, Delete and it refers to the basic
# functions of an app like ours. Each part of CRUD has a get method associated with it. "C" uses http post, "R" is http get request,
# "U" uses http put or patch requests, and "D" uses http delete requests. We'll see how this is put into practice for our end user to
# allow them to retrieve and view posts on our message board. We'll also create a faux-database (using an array) to store user's posts
# and assign each post a unique ID. We've imported 'randrange' from 'random' which is a random number generator.

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

# 'my_posts' is our array that will fill in for a database (which will be covered later). In my_posts we will store the title, content,
# and id number of our user's posts in the form of a dictionary. Basically, we want to be able to store all our user's posts for later
# retrieval and viewing, updating or deleting. We've assigned id's to the first two array entries. From now on our my_posts array will
# be updated by the user and will not appear as hardcoded in the list as the first two entries are but they will be retrievable from
# my_posts until the code is saved again, at which point the data not hardcoded (ie the first two entries we created on the backend)
# # will be lost.

# The array is a list that contains dictionaries or our user's title, content and an ID number we assign.

my_posts = [{"title":"title of post 1", "content":"content of post 1", "id":1}, {"title":"favorite food", "content":"I like pizza",
"id":2}]

@app.get("/") 
def root():
    return {"message": "this message will automatically reload :)"}

# Also just a sidenote, I've updated the .get and .post request domain folders to "/posts" which is standard protocol for naming domains.
# I've also updated the return value so that when the user sends a get request to /posts, it will return our my_posts array.
@app.get("/posts") 
def posts():
    return {"data":my_posts}

# Here is the meat of our new code. Essentially we want all user generated data to be saved into our my_posts array and assigned a
# random ID number. Later on when we learn to use databases, post IDs will be assigned by our database module but for now we have to
# create our own.

# So all the function name and parameters stay the same. But the first operation performed by the function is to now create a variable
# 'post_dict whose value is our user's post converted into dictionary format like we did before to print to the terminal. Then we are
# going to utilize the randrange function to assign our random id to post_dict. That will add the 'id' value to our post dictionary
# and assign it a random number between 0 and 99999999. Then we want to add this post class (which is now in the form of a dictionary)
# to the 'my_posts' array. And finally we return to the user the post_dict data.

# Notice how python created the 'id' key for our 'post_dict' and assigned it a value all in one fell swoop.

@app.post("/posts") 
def create_posts(post: Post):
    post_dict=post.dict()
    print(post_dict)
    post_dict['id']=randrange(0, 99999999) 
    my_posts.append(post_dict)
    return {'data': post_dict}
    
