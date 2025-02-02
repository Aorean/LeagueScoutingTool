#hahalololl
from itertools import count

from dotenv import load_dotenv
import os
import requests
import pandas as pd
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

print(len(matchhistory))

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
    print(riot_id_tagline)
    win = player["win"]
    kills = player["kills"]
    assists = player["assists"]
    deaths = player["deaths"]
    neutral_minions_killed = player["neutralMinionsKilled"]
    # total_minions_killed = player["total_Minions_Killed"]
    champ_exp = player["champExperience"]
    champ_lvl = player["champLevel"]
    gold_earned = player["goldEarned"]
    # champ_id = player["champId"]
    champ_name = player["championName"]
    vision_score = player["visionScore"]
    detectorwards_placed = player["detectorWardsPlaced"]
    dragon_kills = player["dragonKills"]
    first_blood_kill = player["firstBloodKill"]
    total_dmg_dealt = player["totalDamageDealtToChampions"]
    total_dmg_taken = player["totalDamageTaken"]
    summoner1_id = player["summoner1Id"]
    summoner2_id = player["summoner2Id"]
    # Match >InfoDto > ParicipantDto > PerksDto > PerksStatsDto
    perks_dto = player["perks"]

#######################################################################################################################

print(player_info)
print(player_info["Moris "])
print(len(player_info))

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
