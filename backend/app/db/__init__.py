import os
import sys
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

# Determine the parent directory for the database file path
parent = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db_path = f'{parent}/database.sqlite3'
print("Database Path:", db_path)  # Debug line

# Create the SQLAlchemy engine
engine = create_engine(f'sqlite:///{db_path}', echo=True)
Base = declarative_base()

# Define your model
class School(Base):
    __tablename__ = "woot"
    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __init__(self, name):
        self.name = name

# Create all tables
Base.metadata.create_all(engine)

# Setup the session
session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

class Model(object):
    query = session.query_property()
