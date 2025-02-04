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

#######################################################################################################################

match1 = get_match(region, matchId, api_key)

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

    player_data_matchhistory()

#######################################################################################################################

