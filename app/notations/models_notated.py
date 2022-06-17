# this is a python file we created along with database.py that assists our code in using sqlalchemy to translate python commands
# into sql commands. We are essentially teaching sqlalchemy our posts template and building a table the way we did in PGadmin.
# Notice how we define our column values and set nullable/primary key/etc. properties. We even imported our unique database.py file
# into this module to link it up with the rest of the sqlalchemy database connection code. All this information exists and was copied
# from the fastapi website under sqlalchemy documentation which i have bookmarked.

# Careful with those imported classes. When i first created this file, VS code tried to pull 'Boolean' and 'String' from the wrong modules
# and completely crashed the app.

from sqlalchemy import Column, Integer, Boolean, String
from .database import Base

class Post(Base):
    __tablename__= 'posts'

    id=Column(Integer, primary_key=True, nullable=False)
    title=Column(String, nullable=False)
    content=Column(String, nullable=False)
    published=Column(Boolean, default=True)
