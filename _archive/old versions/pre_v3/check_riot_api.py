from backend.functions.api import get_puuid, get_match,  get_matchhistory


import os
from dotenv import load_dotenv
load_dotenv()

test_api_key = os.environ.get("api_key")
test_data = []

test_puuid = get_puuid(summoner_name = "Aorean", tag_line="1311", region = "europe", api_key=test_api_key)
test_matchhistory = get_matchhistory(region = "europe", puuid = test_puuid, api_key=test_api_key, startTime=20250108)
test_getmatch = get_match(region = "europe", matchId = test_matchhistory[0], api_key = test_api_key)

print(test_puuid)
print(test_matchhistory)
print(test_getmatch)