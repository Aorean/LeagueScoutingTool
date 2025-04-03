import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, insert
from sqlalchemy.orm import sessionmaker, declarative_base
import psycopg2
from sql_functions import *

load_dotenv()
#Login for Database
db_username = os.environ.get("db_username")
db_host = os.environ.get("db_host")
db_port = os.environ.get("db_port")
db_name = os.environ.get("db_name")
db_password = os.environ.get("db_password")

db_connection = [
                    db_name,
                    db_username,
                    db_password,
                    db_host,
                    db_port
                 ]

conn_url = create_db_connection_string(db_username, db_password, db_host, db_port, db_name)


