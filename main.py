#hahalololl
from itertools import count
from operator import index

from dotenv import load_dotenv
import os
import requests
import pandas as pd
from numpy.ma.core import append
from pandas import period_range

load_dotenv()

riot_id = input("Riot ID: ")
riot_id_list = riot_id.split("#")

summoner_name = riot_id_list[0]
tag_line = riot_id_list[1]
api_key = os.environ.get("api_key")
region = "europe"

#######################################################################################################################

def get_puuid(summoner_name, tag_line, region, api_key):
    # request Riot API to get puuid for further use
    root_url = f"https://{region}.api.riotgames.com/"
    puuid_url = f"riot/account/v1/accounts/by-riot-id/{summoner_name}/{tag_line}?api_key={api_key}"

    response_puuid = requests.get(root_url + puuid_url)
    puuid = response_puuid.json()["puuid"]

    return puuid


def get_matchhistory(region, puuid, api_key, startTime=20250108):
    root_url = f"https://{region}.api.riotgames.com/"
    history_url = f"lol/match/v5/matches/by-puuid/{puuid}/ids?{startTime}&api_key={api_key}"

    response_history = requests.get(root_url + history_url)

    return response_history.json()


def get_match(region, matchId, api_key):
    root_url = f"https://{region}.api.riotgames.com/"
    match_url = f"/lol/match/v5/matches/{matchId}?api_key={api_key}"

    response_match = requests.get(root_url + match_url)
    response_match = response_match.json()

    return response_match


#######################################################################################################################

get_puuid(summoner_name, tag_line, region, api_key)

#######################################################################################################################

puuid = get_puuid(summoner_name, tag_line, region, api_key)

#######################################################################################################################

get_matchhistory(region, puuid, api_key, startTime=20250108)

#######################################################################################################################

matchhistory = get_matchhistory(region, puuid, api_key, startTime=20250108)
matchId = matchhistory[0]

#######################################################################################################################

get_match(region, matchId, api_key)
match = get_match(region, matchId, api_key)

#######################################################################################################################

match1 = get_match(region, matchId, api_key)

#######################################################################################################################

# accessing the Dtos to process data into smaller packages
# Match > MetadataDto
metadata = match["metadata"]
players = metadata["participants"]

# Match > InfoDto
info = match["info"]
game_creation = info["gameCreation"]
game_duration = info["gameDuration"]
game_mode = info["gameMode"]
game_version = info["gameVersion"]  # wird später noch als "Patch" eingepflegt
tournament_code = info["tournamentCode"]
teams = info["teams"]

# Match > InfoDto > ParticipantDt#    riot_id_game_name.append(player["riotIdGameName"])
participant_dto = info["participants"]
player_info = dict()
riot_id_game_name = []

for player in participant_dto:
    player_info[player["riotIdGameName"]] = player["win"],player["kills"],player["assists"],player["deaths"]
    riot_id_game_name.append(player["riotIdGameName"])
    riot_id_tagline = player["riotIdTagline"]
    champ_name = player["championName"]
    win = player["win"]
    kills = player["kills"]
    deaths = player["deaths"]
    assists = player["assists"]
    neutral_minions_killed = player["neutralMinionsKilled"]
    #total_minions_killed = player["total_Minions_Killed"]
    champ_exp = player["champExperience"]
    champ_lvl = player["champLevel"]
    gold_earned = player["goldEarned"]
    # champ_id = player["champId"]
    vision_score = player["visionScore"]
    detectorwards_placed = player["detectorWardsPlaced"]
    dragon_kills = player["dragonKills"]
    first_blood_kill = player["firstBloodKill"]
    total_dmg_dealt = player["totalDamageDealtToChampions"]
    total_dmg_taken = player["totalDamageTaken"]
    summoner1_id = player["summoner1Id"]
    summoner2_id = player["summoner2Id"]
    match player["summoner1Id"]:
        case "1":
            summoner1_id = "Cleanse"
        case "3":
            summoner1_id = "Exhaust"
        case "4":
            summoner1_id = "Flash"
        case "6":
            summoner1_id = "Ghost"
        case "7":
            summoner1_id = "Heal"
        case "11":
            summoner1_id = "Smite"
        case "12":
            summoner1_id =  "Teleport"
        case _:
            summoner1_id = summoner1_id

    if summoner2_id == 1:
        summoner2_id = "Cleanse"
    if summoner2_id == 3:
        summoner2_id = "Exhaust"
    if summoner2_id == 4:
        summoner2_id = "Flash"
    if summoner2_id == 6:
        summoner2_id = "Ghost"
    if summoner2_id == 7:
        summoner2_id = "Heal"
    if summoner2_id == 11:
        summoner2_id = "Smite"
    if summoner2_id == 12:
        summoner2_id = "Teleport"
    else:
        summoner2_id = summoner2_id
    # Match >InfoDto > ParicipantDto > PerksDto > PerksStatsDto
    print(champ_name , "Summoner 1: " , summoner1_id , "     " , "Summoner 2: " , summoner2_id)




# Match > InfoDto > TeamDto > BanDto
#banns red/blue + championId und pickTurn
# [0] blueside [1] redside
banns_total_red = []
banns_total_blue = []

teaminfo_blue = teams[0]
teaminfo_red = teams[1]
banns_blue = teaminfo_blue["bans"]
banns_total_red.append(banns_blue)
banns_red = teaminfo_red["bans"]
banns_total_red.append(banns_red)
print(banns_total_blue + banns_total_red)


obj_blue = []
obj_red = []
obj_total = [obj_blue , obj_red]

obj_blue_dict = teaminfo_blue["objectives"]
obj_blue.append(obj_blue_dict)
obj_red_dict = teaminfo_red["objectives"]
obj_red.append(obj_red_dict)



#following doesnt work
"""
#atakhan = obj_blue["atakhan"]
#obj_total.append(atakhan)
baron = obj_blue["baron"]
obj_total.append(baron)
champion_kills = obj_blue["champion"]
obj_total.append(champion_kills)
dragon = obj_blue["dragon"]
obj_total.append(dragon)
grubs = obj_blue["horde"]
obj_total.append(grubs)
inhibitors = obj_blue["inhibitor"]
obj_total.append(inhibitors)
rift_herald = obj_blue["riftHerald"]
obj_total.append(rift_herald)
tower = obj_blue["tower"]
obj_total.append(tower)
"""

print(obj_total)
# [0] blueside [1] redside

#"atakhan", "baron", "champion", "dragon", "horde", "inhibitor", "riftHerald", "tower", "win"
#print(teams)
#print(ban_id)
#######################################################################################################################
"""
print(player_info)
print(player_info["Moris "])
print(len(player_info))
"""
##for player in participant_dto:
    ##print(riot_id_game_name)

"""
for game in matchhistory:
    get_match(region, matchId, api_key)
    match = get_match(region, matchId, api_key)
    print(champions)



    match_df = pd.DataFrame(match)
    champions_played = match["InfoDto"]["ParticipantDto"]["championName"]
    print(match_df)
    print(champions_played)
"""

# match_df1 = pd.DataFrame(match1)


###############################################

# print(puuid)

################################################

# print(matchhistory)

#################################################

# print(match1)

#################################################

# print(match_df1)

#################################################

# player = puuid

#################################################
print(match)