# this lesson looks at creating a voting function to allow users to like and unlike a post. We have created a new router just like we did for post,auth, etc. We have also created a new shcemas.Vote which includes an interesting type: dir: conint(le=1). This translates to 'dir' must be an integer that is less than 1. So we are imposing a rule that the user can like a post or if they liked it before but want to change their mind and unlike it they can do that. 1 will be a like, 0 will be an unlike. Hence we only want the user to have 2 possible inputs for this integer.

# we also created a new models.Votes. This is a new type of table: it has two primary keys! That's called a conditional key I believe and basically it will help us avoid duplicates where two columns in our table both have the same value. So in this scenario we don't want a user to vote more than once on any given post. Our table consists of only two columns: user_id and post_id so to ensure a user hasn't voted twice, the table won't allow an entry when that same user_id/post_id values already exist in the same row. Also, both rows are foreign keys, so they get their value from other tables: user_id from 'users.id' and post_id from 'posts.id' And so the logic is that when a user votes on a post, their user id and the post id of the post they liked will be entered in the Votes table and the existence of that row signifies their vote. If they want to unlike a post, that row would be deleted from the Votes table.

from fastapi import Body, FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from app import database
from .. import schemas, models, utils, oauth2

# Standard router code and docs tag

router=APIRouter(
    prefix="/vote",
    tags=["Vote"]
)

# So here's our function. We start by setting up dependancies: our vote schema, our database session and our usual current_user data. Then we query our Votes table to determine if a row already exists for this vote (in other words has the user already voted on this post). We save the query to the found_vote variable using the .first() method to make it actionable. If they tried to vote and the query brought back a result, they get an HTTP exception. Otherwise we update the Votes table to include their vote. Take note of the syntax to update a table: it's so short and simple and you can include multiple column values in the arguments. Don't forget as always to db.add() and db.commit().

# If the user provides 0 as the vote.dir (note how we use an else statement instead of 'if vote.dir ==0' since 0 is the only other option) and the vote doesn't exist, they get an exception. Otherwise we simply .delete() and .commit() the changes. Notice how we apply the .delete() method to 'query' and not 'found_vote'. That's counterintuitive to me but is the form of the query that .delete always works with so remember to use that going forward to avoid errors. And again we .commit() the delete and we're done.

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session=Depends(database.get_db), current_user: int=Depends(oauth2.get_current_user)):
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

# i wanted to take a moment to just pontificate about the fascinating logic of a function like this. it's quite creative how the engineer devised a database scheme to express this operation. If you had asked me how to translate a voting function into python I don't think i could have come up with an answer this elegant and straigtforward. I think a lot of software engineering is like this: problem solving that is directly to the point and above all else efficient. That doesn't mean it's necessarily intuitive though.

# take the starting point of this function for example. It starts by defining the actions to perform if the user is breaking the rules. It asks "does this vote already exist? If so, here's your error message" then it goes on to say "ok you haven't broken the rule, so here's what we're going to do." And it follow that scheme for two separate parts of the function. That is to say, let's make sure you didn't make a mistake first, then we'll perform your requested action. And that's the most efficient way to do it. Sometimes I'll be practicing coding and it will seem so roundabout and convoluted and verbose and I just know I'm not doing this right. I'm taking the long way. but discovering the shortest line between two points is really the challenge here.