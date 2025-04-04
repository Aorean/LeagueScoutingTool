#Using processdata in main, minimalistic code, just running the functions
#and getting the values/classes I need.
#add "google sheet export" Boolean in user_input
from config import *

#SQL imports
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


#my stuff
from backend.process_data.process_data import classes_player, dict_matches, list_champpools
from backend.functions.sql_functions import *



#connection to postgrsql
db_engine = create_engine(conn_url)

#table classes
DB_PLAYER = PLAYER
DB_MATCH = MATCH
DB_PLAYERSTATS = PLAYERSTATS
DB_OBJECTIVES = OBJECTIVES
DB_CHAMPPOOL = CHAMPPOOL

#create tables if not in sql
Base.metadata.create_all(db_engine)

#def session
SessionLocal = sessionmaker(bind=db_engine, autocommit=False, autoflush=False)
#open session
session = SessionLocal()

#getting list of classes player
classes_player = classes_player
#getting dict of classes matches/playerstats/objectives
dict_matches = dict_matches
#getting list of classes champpools
classes_champpool = list_champpools

#function to insert or update player
insert_or_update_player("player" ,db_connection, classes_player=classes_player)
insert_or_update_player("match" ,db_connection, dict_matches=dict_matches)
insert_or_update_player("playerstats" ,db_connection, dict_matches=dict_matches)
insert_or_update_player("objectives" ,db_connection, dict_matches=dict_matches)
insert_or_update_player("champpool" ,db_connection, classes_champpool=classes_champpool)

#close session with sql
session.close()
