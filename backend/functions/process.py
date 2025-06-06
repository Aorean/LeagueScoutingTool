from backend.def_classes.arena import arena_Match, arena_Playerstats
from backend.def_classes.howling_abyss import aram_Match, aram_Playerstats
from backend.def_classes.summoners_rift import Match, Objectives, Playerstats
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