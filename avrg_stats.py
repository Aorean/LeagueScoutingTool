# getting data from existing sql tables, processing them and inserting them into
# classes for a new table in sql
# tables: player_arvg_stats, champpool_players
from itertools import count



from def_classes.champpool import stats_for_champpool, Champpool
from main import db_connection
from sql_functions import *

def get_data_for_champpool(db_connection):
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

    puuids = to_process[0]
    game_datas = to_process[1]

    print(game_datas)
    for puuid in puuids:
        #amount of champions
        unique_champs = []
        for game_data in game_datas:
            player = list(game_data[0])
            opponent = list(game_data[1])

            #filling unique_champs
            if puuid == player[1]:
                if player[6] not in unique_champs:
                    unique_champs.append(game_data[0][6])


            #get kda
            if player[9] > 0:
                kda = round((player[8] + player[10])/player[9],2)
                player.append(kda)
            elif player[9] == 0:
                kda =  player[8] + player[10]
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

            print(player)
            print(opponent)
        list_champpool_classes = []



        """
        for game_data in game_datas:
            if puuid == game_data[1]:
                for champ in unique_champs:
                    if champ == game_data[6]:
                        if champ in list_champpool_classes:

                        elif champ not in list_champpool_classes:
                            champ_stats = Champpool(game_data)
        """

champpool_data = get_data_for_champpool(db_connection)

get_champpool(champpool_data)


"""
def get_avrg_champpool(db_connection):
    query = get_query(querytype="select", selection="*", schema="playerdata", table="playerstats")
    select_playerstats = execute_query(db_connection=db_connection, query=query)
    #riot_ids from process_data.py
    query_player = SELECT_PK_PLAYER(db_connection)

    test = select_playerstats[0]

    list_classes_all_players = []
    print(type(test))
    print(test[0])
    classes_champpool = []
    for player in query_player:
        classes_one_player = []


        player_puuid = player[0]
        print(player_puuid)

        for matchdata in select_playerstats:



            primary_key = matchdata[0]
            puuid = matchdata[1]
            matchid = matchdata[2]
            gamertag = matchdata[3]
            tagline = matchdata[4]
            team = matchdata[5]
            champ = matchdata[6]
            role = matchdata[7]
            kills = matchdata[8]
            deaths = matchdata[9]
            assists = matchdata[10]
            cs = matchdata[11]
            level = matchdata[12]
            exp = matchdata[13]
            gold = matchdata[14]
            visionscore = matchdata[15]
            summonerspell1 = matchdata[16]
            summonerspell2 = matchdata[17]
            item1 = matchdata[18]
            item2 = matchdata[19]
            item3 = matchdata[20]
            item4 = matchdata[21]
            item5 = matchdata[22]
            item6 = matchdata[23]
            keyrune = matchdata[24]
            win = matchdata[25]

            if deaths != 0:
                kda = round((kills + assists) / deaths , 2)
            elif deaths == 0:
                kda = kills + assists

            diff_stats = {}

            for opponent in select_playerstats:
                opponent_matchid = opponent[2]
                opponent_role = opponent[7]
                opponent_puuid = opponent[1]
                if matchid+role == opponent_matchid+opponent_role:
                    if opponent_puuid != puuid:
                        opponent_cs = opponent[11]
                        opponent_level = opponent[12]
                        opponent_exp = opponent[13]
                        opponent_gold = opponent[14]
                        opponent_visionscore = opponent[15]

                        diff_stats = {
                            "cs" : cs - opponent_cs,
                            "exp": exp - opponent_exp,
                            "level" : level - opponent_level,
                            "gold" : gold - opponent_gold,
                            "visionscore" : visionscore - opponent_visionscore
                        }
                        print("diff " , diff_stats)

            stats = stats_for_champpool(matchdata, diff_stats, kda)
            stats.print_all()

            classes_one_player.append(stats)

        list_classes_all_players.append(classes_one_player)

    for player in list_classes_all_players:
        dict_champpool = {}

        unique_champs = []


        for match in player:
            if match.champ not in unique_champs:
                unique_champs.append(match.champ)


        for champion in unique_champs:

            dict_champ = {
                "puuid": [],
                "champ": [],
                "games_played": [],
                "kda": [],
                "kills": [],
                "deaths": [],
                "assists": [],
                "exp": [],
                "level": [],
                "gold": [],
                "visionscore": [],
                "exp_diff": [],
                "level_diff": [],
                "gold_diff": [],
                "visionscore_diff": [],
                "summonerspell1": [],
                "summonerspell2": [],
                "role": [],
                "win": [],
                "side": [],
            }

            for match in player:
                if match.champ == champion:
                    dict_champ["puuid"].append(player[1])
                    dict_champ["champ"].append(match.champ)
                    dict_champ["games_played"].append(1)
                    dict_champ["kda"].append(match.kda)
                    dict_champ["kills"].append(match.kills)
                    dict_champ["deaths"].append(match.deaths)
                    dict_champ["assists"].append(match.assists)
                    dict_champ["exp"].append(match.exp)
                    dict_champ["level"].append(match.level)
                    dict_champ["gold"].append(match.gold)
                    dict_champ["visionscore"].append(match.visionscore)
                    dict_champ["exp_diff"].append(match.exp_diff)
                    dict_champ["level_diff"].append(match.level_diff)
                    dict_champ["gold_diff"].append(match.gold_diff)
                    dict_champ["visionscore_diff"].append(match.visionscore_diff)
                    dict_champ["summonerspell1"].append(match.summonerspell1)
                    dict_champ["summonerspell2"].append(match.summonerspell2)
                    dict_champ["role"].append(match.role)
                    dict_champ["win"].append(match.win)
                    dict_champ["side"].append(match.side)

            dict_champ["games_played"] = sum(dict_champ["games_played"])
            dict_champ["kda"] = round(sum(dict_champ["kda"]) / len(dict_champ["kda"]),2)
            dict_champ["kills"] = round(sum(dict_champ["kills"]) / len(dict_champ["kills"]),2)
            dict_champ["deaths"] = round(sum(dict_champ["deaths"]) / len(dict_champ["deaths"]), 2)
            dict_champ["assists"] = round(sum(dict_champ["assists"]) / len(dict_champ["assists"]), 2)
            dict_champ["exp"] = round(sum(dict_champ["exp"]) / len(dict_champ["exp"]), 2)
            dict_champ["level"] = round(sum(dict_champ["level"]) / len(dict_champ["level"]), 2)
            dict_champ["gold"] = round(sum(dict_champ["gold"]) / len(dict_champ["gold"]), 2)
            dict_champ["visionscore"] = round(sum(dict_champ["visionscore"]) / len(dict_champ["visionscore"]), 2)
            dict_champ["exp_diff"] = round(sum(dict_champ["exp_diff"]) / len(dict_champ["exp_diff"]), 2)
            dict_champ["level_diff"] = round(sum(dict_champ["level_diff"]) / len(dict_champ["level_diff"]), 2)
            dict_champ["gold_diff"] = round(sum(dict_champ["gold_diff"]) / len(dict_champ["gold_diff"]), 2)
            dict_champ["visionscore_diff"] = round(sum(dict_champ["visionscore_diff"]) / len(dict_champ["visionscore_diff"]), 2)

            summonerspell1_max = ""
            summonerspell1_value = 0
            for val in dict_champ["summonerspell1"]:
                value = dict_champ["summonerspell1"].count(val)
                if value > summonerspell1_value:
                    summonerspell1_value = value
                    summonerspell1_max = val

            summonerspell2_max = ""
            summonerspell2_value = 0
            for val in dict_champ["summonerspell2"]:
                value = dict_champ["summonerspell2"].count(val)
                if value > summonerspell2_value:
                    summonerspell2_value = value
                    summonerspell2_max = val

            role_max = ""
            role_value = 0
            for val in dict_champ["role"]:
                value = dict_champ["role"].count(val)
                if value > role_value:
                    role_value = value
                    role_max = val

            dict_champ["summonerspell1"] = summonerspell1_max
            dict_champ["summonerspell2"] = summonerspell2_max
            dict_champ["role"] = role_max
            win_count = 0
            for win in dict_champ["win"]:
                if win:
                    win_count+=1



            ind_blue = 0
            ind_red = 0
            blue_count = 0
            red_count = 0
            blue_win = 0
            red_win = 0
            for side_win in dict_champ["side"]:
                if side_win == 100:
                    blue_count+=1
                    if dict_champ["win"][ind_blue]:
                        blue_win+=1

            for side_win in dict_champ["side"]:
                if side_win == 200:
                    red_count+=1
                    if dict_champ["win"][ind_red]:
                        red_win+=1

            if blue_win == 0:
                winrate_blue = 0
            elif blue_win > 0:
                winrate_blue = round(blue_count/blue_win, 4)

            if red_win == 0:
                winrate_red = 0
            elif red_win > 0:
                winrate_red = round(red_count / red_win, 4)


            winrate = round(dict_champ["games_played"] / win_count, 4)

            dict_champ["win"] = winrate

            dict_champ["winrate_blue"] = winrate_blue
            dict_champ["winrate_red"] = winrate_red

            print(dict_champ)

            Champpool(dict_champ)






            if match.champ in dict_champpool:
                champ_champpool = dict_champpool[match.champ]
                for key in champ_champpool:
                    stat = champ_champpool[key]










    return classes_champpool



test = get_avrg_champpool(db_connection)
"""