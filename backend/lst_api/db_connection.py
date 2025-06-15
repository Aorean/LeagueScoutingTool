from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker



from backend.config import db_engine

local_session = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)

Base = declarative_base()