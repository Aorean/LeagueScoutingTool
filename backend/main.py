#Using processdata in main, minimalistic code, just running the functions
#and getting the values/classes I need.
#add "google sheet export" Boolean in user_input


#SQL imports
from sqlalchemy.orm import sessionmaker

import json

#psql
from backend.functions.psql import insert_or_update_player
from backend.def_classes.sql_tables import *

from backend.config import db_engine, db_connection
from backend.db_base import Base

#process data
from backend.functions.general import get_playerclass, get_matchhistoriesclass, get_masteryclasses
from backend.functions.process import process_input                                     #, process_matches
from backend.functions.process import process_matches                                          #temporary
import os
from dotenv import load_dotenv

from backend.functions.general import create_dashboard_json
from backend.process_data.avrg_stats import *

from backend.process_data.playerinfo import get_playerinfo_classes

load_dotenv()
api_key = os.environ.get("api_key")





def run_main(user_input, api_key, db_connection):
    #use function to get data for API
    api_data = process_input(user_input)
    region = api_data[0]
    riot_ids = api_data[1]

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
    DB_MASTERY = MASTERY()
    #create tables if not in sql
    Base.metadata.create_all(db_engine)
    
    #call riot api for puuids and save it in a list of classes "classes_player"
    classes_player = get_playerclass(riot_ids, region, api_key)

    #function to insert or update player
    insert_or_update_player("player" ,db_connection, classes_player=classes_player)

    #call riot api for matchhistories for each player and saving it in "classes_matchhistory"
    classes_matchhistory = get_matchhistoriesclass(classes_player, region, api_key)

    #call riot api for single matches and saving it in a dict
    dict_matches = process_matches(classes_matchhistory, region, api_key, db_connection)

    #function to insert or update matchdatas
    insert_or_update_player("match" ,db_connection, dict_matches=dict_matches)
    insert_or_update_player("playerstats" ,db_connection, dict_matches=dict_matches)
    insert_or_update_player("objectives" ,db_connection, dict_matches=dict_matches)

    #process matchdata from playerstats to get important data for champpools
    champpool_data = get_data_for_champpool(db_connection)
    
    #taking the above data and processing it into classes, getting a list of classes
    classes_champpool = get_champpool(champpool_data)
    #function to insert or update champool
    insert_or_update_player("champpool" ,db_connection, classes_champpool=classes_champpool)

    #getting list of classes playerinfo
    classes_playerinfo = get_playerinfo_classes(db_connection, api_key)
    #function to insert or update playerinfo
    insert_or_update_player("playerinfo", db_connection, classes_playerinfo=classes_playerinfo)


    classes_mastery = get_masteryclasses(classes_player=classes_player, region=region, api_key=api_key)

    insert_or_update_player("mastery", db_connection, mastery_classes=classes_mastery)






    puuids = []
    for player in classes_player:
        puuids.append(player.puuid)

    dashboard = create_dashboard_json(puuids, db_connection)

    return_json = json.dumps(dashboard)

    session.close()




    return return_json


def json_champpool(player, db_connection):
    return_dict = {}
    return_dict["champpools"] = []
    for puuid in player:
        query = get_query("select_json", schema="playerdata", table="champpool", selection="puuid", value=puuid)
        data = execute_query(db_connection, query)
        
        return_dict["champpools"].append(data[0][0])

    return_json = json.dumps(return_dict, indent=4)

    return return_json


def json_mastery(player, db_connection):
    return_dict = {}
    return_dict["masteries"] = []
    for puuid in player:
        query = get_query("select_json", schema="playerdata", table="mastery", selection="puuid", value=puuid)
        data = execute_query(db_connection, query)
        
        return_dict["masteries"].append(data[0][0])

    return_json = json.dumps(return_dict, indent=4)

    return return_json


"""

###############DEBUGGING###############
userinput = "https://op.gg/lol/multisearch/euw?summoners=Aorean%231311%2CQaQ%2300000%2CMoris%23RIVEN%2Cihatethisnerd%23euw%2Ci+is+pidgeon%23EUW"

api_data = process_input(userinput)
region = api_data[0]
riot_ids = api_data[1]


test=run_main(userinput, api_key, db_connection)

###############DEBUGGING###############

"""