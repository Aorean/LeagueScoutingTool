# Try def_classes
# get a SQL Databank schema (break my data apart into smaller chunks)
# add functions, for better overview

#dict for every Dataframe
#key is primary key for SQL

from dotenv import load_dotenv
import os

#import api functions
from backend.functions.function_api import get_puuid, get_summoner_id, get_rank

#import def_classes
from backend.def_classes.player import Player
from def_classes.player_info import Player_Info


load_dotenv()

#Login for Database
db_username = os.environ.get("db_username")
db_host = os.environ.get("db_host")
db_port = os.environ.get("db_port")
db_name = os.environ.get("db_name")
db_password = os.environ.get("db_password")



region = "europe"                                                   #input("Region: ")

api_key = os.environ.get("api_key")

print("For multiple Accounts put a ',' between the Riot IDs!")
riot_id = "Aorean#1311,Moris#RIVEN,QaQ#00000,iHateThisNerd#EUW" #"G2 BrokenBlade#1918,G2 Caps#1323,FNC Upset#0308"                                #input("Riot ID: ")


#split gamertag, tagline
riot_ids = riot_id.split(",")
riot_gamenames_gametags = []

#seperating all riot ids
for id in riot_ids:
    gamename_tagline = id.split("#")
    riot_gamenames_gametags.append(gamename_tagline)


class_player = []
class_player_info = []

for account in riot_gamenames_gametags:
    #api requests
    puuid = get_puuid(summoner_name=account[0], tag_line=account[1], region=region, api_key=api_key)
    summoner_id = get_summoner_id(region="EUW1", puuid=puuid, api_key=api_key)
    rankdata = get_rank(region="EUW1", summoner_id=summoner_id["id"], api_key=api_key)

    elo = rankdata[0]["tier"] + " " + rankdata[0]["rank"]
    wins = rankdata[0]["wins"]
    losses = rankdata[0]["losses"]

    print(rankdata)

    player1 =  Player(puuid, account[0], account[1])
    playerinfo1 = Player_Info(puuid, elo, wins, losses)

    class_player.append(player1)
    class_player_info.append(playerinfo1)

for player in class_player:
    print(player.puuid)

for player in class_player_info:
    print(player.winrate)