from fastapi import FastAPI 
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine
from .routers import posts, users, auth, vote
from .config import settings


# CREATE FASTAPI VARIABLE
app=FastAPI()

origins=["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# CREATE ROUTERS FOR PATH OPERATORS
app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(vote.router)

# Root path
@app.get("/") 
def root():
    return {"greetings": "this is the official pando llc homepage :)"}
