# getting data from existing sql tables, processing them and inserting them into
# classes for a new table in sql
# tables: player_arvg_stats, champpool_players


import json

from backend.def_classes.summoners_rift import Champpool
from backend.config import db_connection
from backend.functions.psql import *



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

    #print(all_puuid)

    #print(all_matches)

    #print(all_playerstats)

    #filter matches and playerstats to only include no remake games and ranked
    no_earlyff_rank_matches = []
    no_earlyff_rank_playerstats = []



    for match in all_matches:
        for playerstats in all_playerstats:
            match_matchid = match[0]
            playerstats_matchid = playerstats[2]


            if match_matchid == playerstats_matchid:
                early_ff_match = match[2]

                if early_ff_match == False:
                    gamemode = playerstats[29]
                    
                    #gamemode 440 = SOLODUO, gamemode 420 = FLEX
                    if gamemode == 440 or gamemode == 420:
                        no_earlyff_rank_matches.append(match)
                        no_earlyff_rank_playerstats.append(playerstats)

    #getting unique seasons played by player

    seasons_by_player = {}
    for puuid in all_puuid:
        seasons_played = []

        for match in all_matches:
            matchid = match[0]
            season = match[1]

            if season not in seasons_played:
                seasons_played.append(season)
            elif season in seasons_played:
                continue
        
        seasons_by_player[puuid] = seasons_played



    #sort by matches, return [[[playerA1, playerA2,...], [playerB1, playerB2,...]]...],]
    puuid_matched_stats = {}
    for puuid in all_puuid:

        full_match_playerstats = []
        for playerstats in no_earlyff_rank_playerstats:
            #create a list of opponent and player
            matched_playerstats = []
            playerstats_puuid = playerstats[1]

            if puuid == playerstats_puuid:
                
                matched_playerstats.append(playerstats)
                for opponentstats in no_earlyff_rank_playerstats:
                    matchid = playerstats[2]
                    matchid_opponent = opponentstats[2]

                    role =playerstats[7]
                    role_opponent = opponentstats[7]

                    team = playerstats[5]
                    team_opponent = opponentstats[5]

                    if (
                        matchid == matchid_opponent and 
                        role == role_opponent and 
                        team != team_opponent
                    ):
                        matched_playerstats.append(opponentstats)
                        print("opponent found")

            
            if len(matched_playerstats) > 0:
                full_match_playerstats.append(matched_playerstats)

        puuid_matched_stats[puuid] = full_match_playerstats

    return_dict = {}

    for season_key in seasons_by_player:
        seasons = seasons_by_player[season_key]
        seasons_dict = {}
        for season in seasons:
            seasons_dict[season] = []
            for match_key in puuid_matched_stats:
                matched_playerstats = puuid_matched_stats[match_key]
                for matched_match in matched_playerstats:
                    print(matched_match)
                    season_match = matched_match[0][26]
                    if season == season_match:
                        seasons_dict[season].append(matched_match)

        return_dict[season_key] = seasons_dict

    with open("season_test.json", "w") as f:
        json.dump(return_dict, f, indent=4)

            

 
            
            
            













    """


    for playerdata in select_playerstats:
        matchid_player = playerdata[2]
        for match in all_matches:
            matchid_match = match[0]
            if matchid_player in matchid_match:
                all_playerstats.append(playerdata)
                



    # dict with puuid as a key and seasons played (list) as value
    all_seasons_played = {}



    champpool_data = []
    for puuid in list_puuid:
        seasons_played = []
        for match in select_matchids:
            matchid = match[0]
            season = match[1]

            if season not in seasons_played:
                seasons_played.append(season)
            elif season in seasons_played:
                continue

        all_seasons_played[puuid] = seasons_played

        for matchdata in all_playerstats:
            if matchdata[29] == "CLASSIC": #checking for summoners_rift games
                if puuid == matchdata[1]:
                    champpool_data.append([matchdata])


    for gamedata in champpool_data:
        for matchdata in all_playerstats:    #matchdata = main_player
            #[2] should be matchid and [7] should be role
            if gamedata[0][2] == matchdata[2] and gamedata[0][7] == matchdata[7]:
                if gamedata[0][5] != matchdata[5]:  #[5] = team
                    #[1] should be puuid
                    if gamedata[0][1] != matchdata[1]:
                        #i dont understand what is happenening here
                        gamedata.append(matchdata)
                        for matchid in select_matchids:
                            if matchid[0] == gamedata[0][2]:
                                gamedata.append(matchid[1])
                            

    to_process = [list_puuid, champpool_data]


    ###########################################
    #▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼#
    debug_json = json.dumps(to_process, indent=4)
    with open("debug.json", "w") as f:
        f.write(debug_json)

    print(to_process)
    #▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲#
    ###########################################

    """

    return []










def get_champpool(to_process):
    amnt_players = len(to_process[1])
    all_champpools = []
    puuids = to_process[0]
    game_datas = to_process[1]
    
    index_season = 0

    for puuid in puuids:
        """
        seasons_played = []
        for game in game_datas:
            if game[30] in seasons_played:       #add index for season
                continue
            elif game[30] not in seasons_played: #add index for season
                seasons_played.append(game[30])  #add index for season
        """
        #amount of champions
        unique_champs = []

        matchdata_player = []



        for game_data in game_datas:

#
            

            player = list(game_data[0])

            opponent = list(game_data[1])

            
            #filling unique_champs
            if puuid == player[1]: #[1] = puuid 
                if player[6] not in unique_champs: #[6] = champ
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
                    champ_class.kda.append(int(match_data[26]))
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
            

            all_champpools.append(champ_class)



    return all_champpools
