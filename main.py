#Using processdata in main, minimalistic code, just running the functions
#and getting the values/classes I need.
#add "google sheet export" Boolean in user_input

#SQL imports
import psycopg2
from sqlalchemy import create_engine, insert
from sqlalchemy.orm import sessionmaker, declarative_base


#my stuff
from process_data import classes_player, dict_matches
from sql_tables import PLAYER, MATCH, PLAYERSTATS, OBJECTIVES, Base
from sql_functions import *

#dotenv
from dotenv import load_dotenv
import os

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


#connection to postgrsql
conn_url = create_db_connection_string(db_username, db_password, db_host, db_port, db_name)
db_engine = create_engine(conn_url)

#table classes
DB_PLAYER = PLAYER
DB_MATCH = MATCH
DB_PLAYERSTATS = PLAYERSTATS
DB_OBJECTIVES = OBJECTIVES
print(Base.metadata.tables.keys())
#create tables if not in sql
Base.metadata.create_all(db_engine)

#def session
SessionLocal = sessionmaker(bind=db_engine, autocommit=False, autoflush=False)
session = SessionLocal()

#getting list of classes
classes_player = classes_player
#getting dict of classes
dict_matches = dict_matches


#function to insert or update player
insert_or_update_player("player" ,db_connection, classes_player=classes_player)
insert_or_update_player("match" ,db_connection, dict_matches=dict_matches)
insert_or_update_player("playerstats" ,db_connection, dict_matches=dict_matches)
insert_or_update_player("objectives" ,db_connection, dict_matches=dict_matches)

#tests
get_avrg_playerstats(db_connection)


session.close()
