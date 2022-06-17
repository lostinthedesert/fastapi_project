# Here we will introduce a jwt token issuing process to our authentication procedure. This file works with oauth2.py as well as the 
# usual imports/modules. We have also imported 'OAuth2passwordrequestform' to take the place of our login schema. More on that later.

from http.client import HTTPException
from .. import schemas, models, database, utils, oauth2
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import UserCreate



router=APIRouter(tags=["Authentication"])

# Here is our updated 'login()' function. Notice we have changed our 'credentials' variable in the function parameter to the 
# 'passwordrequestform' object from fastapi.security and set a dependancy like we do with 'db'. I'm not sure why this works
# better than just calling the 'schemas.UserLogin' model but apparently that's what we have to do. Note this requestform model
# doesn't have an 'email' key. it has a 'username' and 'password' keys. We will be accepting the user's email as their username
# for our login (hence the 'credentials.username' variable later in the function). Just like before we look up the corresponding
# row in the user table and verify the password. Then things get interesting.

# we create an 'access_token' variable that consists of our 'create_access_token' function from our new oauth2.py file and pass
# in the 'user.id' value from our table. This data will be passed into our jwt token along with "exp", SECRET_KEY, and our 
# encoding algorithm to create a jwt token. Notice the weird syntax for 'create_access_token'. I don't know why we can't just
# pass the dictionary model of user_id:user.id but we also have to include 'data='. 

# Lastly we return our shiny new token to the user. The "token type":"bearer" is standard jwt token jargon I guess, not important.

# Important to note on the Postman testing side, we no longer can send login requests through the 'body' using 'raw' json. We now have to
# use 'form data' and enter key: username, value: user's email and key: password, value: user's plain password.

@router.post("/login")
def login(credentials: OAuth2PasswordRequestForm=Depends(), db: Session=Depends(database.get_db)):
    user=db.query(models.User).filter(models.User.email==credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="invalid credentials")
    if not utils.verify(credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="invalid credentials")
    access_token=oauth2.create_access_token(data={"user_id":user.id})
    return {"access token":access_token, "token type":"bearer"}