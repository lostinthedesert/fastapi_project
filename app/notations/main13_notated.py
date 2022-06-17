# This quick lesson is going to look at setting up path operators for retreiving user info from our users table. very similar to 
# how we query out database for posts.

from random import randrange
from typing import Optional, List
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends 
import psycopg2 
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models, schemas, utils
from .database import engine, SessionLocal, get_db



# CONNECT TO FASTAPI DATABASE ON POSTGRES USING SQLALCHEMY
models.Base.metadata.create_all(bind=engine)

# CREATE FASTAPI VARIABLE
app=FastAPI()

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

# Get all posts
@app.get("/posts", response_model= List[schemas.Post]) 
def posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts

# create a new post
@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model= schemas.Post) 
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    new_post=models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

# Get a single post
@app.get("/posts/{id}", response_model= schemas.Post)   
def get_post(id: int, db: Session = Depends(get_db)):
    one_post=db.query(models.Post).filter(models.Post.id==id).first()   
    if not one_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{id} not found") 
    return one_post

# Delete a post
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)   
def delete_post(id: int, db: Session = Depends(get_db)): 
    one_post=db.query(models.Post).filter(models.Post.id==id)
    if one_post.first()==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{id} not found")  
    one_post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# Update a post
@app.put("/posts/{id}", status_code=status.HTTP_202_ACCEPTED, response_model= schemas.Post)   
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db)): 
    one_post=db.query(models.Post).filter(models.Post.id==id)
    update_post = one_post.first()
    if update_post ==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{id} not found")
    one_post.update(post.dict(), synchronize_session=False)
    db.commit()
    return one_post.first()

# CREATE USER
@app.post("/users", status_code=status.HTTP_202_ACCEPTED, response_model= schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_password=utils.hash(user.password)
    user.password=hashed_password
    
    new_user=models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# Just like all get requests. Our domain is /users/id and we want to make sure the response conforms to our UserResponse schema so 
# the password is not sent back to the user. Then we run a query and filter by 'id' making sure to grab the .first() hit and then
# stop searching. Insert our HTTPException and return the query to the user. Done!

# GET USER DATA  
@app.get("/users/{id}", response_model=schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user=db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user id: {id} not found")
    return user
    
