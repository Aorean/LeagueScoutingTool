from backend.config import db_engine, db_connection
from backend.db_base import Base

#SQL imports
from sqlalchemy.orm import sessionmaker

import json

#psql
from backend.functions.psql import insert_or_update_player, get_query, execute_query
from backend.def_classes.sql_tables import *

#process data
from backend.config import db_connection
from backend.functions.general import get_playerclass, get_matchhistoriesclass

import os
from dotenv import load_dotenv
from backend.functions.process import process_input

from backend.process_data.avrg_stats import *

from backend.process_data.playerinfo import get_playerinfo_classes
from backend.main import json_champpool, json_mastery
#from backend.main import run_main

from backend.def_classes.summoners_rift import Match, Objectives, Playerstats, Champpool
from backend.process_data.c_dragon import *
from backend.functions.api import get_match
import dotenv
import os
api_key = os.environ.get("api_key")

userinput = "https://op.gg/lol/multisearch/euw?summoners=Aorean%231311%2CQaQ%2300000%2CMoris%23RIVEN%2Cihatethisnerd%23euw%2Ci+is+pidgeon%23EUW"

puuids = [
        "bO5blHOm9YeY2MXm15I3DiHVtQPb8PuQov9J-wJ4X3CBuhjScuFDdaEM7VMFtciIC5htsuFYT43ytw",
        "xN9AE0xmaCYwytheZ-FfNqdPBBDN1EUwlia3opOR1ms1KDWrJUpTPpEOjvTx4c6J_70OchHbztx-XA"
        ]


test=json_mastery(player=puuids, db_connection=db_connection)

with open("testChamppool.json", "w") as f:
    f.write(test)



"""

api_data = process_input(userinput)
region = api_data[0]
riot_ids = api_data[1]


#call riot api for puuids and save it in a list of classes "classes_player"
#classes_player = get_playerclass(riot_ids, region, api_key)
#for player in classes_player:
#    print(player.puuid)

#classes_matchhistory = get_matchhistoriesclass(classes_player, region, api_key)

#run_main(userinput, api_key, db_connection)

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




            ######REMOVE######DEBUG######
            try:
                path = os.path.join("__TESTDATA__", "get_match")

                file_path = os.path.join(path, f"{matchid}.json")
                with open(file_path, "r") as single_match_json:
                    single_match = json.load(single_match_json)
                    ######REMOVE######DEBUG######




                    #generell matchdata
                    
                    #Errorcatches
                    if "httpStatus" in single_match:
                        if single_match["httpStatus"] == 404:
                            print("Match not found")
                    elif "status" in single_match:
                        if single_match["status"]["status_code"] == 403:
                            print("Forbidden")
                    #elif "riotIdGameName" not in single_match["info"]["participants"]:
                    #    print("STOPPED")
                    #    continue

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


            ######REMOVE######DEBUG######
            except FileNotFoundError:
                print("MATCH NOT FOUND")
                continue
            ######REMOVE######DEBUG######
    
    return full_matchinfo




#dict_matches = process_matches(classes_matchhistory, region, api_key, db_connection)

#with open("newnewnew.json", "w") as f:
    #json.dump(dict_matches, f, indent=4)

"""