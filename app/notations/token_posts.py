# good old familiar posts.py. this is a continuation of the 'token_' series picking up from token_oauth2.py. scroll down to 'create_post'
# for the relevant new code.

from typing import List

from app import oauth2
from .. import schemas, models, utils
from ..database import SessionLocal, get_db
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

router=APIRouter(
    prefix="/posts",
    tags=["Posts"]
)
# Get all posts
@router.get("/", response_model= List[schemas.Post]) 
def posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts

# so notice in the function parameters a new 'dependancy'. by the way dependancies are what we've been working with all along.
# they simply tell the user what they must submit in order to get a response from the api. We have been using dependancies to 
# dictate what type of data (string, integer, boolean, etc.) the user could submit and in what form (dictionary) it must be 
# submitted. 'db' has also ensured that we are connected to our 'fastapi' database in order to proceed creating/updating posts. Now
# we also are requiring them to submit their validated token (in the form of a 'user_id' extracted from the decoded token). No token,
# no postin'. Everything else stayed the same.

# So now when a user wants to create a post, fastapi is going to say "where's your user_id?". And that can only be retrieved by
# going through 'get_current_user' which extracts that id number from the token received by the user upon successful login.

# Note that all this new validation comes into play on the front end. So when the user wants to create a post (using Postman
# as our framework) they must provide the token in the form of the string we returned to them upon login. What that means is in 
# postman we have to use the 'authorization' tab, choose the type 'bearer' and paste our token string into that field. Or we could
# use the 'header' tab, enter a key of 'Bearer' and a value of our token string.

# create a new post
@router.post("/", status_code=status.HTTP_201_CREATED, response_model= schemas.Post) 
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), user_id: int=Depends(oauth2.get_current_user)):
    print(user_id)
    new_post=models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

# Get a single post
@router.get("/{id}", response_model= schemas.Post)   
def get_post(id: int, db: Session = Depends(get_db)):
    one_post=db.query(models.Post).filter(models.Post.id==id).first()   
    if not one_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{id} not found") 
    return one_post

# Delete a post
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)   
def delete_post(id: int, db: Session = Depends(get_db)): 
    one_post=db.query(models.Post).filter(models.Post.id==id)
    if one_post.first()==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{id} not found")  
    one_post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# Update a post
@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED, response_model= schemas.Post)   
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db)): 
    one_post=db.query(models.Post).filter(models.Post.id==id)
    update_post = one_post.first()
    if update_post ==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{id} not found")
    one_post.update(post.dict(), synchronize_session=False)
    db.commit()
    return one_post.first()