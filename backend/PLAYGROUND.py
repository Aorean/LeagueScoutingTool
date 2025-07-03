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
from backend.functions.process import process_userinput, process_matches
import os
from dotenv import load_dotenv


from backend.process_data.avrg_stats import *

from backend.process_data.playerinfo import get_playerinfo_classes



userinput = "https://op.gg/lol/multisearch/euw?summoners=Aorean%231311%2CQaQ%2300000"

def process_input(userinput):
    if userinput.startswith("https://op.gg/lol/multisearch/"):
        processed_link = userinput.split("/")
        region_names = processed_link[-1]
        region = region_names.split("?")[0]+"1"
        names = region_names.split("?")[1].split("=")[1]
        single_names = names.split("%2C")

        print(single_names)

        processed_names = []
        for gamertag_tagline in single_names:
            
            list_name = gamertag_tagline.split("%23")
            gamertag = list_name[0].replace("+", " ")
            tagline = list_name[1]

            processed_names.append([gamertag, tagline])
        if region == "euw1":
            region = "europe"
        processed_userinput = [region, processed_names]
        print(processed_userinput)
        return processed_userinput
    else:
        return False



test=process_input(userinput)
print(test)
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

