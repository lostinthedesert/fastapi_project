# We're going to start looking at authenticating users with a password. See also updates to 'utils.py' and a new login class in
# schemas.py. This file uses the same modules/imports as users and posts. Notice there are two ways to call files in the same parent
# directory: ".." paths two directories above the current directory (so the 'app' folder) or you can call 'app.[filename]'.

from http.client import HTTPException
from .. import schemas, models, database, utils
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import UserCreate


# Here's our router variable linking this file to main.py. The tag parameter sorts the documentation for our website 
# (http://127.0.0.1:8000/docs) into categories. This is a feature of fastapi and allows users to look under the hood of our site
# for more technical description of the code being used to build it. 

router=APIRouter(tags=["Authentication"])

# Here is our path operation for a user to login. This is a post request and we're creating a new domain "/login". Our function 
# uses the familiar format: a pydantic model called UserLogin is linked via the schemas file and we connect to our database
# through sqlalchemy.

# So here's what we're trying to accomplish: we want the user to enter their email/password so that we can authenticate the password
# they entered to login against the hashed password we have saved in our database. So we query the database using the email they provide
# then interject an Exception if it's not found. Then the code gets interesting: by skipping straight to the 'if not' statement we 
# kill two birds with one stone. We authenticate the password or we throw another Exception if it's not a match. See utils.verify
# for how the program verifies the password but basically we created a function('verify()') that uses the .verify method of 
# 'pwd_context' (the same object we imported to do our hashing). By feeding the login password and the password on file (hashed) to 
# this object it does the work of matching them. Then we return a message if the passwords match.

@router.post("/login")
def login(credentials: schemas.UserLogin, db: Session=Depends(database.get_db)):
    user=db.query(models.User).filter(models.User.email==credentials.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="invalid credentials")
    if not utils.verify(credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="invalid credentials")
    return {"token":"sampel token"}