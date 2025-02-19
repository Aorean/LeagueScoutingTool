# Try classes
# get a SQL Databank schema (break my data apart into smaller chunks)
#
from numpy.ma.core import append

import json

from dotenv import load_dotenv
import os

from function_api import get_puuid, get_matchhistory, get_match, get_summoner_id, get_rank
import pygsheets
import pandas as pd



load_dotenv()

region = "europe"                                                   #input("Region: ")

api_key = os.environ.get("api_key")

print("For multiple Accounts put a ',' between the Riot IDs!")
riot_id = "Aorean#1311,Moris#EUW,QaQ#00000"                      #input("Riot ID: ")

#split gamertag, tagline
riot_ids = riot_id.split(",")
riot_gamenames_gametags = []


#Dateframes

#Player                 DONE
#Puuid, Gamertag, Tagline
Dataframe_Player = pd.DataFrame()

#Player_Info            DONE
#Puuid, Matchhistory, Elo, Winrate, Blue/Red Winrate, CS diff., Level diff., Gold diff., Visionscore diff
Dataframe_Player_Info = pd.DataFrame()
#Needed for merge
Dataframe_average_stats =pd.DataFrame()


#Matchhistory           DONE
#MatchID, Participants, Gamestart, Gameend, Gamedurattion, Tournamentcode
Dataframe_Matchhistory = pd.DataFrame()

#Match                  DONE
#Puuid, MatchID, Queuetyp, Gamertag, Tagline, Team, Champion, Championlevel, Gold earned, Position, KDA, Kills, Deaths,
#Assists, Visionscore, Controlwards, Objectives, Result(W/L)
Dataframe_Match = pd.DataFrame()

#Opponent               DONE
#Puuid, MatchID, Queuetyp, Gamertag, Tagline, Team, Champion, Championlevel, Gold earned, Position, KDA, Kills, Deaths,
#Assists, Visionscore, Controlwards, Objectives, Result(W/L)
Dataframe_Opponent = pd.DataFrame()

#Objecives
#MatchID, Puuid, Team, Tower, Grubs, Drake, Herald, Atakhan, Baron, Inhibitor
Dataframe_Objectives = pd.DataFrame()

#Championpool
#Puuid, Gamertag, Tagline, Champion, Winrate, KDA, Avrg. Kills/Deaths/Assists, Winrate/Champion, KDA/Champion,
# CS/D/Champion, Leveldiff/Champion, Avrg. dmg%, Avrg. dmg taken%, Mastery, Role, Amount of Games
Dataframe_Championpool = pd.DataFrame()


for id in riot_ids:
    gamename_tagline = id.split("#")
    riot_gamenames_gametags.append(gamename_tagline)

#puuids + SummonerId
puuids = []
summoner_ids = {}
rank_datas = {}

for account in riot_gamenames_gametags:
    puuid_player = get_puuid(account[0], account[1], region, api_key)
    puuids.append(puuid_player)

    summoner_id = get_summoner_id("EUW1", puuid_player, api_key)
    summoner_ids[puuid_player] = summoner_id["id"]

    rank_data = get_rank("EUW1", summoner_id["id"], api_key)

    rank_dict = {}
    rank_dict["rank"] = rank_data[0]["tier"] + " " + rank_data[0]["rank"]
    rank_dict["wins"] = rank_data[0]["wins"]
    rank_dict["losses"] = rank_data[0]["losses"]
    rank_dict["games_total"] = rank_data[0]["wins"] + rank_data[0]["losses"]

    rank_datas[puuid_player] = rank_dict

    # Dateframes
    # Player
    # Puuid, Gamertag, Tagline
    temp_Dataframe_Player = pd.DataFrame({
        "PUUID" : [puuid_player],
        "Gamertag" : [account[0]],
        "Tagline" : [account[1]]
    })
    Dataframe_Player = pd.concat([Dataframe_Player, temp_Dataframe_Player])

matchhistories = {}
puuid_match = {}


# get matchhistories
for player in puuids:
    matchhistories[player] = get_matchhistory(region, player, api_key, startTime=20250108)
    # Player_Info
    # PUUID, Matchhistory, Elo, Wins, Losses, Total, Winrate
    temp_Dataframe_Matchhistory = pd.DataFrame({
        "PUUID" : [player],
        "Matchhistory" : [matchhistories[player]],
        "Elo" : rank_datas[player]["rank"],
        "Wins" : rank_datas[player]["wins"],
        "Losses": rank_datas[player]["losses"],
        "games_total": rank_datas[player]["games_total"],
        "winrate" : round((rank_datas[player]["wins"] / rank_datas[player]["games_total"] * 100), 2) #remove *100 later
    })
    Dataframe_Player_Info = pd.concat([Dataframe_Player_Info, temp_Dataframe_Matchhistory])


for puuid in matchhistories:
    match_history_for_matchdata = matchhistories[puuid]

    matches = []
    opponent_matches = []
    puuid_opponent = []

    average_stats = {}
    cs = []
    level = []
    exp = []
    gold = []
    visionscore = []

    cs_d = []
    gold_d = []
    exp_d = []
    level_d = []
    visionscore_d = []

    for match in match_history_for_matchdata:
        player_scouting = {}
        role_opponent = {}

        stats_compare = {}

        matchdata = get_match(region, match, api_key)
        # accessing the Dtos to process data into smaller packages
        # Match > MetadataDto

        metadata = matchdata["metadata"]
        players = metadata["participants"]

        # Match > InfoDto
        info = matchdata["info"]
        game_id = info["gameId"]
        game_creation = info["gameCreation"]
        game_start = info["gameStartTimestamp"]
        game_end = info["gameEndTimestamp"]
        game_duration = info["gameDuration"]
        game_mode = info["gameMode"]
        game_version = info["gameVersion"]  # wird später noch als "Patch" eingepflegt
        tournament_code = info["tournamentCode"]
        teams = info["teams"]

        # Match > InfoDto > ParticipantDt#    riot_id_game_name.append(player["riotIdGameName"])
        participant_dto = info["participants"]



        for player in participant_dto:
            if puuid == player["puuid"]:
                # merging riotId and riotTagLine
                #gamename_a_tagline.append(player["riotIdGameName"])
                #gamename_a_tagline.append(player["riotIdTagline"])
                #ign = gamename_a_tagline[0] + "#" + gamename_a_tagline[1]

                # merging summonerspells into a list
                #summoner_spell.append(player["summoner1Id"])
                #summoner_spell.append(player["summoner2Id"])

                # getting stats from json
                player_scouting["puuid"] = player["puuid"]
                player_scouting["gamertag"] = player["riotIdGameName"]
                player_scouting["tagline"] = player["riotIdTagline"]
                player_scouting["game_id"] = info["gameId"]
                player_scouting["gamemode"] = info["gameMode"]
                player_scouting["team"] = player["teamId"]
                player_scouting["name"] = player["riotIdGameName"] + "#" + player["riotIdTagline"]
                player_scouting["champ"] = player["championName"]
                player_scouting["champ_level"] = player["champLevel"]
                player_scouting["exp"] = player["champExperience"]
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
                player_scouting["summonerspell1"] = player["summoner1Id"]
                player_scouting["summonerspell2"] = player["summoner2Id"]
                player_scouting["total dmg to champ"] = player["totalDamageDealtToChampions"]
                player_scouting["total_dmg_taken"] = player["totalDamageTaken"]
                player_scouting["game_start_timestamp"] = info["gameStartTimestamp"]
                player_scouting["game_end_timestamp"] = info["gameEndTimestamp"]
                player_scouting["game_duration"] = info["gameDuration"]
                player_scouting["tournament_code"] = info["tournamentCode"]
                player_scouting["win"] = player["win"]

                if "challenges" in player:
                    player_scouting["dmg_taken%"] = round(player["challenges"]["damageTakenOnTeamPercentage"], 2)
                    player_scouting["dmg%"] = round(player["challenges"]["teamDamagePercentage"], 2)
                    player_scouting["kda"] = round(player["challenges"]["kda"], 2)
                else:
                    continue
                """
                stats_player["cs"] = player_scouting["cs"]
                stats_player["champ_level"] = player_scouting["champ_level"]
                stats_player["exp"] = player_scouting["exp"]
                stats_player["gold_earned"] = player_scouting["gold_earned"]
                stats_player["visionscore"] = player_scouting["visionscore"]
                """
                #getting a dict with lists in with stats to get average for 20 games

                cs.append(player_scouting["cs"])
                level.append(player_scouting["champ_level"])
                exp.append(player_scouting["exp"])
                gold.append(player_scouting["gold_earned"])
                visionscore.append(player_scouting["visionscore"])


        for player in participant_dto:
            if (player_scouting["position"] == player["teamPosition"] and player_scouting["team"] != player[
                "teamId"]):
                # merging riotId and riotTagLine
                # prev player_scouting
                role_opponent["puuid"] = player["puuid"]
                role_opponent["gamertag"] = player["riotIdGameName"]
                role_opponent["tagline"] = player["riotIdTagline"]
                role_opponent["game_id"] = info["gameId"]
                role_opponent["gamemode"] = info["gameMode"]
                role_opponent["team"] = player["teamId"]
                role_opponent["name"] = player["riotIdGameName"] + "#" + player["riotIdTagline"]
                role_opponent["champ"] = player["championName"]
                role_opponent["champ_level"] = player["champLevel"]
                role_opponent["exp"] = player["champExperience"]
                role_opponent["gold_earned"] = player["goldEarned"]
                role_opponent["item_1"] = player["item0"]
                role_opponent["item_2"] = player["item1"]
                role_opponent["item_3"] = player["item2"]
                role_opponent["item_4"] = player["item3"]
                role_opponent["item_5"] = player["item4"]
                role_opponent["item_6"] = player["item5"]

                role_opponent["primary_key_rune_0"] = player["perks"]["styles"][0]["selections"][0]["perk"]
                role_opponent["primary_rune_1"] = player["perks"]["styles"][0]["selections"][1]["perk"]
                role_opponent["primary_rune_2"] = player["perks"]["styles"][0]["selections"][2]["perk"]
                role_opponent["primary_rune_3"] = player["perks"]["styles"][0]["selections"][3]["perk"]

                role_opponent["secondary_rune 0"] = player["perks"]["styles"][1]["selections"][0]["perk"]
                role_opponent["secondary_rune 1"] = player["perks"]["styles"][1]["selections"][1]["perk"]

                role_opponent["statrune_defense"] = player["perks"]["statPerks"]["defense"]
                role_opponent["statrune_flex"] = player["perks"]["statPerks"]["flex"]
                role_opponent["statrune_offense"] = player["perks"]["statPerks"]["offense"]

                role_opponent["kills"] = player["kills"]
                role_opponent["deaths"] = player["deaths"]
                role_opponent["assists"] = player["assists"]
                role_opponent["visionscore"] = player["visionScore"]
                role_opponent["controlwards_placed"] = player["detectorWardsPlaced"]
                role_opponent["cs"] = player["totalMinionsKilled"]
                role_opponent["position"] = player["teamPosition"]
                role_opponent["summonerspell1"] = player["summoner1Id"]
                role_opponent["summonerspell2"] = player["summoner2Id"]
                role_opponent["total dmg to champ"] = player["totalDamageDealtToChampions"]
                role_opponent["total_dmg_taken"] = player["totalDamageTaken"]
                role_opponent["game_start_timestamp"] = info["gameStartTimestamp"]
                role_opponent["game_end_timestamp"] = info["gameEndTimestamp"]
                role_opponent["game_duration"] = info["gameDuration"]
                role_opponent["tournament_code"] = info["tournamentCode"]
                role_opponent["win"] = player["win"]

                puuid_opponent.append(role_opponent["puuid"])

                cs_d.append(role_opponent["cs"])
                gold_d.append(role_opponent["champ_level"])
                exp_d.append(role_opponent["exp"])
                level_d.append(role_opponent["gold_earned"])
                visionscore_d.append(role_opponent["visionscore"])

        matches.append(player_scouting)
        opponent_matches.append(role_opponent)

        #Dataframes
        #Matchhistory
        Dataframe_Matchhistory_temp = pd.DataFrame({
            "PUUID" : [puuid],
            "Match_ID" : [game_id],
            "Participants" : [players],
            "Gamestart" : [game_start],
            "Gameend" : [game_end],
            "Gameduration" : [game_duration],
            "Tournamentcode" : [tournament_code]
        })
        Dataframe_Matchhistory = pd.concat([Dataframe_Matchhistory, Dataframe_Matchhistory_temp])

        #Dataframes
        #Match



        Dataframe_Match_temp = pd.DataFrame({
            "PUUID": [puuid],
            "Match_ID": [game_id],
            "Gamestart": [game_start],
            "Gameend": [game_end],
            "Gameduration": [game_duration],
            "Tournamentcode": [tournament_code],
            "Queuetyp" : [game_mode],
            "Ign" : [player_scouting["name"]],
            "Team" : [player_scouting["team"]],
            "Champ" : [player_scouting["champ"]],
            "Level" : [player_scouting["champ_level"]],
            "Position" : player_scouting["position"],

            "Kills": player_scouting["kills"],
            "Deaths": player_scouting["deaths"],
            "Assists": player_scouting["assists"],
            "Controlwards_Placed": player_scouting["controlwards_placed"],
            #"Objectives": player_scouting["objectives"], create a list for objectives
            "Win/Lose": player_scouting["win"],
        })

        Dataframe_Match = pd.concat([Dataframe_Match, Dataframe_Match_temp])

        #create a new df for that, if data is in the dict, merge them into the main df
        """        
        if "kda" in player_scouting:
            "KDA": player_scouting["kda"],
            "Dmg%":
            "Dmgtaken%":
        """


        #Dataframe
        #Opponent

        Dataframe_Opponent_temp = pd.DataFrame({
            "PUUID": role_opponent["puuid"],
            "Match_ID": [game_id],
            "Gamestart": [game_start],
            "Gameend": [game_end],
            "Gameduration": [game_duration],
            "Tournamentcode": [tournament_code],
            "Queuetyp" : [game_mode],
            "Ign" : [role_opponent["name"]],
            "Team" : [role_opponent["team"]],
            "Champ" : [role_opponent["champ"]],
            "Level" : [role_opponent["champ_level"]],
            "Position" : role_opponent["position"],

            "Kills": role_opponent["kills"],
            "Deaths": role_opponent["deaths"],
            "Assists": role_opponent["assists"],
            "Controlwards_Placed": role_opponent["controlwards_placed"],
            #"Objectives": player_scouting["objectives"], create a list for objectives
            "Win/Lose": role_opponent["win"],
        })

        Dataframe_Opponent = pd.concat([Dataframe_Opponent, Dataframe_Opponent_temp])

        #create a new df for that, if data is in the dict, merge them into the main df
        """        
        if "kda" in player_scouting:
            "KDA": player_scouting["kda"],
            "Dmg%":
            "Dmgtaken%":
        """
    #getting average per player
    # Dateframes
    # Player_Info
    # Avrg CS, Avrg Level, Avrg exp, Avrg Gold, Avrg Visionscore, CS diff., Level diff., Gold diff., Visionscore diff
    avrg_cs = round(sum(cs) / len(cs), 2)
    avrg_level = round(sum(level) / len(level), 2)
    avrg_exp = round(sum(exp) / len(exp), 2)
    avrg_gold = round(sum(gold) / len(gold), 2)
    avrg_visionscore = round(sum(visionscore) / len(visionscore), 2)

    avrg_cs_d =  round(avrg_cs - sum(cs_d) / len(cs_d), 2)
    avrg_gold_d = round(avrg_level - sum(gold_d) / len(gold_d), 2)
    avrg_exp_d = round(avrg_exp - sum(exp_d) / len(exp_d), 2)
    avrg_level_d = round(avrg_level - sum(level_d) / len(level_d), 2)
    avrg_visionscore_d = round(avrg_visionscore - sum(visionscore_d) / len(visionscore_d), 2)

    average_stats["puuid"] = puuid
    average_stats["cs"] = avrg_cs
    average_stats["level"] = avrg_level
    average_stats["exp"] = avrg_exp
    average_stats["gold"] = avrg_gold
    average_stats["visionscore"] = avrg_visionscore

    average_stats["cs_diff"] = avrg_cs_d
    average_stats["gold_diff"] = avrg_gold_d
    average_stats["exp_diff"] = avrg_exp_d
    average_stats["level_diff"] = avrg_level_d
    average_stats["visionscore_diff"] = avrg_visionscore_d

    Dataframe_average_stats_temp = pd.DataFrame({
        "PUUID" : [average_stats["puuid"]],
        "cs" : [average_stats["cs"]],
        "level" : [average_stats["level"]],
        "exp" : [average_stats["exp"]],
        "gold" : [average_stats["gold"]],
        "visionscore" : [average_stats["visionscore"]],
        "cs_diff" : [average_stats["cs_diff"]],
        "gold_diff" : [average_stats["gold_diff"]],
        "exp_diff" : [average_stats["exp_diff"]],
        "level_diff" : [average_stats["level_diff"]],
        "visionscore_diff" : [average_stats["visionscore_diff"]]
    })

    Dataframe_average_stats = pd.concat([Dataframe_average_stats, Dataframe_average_stats_temp])

    puuid_match[puuid] = matches
    puuid_match[puuid_opponent[0]] = opponent_matches

Dataframe_Player_Info = pd.merge(Dataframe_Player_Info, Dataframe_average_stats, on="PUUID")

print("Dataframe_Match" , Dataframe_Match)

#getting Dataframes for all matches and appending them, so they are in 1 Dataframe
full_match_info_df = pd.DataFrame()

for game_puuid in puuid_match:
    match_info = puuid_match[game_puuid]
    match_info_df = pd.DataFrame(match_info)

    full_match_info_df = pd.concat([full_match_info_df , match_info_df])

with open("puuid_match" , "w") as f:
    f.write(json.dumps(puuid_match, indent=4))

df_puuid_match = pd.DataFrame(puuid_match)

print(df_puuid_match)

# adding the data into the google sheet (some stuff needs to be fixed (obj, kda)
service_acc = pygsheets.authorize(service_account_file="json//spreadsheet-automator-449612-b3a5d5ca0942.json")

sheet = service_acc.open_by_url(
    "https://docs.google.com/spreadsheets/d/1iHweQST_7PNmN-PbfCDlZFUAhQzesQLrw60-WgrNK1I/edit?usp=sharing")

#inactive
"""google_sheet = sheet.worksheet("title", "Diagramme/Layouts")
google_sheet.set_dataframe(full_match_info_df, "A1")"""

google_sheet_test = sheet.worksheet("title", "DF_PLAYER")
google_sheet_test.set_dataframe(Dataframe_Player, "A1")

google_sheet_test = sheet.worksheet("title", "DF_PLAYER_INFO")
google_sheet_test.set_dataframe(Dataframe_Player_Info, "A1")

google_sheet_test = sheet.worksheet("title", "DF_Matchhistory")
google_sheet_test.set_dataframe(Dataframe_Matchhistory, "A1")

google_sheet_test = sheet.worksheet("title", "DF_Match")
google_sheet_test.set_dataframe(Dataframe_Match, "A1")

#for side by side
google_sheet_test = sheet.worksheet("title", "DF_Match")
google_sheet_test.set_dataframe(Dataframe_Opponent, "S1")

google_sheet_test = sheet.worksheet("title", "DF_Opponent")
google_sheet_test.set_dataframe(Dataframe_Opponent, "A1")

#for future DFs
"""google_sheet_test = sheet.worksheet("title", "Tabellenblatt3")
google_sheet_test.set_dataframe(Dataframe_Opponent, "A1")

google_sheet_test = sheet.worksheet("title", "Tabellenblatt3")
google_sheet_test.set_dataframe(Dataframe_Opponent, "A1")"""


    #result:
    # puuid_match =
    # {puuid1 :
    # [
    # matchid1 : match.json1 ,
    # matchid2 : match.json2 ,
    # ...
    # ]
    # puuid2 :
    # [
    # matchid1 : match.json1 ,
    # matchid2 : match.json2 ,
    # ...
    # ]
    # }










# {puuid1 :
# [
# matchid1 : match.json1 ,
# matchid2 : match.json2 ,
# ...
# ]
# puuid2 :
# [
# matchid1 : match.json1 ,
# matchid2 : match.json2 ,
# ...
# ]
# }


