from backend.config import db_connection
from backend.process_data.avrg_stats import get_data_for_champpool
import json
from backend.def_classes.summoners_rift import Playerstats
from backend.process_data.c_dragon import *
from backend.process_data.avrg_stats import get_champpool, get_data_for_champpool






to_process = get_data_for_champpool(db_connection)

#champool_classes = get_champpool(to_process)










"""
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

