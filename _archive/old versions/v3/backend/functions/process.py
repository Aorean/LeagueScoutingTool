from backend.def_classes.arena import arena_Match, arena_Playerstats
from backend.def_classes.howling_abyss import aram_Match, aram_Playerstats
from backend.def_classes.summoners_rift import Match, Objectives, Playerstats, Champpool
from backend.process_data.c_dragon import *
from backend.functions.psql import get_query,execute_query, filter_matchhistory
from backend.functions.general import get_match
import os

import json

def process_input(userinput):
    if userinput.startswith("https://op.gg/lol/multisearch/"):
        processed_link = userinput.split("/")
        region_names = processed_link[-1]
        region = region_names.split("?")[0]+"1"
        names = region_names.split("?")[1].split("=")[1]
        single_names = names.split("%2C")



        processed_names = []
        for gamertag_tagline in single_names:
            
            list_name = gamertag_tagline.split("%23")
            gamertag = list_name[0].replace("+", " ")
            tagline = list_name[1]

            processed_names.append([gamertag, tagline])
        if region == "euw1":
            region = "europe"
        processed_userinput = [region, processed_names]

        return processed_userinput
    else:
        return False

def process_matches(classes_matchhistory, region, api_key, db_connection):

    full_matchinfo = {}
    for class_matchhistory in classes_matchhistory:
        matchids = class_matchhistory.matchhistory
        filtered_matchhistory = filter_matchhistory(db_connection, matchids)

        #DEBUG#
        #print("FILTERED MATCHHISTORY: ", filtered_matchhistory)

        #tracking to process
        index = 0
        total = len(filtered_matchhistory)


        for matchid in filtered_matchhistory:




            #tracking to process
            index+=1
            print(f"Processed {index} from {total}\n To process: {total - index}")


            #DEBUG#
            print(matchid)
            #DEBUG


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
            #elif "riotIdGameName" not in single_match["info"]["participants"]:
            #    print("IDK")
            #    continue

            else:
                #DEBUG#
                print("MATCH FOUND")
                #DEGBUG'

                class_match = Match(matchid, single_match)
                
                cdragon_items = cdragon_request(class_match.patch, "items")
                cdragon_perks = cdragon_request(class_match.patch, "perks")
                cdragon_summonerspells = cdragon_request(class_match.patch, "summoner-spells")
                #checking for gamemode with important stats (ranked (+flexq))
                #if class_match.gamemode == "CLASSIC":


                    #participant matchdata
                participants = single_match["info"]["participants"]


                all_participants = []
                objective_teams =  {}

                if (class_match.gamemode == 0 or
                    class_match.gamemode == 420 or
                    class_match.gamemode == 440
                ): 
                    for participant in participants:
                        
                        class_playerstats = Playerstats(participant, matchid, participant["puuid"], single_match)


                        class_playerstats.translate_ids(cdragon_items, cdragon_summonerspells, cdragon_perks)
                        all_participants.append(class_playerstats)

                    #objectives matchdata
                    teams = single_match["info"]["teams"]
                    


                    
                    for team in teams:
                        objective_team = Objectives(team=team, matchid=matchid)
                        objective_teams[objective_team.teamid] = objective_team


                matchinfo = [class_match, all_participants, objective_teams]
                full_matchinfo.update({
                    matchid: matchinfo
                })




    return full_matchinfo

########           FUNCTION         ########
########   get_data_for_champpool   ########
def filter_earlyffs(all_matches, all_playerstats):
    no_earlyff_rank_matches = []
    no_earlyff_rank_playerstats = []

    for match in all_matches:
        for playerstats in all_playerstats:
            
            match_matchid = match[0]
            
            playerstats_matchid = playerstats[0]

            
            if match_matchid == playerstats_matchid:
                early_ff_match = match[2]

                #early surrender filter not neccessery
                #query selects only non early surrender games
                if early_ff_match == False:
                    gamemode = playerstats[26]
                    
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

                season = playerstats[25]
                
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
                    
                    matchid = playerstats[0]
                    matchid_opponent = opponentstats[0]
                    
                    role =playerstats[4]
                    role_opponent = opponentstats[4]
                    
                    team = playerstats[2]
                    team_opponent = opponentstats[2]
                    
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
                    
                    season_match = matched_match[0][25]
                    puuid_match = matched_match[0][1]
                    
                    
                    if season_key == puuid_match:   #somehow only 1 puuid gets matched and dict only contains 1 player, why?
                        
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

                champ_player = player[3]
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


                kills = player[5]
                deaths = player[6]
                assists = player[7]
                cs = player[8]
                level = player[9]
                exp = player[10]
                gold = player[11]
                visionscore = player[12]

                cs_opponent = opponent[8]
                level_opponent = opponent[9]
                exp_opponent = opponent[10]
                gold_opponent = opponent[11]
                visionscore_opponent = opponent[12]

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

    return to_process


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
                    playerstats_champ = playerstats[3]

                    if playerstats_champ == champ:


                        class_champpool.games_played+=1
                        class_champpool.kda.append(playerstats[32])
                        class_champpool.kills.append(playerstats[5])
                        class_champpool.deaths.append(playerstats[6])
                        class_champpool.assists.append(playerstats[7])
                        class_champpool.cs.append(playerstats[8])
                        class_champpool.exp.append(playerstats[10])
                        class_champpool.level.append(playerstats[9])
                        class_champpool.gold.append(playerstats[11])
                        class_champpool.visionscore.append(playerstats[12])
                        class_champpool.cs_diff.append(playerstats[27])
                        class_champpool.exp_diff.append(playerstats[29])
                        class_champpool.level_diff.append(playerstats[28])
                        class_champpool.gold_diff.append(playerstats[30])
                        class_champpool.visionscore_diff.append(playerstats[31])
                        class_champpool.summonerspell1.append(playerstats[13])
                        class_champpool.summonerspell2.append(playerstats[14])
                        class_champpool.fav_role.append(playerstats[4])
                        class_champpool.team.append(playerstats[2])
                        class_champpool.winrate.append(playerstats[22])
                        #class_champpool.win_blue.append(playerstats[30])
                        #class_champpool.winrate.append(playerstats[30])
                class_champpool.avarage_stats()


                all_champpools.append(class_champpool)

    return all_champpools