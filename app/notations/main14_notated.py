# Wooooah what happened to main.py?? The file has been cut down significantly. That is because we are using something called 'routers'
# to organize the project into different files. main.py is going to be our starting junction but from there we will route the operations
# to a relevant external file via a router. So if a user wants to get a post, our code will rout that request through the posts.py file
# which now contains our code for HTTP request for posts. That file and another called 'users' are in a folder in the 'app' directory
# called 'routers'. See below for the relevant code...

from random import randrange
from typing import Optional, List
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends 
import psycopg2 
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models, schemas, utils
from .database import engine, SessionLocal, get_db
from .routers import posts, users


# CONNECT TO FASTAPI DATABASE ON POSTGRES USING SQLALCHEMY
models.Base.metadata.create_all(bind=engine)

# CREATE FASTAPI VARIABLE
app=FastAPI()

# connect to fastapi database
while True:

    try:
        conn=psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='dummy123', 
        cursor_factory=RealDictCursor)
        cursor=conn.cursor()
        print('database connection was successful')
        break
    except Exception as error:
        print('connecting to database failed')
        print('error was ', error)
        time.sleep(2)

# Here is our new code. Simple. 'include_routers' is a fastAPI object that directs our program to our new 'routers' folder which contains
# the files 'posts' and 'users'. So fastAPI knows to refer to these files when receiving requests from our API. See posts/usere_notated
# for the other half of this new router code.

# CREATE ROUTERS FOR POSTS/USERS REQUESTS
app.include_router(posts.router)
app.include_router(users.router)

# Root path
@app.get("/") 
def root():
    return {"message": "this message will automatically reload :)"}
