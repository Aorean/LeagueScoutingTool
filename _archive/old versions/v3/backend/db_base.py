from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

Base = declarative_base()

def create_db_engine(conn_url):
    return create_engine(conn_url)