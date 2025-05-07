#Using processdata in main, minimalistic code, just running the functions
#and getting the values/classes I need.
#add "google sheet export" Boolean in user_input
from config_data import db_engine, db_connection
from db_base import Base

#SQL imports
from sqlalchemy.orm import sessionmaker



#my stuff
from functions.sql_functions import *

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
DB_MATCHHISTORY = MATCHHISTORY()

#create tables if not in sql
Base.metadata.create_all(db_engine)



#import
from process_data.process_data import classes_player
#getting list of classes player
classes_player = classes_player
#function to insert or update player
insert_or_update_player("player" ,db_connection, classes_player=classes_player)

#####REMOVE#######
#import
#from process_data.process_data import classes_matchhistory
#getting dict of classes matches/playerstats/objectives
#classes_matchhistory = classes_matchhistory
#function to insert or update matchdatas
#insert_or_update_player("matchhistory" ,db_connection, matchhistories=classes_matchhistory)
#####REMOVE#######

#import
from process_data.process_data import dict_matches
#getting dict of classes matches/playerstats/objectives
dict_matches = dict_matches
#function to insert or update matchdatas
insert_or_update_player("match" ,db_connection, dict_matches=dict_matches)
#insert_or_update_player("playerstats" ,db_connection, dict_matches=dict_matches)
#insert_or_update_player("objectives" ,db_connection, dict_matches=dict_matches)

#import
from process_data.process_data import list_champpools
#getting list of classes champpools
classes_champpool = list_champpools
#function to insert or update champool
#insert_or_update_player("champpool" ,db_connection, classes_champpool=classes_champpool)

#import
from process_data.playerinfo import export as list_playerinfos_class
#getting list of classes playerinfo
classes_playerinfo = list_playerinfos_class
#function to insert or update playerinfo
#insert_or_update_player("playerinfo", db_connection, classes_playerinfo=classes_playerinfo)








#close session with sql
session.close()

