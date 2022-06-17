# Continuing from main14_notated.py here is the rest of our new router code. We have imported a new object from fastapi: APIRouter.
# And we have defined a new variable below: 'router'. Note that 'router' has replaced 'app' as the new decorator variable in our
# path operators. Now when our main.py file receives a front end request, the 'include_router' objects in main.py will direct it to this
# file and 'users.py' to handle all relevant requests. 'posts.py' and users.py are now arms of the main.py file. All relevant modules 
# have been imported to the new router files.

from typing import List
from .. import schemas, models, utils
from ..database import SessionLocal, get_db
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

router=APIRouter()

# Get all posts
@router.get("/posts", response_model= List[schemas.Post]) 
def posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts

# create a new post
@router.post("/posts", status_code=status.HTTP_201_CREATED, response_model= schemas.Post) 
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    new_post=models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

# Get a single post
@router.get("/posts/{id}", response_model= schemas.Post)   
def get_post(id: int, db: Session = Depends(get_db)):
    one_post=db.query(models.Post).filter(models.Post.id==id).first()   
    if not one_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{id} not found") 
    return one_post

# Delete a post
@router.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)   
def delete_post(id: int, db: Session = Depends(get_db)): 
    one_post=db.query(models.Post).filter(models.Post.id==id)
    if one_post.first()==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{id} not found")  
    one_post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# Update a post
@router.put("/posts/{id}", status_code=status.HTTP_202_ACCEPTED, response_model= schemas.Post)   
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db)): 
    one_post=db.query(models.Post).filter(models.Post.id==id)
    update_post = one_post.first()
    if update_post ==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{id} not found")
    one_post.update(post.dict(), synchronize_session=False)
    db.commit()
    return one_post.first()