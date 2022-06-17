# Couple of minor updates for this version: We moved the 'Post(BaseModel)' class to its own module and added some variations so it 
# can now be seen as an import as part of 'schemas'. Scroll down for more...

from random import randrange
from typing import Optional
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends
import psycopg2 
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models, schemas
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
@app.get("/posts") 
def posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts

# We are adding some code to the path parameter: 'response_model ='. As noted above we are now importing 'schemas' for our Post model.
# this code basically says 'Here is the model we want to send data back to the user in'. It allows us to control what the user gets back
# instead of just sending them the entire row/table from the database. Much in the same way we dictate what data the user must send
# us when creating/updating a post.

# We also changed the 'post' variable in the path operation to link it to the new location of the 'Post' class which is now called
# 'PostCreate.

# create a new post
@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model= schemas.Post) 
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    new_post=models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

# Get a single post
@app.get("/posts/{id}")   
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

    