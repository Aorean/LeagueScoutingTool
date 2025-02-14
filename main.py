# Try classes
# get a SQL Databank schema (break my data apart into smaller chunks)
#


from dotenv import load_dotenv
import os
import requests
from function_api import get_puuid, get_matchhistory, get_match
import pygsheets
import pandas as pd

load_dotenv()



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
            player_scouting["puuid"] = player["puuid"]
            player_scouting["gamertag"] = player["riotIdGameName"]
            player_scouting["tagline"] = player["riotIdTagline"]
            player_scouting["game_id"] = info["gameId"]
            player_scouting["team"] = player["teamId"]
            player_scouting["name"] = ign
            player_scouting["champ"] = player["championName"]
            player_scouting["champ_level"] = player["champLevel"]
            player_scouting["gold_earned"] = player["goldEarned"]
            player_scouting["item_1"] = player["item0"]
            player_scouting["item_2"] = player["item1"]
            player_scouting["item_3"] = player["item2"]
            player_scouting["item_4"] = player["item3"]
            player_scouting["item_5"] = player["item4"]
            player_scouting["item_6"] = player["item5"]

            player_scouting["primary_key_rune_0"] = player["perks"]["styles"][0]["selections"][0]["perk"]
            player_scouting["primary_rune_1"] = player["perks"]["styles"][0]["selections"][1]["perk"]
            player_scouting["primary_rune_2"] = player["perks"]["styles"][0]["selections"][2]["perk"]
            player_scouting["primary_rune_3"] = player["perks"]["styles"][0]["selections"][3]["perk"]

            player_scouting["secondary_rune 0"] = player["perks"]["styles"][1]["selections"][0]["perk"]
            player_scouting["secondary_rune 1"] = player["perks"]["styles"][1]["selections"][1]["perk"]

            player_scouting["statrune_defense"] = player["perks"]["statPerks"]["defense"]
            player_scouting["statrune_flex"] = player["perks"]["statPerks"]["flex"]
            player_scouting["statrune_offense"] = player["perks"]["statPerks"]["offense"]

            player_scouting["kills"] = player["kills"]
            player_scouting["deaths"] = player["deaths"]
            player_scouting["assists"] = player["assists"]
            player_scouting["visionscore"] = player["visionScore"]
            player_scouting["controlwards_placed"] = player["detectorWardsPlaced"]
            player_scouting["cs"] = player["totalMinionsKilled"]
            player_scouting["position"] = player["teamPosition"]
            player_scouting["kda"] = round(player["challenges"]["kda"], 2)
            player_scouting["summonerspells"] = summoner_spell
            player_scouting["dmg%"] = round(player["challenges"]["teamDamagePercentage"], 2)
            player_scouting["total dmg to champ"] = player["totalDamageDealtToChampions"]
            player_scouting["dmg_taken%"] = round(player["challenges"]["damageTakenOnTeamPercentage"], 2)
            player_scouting["total_dmg_taken"] = player["totalDamageTaken"]
            player_scouting["game_start_timestamp"] = info["gameStartTimestamp"]
            player_scouting["game_end_timestamp"] = info["gameEndTimestamp"]
            player_scouting["game_duration"] = info["gameDuration"]
            player_scouting["tournament_code"] = info["tournamentCode"]
            player_scouting["win"] = player["win"]

    return player_scouting



def role_opponent_data_matchhistory():
    for opponent in participant_dto:
        if (player_scouting["position"] == opponent["teamPosition"] and player_scouting["team"] != opponent["teamId"]):
            # merging riotId and riotTagLine
            # prev player_scouting

            opponent_gamename_a_tagline = []
            opponent_summoner_spell = []

            opponent_gamename_a_tagline.append(opponent["riotIdGameName"])
            opponent_gamename_a_tagline.append(opponent["riotIdTagline"])
            opponent_ign = opponent_gamename_a_tagline[0] + "#" + opponent_gamename_a_tagline[1]

            # merging summonerspells into a list
            opponent_summoner_spell.append(opponent["summoner1Id"])
            opponent_summoner_spell.append(opponent["summoner2Id"])

            #getting matchdata from role opponent
            role_opponent["puuid"] = opponent["puuid"]
            role_opponent["game_id"] = info["gameId"]
            role_opponent["team"] = opponent["teamId"]
            role_opponent["name"] = opponent_ign
            role_opponent["champ"] = opponent["championName"]
            role_opponent["champ_level"] = opponent["champLevel"]
            role_opponent["gold_earned"] = opponent["goldEarned"]
            role_opponent["item_1"] = opponent["item0"]
            role_opponent["item_2"] = opponent["item1"]
            role_opponent["item_3"] = opponent["item2"]
            role_opponent["item_4"] = opponent["item3"]
            role_opponent["item_5"] = opponent["item4"]
            role_opponent["item_6"] = opponent["item5"]

            role_opponent["primary_key_rune_0"] = opponent["perks"]["styles"][0]["selections"][0]["perk"]
            role_opponent["primary_rune_1"] = opponent["perks"]["styles"][0]["selections"][1]["perk"]
            role_opponent["primary_rune_2"] = opponent["perks"]["styles"][0]["selections"][2]["perk"]
            role_opponent["primary_rune_3"] = opponent["perks"]["styles"][0]["selections"][3]["perk"]

            role_opponent["secondary_rune 0"] = opponent["perks"]["styles"][1]["selections"][0]["perk"]
            role_opponent["secondary_rune 1"] = opponent["perks"]["styles"][1]["selections"][1]["perk"]

            role_opponent["statrune_defense"] = opponent["perks"]["statPerks"]["defense"]
            role_opponent["statrune_flex"] = opponent["perks"]["statPerks"]["flex"]
            role_opponent["statrune_offense"] = opponent["perks"]["statPerks"]["offense"]

            role_opponent["kills"] = opponent["kills"]
            role_opponent["deaths"] = opponent["deaths"]
            role_opponent["assists"] = opponent["assists"]
            role_opponent["visionscore"] = opponent["visionScore"]
            role_opponent["controlwards_placed"] = opponent["detectorWardsPlaced"]
            role_opponent["cs"] = opponent["totalMinionsKilled"]
            role_opponent["position"] = opponent["teamPosition"]
            role_opponent["kda"] = round(opponent["challenges"]["kda"], 2)
            role_opponent["summonerspells"] = opponent_summoner_spell
            role_opponent["dmg%"] = round(opponent["challenges"]["teamDamagePercentage"], 2)
            role_opponent["total dmg to champ"] = opponent["totalDamageDealtToChampions"]
            role_opponent["dmg_taken%"] = round(opponent["challenges"]["damageTakenOnTeamPercentage"], 2)
            role_opponent["total_dmg_taken"] = opponent["totalDamageTaken"]
            role_opponent["game_start_timestamp"] = info["gameStartTimestamp"]
            role_opponent["game_end_timestamp"] = info["gameEndTimestamp"]
            role_opponent["game_duration"] = info["gameDuration"]
            role_opponent["tournament_code"] = info["tournamentCode"]
            role_opponent["win"] = opponent["win"]

    return role_opponent


#######################################################################################################################
# test
"""
player_data_matchhistory()
print(player_scouting())
#
"""
matchdata_20_games = []
# list and dict for context
objectives_team = []

for matchId in matchhistory:
    match = get_match(region, matchId, api_key)
    player_scouting = {}
    role_opponent = {}

    # accessing the Dtos to process data into smaller packages
    # Match > MetadataDto
    metadata = match["metadata"]
    players = metadata["participants"]

    # Match > InfoDto
    info = match["info"]
    game_id = info["gameId"]
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

    gamename_a_tagline = []
    summoner_spell = []

    player_data_matchhistory()
    role_opponent_data_matchhistory()

    # appending alternating teams for better view in gsheet
    if player_scouting["team"] == 100:
        player_scouting["team"] = "Blue"
        role_opponent["team"] = "Red"
        matchdata_20_games.append(player_scouting)
        matchdata_20_games.append(role_opponent)
    if player_scouting["team"] == 200:
        role_opponent["team"] = "Blue"
        player_scouting["team"] = "Red"
        matchdata_20_games.append(role_opponent)
        matchdata_20_games.append(player_scouting)

    print(player_scouting["kda"])

    # checking each objective
    for team in teams:
        # list where every objective per team gets saved
        list_objectives = []
        # dict to save objective with keyword
        objectives = {}

        side = team["teamId"]
        objs = team["objectives"]
        objectives["game_id"] = info["gameId"]
        objectives["side"] = side
        # objectives["baron"] = objs["baron"]
        objectives["baronkills"] = objs["baron"]["kills"]
        objectives["baronfirst"] = objs["baron"]["first"]

        # objectives["dragon"] = objs["dragon"]
        objectives["dragonkills"] = objs["dragon"]["kills"]
        objectives["dragonfirst"] = objs["dragon"]["first"]

        # objectives["grubs"] = objs["horde"]
        objectives["grubskills"] = objs["horde"]["kills"]
        objectives["grubsfirst"] = objs["horde"]["first"]

        # objectives["rift_herald"] = objs["riftHerald"]
        objectives["rift_heraldkills"] = objs["riftHerald"]["kills"]
        objectives["rift_heraldfirst"] = objs["riftHerald"]["first"]

        # objectives["tower"] = objs["tower"]
        objectives["towerkills"] = objs["tower"]["kills"]
        objectives["towerfirst"] = objs["tower"]["first"]

        # objectives["inhibitor"] = objs["inhibitor"]
        objectives["inhibitorkills"] = objs["inhibitor"]["kills"]
        objectives["inhibitorfirst"] = objs["inhibitor"]["first"]

        # using dict above to create a connection between "side" and objectives "objectives_team"
        # putting that list into a list of the last 20 games "total_objectives_20_games"

        objectives_team.append(objectives)

###########################################################################################
# creating Dataframe for storing in Database, creating Dataframes after the SQL schema I created



player_df = pd.DataFrame()
playerinfo_df = pd.DataFrame()

for  in matchdata_20_games:
    # player_df
    player_create_df = pd.DataFrame({
        "puuid" : [match_info["puuid"]],
        "gamertag" : [match_info["gamertag"]],
        "tagline" : [match_info["tagline"]],
    })
    player_df = pd.concat([player_df, player_create_df])

    # playerinfo_df
    playerinfo_create_df = pd.Dataframe({
        "puuid": [match_info["puuid"]],
        "gamertag": [match_info["gamertag"]],  # necessary?
        "tagline": [match_info["tagline"]],  # necessary?
        # Elo
        # Winrate
        # Blue/Red Winrate
        # Stats vs Opponent
        "kda" : [match_info[""]]

    })



player_df = pd.DataFrame()
for match_id in matchhistory:
    game = get_match(region , matchId = match_id , api_key = api_key)
    player_processed = process_player(game , puuid = puuid)

    df = pd.concat([player_df , player_processed])

# player info
player_info_df = pd.DataFrame({




})



###########################################################################################


print(player_df)




###########################################################################################

# using cdragon to convert the numbers into names of f.e. items, runes, summoners, etc.)
# code copied 1 by 1 from tutorial, but doesnt work anyway lol
# dict creation from json_extraction works, but replacing the values doesnt

perk = "https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/perks.json"
perkstyle = "https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/perkstyles.json"

perk_json = requests.get(perk).json()
perkstyle_json = requests.get(perkstyle).json()

def json_extract(obj, key):

    arr = []

    def extract (obj, arr, key):
        if isinstance(obj, dict):
            for k, v in obj.items():
                if k == key:
                    arr.append(v)
                elif isinstance(v, (dict, list)):
                    extract(v, arr, key)
        elif isinstance(obj, list):
            for item in obj:
                extract(item, arr, key)

        return arr

    values = extract(obj, arr, key)
    return values

perk_ids = json_extract(perk_json, "id")
perk_name = json_extract(perk_json, "name")

perk_dict =dict(map(lambda i, j : (int(i), j), perk_ids, perk_name))

df_matchdata = pd.DataFrame(matchdata_20_games)
df_objectivedata = pd.DataFrame(objectives_team)

df_matchdata.replace(perk_dict)

print(perk_dict)

print(df_matchdata)
print(df_objectivedata)


#######################################################################################################################
# role opponent data processing

# needs to be in a for loop


#######################################################################################################################

# adding the data into the google sheet (some stuff needs to be fixed (obj, kda)
service_acc = pygsheets.authorize(service_account_file="json//spreadsheet-automator-449612-b3a5d5ca0942.json")

sheet = service_acc.open_by_url(
    "https://docs.google.com/spreadsheets/d/1iHweQST_7PNmN-PbfCDlZFUAhQzesQLrw60-WgrNK1I/edit?usp=sharing")

google_sheet = sheet.worksheet("title", "Metadata")

google_sheet.set_dataframe(df_matchdata, "A1")
google_sheet.set_dataframe(df_objectivedata, "AR1")

#######################################################################################################################

"""

# Match > InfoDto > TeamDto > BanDto
#banns red/blue + championId und pickTurn
# [0] blueside [1] redside
banns_total_red = []
banns_total_blue = []

teaminfo_blue = teams[0]
teaminfo_red = teams[1]
banns_blue = teaminfo_blue["bans"]
banns_total_red.append(banns_blue)
banns_red = teaminfo_red["bans"]
banns_total_red.append(banns_red)
print(banns_total_blue + banns_total_red)

#following doesnt work

#atakhan = obj_blue["atakhan"]
#obj_total.append(atakhan)
baron = obj_blue["baron"]
obj_total.append(baron)
champion_kills = obj_blue["champion"]
obj_total.append(champion_kills)
dragon = obj_blue["dragon"]
obj_total.append(dragon)
grubs = obj_blue["horde"]
obj_total.append(grubs)
inhibitors = obj_blue["inhibitor"]
obj_total.append(inhibitors)
rift_herald = obj_blue["riftHerald"]
obj_total.append(rift_herald)
tower = obj_blue["tower"]
obj_total.append(tower)


print(obj_total)
# [0] blueside [1] redside

#"atakhan", "baron", "champion", "dragon", "horde", "inhibitor", "riftHerald", "tower", "win"
#print(teams)
#print(ban_id)

#######################################################################################################################

# print(puuid)

################################################

# print(matchhistory)

#################################################

#print(match1)

#################################################

# print(match_df1)

#################################################

# player = puuid

#################################################

#print(match)
"""