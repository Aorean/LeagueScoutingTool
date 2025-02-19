import requests
import time

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
    while True:
        response_history = requests.get(root_url + history_url)
        if response_history == 429:
            time.sleep(10)
            continue

        return response_history.json()


def get_match(region, matchId, api_key):
    root_url = f"https://{region}.api.riotgames.com/"
    match_url = f"/lol/match/v5/matches/{matchId}?api_key={api_key}"

    while True:
        resp_match = requests.get(root_url + match_url)
        if resp_match.status_code == 429:
            print("API limit reached, please wait!")
            time.sleep(10)
            continue

        response_match = resp_match.json()
        return response_match

def get_summoner_id(region, puuid, api_key):
    root_url = f"https://{region}.api.riotgames.com/"
    summoner_id_url = f"/lol/summoner/v4/summoners/by-puuid/{puuid}?api_key={api_key}"
    response_summoner_id = requests.get(root_url + summoner_id_url)

    response_summoner_id = response_summoner_id.json()

    return response_summoner_id

def get_rank(region, summoner_id, api_key):
    root_url = f"https://{region}.api.riotgames.com/"
    rank_url = f"/lol/league/v4/entries/by-summoner/{summoner_id}?api_key={api_key}"
    response_rank = requests.get(root_url + rank_url)

    response_rank = response_rank.json()

    return response_rank


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
            return player_scouting


#googlesheets api
