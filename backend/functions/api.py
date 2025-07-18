import requests
import time
import json
import os

def get_puuid(summoner_name: str, tag_line, region, api_key):
    # request Riot API to get puuid for further use
    root_url = f"https://{region}.api.riotgames.com/"
    puuid_url = f"riot/account/v1/accounts/by-riot-id/{summoner_name}/{tag_line}?api_key={api_key}"

    while True:
        response_puuid = requests.get(root_url + puuid_url)
        if (response_puuid.status_code == 429) or (response_puuid.status_code == 502) or (response_puuid.status_code == 504):
            if response_puuid.status_code == 429:
                print("API limit reached, please wait!")
            if response_puuid.status_code == 502:
                print("Bad Gateaway")
            if response_puuid.status_code == 504:
                print("Gateaway Timeout")
            time.sleep(120)

            continue
        

        puuid = response_puuid.json()["puuid"]

        return puuid

def get_matchhistory(region, puuid, api_key, startindex):
    root_url = f"https://{region}.api.riotgames.com/"
    history_url = f"lol/match/v5/matches/by-puuid/{puuid}/ids?startTime=20250108&start={startindex}&count=100&api_key={api_key}"
    while True:
        response_history = requests.get(root_url + history_url)
        if response_history == 429:
            time.sleep(120)
            continue

        response = response_history.json()


        return response_history.json()

#/ids?start=1000&count=100&

def get_match(region, matchId, api_key):
    root_url = f"https://{region}.api.riotgames.com/"
    match_url = f"/lol/match/v5/matches/{matchId}?api_key={api_key}"

    while True:
        resp_match = requests.get(root_url + match_url)
        if (resp_match.status_code == 429) or (resp_match.status_code == 502) or (resp_match.status_code == 504):
            if resp_match.status_code == 429:
                print("API limit reached, please wait!")
            if resp_match.status_code == 502:
                print("Bad Gateaway")
            if resp_match.status_code == 504:
                print("Gateaway Timeout")
            time.sleep(120)

            continue

        response_match = resp_match.json()

        return response_match


#seems like riot changed stuff and i dont need this anymore
def get_summoner_id(region, puuid, api_key):
    root_url = f"https://{region}.api.riotgames.com/"
    summoner_id_url = f"/lol/summoner/v4/summoners/by-puuid/{puuid}?api_key={api_key}"
    while True:
        response_summoner_id = requests.get(root_url + summoner_id_url)
        if (response_summoner_id.status_code == 429) or (response_summoner_id.status_code == 502) or (response_summoner_id.status_code == 504):
            if response_summoner_id.status_code == 429:
                print("API limit reached, please wait!")
            if response_summoner_id.status_code == 502:
                print("Bad Gateaway")
            if response_summoner_id.status_code == 504:
                print("Gateaway Timeout")
            time.sleep(120) 

            continue
    

        response_summoner_id = response_summoner_id.json()

        return response_summoner_id

def get_rank(region, summoner_id, api_key):
    root_url = f"https://{region}.api.riotgames.com/"
    rank_url = f"/lol/league/v4/entries/by-puuid/{summoner_id}?api_key={api_key}"
    while True:
        response_rank = requests.get(root_url + rank_url)
        if (response_rank.status_code == 429) or (response_rank.status_code == 502) or (response_rank.status_code == 504):
            if response_rank.status_code == 429:
                print("API limit reached, please wait!")
            if response_rank.status_code == 502:
                print("Bad Gateaway")
            if response_rank.status_code == 504:
                print("Gateaway Timeout")
            time.sleep(120)

            continue
    
        response_rank = response_rank.json()

        return response_rank

def get_mastery(region, puuid, api_key):
    if region == "europe":
        region = "euw1"
    root_url = f"https://{region}.api.riotgames.com/"
    mastery_url = f"lol/champion-mastery/v4/champion-masteries/by-puuid/{puuid}?api_key={api_key}"
    while True:
        resp_mastery = requests.get(root_url + mastery_url)
        if (resp_mastery.status_code == 429) or (resp_mastery.status_code == 502) or (resp_mastery.status_code == 504):
            if resp_mastery.status_code == 429:
                print("API limit reached, please wait!")
            if resp_mastery.status_code == 502:
                print("Bad Gateaway")
            if resp_mastery.status_code == 504:
                print("Gateaway Timeout")
            time.sleep(120)

            continue

        resp_mastery = resp_mastery.json()

        return resp_mastery