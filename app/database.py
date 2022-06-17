from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import time
from .config import settings
#import psycopg2 
#from psycopg2.extras import RealDictCursor

# connection string
SQLALCHEMY_DATABASE_URL =f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}'

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


# OLD FASTAPI CONNECTION CODE (BEFORE SQLALCHEMY)
#while True:

#   try:
#      conn=psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='dummy123', 
#        cursor_factory=RealDictCursor)
#        cursor=conn.cursor()
#        print('database connection was successful')
#        break
#    except Exception as error:
#        print('connecting to database failed')
#        print('error was ', error)
#        time.sleep(2)