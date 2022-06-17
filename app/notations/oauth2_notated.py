# This is our new  module for creating jwt tokens. See jwt.txt for notes on jwt tokens. We have installed 'jose' which fastapi docs
# recommends for jwt tokens and followed a lot of instructions to code this file. The 'SECRET_KEY' is just a random string that I 
# copy pasted from the fastapi docs page on oauth2, also the algorithm and token_expire_minutes are copied from their recommendations.

# then we go on to define a function 'create_access_token' which will require us to pass a parameter in the form of a dictionary. 
# we create a variable 'to_encode' which for some reason i don't understand must be a .copy() of our data dictionary. next we have to
# create a variable that represents the expiration date of our jwt token. For that we have imported a datetime module that will allow
# us to set a time starting at the token's creation plus 30 minutes. Note the syntax of the 'datetime' and timedelta objects.

# so what's going to happen is, this function will be called inside another function in our auth.py file. That parent function will
# provide the 'data' key/values. But we want to add another key right now called "exp" and set it's value equal to our 'expire' variable.
# and then we want to call our new 'jwt' object with the .encode() method and pass it our 'data' variable (a dictionary), our 
# 'SECRET_KEY' (see variable above) and the alogrithm 'HS256'. 'jwt()' is going to take those variables and encode them to make our 
# token that will then be used by the user to authenticate their credentials. 

# See auth2_notated.py for the rest of this equation (NOT oauth2_notated.py)

from jose import JWTError, jwt
from datetime import datetime, timedelta


SECRET_KEY="09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode=data.copy()
    expire=datetime.now()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    encoded_jwt=jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt