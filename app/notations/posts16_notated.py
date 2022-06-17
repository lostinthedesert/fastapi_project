# we're looking at query parameters today. a lot of this code happens on Postman so I will be referring to that. basically what this
# does is allows the user to filter requests based on some criteria. So say they only want the first 5 posts or they want to skip
# the first post in the database or they want to search by keywords in the title. All those things are accomplished by using query
# parameters. they will look familiar to anyone who has ever looked at a url. For example:

# https://www.youtube.com/watch?v=0sOvCWFmrtA&t=30723s

# let's break this down. obviously we have the domain youtube.com and the path parameter '/watch' (just like we have '/posts',
# '/login') but then what's the rest of those characters. The question mark is the begining of our query parameter. After that we
# have a parameter 'v' equal to some value that is dictating the results we are seeing on the page. the '&' separates another 
# query parameter, this one called 't' with a value of 30723s.

from operator import contains
from pyexpat import model
from typing import List, Optional

from app import oauth2
from .. import schemas, models, utils
from ..database import SessionLocal, get_db
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

router=APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

# and this is how we define query parameters. notice the new arguments in the function parameters starting with 'limit'. We have
# defined it as data type int and set a default value of 10. That means, if the user doesn't specify a limit for the number of posts
# returned by our get request, we will return the first 10. 

# Switching over to postman, the user can define their desired limit by appending this to the end of our '/posts' url:
# "?limit=3" (minus the quotation marks).
# Now when the user sends their request, they will receive only 3 results, though there may be more in the database.

# now notice how we apply this parameter to the db.query below. It is simply appended onto the query string like so: .limit(limit).all()
# the next query paramter is 'skip' and it works in the same way. It's corresponding sqlalchemy query method is .'offset()'.
# and lastly we have 'search' which we've made an optional string type and set the default as empty quotations. Notice the method in 
# the db.query is the familiar '.filter()' and the Post.title is specified as the column to be searched and then 'contains()' is
# appended to that to execute the search.

# so here is an example of a full query parameter typed out as a url:
# "{{URL}}posts?limit=3&skip=1&search=bill" (remember we are using the {{URL}} placeholder in our DEV environment in Postman)

# Get all posts
@router.get("/", response_model= List[schemas.Post]) 
def posts(db: Session = Depends(get_db), current_user: int=Depends(oauth2.get_current_user), limit: int=10,
skip: int=0, search: Optional[str]=""):
    print(limit)
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts

# create a new post
@router.post("/", status_code=status.HTTP_201_CREATED, response_model= schemas.Post) 
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int=Depends(oauth2.get_current_user)):
    new_post=models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

# Get a single post
@router.get("/{id}", response_model= schemas.Post)   
def get_post(id: int, db: Session = Depends(get_db), current_user: int=Depends(oauth2.get_current_user)):
    one_post=db.query(models.Post).filter(models.Post.id==id).first()   
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