# this lesson looks at converting our existing http requests into our database (versus the fake database we set up using the 'my_posts'
# list. This is simple integration of the sql language we just learned into our path parameter functions.)

from msilib.schema import Class
from random import randrange
from tkinter import EXCEPTION
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

# connect to fastapi database
while True:

    try:
        conn=psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='Supbitch..318', 
        cursor_factory=RealDictCursor)
        cursor=conn.cursor()
        print('database connection was successful')
        break
    except Exception as error:
        print('connecting to database failed')
        print('error was ', error)
        time.sleep(2)


# Root path
@app.get("/") 
def root():
    return {"message": "this message will automatically reload :)"}

# we start by calling our cursor and appending the .execute method. in this case we are talking about a get request so we use SELECT
# since we just want to read the posts and then simply specifying * (all) rows from the table 'posts'. Next we need to call the 
# .fetchall() method and assign that a variable 'posts'. And we return the 'posts' table to the user.

# Get all posts
@app.get("/posts") 
def posts():
    cursor.execute("SELECT * FROM posts   ")
    posts=cursor.fetchall()
    print(posts)
    return {"data":posts}

# next we want to create a new post so we use INSERT INTO posts and in parentheses specify the columns we want to insert into our
# table. Keep in mind these colunms already exist in the posts table so we're just making a new row following our existing template.
# 'title' and 'content' will require some user input but if they don't provide 'published' we have already set a default value for that
# column in PGadmin so it will not throw an error. 

# Now here's where it gets fun: the next command is 'VALUES' which tells sql which values to set for each of the columns we just 
# specified (and order is very important here) but instead of just telling it the value of 'post.title' etc we are going to use 
# placeholders ('%s'). This is a measure to prevent something called a sql injection where a user could manipulate our backend code
# by entering their own sql code. To prevent this attack we use placeholders. Then we specify postgres to return all new columns and 
# we close our triple " and then use a comma to separate our next parameter which will be the placeholder values. And these must go
# in order of the original column values. Now we can tell postgres to insert the user's data for each of the given keys.

# Again we do fetch but this time it's 'fetchone()' because we only want this one row we are working with. And last we must do a 
# conn.commit to save the changes to our table. And return the new post to the user.

# create a new post
@app.post("/posts", status_code=status.HTTP_201_CREATED) 
def create_posts(post: Post):
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", (post.title, post.content,
    post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {'data': new_post}

# Let's retrieve a post to read by its id. So we are passing the user-provided id into the 'get_post' function. Then executing some 
# sql code (in triple ") and specifying "WHERE id =". Again we use a placeholder and pass the user provided id to the sql command in 
# the next parameter. Now it gets a little convoluted but basically the user-provided id needs to be converted back into a string 
# because sql only takes strings. Remember that before we specified the user had to enter an integer for the id, and we want to keep
# it that way but that means we must convert it back to a string for sql to interpret it. And you'll notice a random comma at the end
# of the 'str(id)'. I don't know why we need that but it prevents an error when retrieving an HTTP exception. Just ignore it, it's a
# work around for a bug.

# Again we do a .fetchone() and return it to the user. Done!

# Get a single post
@app.get("/posts/{id}")   
def get_post(id: int):     
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),) )
    one_post=cursor.fetchone()
    if not one_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{id} not found") 
    return({"post detail": one_post})  

# let's delete a post by id. Use DELETE FROM and provide the id in the same way we did for the get request. Since we're not 
# SELECTing here we want to tell postgres to RETURN(ing) the chosen post. This will allow us to print() the deleted post to ourself
# on the back end if we choose (which i have not done here). Simple, same as before and we can throw an HTTP exception if the post
# id provided doesn't exist.

# Delete a post
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)   
def delete_post(id: int): 
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    del_post=cursor.fetchone()
    conn.commit() 
    if del_post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{id} not found")  
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# Finally we want to update an existing post. You can see the syntax is to SET your new values(again using placeholders) for the desired
# columns and specify WHERE id = and we wanted postgres to RETURN(ing) our updated row, the next parameter collects the values for the
# placeholders (always in the correct order). Notice how 'str(id)' is not appended to 'post' becasue we are gathering that from the 
# path parameter not the body of the interface. Again we fetchone() the row and .commit() the changes and return the new post to the 
# user.

# Update a post
@app.put("/posts/{id}", status_code=status.HTTP_202_ACCEPTED)   
def update_post(id: int, post: Post): 
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *   """, (post.title, post.content,
    post.published, str(id),))
    update_post=cursor.fetchone()
    conn.commit()
    if update_post ==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{id} not found")
    return{'message':update_post}