import requests

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