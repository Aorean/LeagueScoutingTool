from dotenv import load_dotenv
import requests
import os

load_dotenv()

SAMPLE_SUMMONER_ID = "Aorean"
SAMPLE_SUMMONER_TAG_LINE = "1311"
API_KEY = os.environ.get("API_KEY")
API_URL = "https://europe.api.riotgames.com"
API_ACCOUNTS_ENDPOINT = "riot/account/v1/accounts"
API_MATCH_ENDPOINT = "lol/match/v5/matches"


class Player:
    def __init__(self, champ, damage_taken):
        self.champ = champ
        self.damage_taken = damage_taken


def get_puuid(id, tag_line, api_key):
    return requests.get(f"{API_URL}/{API_ACCOUNTS_ENDPOINT}/by-riot-id/{id}/{tag_line}?api_key={api_key}").json()["puuid"]

def get_matchhistory(puuid, api_key):
    return requests.get(f"{API_URL}/{API_MATCH_ENDPOINT}/by-puuid/{puuid}/ids?{20250108}&api_key={api_key}").json()

def get_match(matchid, api_key):
    return requests.get(f"{API_URL}/{API_MATCH_ENDPOINT}/{matchid}?api_key={api_key}").json()


puuid = get_puuid(SAMPLE_SUMMONER_ID, SAMPLE_SUMMONER_TAG_LINE, API_KEY)
matchid = get_matchhistory(puuid, API_KEY)[0]
match = get_match(matchid, API_KEY)
players = []

for player in match["info"]["participants"]:
    if player["puuid"] not in [puuid, "SOME-OTHER-PUUID"]:
        continue

    p = Player(player["championName"], player["totalDamageTaken"])
    players.append(p)

for player in players:
    print(f"{player.champ}: {player.damage_taken}")