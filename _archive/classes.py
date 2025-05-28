from dotenv import load_dotenv
import os
from _archive import class_file as class_file

from backend.functions.api import get_puuid

region = "europe"                                                   #input("Region: ")
load_dotenv()
api_key = os.environ.get("api_key")


print(api_key)
print("For multiple Accounts put a ',' between the Riot IDs!")
riot_id = "Aorean#1311,Moris#RIVEN,QaQ#00000,iHateThisNerd#EUW"          #"G2 BrokenBlade#1918,G2 Caps#1323,FNC Upset#0308"                   #input("Riot ID: ")

#split gamertag, tagline
riot_ids = riot_id.split(",")
riot_gamenames_gametags = []

#seperating all riot ids
for id in riot_ids:
    gamename_tagline = id.split("#")
    riot_gamenames_gametags.append(gamename_tagline)

players = []

for account in riot_gamenames_gametags:

    puuid = get_puuid(summoner_name=account[0], tag_line=account[1], region=region, api_key=api_key)


    player1 = class_file.Player(puuid, account[0], account[1])


    players.append(player1)




for player in players:
    player.set_kda(5)
    print(player.kda)