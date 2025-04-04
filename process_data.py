
from def_func import process_userinput, get_playerclass, get_matchhistoriesclass, process_matches
import os
from dotenv import load_dotenv

from avrg_stats import *



load_dotenv()
api_key = os.environ.get("api_key")

#read user_input
user_input = []
with open("user_input", "r") as f:
    for line in f:
        user_input.append(line)



#use function to get data for API
api_data = process_userinput(user_input)
region = api_data[0]
riot_ids = api_data[1]

#call riot api for puuids and save it in a list of classes "classes_player"
classes_player = get_playerclass(riot_ids, region, api_key)

#call riot api for matchhistories for each player and saving it in "classes_matchhistory"
classes_matchhistory = get_matchhistoriesclass(classes_player, region, api_key)

#call riot api for single matches and saving it in a dict
#key = matchid, value = list // list[0] = generall matchdata // list[1] = class stats all players // list[2] = class objectives
dict_matches = process_matches(classes_matchhistory, region, api_key)

#process matchdata from playerstats to get important data for champpools
champpool_data = get_data_for_champpool(db_connection)
#taking the above data and processing it into classes, getting a list of classes
list_champpools = get_champpool(champpool_data)





