# we are going to take what we learned in the sql join.txt file and apply it to our code using sqlalchemy to joing tables and return reslults to the user that will include a vote count. We've imported 'func' form sqlalachemy and created a new PostOut schema in schemas.

# we also need to note here that when we query a joined table, the data returned is all shuffled up. It doesn't come back nice and neat like our regular queries do that come straight from our pydantic models. The values are all out of order and since we're creating a new column to count the number of votes each post has, we are left with an extra column value ("votes") that we don't yet have a schema for. 

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

# here is our new query. It's a long one. But remember all this is is sql code that's been converted into sqlalchemy syntax. So we're still performing our same basic database query: select post_id, count(post_id) as votes from posts LEFT JOIN votes on post.id=post_id group by post_id. so note how that reads in sqlalchemy. The big differences are the 'func.count' syntax to add 'COUNT' to the results and '.label' to rename 'COUNT' "votes". by default sqlalchemy does a LEFT JOIN but we have to specify 'isouter' because sqlalchemy does INNER JOIN by default (we've been working with outer join). And then 'group_by' is pretty much the same as sql. Then we apply our old filters to allow the user to limit,skip,search. And that's it! Check out schemas_notated.py for an explanation of the new response model schema.

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

# also updated get single post using the same new code. just tacked on the .filter to include the user provided post.id.

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