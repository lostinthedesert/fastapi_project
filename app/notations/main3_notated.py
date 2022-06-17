# this lesson looks at using 'pydantic' (a library) to validate user-provided data to make sure it conforms to our back end schema
# (eg. user must provide a 'title' that is a string, a boolean value for 'published', etc.) We are importing 'BaseModel' from 
# # pydantic which appears to be a basic key:value library schema.

from typing import Optional
from fastapi import Body, FastAPI
from pydantic import BaseModel

app=FastAPI()

# Here we've created a class called 'Post' that contains a few 'type' variables. Notice how we use a colon instead of an equal sign 
# to define the variables. That's because we are defining types (such as string, integer, etc.). And bassically this is just telling
# the 'createpost' function what types of data to look for from the user. If they're data doesn't meet this guideline, it will throw
# an error. So for example the 'title' value must be a string, rating (which is Optional and does not have to be provided by the user)
# must be an integer. Furthermore if the user tries to send a post request without including one of these variable (with the exception
#  of 'rating' which is optional), the program will throw an error. So it's really dictating to the user what they have to provide.
# Remember that data is being translated and sent using json which takes the form of a key:value library.

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int]= None


@app.get("/") 
def root():
    return {"message": "this message will automatically reload :)"}

@app.get("/posts") 
def posts():
    return {"data":"this is your post"}

# Here the 'create_posts' function is called using the 'post' variable which is assigned the 'Post' class (for some reason a colon is
# used here instead of an = sign, maybe because 'Post uses pydantic's BaseModel parameter and that's a library but I don't know). Also
# interesting to note that 'post' is defined as a variable and used to pass a parameter to 'create_post' all in one instance.

# So FastAPI is engaged but this time we're using the http post request instead of get like before. That's because we want the user
# to submit some data in addition to receiving. Again this is happening in the '/createpost' directory of our server. We then define
# a function 'create_posts' to be used by FastAPI (hence the decorator). We want the function to print (to the terminal) whatever values
# get stored in the 'Post' class by the user, then we want them printed as a dictionary ('.dict()' method). Then we want FastAPI to 
# return the user's data to '/createposts' with the title 'data'. The user will see their data returned as a library (typical of
# json)

@app.post("/createposts") 
def create_posts(post: Post):
    print(post)
    print(post.dict())
    return {'data': post }