# this is an edit to the get_current_user function. Before that function called the verify_access_token and returned the user_id. Now
# we want it to return the entire user (id, email, password, created_at)> We need to call models.py and Session from sqlalchemy.orm.

from email import header
from jose import JWTError, jwt
from datetime import datetime, timedelta

from sqlalchemy.orm import Session
from . import schemas, database, models
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status

oauth2_scheme=OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY="09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def create_access_token(data: dict):
    to_encode=data.copy()
    expire=datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    encoded_jwt=jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    try:
        payload=jwt.decode(token,SECRET_KEY, algorithms=[ALGORITHM])
        id = payload.get("user_id")
        if id is None:
            raise credentials_exception
        token_data=schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception
    return token_data

# we will add another dependancy so get_current_user connects to our database. the credential_exception variable remains the same.
# But now we redefine 'token' from the original token (stored in 'oauth2_scheme) to the returned value of 'verify_access_token' which is
# a user id. Note that in the process of redefining 'token' we also call 'verify_access_token' (while passing the old token value:
# oauth2_scheme). Once 'verify_access_token' is called, the token variable changes values to 'token_data' (user id). Then we run a query
# base on token.id and assign the resulting user to 'user' which is now the return value of 'get_current_user'. 

# Now over in posts.py we have a new dependancy variable 'current_user' which contains all the user data instead of just models.User.id.

def get_current_user(token: str=Depends(oauth2_scheme), db: Session=Depends(database.get_db)): 
    credentials_exception=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate "
    "credentials", headers={"WWW-AUTHENTICATE":"Bearer"})
    token= verify_access_token(token, credentials_exception)
    user=db.query(models.User).filter(models.User.id==token.id).first()
    
    return user