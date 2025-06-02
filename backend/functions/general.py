from backend.def_classes.summoners_rift import Player,Matchhistory,Match,Playerstats,Objectives
from backend.def_classes.howling_abyss import aram_Match, aram_Playerstats
from backend.def_classes.arena import arena_Match, arena_Playerstats
from backend.process_data.c_dragon import *
from backend.functions.psql import get_query,execute_query, filter_matchhistory
from backend.functions.api import *



def get_playerclass(riot_ids, region, api_key):
    classes_player = []
    for riot_id in riot_ids:
        puuid = get_puuid(riot_id[0], riot_id[1], region, api_key)
        class_player = Player( puuid, riot_id[0], riot_id[1])
        classes_player.append(class_player)

    return classes_player

def get_matchhistoriesclass(classes_player, region, api_key):
    classes_matchhistory = []
    for class_player in classes_player:
        puuid = class_player.puuid

        #looping get matchhistory, so it gets more data until 
        #return from api is empty



        
        
        full_matchhistory = []
        startindex = 0
        while True:
            matchhistory = get_matchhistory(region, puuid, api_key, startindex)
            print(f"Matchhistory added {startindex}")
            startindex+=100
            
            if not matchhistory:
                break

            for match in matchhistory:
                full_matchhistory.append(match)
        #add check if match is already in sql
        #query_matchid = get_query(selection="matchid",schema="playerstats", table="match")
        
        class_matchhistory = Matchhistory(puuid, full_matchhistory)  
        classes_matchhistory.append(class_matchhistory)


    return classes_matchhistory


