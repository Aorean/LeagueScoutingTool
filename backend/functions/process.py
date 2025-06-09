from backend.def_classes.arena import arena_Match, arena_Playerstats
from backend.def_classes.howling_abyss import aram_Match, aram_Playerstats
from backend.def_classes.summoners_rift import Match, Objectives, Playerstats, Champpool
from backend.process_data.c_dragon import *
from backend.functions.psql import get_query,execute_query, filter_matchhistory
from backend.functions.general import get_match

import json

def process_userinput(user_input):
    usernames = user_input[0].split(",")
    region = user_input[1]

    api_data = []
    api_data.append(region)

    accounts = []
    for username in usernames:
        split = username.split("#")
        #strip trailing newline
        strip = split[1].rstrip()
        split[1] = strip
        #append account to list
        accounts.append(split)

    #append accounts to return data
    api_data.append(accounts)

    return api_data

def process_matches(classes_matchhistory, region, api_key, db_connection):

    full_matchinfo = {}
    for class_matchhistory in classes_matchhistory:
        matchids = class_matchhistory.matchhistory
        filtered_matchhistory = filter_matchhistory(db_connection, matchids)

        #tracking to process
        index = 0
        total = len(filtered_matchhistory)


        for matchid in filtered_matchhistory:
            
            #tracking to process
            index+=1
            print(f"Processed {index} from {total}\n To process: {total - index}")


            single_match = get_match(region, matchid, api_key)

            #with open(f"{matchid}.json", "w") as f:
            #    json.dump(single_match, f, indent=4)

            #generell matchdata
            
            #Errorcatches
            if "httpStatus" in single_match:
                if single_match["httpStatus"] == 404:
                    print("Match not found")
            elif "status" in single_match:
                if single_match["status"]["status_code"] == 403:
                    print("Forbidden")


            else:
                class_match = Match(class_matchhistory.PUUID, matchid, single_match)

                cdragon_items = cdragon_request(class_match.patch, "items")
                cdragon_perks = cdragon_request(class_match.patch, "perks")
                cdragon_summonerspells = cdragon_request(class_match.patch, "summoner-spells")
                #checking for gamemode with important stats (ranked (+flexq))
                #if class_match.gamemode == "CLASSIC":


                    #participant matchdata
                participants = single_match["info"]["participants"]


                all_participants = []

                if (class_match.gamemode == 0 or
                    class_match.gamemode == 420 or
                    class_match.gamemode == 440
                ): 
                    for participant in participants:
                        print(matchid)
                        class_playerstats = Playerstats(participant, matchid, participant["puuid"], single_match)


                        class_playerstats.translate_ids(cdragon_items, cdragon_summonerspells, cdragon_perks)
                        all_participants.append(class_playerstats)

                    #objectives matchdata
                    teams = single_match["info"]["teams"]
                    objective_teams =  {}


                    
                    for team in teams:
                        objective_team = Objectives(team=team, matchid=matchid)
                        objective_teams[objective_team.teamid] = objective_team


                    matchinfo = [class_match, all_participants, objective_teams]
                    full_matchinfo.update({
                        matchid: matchinfo
                    })

                """
                #ARENA
                if class_match.gamemode =="CHERRY":
                    all_participants = []
                    participants = single_match["info"]["participants"]
                    for participant in participants:
                        puuid = participant["puuid"]
                        class_playerstats = arena_Playerstats(participant, single_match)

                        class_playerstats.translate_ids(cdragon_items, cdragon_summonerspells, cdragon_perks)
                        all_participants.append(class_playerstats)

                    matchinfo = [class_match, all_participants]
                    full_matchinfo.update({
                        matchid: matchinfo
                    })

                #ARAM
                if class_match.gamemode =="ARAM":
                    participants = single_match["info"]["participants"]
                    all_participants = []
                    for participant in participants:
                        class_playerstats = aram_Playerstats(participant, single_match)

                        class_playerstats.translate_ids(cdragon_items, cdragon_summonerspells, cdragon_perks)
                        all_participants.append(class_playerstats)

                    matchinfo = [class_match, all_participants]
                    full_matchinfo.update({
                        matchid: matchinfo
                    })
                """
    return full_matchinfo

########           FUNCTION         ########
########   get_data_for_champpool   ########
def filter_earlyffs(all_matches, all_playerstats):
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

    return_list = [no_earlyff_rank_matches, no_earlyff_rank_playerstats]

    return return_list

def get_seasons_by_player(all_puuid, all_playerstats):
    seasons_by_player = {}

    for puuid in all_puuid:
        seasons_played = []

        for playerstats in all_playerstats:

            if playerstats[1] == puuid:

                season = playerstats[26]

                if season not in seasons_played:
                    seasons_played.append(season)
                elif season in seasons_played:
                    continue
            
        seasons_by_player[puuid] = seasons_played

    return seasons_by_player
    
def matching_opponents(all_puuid, no_earlyff_rank_playerstats):
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
                        

                #to filter out empty lists
                if len(matched_playerstats) > 0:
                    full_match_playerstats.append(matched_playerstats)

        puuid_matched_stats[puuid] = full_match_playerstats

    return puuid_matched_stats

def sort_data_by_season(seasons_by_player, puuid_matched_stats):
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

    return return_dict


########    FUNCTION       ########
########   get_champpool   ########
def get_unique_champs(to_process):
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

    return unique_champs_puuid

def append_diff_stats(to_process):
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

def create_champpool_classes(unique_champs_puuid, to_process):
    all_champpools = []
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


                all_champpools.append(class_champpool)

    return all_champpools