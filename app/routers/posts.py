from operator import contains
from typing import List, Optional

from app import oauth2
from .. import schemas, models, utils
from ..database import SessionLocal, get_db
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func

router=APIRouter(
    prefix="/posts",
    tags=["Posts"]
)
# Get all posts
@router.get("/", response_model= List[schemas.PostOut])
def posts(db: Session = Depends(get_db), current_user: int=Depends(oauth2.get_current_user), limit: int=10, skip: int=0, search: Optional[str]=""):
    
    results=query=db.query(models.Post, func.count(models.Votes.post_id).label("votes")).join(models.Votes, models.Votes.post_id==models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    return results

# create a new post
@router.post("/", status_code=status.HTTP_201_CREATED, response_model= schemas.Post) 
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int=Depends(oauth2.get_current_user)):
    new_post=models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

# Get a single post
@router.get("/{id}", response_model= schemas.PostOut)   
def get_post(id: int, db: Session = Depends(get_db), current_user: int=Depends(oauth2.get_current_user)):
    one_post=query=db.query(models.Post, func.count(models.Votes.post_id).label("votes")).join(models.Votes, models.Votes.post_id==models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id==id).first()   
    if not one_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{id} not found") 
    return one_post

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