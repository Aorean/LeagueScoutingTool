from backend.def_classes.player import Player
from backend.def_classes.matchhistory import Matchhistory
from def_classes.match import Match, Playerstats
from def_classes.objectives import Objectives
from backend.process_data.c_dragon import *

from function_api import *



def process_userinput(user_input):
    usernames = user_input[0].split(",")
    region = user_input[1]

    api_data = []
    api_data.append(region)

    accounts = []

    for username in usernames:
        split = username.split("#")
        #strip trailing newline
        strip = split[1].rstrip()
        split[1] = strip
        #append account to list
        accounts.append(split)

    #append accounts to return data
    api_data.append(accounts)

    return api_data

def get_playerclass(riot_ids, region, api_key):
    classes_player = []
    for riot_id in riot_ids:
        puuid = get_puuid(riot_id[0], riot_id[1], region, api_key)
        class_player = Player( puuid, riot_id[0], riot_id[1])
        classes_player.append(class_player)

    return classes_player

def get_matchhistoriesclass(classes_player, region, api_key):
    classes_matchhistory = []
    for class_player in classes_player:
        puuid = class_player.puuid
        matchhistory = get_matchhistory(region, puuid, api_key)
        class_matchhistory = Matchhistory(puuid, matchhistory)
        classes_matchhistory.append(class_matchhistory)

    return classes_matchhistory

def process_matches(classes_matchhistory, region, api_key):

    full_matchinfo = {}
    for class_matchhistory in classes_matchhistory:
        matchids = class_matchhistory.matchhistory
        for matchid in matchids:
            single_match = get_match(region, matchid, api_key)

            #generell matchdata
            class_match = Match(class_matchhistory.puuid, matchid, single_match)
            #checking for gamemode with important stats (ranked (+flexq))
            if class_match.gamemode == "CLASSIC":
                #participant matchdata
                participants = single_match["info"]["participants"]
                all_participants = []
                for participant in participants:
                    class_playerstats = Playerstats(participant, matchid, participant["puuid"])
                    class_playerstats.translate_ids(dict_items, dict_summonerspells, dict_primary_runes)
                    all_participants.append(class_playerstats)

                #objectives matchdata
                teams = single_match["info"]["teams"]
                objective_teams =  {}

                for team in teams:
                    objective_team = Objectives(team=team, matchid=matchid)
                    objective_teams[objective_team.teamid] = objective_team


                matchinfo = [class_match, all_participants, objective_teams]
                full_matchinfo.update({
                    matchid: matchinfo
                })


    return full_matchinfo

def get_champpoolclasses(dict_matches, classes_player):
    #CHANGE THIS, QUERY FROM SQL AND GET STATS FROM THERE

    for class_player in classes_player:
        dict_champ_stats = {

        }
        #stats in lists to get avrgs
        kda = []
        kills = []
        deaths = []
        assists = []
        exp = []
        level = []
        visionscore = []

        #stats roleopponent in list to get avrgs diff
        opponent_kda = []
        opponent_kills = []
        opponent_deaths = []
        opponent_assists = []
        opponent_exp = []
        opponent_level = []
        opponent_visionscore = []

        for matchid in dict_matches:
            match = dict_matches[matchid]
            #match[1] shows all participants from the match in classes
            participants = match[1]

            #role to get roleopponent
            opponent_check = ""
            for participant in participants:
                if participant.puuid == class_player.puuid:

                    #filling lists

                    kills.append(participant.kills)
                    deaths.append(participant.deaths)
                    assists.append(participant.assists)
                    exp.append(participant.exp)
                    level.append(participant.level)
                    visionscore.append(participant.visionscore)

                    opponent_check = participant.role

                if participant.role == opponent_check:

                    #filling lists opponent

                    opponent_kills.append(participant.kills)
                    opponent_deaths.append(participant.deaths)
                    opponent_assists.append(participant.assists)
                    opponent_exp.append(participant.exp)
                    opponent_level.append(participant.level)
                    opponent_visionscore.append(participant.visionscore)


















def get_playerscouting(player, info):
    player_scouting = {}
    # merging riotId and riotTagLine
    # gamename_a_tagline.append(player["riotIdGameName"])
    # gamename_a_tagline.append(player["riotIdTagline"])
    # ign = gamename_a_tagline[0] + "#" + gamename_a_tagline[1]

    # merging summonerspells into a list
    # summoner_spell.append(player["summoner1Id"])
    # summoner_spell.append(player["summoner2Id"])

    # getting stats from json
    player_scouting["gamertag"] = player["riotIdGameName"]
    player_scouting["tagline"] = player["riotIdTagline"]
    player_scouting["team"] = player["teamId"]
    player_scouting["name"] = player["riotIdGameName"] + "#" + player["riotIdTagline"]
    player_scouting["champ"] = player["championName"]
    player_scouting["level"] = player["champLevel"]
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
    player_scouting["win"] = player["win"]

    if "challenges" in player:
        player_scouting["dmg_taken%"] = round(player["challenges"]["damageTakenOnTeamPercentage"], 2)
        player_scouting["dmg%"] = round(player["challenges"]["teamDamagePercentage"], 2)
        player_scouting["kda"] = round(player["challenges"]["kda"], 2)
    else:
        player_scouting["dmg_taken%"] = "NaN"
        player_scouting["dmg%"] = "NaN"
        player_scouting["kda"] = "NaN"

    return player_scouting

def get_roleopponent(player, info):
    # merging riotId and riotTagLine
    # prev player_scouting
    role_opponent = {}
    role_opponent["gamertag"] = player["riotIdGameName"]
    role_opponent["tagline"] = player["riotIdTagline"]
    role_opponent["team"] = player["teamId"]
    role_opponent["name"] = player["riotIdGameName"] + "#" + player["riotIdTagline"]
    role_opponent["champ"] = player["championName"]
    role_opponent["level"] = player["champLevel"]
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
    role_opponent["win"] = player["win"]

    if "challenges" in player:
        role_opponent["dmg_taken%"] = round(player["challenges"]["damageTakenOnTeamPercentage"], 2)
        role_opponent["dmg%"] = round(player["challenges"]["teamDamagePercentage"], 2)
        role_opponent["kda"] = round(player["challenges"]["kda"], 2)
    else:
        role_opponent["dmg_taken%"] = "NaN"
        role_opponent["dmg%"] = "NaN"
        role_opponent["kda"] = "NaN"

    return role_opponent
