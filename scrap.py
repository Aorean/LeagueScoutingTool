# hahalololl


from dotenv import load_dotenv
import os
import requests
from function_api import get_puuid, get_matchhistory, get_match
import pygsheets
import pandas as pd

load_dotenv()

# vorbereitung auf google sheets


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
            player_scouting["game_id"] = info["gameId"]
            player_scouting["team"] = player["teamId"]
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
            role_opponent["game_id"] = info["gameId"]
            role_opponent["team"] = opponent["teamId"]
            role_opponent["name"] = opponent_ign
            role_opponent["champ"] = opponent["championName"]
            role_opponent["kills"] = opponent["kills"]
            role_opponent["deaths"] = opponent["deaths"]
            role_opponent["assists"] = opponent["assists"]
            role_opponent["cs"] = opponent["totalMinionsKilled"]
            role_opponent["position"] = opponent["teamPosition"]
            role_opponent["kda"] = opponent["challenges"]["kda"]
            role_opponent["summonerspells"] = summoner_spell
            role_opponent["total dmg to champ"] = opponent["totalDamageDealtToChampions"]
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

        # appending alternating teams for better view in gsheet

"""

    ##################################################################################################


    role_opponent = {}

    # prev riot_id_game_name
    opponent_riot_id_game_name = []

    # prev detail_player
    is_this_needed = {}

    # prev gamename_a_tagline
    opponent_gamename_a_tagline = []

    # prev summoner_spell
    opponent_summoner_spell = []

    opponent_matchdata_20_games.append(role_opponent)

    if player_scouting["team"] == 100:
        player_scouting["team"] = "Blue"
        role_opponent["team"] = "Red"
        matchdata_20_games.append(player_data_matchhistory())
        matchdata_20_games.append(role_opponent_data_matchhistory())
    if player_scouting["team"] == 200:
        role_opponent["team"] = "Blue"
        player_scouting["team"] = "Red"
        matchdata_20_games.append(role_opponent_data_matchhistory())
        matchdata_20_games.append(player_data_matchhistory())
        if role_opponent["team"] == 100:
            role_opponent["team"] = "Blue"
            player_scouting["team"] = "Red"
            matchdata_20_games.append(role_opponent_data_matchhistory())
            matchdata_20_games.append(player_data_matchhistory())
        if role_opponent["team"] == 200:
            matchdata_20_games.append(player_data_matchhistory())
            matchdata_20_games.append(role_opponent_data_matchhistory())
"""
df_matchdata = pd.DataFrame(matchdata_20_games)
df_objectivedata = pd.DataFrame(objectives_team)

print(df_matchdata)
print(df_objectivedata)

# i would like to get objectives from the 2 lists printed in altering order, but idk how yet
"""
for element in total_data_20_games:
    for player_stat in matchdata_20_games:
        print(player_stat)
        break

    for obj_stat in total_objectives_20_games:
        print(obj_stat)
        break
"""
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
google_sheet.set_dataframe(df_objectivedata, "P1")

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


obj_blue = []
obj_red = []
obj_total = [obj_blue , obj_red]

obj_blue_dict = teaminfo_blue["objectives"]
obj_blue.append(obj_blue_dict)
obj_red_dict = teaminfo_red["objectives"]
obj_red.append(obj_red_dict)



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


match_data = match["info"]
player_data = match_data["participants"]

print(len(player_data))
for player in match_data["participants"]:
    perks = player["perks"]
    primary_perk = perks["styles"]
    dgiapdjng = primary_perk[0]
    print("!!!!!!!!" , dgiapdjng["selections"])

#    primary_tree = primary_perk["perk"] , primary_perk["var1"] , primary_perk["var2"] , primary_perk["var3"]
#    secondary_tree = secondary_perk["var1"] , secondary_perk["var2"]








#######################################################################################################################

print(player_info)
print(player_info["Moris "])
print(len(player_info))

##for player in participant_dto:
    ##print(riot_id_game_name)


for game in matchhistory:
    get_match(region, matchId, api_key)
    match = get_match(region, matchId, api_key)
    print(champions)



    match_df = pd.DataFrame(match)
    champions_played = match["InfoDto"]["ParticipantDto"]["championName"]
    print(match_df)
    print(champions_played)


# match_df1 = pd.DataFrame(match1)


###############################################

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