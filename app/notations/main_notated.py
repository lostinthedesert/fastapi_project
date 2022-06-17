# importing FastAPI which will handle all the functions we create, basically translating them into json and adding them to our server
# (this computer)

from fastapi import FastAPI

# create a variable for FastAPI
app=FastAPI()

# Decorator function that will feed inner functions to FastAPI. '.get' is an HTTP request method. Since we are dealing with APIs that
# communicate over the internet, http is used as a language to facilitate that communication. The argument '/' signals that we are
# directing our function to perform some action in the root directory of our server. In this case to return the message 'this message
# will automatically reload'. These decorators are called 'path operators' because they are directed at some path, in this case an
# http address.

# Sidenote: we created our server by running the following command in the command prompt: uvicorn main:app --reload. That returns some
# output including the http address of our server: http://127.0.0.1:8000 (which is the universal ip address of the local machine). 
# uvicorn is part of the documentation provided by the FastAPI developers that is required to use FastAPI and can be found on their
# website along with instructions for setting up a server with FastAPI. From now on when we feed code into the @app decorator,
# it will end up affecting this server. (note: the '--reload' tag at the end of the uvicorn command causes the server to update
# every time our source python file changes)

@app.get("/") 
def root():
    return {"message": "this message will automatically reload :)"}

# Same code here except this time we are focusing on the /posts folder of our server. We define a new function 'posts()' and add
# a new message. now when we go to http://127.0.0.1:8000/posts the following message will appear. We are basically creating new 
# http addresses every time we run a function in this manner.

@app.get("/posts") 
def posts():
    return {"data":"this is your post"}