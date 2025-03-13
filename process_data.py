
from def_func import process_userinput, get_playerclass, get_matchhistoriesclass, get_matchclass
import os
from dotenv import load_dotenv



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
#key = matchid, value = list // list[0] = generall matchdata // list[1] = class stats all players
dict_matches = get_matchclass(classes_matchhistory, region, api_key)


"""
for class_player in classes_player:
    print(class_player.gamertag)

for class_matchhistory in classes_matchhistory:
    print(class_matchhistory.matchhistory)
"""


for matchid in dict_matches:
    match = dict_matches[matchid]

    class_match = match[0]
    participants = match[1]

    print(class_match.matchid + " " + class_match.gamemode)
    for participant in participants:
        for player in classes_player:
            if participant.puuid == player.puuid:
                print(participant.gamertag + "#" + participant.tagline + " " + participant.champ)

