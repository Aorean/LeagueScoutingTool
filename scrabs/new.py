# Try def_classes
# get a SQL Databank schema (break my data apart into smaller chunks)
# add functions, for better overview

import json

from dotenv import load_dotenv
import os

from function_api import get_puuid, get_matchhistory, get_match, get_summoner_id, get_rank
import pygsheets
import pandas as pd

from pangres import upsert
from sqlalchemy import text, create_engine
from sqlalchemy.engine import  URL
import psycopg2

load_dotenv()

#Login for Database
db_username = os.environ.get("db_username")
db_host = os.environ.get("db_host")
db_port = os.environ.get("db_port")
db_name = os.environ.get("db_name")
db_password = os.environ.get("db_password")



region = "europe"                                                   #input("Region: ")

api_key = os.environ.get("api_key")

print("For multiple Accounts put a ',' between the Riot IDs!")
riot_id = "Aorean#1311,Moris#25933,QaQ#00000,iHateThisNerd#EUW"                      #input("Riot ID: ")

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

#Objecives              DONE
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
puuid_champpool = {}


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


    # Dataframe
    # Champpool
    unique_champ_pool = {}
    stats_unique_champ_pool = {}

    all_champs = []

    for match in match_history_for_matchdata:
        player_scouting = {}
        role_opponent = {}

        stats_compare = {}

        # Dataframe
        # Champpool
        champ_wr = []
        champ_kda = []
        champ_kills = []
        champ_deaths = []
        champ_assists = []
        champ_visionscore = []

        champ_visionscore_d = []
        champ_exp_d = []
        champ_gold_d = []
        champ_cs_d = []

        champ_dmg_p = []
        champ_dmgtaken_p = []

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
                    player_scouting["dmg_taken%"] = "NaN"
                    player_scouting["dmg%"] = "NaN"
                    player_scouting["kda"] = "NaN"

                #getting a dict with lists in with stats to get average for 20 games
                cs.append(player_scouting["cs"])
                level.append(player_scouting["champ_level"])
                exp.append(player_scouting["exp"])
                gold.append(player_scouting["gold_earned"])
                visionscore.append(player_scouting["visionscore"])

                all_champs.append(player_scouting["champ"])

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

                if "challenges" in player:
                    role_opponent["dmg_taken%"] = round(player["challenges"]["damageTakenOnTeamPercentage"], 2)
                    role_opponent["dmg%"] = round(player["challenges"]["teamDamagePercentage"], 2)
                    role_opponent["kda"] = round(player["challenges"]["kda"], 2)
                else:
                    role_opponent["dmg_taken%"] = "NaN"
                    role_opponent["dmg%"] = "NaN"
                    role_opponent["kda"] = "NaN"

                cs_d.append(role_opponent["cs"])
                gold_d.append(role_opponent["champ_level"])
                exp_d.append(role_opponent["exp"])
                level_d.append(role_opponent["gold_earned"])
                visionscore_d.append(role_opponent["visionscore"])

        matches.append(player_scouting)
        opponent_matches.append(role_opponent)

        #Dataframes
        #Matchhistory
        KEY_PUUID_MATCH_ID_MATCHHISTORY = puuid , game_id
        Dataframe_Matchhistory_temp = pd.DataFrame({
            "KEY_PUUID_MATCH_ID": [KEY_PUUID_MATCH_ID_MATCHHISTORY],
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
        KEY_PUUID_MATCH_ID_MATCH = puuid , game_id
        Dataframe_Match_temp = pd.DataFrame({
            "KEY_PUUID_MATCH_ID" : [KEY_PUUID_MATCH_ID_MATCH],
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

            "KDA": player_scouting["kda"],
            "Kills": player_scouting["kills"],
            "Deaths": player_scouting["deaths"],
            "Assists": player_scouting["assists"],
            "Controlwards_Placed": player_scouting["controlwards_placed"],
            "Dmg_percent": player_scouting["dmg%"],
            "Dmgtaken_percent": player_scouting["dmg_taken%"],
            #"Objectives": player_scouting["objectives"], create a list for objectives
            "Win/Lose": player_scouting["win"],
        })

        Dataframe_Match = pd.concat([Dataframe_Match, Dataframe_Match_temp])

        #Dataframe
        #Opponent
        if game_mode == "CLASSIC":
            KEY_PUUID_MATCH_ID_ROLEOPPONENT = role_opponent["puuid"] , game_id
            Dataframe_Opponent_temp = pd.DataFrame({
                "KEY_PUUID_MATCH_ID" : [KEY_PUUID_MATCH_ID_ROLEOPPONENT],
                "Roleopponent_PUUID": role_opponent["puuid"],
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

                "KDA": role_opponent["kda"],
                "Kills": role_opponent["kills"],
                "Deaths": role_opponent["deaths"],
                "Assists": role_opponent["assists"],
                "Controlwards_Placed": role_opponent["controlwards_placed"],
                "Dmg_percent": role_opponent["dmg%"],
                "Dmgtaken_percent": role_opponent["dmg_taken%"],
                #"Objectives": player_scouting["objectives"], create a list for objectives
                "Win/Lose": role_opponent["win"],
            })

            Dataframe_Opponent = pd.concat([Dataframe_Opponent, Dataframe_Opponent_temp])

        # Objectives per team per Match ID
        for team in teams:
            # list where every objective per team gets saved
            list_objectives = []
            # dict to save objective with keyword
            objectives = {}

            side = team["teamId"]
            objs = team["objectives"]
            objectives["game_id"] = info["gameId"]
            objectives["side"] = side

            if player_scouting["team"] == team["teamId"]:
                objectives["puuid"] = player_scouting["puuid"]
            if role_opponent["team"] == team["teamId"]:
                objectives["puuid"] = role_opponent["puuid"]


            # atakhan
            if "atakhan" in objs:
                objectives["atakhankills"] = objs["atakhan"]["kills"]
                objectives["atakhanfirst"] = objs["atakhan"]["first"]
            else:
                objectives["atakhankills"] = 0
                objectives["atakhanfirst"] = 0

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
            KEY_PUUID_MATCH_ID_TEAM = objectives["puuid"] , game_id , side
            if game_mode == "CLASSIC":
                Dataframe_Objectives_temp = pd.DataFrame({
                    "KEY_PUUID_MATCH_ID_TEAM" : [KEY_PUUID_MATCH_ID_TEAM],
                    "PUUID" : [objectives["puuid"]],
                    "Match_ID": [game_id],
                    "Team": [side],
                    "Atakhankills" : [objectives["atakhankills"]],
                    "Atakhanfirst" : [objectives["atakhanfirst"]],
                    "Baronkills": [objectives["baronkills"]],
                    "Baronfirst": [objectives["baronfirst"]],
                    "Dragonkills": [objectives["dragonkills"]],
                    "Dragonfirst": [objectives["dragonfirst"]],
                    "Grubskills": [objectives["grubskills"]],
                    "Grubsfirst": [objectives["grubsfirst"]],
                    "Rift_Heraldkills": [objectives["rift_heraldkills"]],
                    "Rift_Heraldfirst": [objectives["rift_heraldfirst"]],
                    "Towerkills": [objectives["towerkills"]],
                    "Towerfirst": [objectives["towerfirst"]],
                    "Inhibitorkills": [objectives["inhibitorkills"]],
                    "Inhibitorfirst": [objectives["inhibitorfirst"]],
                })
                Dataframe_Objectives = pd.concat([Dataframe_Objectives, Dataframe_Objectives_temp])

        # Dateframes
        # Champpool
        if game_mode == "CLASSIC":
            champ_wr.append(player_scouting["win"])
            champ_kda.append(player_scouting["kda"])
            champ_kills.append(player_scouting["kills"])
            champ_deaths.append(player_scouting["deaths"])
            champ_assists.append(player_scouting["assists"])
            champ_visionscore.append(player_scouting["visionscore"])

            champ_visionscore_d.append((player_scouting["visionscore"] - role_opponent["visionscore"]))
            champ_exp_d.append((player_scouting["exp"] - role_opponent["exp"]))
            champ_gold_d.append((player_scouting["gold_earned"] - role_opponent["gold_earned"]))
            champ_cs_d.append((player_scouting["cs"] - role_opponent["cs"]))

            champ_dmg_p.append(player_scouting["dmg%"])
            champ_dmgtaken_p.append(player_scouting["dmg_taken%"])

            stats_unique_champ = {}

            #stats_unique_champ["puuid"] = puuid
            stats_unique_champ["champ"] = player_scouting["champ"]
            stats_unique_champ["win"] = champ_wr
            stats_unique_champ["champ_kda"] = champ_kda
            stats_unique_champ["champ_kills"] = champ_kills
            stats_unique_champ["champ_deaths"] = champ_deaths
            stats_unique_champ["champ_assists"] = champ_assists
            stats_unique_champ["champ_visionscore"] = champ_visionscore

            stats_unique_champ["champ_visionscore_d"] = champ_visionscore_d
            stats_unique_champ["champ_exp_d"] = champ_exp_d
            stats_unique_champ["champ_gold_d"] = champ_gold_d
            stats_unique_champ["champ_cs_d"] = champ_cs_d

            stats_unique_champ["champ_dmg_p"] = champ_dmg_p
            stats_unique_champ["champ_dmgtaken_p"] = champ_dmgtaken_p

            stats_champ = {}

            if player_scouting["champ"] in stats_unique_champ_pool:
                champ_played = stats_unique_champ_pool[player_scouting["champ"]]
                champ_played["champ"] = player_scouting["champ"]
                champ_played["win"].extend(champ_wr)
                champ_played["champ_kda"].extend(champ_kda)
                champ_played["champ_kills"].extend(champ_kills)
                champ_played["champ_deaths"].extend(champ_deaths)
                champ_played["champ_assists"].extend(champ_assists)
                champ_played["champ_visionscore"].extend(champ_visionscore)

                champ_played["champ_visionscore_d"].extend(champ_visionscore_d)
                champ_played["champ_exp_d"].extend(champ_exp_d)
                champ_played["champ_gold_d"].extend(champ_gold_d)
                champ_played["champ_cs_d"].extend(champ_cs_d)

                champ_played["champ_dmg_p"].extend(champ_dmg_p)
                champ_played["champ_dmgtaken_p"].extend(champ_dmgtaken_p)

            if player_scouting["champ"] not in stats_unique_champ_pool:
                stats_unique_champ_pool[player_scouting["champ"]] = stats_unique_champ


            puuid_champpool[puuid] = []
            puuid_champpool[puuid].append(stats_unique_champ_pool)

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



with open("../puuid_match", "w") as f:
    f.write(json.dumps(puuid_champpool, indent=4))

# Dataframe
# Champpool
# getting unique champs per player
avrg_stats_dict = {}
for puuid_player in puuid_champpool:
    key_champpool = puuid_champpool[puuid_player]
    for championpool in key_champpool:
            for key_champion in championpool:
                champion = championpool[key_champion]
                avrg_stats_dict["puuid"] = puuid_player
                avrg_stats_dict["champ"] = champion["champ"]

                wins = 0
                for game_outcome in champion["win"]:

                    if game_outcome == True:
                        wins += 1
                    if game_outcome == False:
                        wins += 0

                if wins == 0:
                    avrg_stats_dict["winrate"] = 0
                if wins > 0:
                    avrg_stats_dict["winrate"] = round(wins/ len(champion["win"]), 2)

                avrg_stats_dict["amount_games"] = len(champion["win"])
                avrg_stats_dict["kda"] = round(sum(champion["champ_kda"]) / len(champion["champ_kda"]) , 2)
                avrg_stats_dict["kills"] = round(sum(champion["champ_kills"]) / len(champion["champ_kills"]) , 2)
                avrg_stats_dict["deaths"] = round(sum(champion["champ_deaths"]) / len(champion["champ_deaths"]) , 2)
                avrg_stats_dict["assists"] = round(sum(champion["champ_assists"]) / len(champion["champ_assists"]) , 2)
                avrg_stats_dict["visionscore"] = round(sum(champion["champ_visionscore"]) / len(champion["champ_visionscore"]) , 2)

                avrg_stats_dict["visionscore_diff"] = round(sum(champion["champ_visionscore_d"]) / len(champion["champ_visionscore_d"]) , 2)
                avrg_stats_dict["gold_diff"] = round(sum(champion["champ_gold_d"]) / len(champion["champ_gold_d"]) , 2)
                avrg_stats_dict["cs_diff"] = round(sum(champion["champ_cs_d"]) / len(champion["champ_cs_d"]) , 2)

                avrg_stats_dict["dmg_p"] = round(sum(champion["champ_dmg_p"]) / len(champion["champ_dmg_p"]) , 2)
                avrg_stats_dict["dmg_taken_p"] = round(sum(champion["champ_dmgtaken_p"]) / len(champion["champ_dmgtaken_p"]) , 2)


                KEY_PUUID_CHAMP = puuid_player + avrg_stats_dict["champ"]
                temp_Dataframe_Champpool = pd.DataFrame({
                    "KEY_PUUID_CHAMP" : [KEY_PUUID_CHAMP],
                    "PUUID" : [puuid_player],
                    "champ" : [avrg_stats_dict["champ"]],
                    "kda": [avrg_stats_dict["kda"]],
                    "winrate" : [avrg_stats_dict["winrate"]],
                    "amount_games" : [avrg_stats_dict["amount_games"]],
                    "kills" : [avrg_stats_dict["kills"]],
                    "deaths": [avrg_stats_dict["deaths"]],
                    "assists": [avrg_stats_dict["assists"]],
                    "visionscore": [avrg_stats_dict["visionscore"]],

                    "visionscore_diff": [avrg_stats_dict["visionscore_diff"]],
                    "gold_diff": [avrg_stats_dict["gold_diff"]],
                    "cs_diff": [avrg_stats_dict["cs_diff"]],

                    "dmg_p": [avrg_stats_dict["dmg_p"]],
                    "dmg_taken_p": [avrg_stats_dict["dmg_taken_p"]]
                })

                Dataframe_Championpool = pd.concat([Dataframe_Championpool, temp_Dataframe_Champpool])


Dataframe_Player_Info = pd.merge(Dataframe_Player_Info, Dataframe_average_stats, on="PUUID")

#getting Dataframes for all matches and appending them, so they are in 1 Dataframe
full_match_info_df = pd.DataFrame()

for game_puuid in puuid_match:
    match_info = puuid_match[game_puuid]
    match_info_df = pd.DataFrame(match_info)

    full_match_info_df = pd.concat([full_match_info_df , match_info_df])

# adding the data into the google sheet (some stuff needs to be fixed (obj, kda)
service_acc = pygsheets.authorize(service_account_file="../json/spreadsheet-automator-449612-b3a5d5ca0942.json")

sheet = service_acc.open_by_url(
    "https://docs.google.com/spreadsheets/d/1iHweQST_7PNmN-PbfCDlZFUAhQzesQLrw60-WgrNK1I/edit?usp=sharing")

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
google_sheet_test.set_dataframe(Dataframe_Opponent, "AC1")

google_sheet_test = sheet.worksheet("title", "DF_Opponent")
google_sheet_test.set_dataframe(Dataframe_Opponent, "A1")


google_sheet_test = sheet.worksheet("title", "DF_Objectives")
google_sheet_test.set_dataframe(Dataframe_Objectives, "A1")

google_sheet_test = sheet.worksheet("title", "DF_Champpool")
google_sheet_test.set_dataframe(Dataframe_Championpool, "A1")


#resetting Index/Primarykey
Dataframe_Player = Dataframe_Player.reset_index(drop=True)
Dataframe_Player_Info = Dataframe_Player_Info.reset_index(drop=True)
Dataframe_Matchhistory = Dataframe_Matchhistory.reset_index(drop=True)
Dataframe_Match = Dataframe_Match.reset_index(drop=True)
Dataframe_Opponent = Dataframe_Opponent.reset_index(drop=True)
Dataframe_Objectives = Dataframe_Objectives.reset_index(drop=True)
Dataframe_Championpool = Dataframe_Championpool.reset_index(drop=True)

#setting new Index/Primarykey
Dataframe_Player = Dataframe_Player.set_index("PUUID")
Dataframe_Player_Info = Dataframe_Player_Info.set_index("PUUID")
Dataframe_Matchhistory = Dataframe_Matchhistory.set_index("KEY_PUUID_MATCH_ID")
Dataframe_Match = Dataframe_Match.set_index(["KEY_PUUID_MATCH_ID"])
Dataframe_Opponent = Dataframe_Opponent.set_index(["KEY_PUUID_MATCH_ID"])
Dataframe_Objectives = Dataframe_Objectives.set_index(["KEY_PUUID_MATCH_ID_TEAM"])
Dataframe_Championpool = Dataframe_Championpool.set_index("KEY_PUUID_CHAMP")


#storing Dataframes into SQL
#connection to postgrsql
def create_db_connection_string(db_username, db_password, db_host, db_port, db_name):
    connection_url = "postgresql+psycopg2://" + db_username + ":" + db_password + "@" + db_host + ":" + db_port + "/" + db_name
    return connection_url

conn_url = create_db_connection_string(db_username, db_password, db_host, db_port, db_name)
db_engine = create_engine(conn_url, pool_recycle=3600)

connection = db_engine.connect()


#def upsert in postgresql_upsert
def postgresql_upsert(df, table_name):
    upsert(
        con=connection,
        df=df,
        schema="playerdata",
        table_name=table_name,
        create_table=True,
        create_schema=True,
        if_row_exists="update"
    )

#adding the Dataframes to the uploadschedule
# SQL Dataframe_Player
postgresql_upsert(
    df=Dataframe_Player,
    table_name="Player",
)
"""
upsert(
    con=connection, df=Dataframe_Player, schema="playerdata", table_name="Player", create_table=True,
    create_schema=True, if_row_exists="update"
)
"""
# SQL Dataframe_Player_Info
upsert(
    con=connection, df=Dataframe_Player_Info, schema="playerdata", table_name="Player_Info", create_table=True,
    create_schema=True, if_row_exists="update"
)

# SQL Dataframe_Matchhistory
upsert(
    con=connection, df=Dataframe_Matchhistory, schema="playerdata", table_name="Matchhistory", create_table=True,
    create_schema=True, if_row_exists="update"
)

# SQL Dataframe_Match                              does this work?
upsert(
    con=connection, df=Dataframe_Match, schema="playerdata", table_name="Matchdata", create_table=True,
    create_schema=True, if_row_exists="update"
)

# SQL Dataframe_Opponent                                does this work?
upsert(
    con=connection, df=Dataframe_Opponent, schema="playerdata", table_name="Opponent", create_table=True,
    create_schema=True, if_row_exists="update")

# SQL Dataframe_Objecives                                does this work?
upsert(
    con=connection, df=Dataframe_Objectives, schema="playerdata", table_name="Objecives", create_table=True,
    create_schema=True, if_row_exists="update"
)

# SQL Dataframe_Championpool
upsert(
    con=connection, df=Dataframe_Championpool, schema="playerdata", table_name="Championpool", create_table=True,
    create_schema=True, if_row_exists="update"
)

#push uploadschedule
connection.commit()

#define query
def execute_query(table, connection):
    query = f'SELECT * FROM "playerdata"."{table}"'
    df = pd.read_sql(query, connection)

    print(df)

#query Player
execute_query(table="Player" , connection=connection)

#query Player_Info
execute_query(table="Player_Info" , connection=connection)

#query Matchhistory
execute_query(table="Matchhistory" , connection=connection)

#query Matchdata
execute_query(table="Matchdata" , connection=connection)

#query Opponent
execute_query(table="Opponent" , connection=connection)

#query Objecives
execute_query(table="Objecives" , connection=connection)

#query Championpool
execute_query(table="Championpool" , connection=connection)