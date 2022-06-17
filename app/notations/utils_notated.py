# Here is our self created password hashing module that includes importing passlib. All of this is copy/paste code from the passlib
# docs, including the below function 'hash' which will perform the hashing action for our user's password.

from passlib.context import CryptContext

pwd_context=CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password: str):
    return pwd_context.hash(password)