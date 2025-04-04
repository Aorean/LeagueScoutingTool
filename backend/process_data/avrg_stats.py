# getting data from existing sql tables, processing them and inserting them into
# classes for a new table in sql
# tables: player_arvg_stats, champpool_players

from backend.def_classes.champpool import Champpool
from backend.config import db_connection
from backend.functions.sql_functions import *

def get_data_for_champpool(db):
    #get matches from "playerstats" table
    query_playerstats = get_query(querytype="select", selection="*", schema="playerdata", table="playerstats")
    select_playerstats = execute_query(db_connection=db_connection, query=query_playerstats)

    #get "player" table
    query_player = get_query(querytype="select", selection="puuid", schema="playerdata", table="player")
    select_player = execute_query(db_connection=db_connection, query=query_player)


    list_puuid = []

    #cleanup "player" tuple (remove "(...,)"
    for v in select_player:
        list_puuid.append(v[0])

    champpool_data = []
    for puuid in list_puuid:

        for matchdata in select_playerstats:


            if puuid == matchdata[1]:
                champpool_data.append([matchdata])

    for gamedata in champpool_data:
        for matchdata in select_playerstats:

            if gamedata[0][2] == matchdata[2] and gamedata[0][7] == matchdata[7]:
                if gamedata[0][1] != matchdata[1]:
                    gamedata.append(matchdata)

    to_process =[list_puuid, champpool_data]

    return to_process

def get_champpool(to_process):
    amnt_players = len(to_process[1])
    all_champpools = []
    puuids = to_process[0]
    game_datas = to_process[1]


    for puuid in puuids:


        #amount of champions
        unique_champs = []

        matchdata_player = []
        for game_data in game_datas:
            player = list(game_data[0])
            opponent = list(game_data[1])

            #filling unique_champs
            if puuid == player[1]:
                if player[6] not in unique_champs:
                    unique_champs.append(game_data[0][6])


            #get kda
            try:
                kda = round((player[8] + player[10]) / player[9], 2)
                player.append(kda)
            except ZeroDivisionError as e:
                kda = player[8] + player[10]
                player.append(kda)


            #getting diff stats
            #kills
            kills_diff = player[8] - opponent[8]
            player.append(kills_diff)
            #deaths
            deaths_diff = player[9] - opponent[9]
            player.append(deaths_diff)
            #assists
            assists_diff = player[10] - opponent[10]
            player.append(assists_diff)
            #cs
            cs_diff = player[11] - opponent[11]
            player.append(cs_diff)
            #level
            level_diff = player[12] - opponent[12]
            player.append(level_diff)
            #exp
            exp_diff = player[13] - opponent[13]
            player.append(exp_diff)
            #gold
            gold_diff = player[14] - opponent[14]
            player.append(gold_diff)
            #visionscore
            visionscore_diff = player[15] - opponent[15]
            player.append(visionscore_diff)

            matchdata_player.append(player)


        list_champpool_classes = []

        for champ in unique_champs:
            single_champ = Champpool(champ, puuid)
            list_champpool_classes.append(single_champ)



        for match_data in matchdata_player:
            for champ_class in list_champpool_classes:

                if match_data[6] == champ_class.champ and match_data[1] == champ_class.puuid:
                    champ_class.count()
                    champ_class.name = match_data[3]
                    champ_class.tagline = match_data[4]
                    champ_class.kda.append(match_data[26])
                    champ_class.kills.append(match_data[8])
                    champ_class.deaths.append(match_data[9])
                    champ_class.assists.append(match_data[10])
                    champ_class.cs.append(match_data[11])
                    champ_class.exp.append(match_data[13])
                    champ_class.level.append(match_data[12])
                    champ_class.gold.append(match_data[14])
                    champ_class.visionscore.append(match_data[15])
                    champ_class.cs_diff.append(match_data[30])
                    champ_class.exp_diff.append(match_data[32])
                    champ_class.level_diff.append(match_data[31])
                    champ_class.gold_diff.append(match_data[33])
                    champ_class.visionscore_diff.append(match_data[34])
                    champ_class.summonerspell1.append(match_data[16])
                    champ_class.summonerspell2.append(match_data[17])
                    champ_class.fav_role.append(match_data[7])
                    champ_class.team.append(match_data[5])
                    champ_class.winrate.append(match_data[25])

        for champ_class in list_champpool_classes:
            champ_class.avarage_stats()
            champ_class.print_all()

            all_champpools.append(champ_class)

    return all_champpools
