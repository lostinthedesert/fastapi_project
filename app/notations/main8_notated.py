# this will look at connecting to our postgres database. We will need to import psycopg2 which is a database adapter like SQLite3 that 
# basically helps up connect to our database and communicate with it using python.

from msilib.schema import Class
from random import randrange
from tkinter.font import BOLD
from turtle import pos
from typing import Optional
from fastapi import Body, FastAPI, Response, status, HTTPException
from pydantic import BaseModel
import psycopg2 
from psycopg2.extras import RealDictCursor
import time


app=FastAPI()

# Post class with pydantic library schema
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int]= None

# here is our code. We are creating a conn variable just like with sqlite3 and .connect method but this time we are providing some
# parameters: localhost is our computer that we're using, database was created using PGadmin ('fastapi'), our user is the default 
# postgres user 'postgres' and our password is the one we set up when we installed postgres. The cursor_factory parameter is just
# a technical requirement that fixes an issue python has identifying column values, not important. Note that this is not how an actual
# production app would be coded. Having this data visible to anyone who had your code is a big security issue. There are more secure
# methods that will be covered later.

# I'll come back to the parent while loop later. since we're attempting to communicate with a database we want to use a try loop in 
# case anything goes wrong and we can't connect, then we throw an error. We also set up the cursor just like sqlite3 and give ourselves
# a print out when connection is successful. 'break' refers to the while loop and breaks us out of it once the connection is successful.
# If for some reason we can't connect we want to store the reason ('Exception') as the variable error (new syntax here!) and also print
# back that the connection failed, what the specific reason was ('error' variable) and give the system 2 seconds before it restarts
# the while loop and tries again. This way if we can't connect, the app will keep trying until it succeeds at which point the while loop
# will be broken and we may proceed.

# 'while True' is just standard python syntax when you want a simple loop that will force some condition before allowing the program
# to continue. In this case we don't want our code to continue being interpreted if we can't even connect to our database. So until
# we can, the while loop holds up the program. Again 'break' ends the while loop.

# connect to fastapi database
while True:
    try:
        conn=psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='dummy123', 
        cursor_factory=RealDictCursor)
        cursor=conn.cursor()
        print('database connection was successful')
        break
    except Exception as error:
        print('connecting to database failed')
        print('error was ', error)
        time.sleep(2)

# "database" for user's posts
my_posts = [{"title":"title of post 1", "content":"content of post 1", "id":1}, {"title":"favorite food", "content":"I like pizza",
"id":2}]

# return post using id
def find_post(id):
    for p in my_posts:
        if p['id']==id:
            return p

# return 'my_posts' index using id
def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id']==id:
            return i

# Root path
@app.get("/") 
def root():
    return {"message": "this message will automatically reload :)"}

# Get all posts
@app.get("/posts") 
def posts():
    return {"data":my_posts}

# create a new post
@app.post("/posts", status_code=status.HTTP_201_CREATED) 
def create_posts(post: Post):
    post_dict=post.dict()
    post_dict['id']=randrange(0, 99999999) 
    my_posts.append(post_dict)
    return {'data': post_dict}

# Get a single post
@app.get("/posts/{id}")   
def get_post(id: int):     
    post=find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{id} not found")   
    return({"post detail": post})

# Delete a post
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)   
def delete_post(id: int): 
    index = find_index_post(id)
    if index==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{id} not found")
    my_posts.pop(index)   
    return Response(status_code=status.HTTP_204_NO_CONTENT)

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

    


