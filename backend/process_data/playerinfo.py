from backend.functions.api import get_summoner_id, get_rank
from backend.functions.psql import get_query, execute_query
from backend.def_classes.summoners_rift import Playerinfo


import os
from dotenv import load_dotenv
from backend.config import db_connection


load_dotenv()
api_key = os.environ.get("api_key")

query_puuids = get_query(querytype="select", selection="puuid", schema="playerdata", table="player")

puuids = execute_query(db_connection, query_puuids)


json_playerinfos = []
for puuid in puuids:
    puuid[0]
    json_summonerid = get_summoner_id(region="EUW1", puuid=puuid[0], api_key=api_key)

    summonerid = json_summonerid["id"]
    json_rank = get_rank(region="EUW1", summoner_id=summonerid, api_key=api_key)

    json_playerinfo = [json_summonerid,json_rank]
    json_playerinfos.append(json_playerinfo)

list_playerinfos_class =[]
for playerinfo in json_playerinfos:
    playerinfo_class = Playerinfo(playerinfo)
    list_playerinfos_class.append(playerinfo_class)






export = list_playerinfos_class
