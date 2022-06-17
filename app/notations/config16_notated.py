# this lesson will show how to set up a environment variables. So right now there is some data hard coded into our app that we
# don't want people to see. Things like our SECRET_KEY and our postgres database password. Once our code goes into production anyone
# will be able to view our code and then they will have access to this very sensitive data.

# so the solution to this is to use an enviroment variable. If you go into the windows search bar and type environments, the system
# settings will pop up that allow you to edit environment variables. Take a look. This is just a list of variables with different
# string values that are saved locally on this machine. This is the model we will use to store our secure data so that it can be 
# imported by python into our app, but not exposed for anyone to see. 

# We're going to import 'BaseSettings' from pydantic which is another schema validation model. Then we'll create a class called "Settings"
# that will define data types for all of the important variable that we want stored outside of our app code. Note the last lines of
# code in this class that refer to a file '.env'. that is the file that stores the values for these different variables and it is
# stored in the parent directory along with 'app' etc. All '.env' is is a plain text file that defines these variables. Lastly we
# import .config.py and the 'settings' variable into main.py.

# that's it. We now have our environment variables defined in a separate secure environment that will never be included with the rest
# of the files in this app. It's like the secret pass code library that makes the whole thing work.

from pydantic import BaseSettings

# LINK ENVIRONMENT VARIABLES

class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes:str

    class Config:
        env_file= ".env"

settings=Settings()