# continuing to look at relational database functions. We have now joined models.users and models.posts through the 
# foreign key 'owner_id' so when a user makes a post they have their user id attached to it along with title, content
# etc. We also want to look at restricting actions based on the user currently logged in. For example we don't want to let a
# user delete or update any post, only the ones they created. This involves updating our 'posts' table in the models.py
# to include the new column 'owner_id' and updating the schemas.Post so the owner_id is returned to the user.

from pyexpat import model
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

# we've updated get all posts so that it only returns the posts created by the logged in user. notice how the db.query filters
# to match the owner_id and crrent_user.id.

# Get all posts
@router.get("/", response_model= List[schemas.Post]) 
def posts(db: Session = Depends(get_db), current_user: int=Depends(oauth2.get_current_user)):
    posts = db.query(models.Post).filter(models.Post.owner_id==current_user.id).all()
    return posts

# this is a bit more complicated than the other updates but still pretty simple. basically we want to make sure we have an owner_id
# available when a user creates a new post becuase that column is non-nullable. So what we'll do is pull the user's id from 
# current_user and add it to models.Post (which now includes the owner_id column). you can see how simple that operation is.

# create a new post
@router.post("/", status_code=status.HTTP_201_CREATED, response_model= schemas.Post) 
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int=Depends(oauth2.get_current_user)):
    new_post=models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

## Here we throw an http exception if the user tries to view posts not made by them 

# Get a single post
@router.get("/{id}", response_model= schemas.Post)   
def get_post(id: int, db: Session = Depends(get_db), current_user: int=Depends(oauth2.get_current_user)):
    one_post=db.query(models.Post).filter(models.Post.id==id).first()   
    post=one_post.first()
    if not one_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{id} not found") 
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    return one_post

# same logic: user can only delete their posts and http exception added, notice the syntax for sniffing out a mismatch id.

# Delete a post
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)   
def delete_post(id: int, db: Session = Depends(get_db), current_user: int=Depends(oauth2.get_current_user)): 
    one_post=db.query(models.Post).filter(models.Post.id==id)
    delete_post=one_post.first()
    if one_post.first()==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{id} not found")  
    if delete_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    one_post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# same logic again

# Update a post
@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED, response_model= schemas.Post)   
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int=Depends(oauth2.get_current_user)): 
    one_post=db.query(models.Post).filter(models.Post.id==id)
    update_post = one_post.first()
    if update_post ==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{id} not found")
    if update_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    one_post.update(post.dict(), synchronize_session=False)
    db.commit()
    return one_post.first()