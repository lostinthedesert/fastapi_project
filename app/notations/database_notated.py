# this is a python file we created that runs the necessary scripts to connect to our postgres database using sqlalchemy. This is almost
# all copy/paste from the documentation on the fastapi website which has an entire section dedicated to sqlalchemy. Basically
# sqlalchemy is an intermediary between python and the database and allows us to send instructions to and manipulate our database
# without the need for sql or even PGadmin to create the initial table (we would still need PGadmin to set up the server and it's a
# good backend terminal for managing the database). So by using sqlalchemy we will no longer be feeding postgres sql commands, we will
# allow sqlalchemy to do that by feeding it python commands.

# I don't understand most of this code or what it's doing, but that's ok. Again this is simply a copy/paste from the documentation
# to get sql alchemy up and running and communicating with our postgres database. We did pip install sqlalchemy to acquire these
# modules.

# Also a very important side note: VS code will automatically import modules for you when you type them into your script. That's not 
# always a good thing though because it's just guessing where the classes/functions come from. For example there are numerous classes
# called "Base" and if I type that into my code without telling VS code where to source it from it's going to pick the wrong file and 
# that's going to ruin your app. So be deliberate when using outside classes and functions, make sure to tell python where to import
# them from at the top of the script.

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# connection string
SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:dummy123@localhost/fastapi'

#engine
engine = create_engine(SQLALCHEMY_DATABASE_URL) 

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# dependancy
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()