# This is going to look at continuing to convert our HTTP requests into python commands using sqlalchemy instead of sql to communicate 
# with the database. Note that we have two distinct classes called 'Post' being used in our code: 'Post(BaseModel)' is a pydantic 
# library and dictates what the user must enter on the front end for their input to be accepted. In this case 'title' and 'content' (which
# must be strings. The other Post is 'Post(Base)' from our models.py file that we imported. That is very similar to Post(BaseModel) but it
# is used to create the postgres table 'posts' (in lieu of creating tables in pgadmin) and assign each column its properties/constraints/
# defaults etc. So the similarity in names is confusing but they both perform different functions for our code.

from random import randrange
from typing import Optional
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
import psycopg2 
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models
from .database import engine, SessionLocal, get_db

models.Base.metadata.create_all(bind=engine)

app=FastAPI()

# Post class with pydantic library schema
class Post(BaseModel):
    title: str
    content: str
    published: bool = True

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

# Root path
@app.get("/") 
def root():
    return {"message": "this message will automatically reload :)"}

@app.get("/sqlalchemy")
def test_post(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return{'status': posts}

# We see the line : 'db: Session = Depends(get_db)' being passed by these functions. That's just standard code copied from the 
# fastapi/sqlalchemy docs that tells the api to connect to our database. We can follow the sequence of events in the database.py file
# but it's not important to understand the ins and outs of this line, just that it tells the api we need to connect to the database 
# and that we'll be establishing communications using sqlalchemy.

# We'll also start to notice 'db.query(models.Post)' a lot. Basically this is our python code that tells sqlalchemy to run a query in
# our table 'posts'. The '.all()' method is just telling it to return all of the rows in that table. As usual we want to assign this
# command a variable ('posts'). Then it's a simple as returning {posts} to the user.

# Get all posts
@app.get("/posts") 
def posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data":posts}

# Here we create a new post. Notice the same code being passed by the 'create_post' function to initiate the database connection. Then 
# the next line is really interesting. It looks familiar to a version of our code from before where we converted the 'Post' class
# which stored the user's input into a dictionary format. What this command does is it 'unpacks' the 'Post' class above and tell
# sqlalchemy that the user must submit our criteria from the original 'Post' class when creating a new entry into 'models.Post'. The
# alternative to coding it like this would be to write 'new_post=models.Post(title=post.title, content=post.content, 
# published=post.published). But imagine we had 100 variable types defined in 'Post', we would have to type them out manually. This
# allows us to tell sqlalchemy to just implement the schema in 'Post' when gathering data from the user-much more efficient.

# Next is some sqlalchemy syntax that .adds the new_post values submitted by the user, .commits them to the database, and then .refreshes
# that row (exactly like the RETURNING command in sql) so we can update the 'posts' table and return the user's new post to them.

# Just note that this is exactly what we have been doing in early versions of the code that used a list (my_posts) and then sql to 
# communicate with the postgres database. It's just using different language to accomplish the same task. Now with sqlalchemy
# we are communicating database commands using python instead of SQL. And we are still setting a schema with the 'Post(BaseModel)'
# class to dicatate the acceptable data and format (a library) the user must submit.

# create a new post
@app.post("/posts", status_code=status.HTTP_201_CREATED) 
def create_posts(post: Post, db: Session = Depends(get_db)):
    new_post=models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {'data': new_post}

# This will be another get request that will only return one row from our table using the id column to identify the called post. Very
# similar to the get all function except we add a .filter method and then tell sqlalchemy what column we want to focus on and match 
# with our user provided 'id' value. Then we have to tell sqlalchemy to stop searching the table once it finds a matching row (.first()).
# Otherwise it will continue to search the table for another id match.

# Also note how we are specifying 'models.Post' here. I assume this is to differentiate it from 'Post(BaseModel)'. Basically we're telling
# our app to access the db ('fastapi' in postgres) then run a sql QUERY in the table created by 'models.Post' (which is named 'posts').
# Then we are telling it to .filter the query (like WHERE in sql) models.Post.id == id (user-provided) and then finally to return the 
# .first() hit and stop searching. 

# Note that all of our HTTPExceptions work exactly as they did before without any changes. These seem to be self contained, self
# sufficient lines of code that do not use any sqlalchemy code/syntax.

# Get a single post
@app.get("/posts/{id}")   
def get_post(id: int, db: Session = Depends(get_db)):
    one_post=db.query(models.Post).filter(models.Post.id==id).first()   
    if not one_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{id} not found") 
    return({"post detail": one_post})  

# Here we will delete a post. Very similar to the 'get single post' function except this time the '.first()' is removed from the first
# line of the function but shows up in the next line with the if statement. I don't know why that is. For the actual delete action,
# we simply append '.delete' to our one_post variable and inlcude some sqlalchemy code: 'synchronize_session=False'. Because we are
# working inside a function that passed sqlalchemy commands in the 'def' line, VS Code will recognize additional parameters for 
# common methods like '.delete'. For example, VS Code offered to prefill 'synchronize_session=' when I started typing that line out.
# Details about this particular variable can be found on the sqlalchemy docs, suffice it to say this is the code we need in this 
# instance. As usual when making changes to a database you must .commit().

# Delete a post
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)   
def delete_post(id: int, db: Session = Depends(get_db)): 
    one_post=db.query(models.Post).filter(models.Post.id==id)
    if one_post.first()==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{id} not found")  
    one_post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# This last one is a mix of delete_post and create_post. First we want to narrow our query down to the specific id as usual, then run
# our HTTPException in case the id doesn't match any rows in our posts table. Then we're going to make use of the .update method. Our
# first parameter is post.dict() where we gather the data the user has entered (in the form of a json dictionary) and convert it into
# a python dictionary from our Post model above. Then we apply that same 'synchronize_session' value as we did with delete_post, 
# .commit() our udate and we're done.

# Something I want to emphasize is the purpose of the Post class above (not the models.Post class). What that object does is store
# the user's input while setting the schema that they must submit the data in, that is, the 'title' variable must be a string, etc. 
# Once the user submits in the json format that we specified on Postman, the data is delivered to the back end as a model with a template
# like this: title = user's titles,  content = user's content, published = True. When we apply the method '.dict()' python converts
# that model into a dictionary and then the .update method adds that dictionary (via sql) to our 'posts' table (which is created by
# the models.Post object). Another way of saying it is. 'QUERY the posts table for rows with id value of x, then UPDATE that row
# WHERE title=xyz, content = xyz, published=xyz.

# Also: '.dict()' is a pydantic method. It converts the pydantic MODEL (not a dictionary), in our case 'Post' into a python dictionary.
# Also note: we can treat lines 152 & 155 as one line if we want. It would generate the same outcome to append '.update(post.dict(), 
# synchronize_session=False)' onto the end of line 153 (and doing this would help illustrate the chain of events) as it does now.
# We have split the two lines because we inserted an HTTPException into the flow in case the user's id doesn't exist.

# Update a post
@app.put("/posts/{id}", status_code=status.HTTP_202_ACCEPTED)   
def update_post(id: int, post: Post, db: Session = Depends(get_db)): 
    one_post=db.query(models.Post).filter(models.Post.id==id)
    if one_post.first() ==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{id} not found")
    one_post.update(post.dict(), synchronize_session=False)
    db.commit()
    return{'message': one_post.first()}

    