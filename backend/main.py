#Using processdata in main, minimalistic code, just running the functions
#and getting the values/classes I need.
#add "google sheet export" Boolean in user_input
from backend.config import db_engine, db_connection
from backend.db_base import Base

#SQL imports
from sqlalchemy.orm import sessionmaker


#psql
from backend.functions.psql import insert_or_update_player
from backend.def_classes.sql_tables import *

#process data
from backend.config import db_connection
from backend.functions.general import get_playerclass, get_matchhistoriesclass
from backend.functions.process import process_userinput, process_matches
import os
from dotenv import load_dotenv
from backend.PLAYGROUND import process_input

from backend.process_data.avrg_stats import *

from backend.process_data.playerinfo import get_playerinfo_classes

load_dotenv()
api_key = os.environ.get("api_key")

#read user_input
user_input = []
with open("C:\\Users\\joels\\Desktop\\LeagueScoutingTool\\backend\\user_input", "r") as f:
    for line in f:
        user_input.append(line)


def run_main(user_input, api_key, db_connection):
    #use function to get data for API
    api_data = process_input(user_input)
    region = api_data[0]
    riot_ids = api_data[1]





    #call riot api for puuids and save it in a list of classes "classes_player"
    classes_player = get_playerclass(riot_ids, region, api_key)

    #call riot api for matchhistories for each player and saving it in "classes_matchhistory"
    classes_matchhistory = get_matchhistoriesclass(classes_player, region, api_key)

    #call riot api for single matches and saving it in a dict
    dict_matches = process_matches(classes_matchhistory, region, api_key, db_connection)

    #process matchdata from playerstats to get important data for champpools
    champpool_data = get_data_for_champpool(db_connection)
    #taking the above data and processing it into classes, getting a list of classes
    classes_champpool = get_champpool(champpool_data)

    #getting list of classes playerinfo
    classes_playerinfo = get_playerinfo_classes(db_connection, api_key)


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



    #function to insert or update player
    insert_or_update_player("player" ,db_connection, classes_player=classes_player)

    #function to insert or update matchdatas
    insert_or_update_player("match" ,db_connection, dict_matches=dict_matches)
    insert_or_update_player("playerstats" ,db_connection, dict_matches=dict_matches)
    insert_or_update_player("objectives" ,db_connection, dict_matches=dict_matches)

    #function to insert or update champool
    insert_or_update_player("champpool" ,db_connection, classes_champpool=classes_champpool)

    #function to insert or update playerinfo
    insert_or_update_player("playerinfo", db_connection, classes_playerinfo=classes_playerinfo)


    #close session with sql
    session.close()

