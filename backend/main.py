#Using processdata in main, minimalistic code, just running the functions
#and getting the values/classes I need.
#add "google sheet export" Boolean in user_input
from config_data import db_engine, db_connection
from db_base import Base
#SQL imports
from sqlalchemy.orm import sessionmaker



#my stuff
from process_data.process_data import classes_player, dict_matches, list_champpools
from functions.sql_functions import *
from process_data.playerinfo import export as list_playerinfos_class
from def_classes.sql_tables import *




#def session
SessionLocal = sessionmaker(bind=db_engine, autocommit=False, autoflush=False)
#open session
session = SessionLocal()

#table classes
DB_PLAYER = PLAYER()
DB_MATCH = MATCH()
DB_PLAYERSTATS = PLAYERSTATS()
DB_OBJECTIVES = OBJECTIVES()
DB_CHAMPPOOL = CHAMPPOOL()
DB_PLAYERINFO = PLAYERINFO()

#create tables if not in sql
Base.metadata.create_all(db_engine)

#getting list of classes player
classes_player = classes_player
#getting dict of classes matches/playerstats/objectives
dict_matches = dict_matches
#getting list of classes champpools
classes_champpool = list_champpools
#getting list of classes playerinfo
classes_playerinfo = list_playerinfos_class

#function to insert or update player
insert_or_update_player("player" ,db_connection, classes_player=classes_player)
insert_or_update_player("match" ,db_connection, dict_matches=dict_matches)
insert_or_update_player("playerstats" ,db_connection, dict_matches=dict_matches)
insert_or_update_player("objectives" ,db_connection, dict_matches=dict_matches)
insert_or_update_player("champpool" ,db_connection, classes_champpool=classes_champpool)
insert_or_update_player("playerinfo", db_connection, classes_playerinfo=classes_playerinfo)




#close session with sql
session.close()

