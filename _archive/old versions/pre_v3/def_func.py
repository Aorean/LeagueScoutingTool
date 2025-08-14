import pandas as pd

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



def get_single_match(puuid , single_match):
    single_match_matchhistory = {}
    single_match_matchhistory["match_id"] = single_match["match_id"]
    single_match_matchhistory["participants"] = single_match["participants"]
    single_match_matchhistory["gamestart"] = single_match["gamestart"]
    single_match_matchhistory["gameend"] = single_match["gameend"]
    single_match_matchhistory["gameduration"] = single_match["gameduration"]
    single_match_matchhistory["tournamentcode"] = single_match["tournamentcode"]
    single_match_matchhistory["gamemode"] = single_match["gamemode"]

    return single_match_matchhistory











#Dataframes
def get_df_player(puuid_player, account):
    # Dateframes
    # Player
    # Puuid, Gamertag, Tagline
    temp_Dataframe_Player = pd.DataFrame({
        "PUUID" : [puuid_player],
        "Gamertag" : [account[0]],
        "Tagline" : [account[1]]
    })
    return temp_Dataframe_Player


def get_df_playerinfo(player, matchhistories, rank_datas):
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

    return temp_Dataframe_Matchhistory