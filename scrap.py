from dotenv import load_dotenv
import os
import requests


load_dotenv()

region = "europe"

summoner_name = "Aorean"
tag_line = "1311"
api_key = os.environ.get("api_key")

root_url = f"https://{region}.api.riotgames.com/"
puuid_url = f"riot/account/v1/accounts/by-riot-id/{summoner_name}/{tag_line}?api_key={api_key}"

response_puuid = requests.get(root_url + puuid_url)
puuid = response_puuid.json()

print(puuid)