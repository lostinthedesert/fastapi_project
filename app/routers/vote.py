from fastapi import Body, FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from app import database
from .. import schemas, models, utils, oauth2

router=APIRouter(
    prefix="/vote",
    tags=["Vote"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session=Depends(database.get_db), current_user: int=Depends(oauth2.get_current_user)):
    post= db.query(models.Post).filter(models.Post.id==vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post id: {vote.post_id} does not exist")
    query=db.query(models.Votes).filter(models.Votes.post_id==vote.post_id, models.Votes.user_id==current_user.id)
    found_vote=query.first()
    if vote.dir==1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user id: {current_user.id} has already voted on post id: {vote.post_id}")
        new_vote=models.Votes(user_id=current_user.id, post_id=vote.post_id)
        db.add(new_vote)
        db.commit()
        return {"message":"successfully voted"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user has not voted on this post")
        query.delete(synchronize_session=False)
        db.commit()
        return {"message":"vote deleted"}