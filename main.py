#Using processdata in main, minimalistic code, just running the functions
#and getting the values/classes I need.
#add "google sheet export" Boolean in user_input
from config import *

#SQL imports
import psycopg2
from sqlalchemy import create_engine, insert
from sqlalchemy.orm import sessionmaker, declarative_base


#my stuff
from process_data import classes_player, dict_matches
from sql_tables import PLAYER, MATCH, PLAYERSTATS, OBJECTIVES, CHAMPPOOL, Base
from sql_functions import *
from avrg_stats import list_champpools

#dotenv
from dotenv import load_dotenv
import os

load_dotenv()






#connection to postgrsql

db_engine = create_engine(conn_url)

#table classes
DB_PLAYER = PLAYER
DB_MATCH = MATCH
DB_PLAYERSTATS = PLAYERSTATS
DB_OBJECTIVES = OBJECTIVES
DB_CHAMPPOOL = CHAMPPOOL
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

classes_champpool = list_champpools

#function to insert or update player
insert_or_update_player("player" ,db_connection, classes_player=classes_player)
insert_or_update_player("match" ,db_connection, dict_matches=dict_matches)
insert_or_update_player("playerstats" ,db_connection, dict_matches=dict_matches)
insert_or_update_player("objectives" ,db_connection, dict_matches=dict_matches)
insert_or_update_player("champpool" ,db_connection, classes_champpool=classes_champpool)



session.close()
