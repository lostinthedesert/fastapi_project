from tkinter.font import BOLD
from fastapi import Body, FastAPI

app=FastAPI()

@app.get("/") 
def root():
    return {"message": "this message will automatically reload :)"}

@app.get("/posts") 
def posts():
    return {"data":"this is your post"}

# Now we are moving on to http post requests. This will involve bouncing back and forth between VS Code and the Postman app which allows
# us to test our API by emulating a web browser, simulating a user inputing data on a hypothetical message board.

# You'll notice we are using @app.post() now instead of .get. That's because we want the user side to be able to enter data that
# our API will then gather, alter and return. .get allows the user to gather data from the API but .post allows them to actually
# send data through the API.

# Our http address has changed to /createposts. And we have defined a new function 'create_posts' Then we've got some new vocabulary:
# our parameter for 'create_posts' is a variable we have created called 'payload' that is a dictionary ('dict') which has been converted
# from the 'Body()' function within the 'fastapi' module. Up at the top you'll notice 'Body' has been imported. I don't know why the
# parameter of 'Body()' is '...'. After that we ask the function to print the 'payload' dictionary (which now contains our user generated
# data) to our console and then instruct it to return a string (("new post:" f"title: {payload['title']} content: {payload['content']}"))

# So what the hell is happening here? What you can't see is over on Postman, we have sent a post request (simulating a user) in which
# the "user" has added some data to our host server. It looks like this: {"title":"top beaches in florida", "content": "check out these 
# hot beaches"}. You can see it's in the form of a list using json protocol. Essentially the user has posted this info to our message 
# board. what our 'create_posts' function has done is gathered that info, stored it in a dictionary that it created called payload using
# a Class Object imported from fastapi called 'Body()' and converted into a library. Then our last line of code returns the data to 
# our message board in a slightly altered form: the addition of the "title" and "content" labels. 

# The f-string below follows what we learned in tkinter about parsing data from dictionaries (ie payload['title] is the title key from
# the payload dictionary and should produce the value assigned to that key and so on). So the basic idea is, we created a /createposts
# url that allowed a user to add text to the message board, which was then stored by FastAPI using a dictionary, we then posted that
# data back to the message board where the end user could once again see what they wrote but in our format.

@app.post("/createposts") 
def create_posts(payload: dict = Body(...)):
    print(payload)
    return ("new post:" f"title: {payload['title']} content: {payload['content']}")