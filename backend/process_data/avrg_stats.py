# getting data from existing sql tables, processing them and inserting them into
# classes for a new table in sql
# tables: player_arvg_stats, champpool_players


import json

from backend.def_classes.summoners_rift import Champpool
from backend.config import db_connection
from backend.functions.psql import *
from backend.functions.process import filter_earlyffs, get_seasons_by_player, matching_opponents, sort_data_by_season, get_unique_champs, append_diff_stats, create_champpool_classes


# getting data from existing sql tables, processing them and inserting them into
# classes for a new table in sql
# tables: player_arvg_stats, champpool_players

from backend.def_classes.summoners_rift import Champpool
from backend.config import db_connection
from backend.functions.psql import *










def get_data_for_champpool(db):
    #get matches from "playerstats" table
    query_playerstats = get_query(querytype="select", selection="*", schema="playerdata", table="playerstats")
    select_playerstats = execute_query(db_connection=db_connection, query=query_playerstats)

    #get "player" table
    query_player = get_query(querytype="select", selection="puuid", schema="playerdata", table="player")
    select_player = execute_query(db_connection=db_connection, query=query_player)

    #get "match" table
    query_match = get_query(querytype="select_where", selection="matchid, season, earlysurrender", schema="playerdata", table="match", column="earlysurrender", value="false")
    select_matchids = execute_query(db_connection=db_connection, query=query_match)

    all_puuid = []
    #put all puuids in a list
    for v in select_player:
        all_puuid.append(v[0])


    all_matches = []
    #put all matches in a list
    for match in select_matchids:
        all_matches.append(match)
    
    all_playerstats = []
    #put all playerstats in a list
    for playerstats in select_playerstats:
        all_playerstats.append(playerstats)

    #filter matches and playerstats to only include no remake games and ranked
    filter_earlyff = filter_earlyffs(all_matches, all_playerstats)

    no_earlyff_rank_matches = filter_earlyff[0]   
    no_earlyff_rank_playerstats = filter_earlyff[1]   

    #getting unique seasons played by player
    #output is a dict with {puuid1: [season1, season2, ...], puuid2: [season1, season2, ...]}
    seasons_by_player = get_seasons_by_player(all_puuid, all_playerstats)

    #sort by matches, return [[[playerA1, playerA2,...], [playerB1, playerB2,...]]...],]
    puuid_matched_stats = matching_opponents(all_puuid, no_earlyff_rank_playerstats)

    return_dict = sort_data_by_season(seasons_by_player, puuid_matched_stats)

    with open("season_test.json", "w") as f:
        json.dump(return_dict, f, indent=4)

    return return_dict


def get_champpool(to_process):

    unique_champs_puuid = get_unique_champs(to_process)

    append_diff_stats(to_process)

    all_champpools = create_champpool_classes(unique_champs_puuid, to_process)



    return all_champpools
