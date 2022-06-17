# this is going to be complicated. So this lesson deals with actually using our jwt token to grant users access to perform certain 
# actions on our website. This notation doc should be cross referenced with the other docs that start with 'token_' in the file
# name because there is code being swapped across multiple project files here. But there is a clear chain of events being followed
# throughout this process. I'm going to start at 'oauth2.py' because it is the hub of the action but not necessarily the starting point.

# let me just lay out the basic idea here: so our user now has a jwt token because they logged in with the correct username/password.
# Now if they want to say, create a new post, they will have to provide the token (which will be authenticated per jwt token rules).
# that's accomplished by adding a dependancy to the 'create_post' function parameter that requires a user_id extracted from the token.
# But how we get there is a bit complex, so read on.

# anyway, lets import 'oauth2passwordbearer' and some familiar fastapi objects.

from email import header
from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status

# Very important path back to our 'login' domain and the access_token created there. This allows 'get_access_token' to be called.
oauth2_scheme=OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY="09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# also note we've corrected the datetime method to 'utcnow()'

def create_access_token(data: dict):
    to_encode=data.copy()
    expire=datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    encoded_jwt=jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

# here is our new code. The following two function work hand in hand to validate the token being returned by the user. essentially
# 'verify_access_token' is receiving the token (in the form of the string we created using 'create_access_token' above) and decoding it,
# converting it back to its original parts which remember consist of a user_id, an "exp" value, SECRET_KEY, and our algorithm. Then
# we are going to extract that 'user_id' which was passed to the 'create_access_token' function by the 'login' function over in
# auth.py. We throw an exception if there is no id (which means the token isn't valid). We validate the id type against a 'TokenData'
# schema that we have created for this function and we return the user_id as the variable 'token_data'. Here we are only extracting
# user id but if we wanted we could add/extract more data from the token.

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

# but where did the 'token' and 'credentials_exception' parameters come from and what called the 'verify_access_token' function?
# 'get_current_user did all that for us! this function defines the error message if we are unable to extract an id from a (invalid)
# token (some of this is just copy/paste jargon that I don't necessarily understand). and it calls the 'verify_access_token' fucntion.
# But wait! What is the 'token' dependancy? Well follow the crumbs. You can see that token is a type 'str=Depends(oauth2_scheme)'.
# and if we look at the top of this file we'll see that oauth2_shceme links us to the 'login' path operation in 'auth.py'. And what
# does the 'login()' function in the '/login' path operation return??  The access_token!!! So that's where 'verify_access_token' gets
# its 'token' parameter from: The original token value returned to the user upon successfully providing their username (email)/password.

# Now the question becomes, where did this 'get_current_user' get called from? slide over to 'token_posts.py' to find out.

def get_current_user(token: str=Depends(oauth2_scheme)):
    credentials_exception=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate "
    "credentials", headers={"WWW-AUTHENTICATE":"Bearer"})
    return verify_access_token(token, credentials_exception)
