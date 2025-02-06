# hahalololl
from itertools import count
from operator import index

from dotenv import load_dotenv
import os
import requests
from function_api import get_puuid, get_matchhistory, get_match

import pandas as pd
from numpy.ma.core import append
from pandas import period_range

load_dotenv()

# vorbereitung auf google sheets
"""
import pygsheets
service_acc = pygsheets.authorize(service_account_file="json//spreadsheet-automator-449612-b3a5d5ca0942.json")

sheet =service_acc.open_by_url("https://docs.google.com/spreadsheets/d/1iHweQST_7PNmN-PbfCDlZFUAhQzesQLrw60-WgrNK1I/edit?usp=sharing")

test1 = sheet.worksheet("title", "Metadata")

test1_df = test1.get_as_df()
"""

riot_id = input("Riot ID: ")
riot_id_list = riot_id.split("#")

summoner_name = riot_id_list[0]
tag_line = riot_id_list[1]
api_key = os.environ.get("api_key")
region = "europe"

#######################################################################################################################

get_puuid(summoner_name, tag_line, region, api_key)

#######################################################################################################################

puuid = get_puuid(summoner_name, tag_line, region, api_key)

#######################################################################################################################

get_matchhistory(region, puuid, api_key, startTime=20250108)

#######################################################################################################################

matchhistory = get_matchhistory(region, puuid, api_key, startTime=20250108)
matchId = matchhistory

#######################################################################################################################

matchdata_20_games = []

def player_data_matchhistory():
    for player in participant_dto:
        if puuid == player["puuid"]:
            # merging riotId and riotTagLine
            gamename_a_tagline.append(player["riotIdGameName"])
            gamename_a_tagline.append(player["riotIdTagline"])
            ign = gamename_a_tagline[0] + "#" + gamename_a_tagline[1]

            # merging summonerspells into a list
            summoner_spell.append(player["summoner1Id"])
            summoner_spell.append(player["summoner2Id"])

            # getting stats from json
            player_scouting["team"] = player["teamId"]
            player_scouting["name"] = ign
            player_scouting["champ"] = player["championName"]
            player_scouting["kills"] = player["kills"]
            player_scouting["deaths"] = player["deaths"]
            player_scouting["assists"] = player["assists"]
            player_scouting["cs"] = player["totalMinionsKilled"]
            player_scouting["position"] = player["teamPosition"]
            player_scouting["kda"] = player["challenges"]["kda"]
            player_scouting["summonerspells"] = summoner_spell
            player_scouting["total dmg to champ"] = player["totalDamageDealtToChampions"]
            player_scouting["win"] = player["win"]





            # print one match
            print(player_scouting)
            return player_scouting




#######################################################################################################################

#list and dict for context
total_objectives_20_games = []
objectives_team ={}

for matchId in matchhistory:
    match = get_match(region, matchId, api_key)

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
    riot_id_game_name = []
    detail_player = {}

    player_scouting = {}
    gamename_a_tagline = []
    summoner_spell = []

    #checking each objective
    for team in teams:
        #list where every objective per team gets saved
        list_objectives = []
        #dict to save objective with keyword
        objectives = {}

        side = team["teamId"]


        objs = team["objectives"]
        objectives["baron"] = objs["baron"]
        objectives["dragon"] = objs["dragon"]
        objectives["grubs"] = objs["horde"]
        objectives["rift_herald"] = objs["riftHerald"]
        objectives["tower"] = objs["tower"]
        objectives["inhibitor"] = objs["inhibitor"]

        #using dict above to create a connection between "side" and objectives "objectives_team"
        #putting that list into a list of the last 20 games "total_objectives_20_games"
        list_objectives.append(objectives)
        objectives_team[side] = list_objectives
        total_objectives_20_games.append(objectives_team)


    matchdata_20_games.append(player_data_matchhistory())

print(total_objectives_20_games)
#######################################################################################################################

#getting average from last 20 games

kills_total = 0
deaths_total = 0
assists_total = 0

wins = 0
lose = 0

for single_game in matchdata_20_games:
    kills_total = single_game["kills"] + kills_total

    if single_game["win"] == True:
        wins += 1
    if single_game["win"] == False:
        lose += 1

winrate = wins / len(matchdata_20_games)
kills_avrg = kills_total / len(matchdata_20_games)

print(kills_total)
print(kills_avrg)
print(wins)
print(lose)
print(winrate)

#######################################################################################################################

#check if tournamentcode
#????

# looking for tournament code
"""
if " " not in info["tournamentCode"]:
    print("Primeleaguegame", info["tournamentCode"])
"""
