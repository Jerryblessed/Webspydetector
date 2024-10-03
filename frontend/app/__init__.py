from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker
import sys

parent = "/".join(sys.path[0].split("/")[:-2])
engine = create_engine('sqlite:////{}/database.sqlite3'.format(parent))  # Remove 'convert_unicode=True'
metadata = MetaData()  # No need to bind the engine here
session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

class Model(object):
    query = session.query_property()

# When you need to use metadata, bind it manually
metadata.bind = engine
