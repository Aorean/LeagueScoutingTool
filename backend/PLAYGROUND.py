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
from backend.functions.process import process_matches
import os
from dotenv import load_dotenv


from backend.process_data.avrg_stats import *

from backend.process_data.playerinfo import get_playerinfo_classes



userinput = "https://op.gg/lol/multisearch/euw?summoners=Aorean%231311%2CQaQ%2300000"

puuids = [
        "bO5blHOm9YeY2MXm15I3DiHVtQPb8PuQov9J-wJ4X3CBuhjScuFDdaEM7VMFtciIC5htsuFYT43ytw",
        "xN9AE0xmaCYwytheZ-FfNqdPBBDN1EUwlia3opOR1ms1KDWrJUpTPpEOjvTx4c6J_70OchHbztx-XA",
        "auom9H6uf9iN4yPls9QidJQWB1Mz2n4UIhfap9aQoITqA5gtRU0RE0ojafStbkIYrQzKtqxWmQr_jg",
        "pGSPl_CvQKjMkHq5m1j3CSrL6KEG3gMol1H8G-M_wpoK1LTT2F9Qe9aCYJyGoXf_L0rUpKzJAR6xUQ",
        "puho54jBgun4B2VMgOV27N5Ty0JkEMDR8fdKjLGV8ip9ZmL0BSEwvaTMSIiXNDsM3Ulmlo0Yu4acow"
        ]
def create_dashboard_json(puuids):


    tables = [
        "player",
        "playerinfo",
        "match",
        "playerstats",
        "champpool"
    ]
    dashboard = {
        "player" : [], 
        "tc_Matches": []
        }

    
    for puuid in puuids:
        tc_matches = []
        account = {}
        player = {}
        for table in tables:
            if table == "player":

                query = get_query(querytype="select_json",
                        selection="puuid",
                        schema="playerdata", 
                        table=table,
                        column="puuid",
                        value=puuid
                            )
                row = execute_query(db_connection=db_connection, query=query)
                clean_row = row[0][0][0]

                for key,value in clean_row.items():
                    account[key] = value
            
            if table == "playerinfo":
                query = get_query(querytype="select_json",
                selection="puuid",
                schema="playerdata", 
                table=table,
                column="puuid",
                value=puuid
                    )
                row = execute_query(db_connection=db_connection, query=query)

                clean_row = row[0][0][0]
                account["elo"] = clean_row["division"] + clean_row["rank"]

                try:  
                    account["winrate"] = round(clean_row["wins_total"]/(clean_row["wins_total"]+clean_row["losses_total"]), 2)
                except ZeroDivisionError:
                    if clean_row["wins_total"]==0:
                        account["winrate"] = 0
                    if clean_row["losses_total"]==0:
                        account["winrate"] = 1

            if table == "champpool":
                query = get_query(querytype="top3_json",
                                  selection="champ, kda, games_played, winrate, fav_role",
                                  schema="playerdata",
                                  table=table,
                                  argument="puuid",
                                  value=puuid,
                                  order="games_played")

                row = execute_query(query=query, db_connection=db_connection)

                clean_row = row[0][0]
                
                player["champpool"] = clean_row


            if table == "match":
                query = get_query(querytype="select_json", 
                                  schema="playerdata", 
                                  table=table, 
                                  selection="tournamentcode!", 
                                  value="NULL")
                row = execute_query(db_connection=db_connection, query=query)
                clean_row = row[0][0]
                
                match_json = {
                    
                }
 
                for data in clean_row:
                    data["matchid"]
                    participants_string = data["participants"]
                    
                    participants_list = participants_string.split(",")
                    participants = []
                    for participant_puuid in participants_list:
                        cleanup = participant_puuid.strip('"')
                        prep = {"puuid" : cleanup}
                        participants.append(prep)


                    match_json = {
                        "matchId" : data["matchid"],
                        "participants" : participants,
                        "gameDuration" : data["gameduration"],
                        "tournamentcode" : data["tournamentcode"],
                    }

                    tc_matches.append(match_json)



            if table == "playerstats":
                for matchdata in tc_matches:
                    matchid = matchdata["matchId"]
                    
                    
                    query_playerdata = get_query(querytype="select_json", 
                                schema="playerdata",
                                table="playerstats",
                                selection="matchid",
                                value=matchid
                                )
                    rows_playerstats = execute_query(db_connection=db_connection, query=query_playerdata)
                    
                    clean_playerstat_rows = rows_playerstats[0][0]
                    
                    for playerstat in clean_playerstat_rows:
                        for participants_dict in matchdata["participants"]:
                            test_puuid = participants_dict["puuid"]
                            test2_puuid = playerstat["puuid"]
                            if test_puuid == test2_puuid:
                                for k, v in playerstat.items():
                                    participants_dict[k]=v

        player["account"] = account

        dashboard["player"].append(player)
        dashboard["tc_Matches"] = tc_matches
    
    with open("player_json.json", "w") as f: 
        json.dump(dashboard, f, indent=4)

create_dashboard_json(puuids)

"""
load_dotenv()
#def session
SessionLocal = sessionmaker(bind=db_engine, autocommit=False, autoflush=False)
#open session
session = SessionLocal()




puuids = [
    "pGSPl_CvQKjMkHq5m1j3CSrL6KEG3gMol1H8G-M_wpoK1LTT2F9Qe9aCYJyGoXf_L0rUpKzJAR6xUQ",
    "auom9H6uf9iN4yPls9QidJQWB1Mz2n4UIhfap9aQoITqA5gtRU0RE0ojafStbkIYrQzKtqxWmQr_jg",
    "xN9AE0xmaCYwytheZ-FfNqdPBBDN1EUwlia3opOR1ms1KDWrJUpTPpEOjvTx4c6J_70OchHbztx-XA",
    "bO5blHOm9YeY2MXm15I3DiHVtQPb8PuQov9J-wJ4X3CBuhjScuFDdaEM7VMFtciIC5htsuFYT43ytw"]

tables = [
    "player",
    "playerinfo",
    "match",
    "playerstats",
    "champpool"
]

return_dict = {}
id = 1
for puuid in puuids:
    player_dict = {}

    
    for table in tables:
        table_data = []
        query = get_query(querytype="select_json",
                    selection="puuid",
                    schema="playerdata", 
                    table=table,
                    column="puuid",
                    value=puuid
                        )
        result = execute_query(db_connection=db_connection, query=query)
        
        for row in result:
            table_data.append(row)
        player_dict[table] = table_data
    
    return_dict[id] = player_dict

    id += 1


return_json = json.dumps(return_dict)
with open("test.json", "w") as f:
    json.dump(return_dict, f, indent=4)


#close session with sql
session.close()


class test:
    def __init__(self, data):
        self.value1 = data[0]
        self.value2 = data[1]
        self.value3 = data[2]
        self.value4 = data[3]


data = ["test1", "test2", "test3", "test4"]

testdata = test(data)

print(type(testdata.__dict__.keys()))
keys=testdata.__dict__.keys()
for key in keys:
    print(key)


champpool_data = get_data_for_champpool(db_connection)

with open("debug.txt", "w") as f:
    f.write(json.dumps(champpool_data[1], indent=4))

with open("test.json", "r") as f:
    file = json.load(f)
    participants = file["info"]["participants"][0]
    matchid = file["metadata"]["matchId"]
    puuid = participants["puuid"]



    test_class = Playerstats(participants, matchid, puuid, file)


    test_class.translate_ids
    cdragon_items = cdragon_request(test_class.patch, "items")
    cdragon_perks = cdragon_request(test_class.patch, "perks")
    cdragon_summonerspells = cdragon_request(test_class.patch, "summoner-spells")
    test_class.translate_ids(cdragon_items, cdragon_summonerspells, cdragon_perks)
    test_class.print_all()
"""

