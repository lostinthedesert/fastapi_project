# this is the first section of the 19 hour api tutorial dealing with vs code, fastapi, postman, http methods, virtual environments
# etc. the 'main.py' file will be updated from this source so it will always exists in its latest form but i will save old versions
# of it as 'main2'/main3/etc. so we can follow the progression.

from fastapi import Body, FastAPI

app=FastAPI()

@app.get("/") 
def root():
    return {"message": "this message will automatically reload :)"}

@app.get("/posts") 
def posts():
    return {"data":"this is your post"}

@app.post("/createposts") 
def create_posts(payload: dict = Body(...)):
    print(payload)
    return ("new post: " f"title: {payload['title']} content: {payload['content']}")