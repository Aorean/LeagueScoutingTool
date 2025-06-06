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

                #early surrender filter not neccessery
                #query selects only non early surrender games
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

        for playerstats in all_playerstats:
            #somehow this breaks it.. idk
            #match_puuid = match[1]

            if playerstats[1] == puuid:


                season = playerstats[26]

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
                    
                    season_match = matched_match[0][26]
                    puuid_match = matched_match[0][1]
                    if season_key == puuid_match:
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

    return return_dict










def get_champpool(to_process):
    all_champpools = []
    unique_champs_puuid = {}


    for puuid in to_process:
        
        season_data = to_process[puuid]
        all_unique_champs = {}
        for season in season_data:
            matches = season_data[season]
            unique_champs = []

            for matched_data in matches:
                #access the single match data with oppoenent and player

                #access the player and opponent matchdata
                player = matched_data[0]
                opponent = matched_data[1]

                champ_player = player[6]
                if champ_player in unique_champs:
                    continue
                if champ_player not in unique_champs:
                    unique_champs.append(champ_player)
            
            all_unique_champs[season] = unique_champs
        
        unique_champs_puuid[puuid] = all_unique_champs

        ###
        #Diffstats#
        ###
    for puuid in to_process:
        season_data = to_process[puuid]

        for season in season_data:
            matches = season_data[season]
            for matched_data in matches:
                player = list(matched_data[0])
                opponent = matched_data[1]


                kills = player[8]
                deaths = player[9]
                assists = player[10]
                cs = player[11]
                level = player[12]
                exp = player[13]
                gold = player[14]
                visionscore = player[15]

                cs_opponent = opponent[11]
                level_opponent = opponent[12]
                exp_opponent = opponent[13]
                gold_opponent = opponent[14]
                visionscore_opponent = opponent[15]

                cs_diff = cs - cs_opponent
                level_diff = level - level_opponent
                exp_diff = exp - exp_opponent
                gold_diff = gold - gold_opponent
                visionscore_diff = visionscore - visionscore_opponent

                try:
                    kda = (kills + assists) / deaths
                except ZeroDivisionError as e:
                    kda = 0

                player.append(cs_diff)
                player.append(level_diff)
                player.append(exp_diff)
                player.append(gold_diff)
                player.append(visionscore_diff)
                player.append(kda)

                matched_data[0] = player




    for puuid in to_process:
        
        champpool_season = unique_champs_puuid[puuid]
        to_process_seasons = to_process[puuid]

        for season in champpool_season:
            champpool = champpool_season[season]
            playerstats_season = to_process_seasons[season]

            for champ in champpool:
                class_champpool = Champpool(champ=champ, puuid=puuid, season=season)
                for matched_data in playerstats_season:
                    playerstats = matched_data[0]
                    playerstats_champ = playerstats[6]

                    if playerstats_champ == champ:

                        class_champpool.name = playerstats[3]
                        class_champpool.tagline = playerstats[4]
                        class_champpool.games_played+=1
                        class_champpool.tagline = playerstats[4]
                        class_champpool.kda.append(playerstats[35])
                        class_champpool.kills.append(playerstats[8])
                        class_champpool.deaths.append(playerstats[9])
                        class_champpool.assists.append(playerstats[10])
                        class_champpool.cs.append(playerstats[11])
                        class_champpool.exp.append(playerstats[13])
                        class_champpool.level.append(playerstats[12])
                        class_champpool.gold.append(playerstats[14])
                        class_champpool.visionscore.append(playerstats[15])
                        class_champpool.cs_diff.append(playerstats[30])
                        class_champpool.exp_diff.append(playerstats[32])
                        class_champpool.level_diff.append(playerstats[31])
                        class_champpool.gold_diff.append(playerstats[33])
                        class_champpool.visionscore_diff.append(playerstats[34])
                        class_champpool.summonerspell1.append(playerstats[16])
                        class_champpool.summonerspell2.append(playerstats[17])
                        class_champpool.fav_role.append(playerstats[7])
                        class_champpool.team.append(playerstats[5])
                        class_champpool.winrate.append(playerstats[25])
                        #class_champpool.win_blue.append(playerstats[30])
                        #class_champpool.winrate.append(playerstats[30])
                class_champpool.avarage_stats()
                class_champpool.print_all()

                all_champpools.append(class_champpool)

    return all_champpools



                        


























    '''
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
    '''