# Try def_classes
# get a SQL Databank schema (break my data apart into smaller chunks)
# add functions, for better overview

#could also do one big dict with ALL infos i need for DFs
"""
main_dict:
{
puuid1 =
{
Gamename = ...
Tagline = ...
Elo = ...
Winrate = ...
...
matches =
{
match_id1 =
{
champ = ...
level = ...
gold = ...
kills = ...
---
}
match_id1 =
{
champ = ...
level = ...
gold = ...
kills = ...
---
}
}
puuid2 =
{
...
"""

#dict for every Dataframe
#key is primary key for SQL

import json

from dotenv import load_dotenv
import os

from backend.functions.def_func import get_roleopponent, get_playerscouting, get_single_match
from backend.functions.function_api import get_puuid, get_matchhistory, get_match, get_summoner_id, get_rank
import pandas as pd

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
riot_id = "G2 BrokenBlade#1918,G2 Caps#1323,FNC Upset#0308"    #"Aorean#1311,Moris#25933,QaQ#00000,iHateThisNerd#EUW"                            #input("Riot ID: ")


puuid_matchid_playerscouting = {}

#Dateframes

#Player                 DONE
#Puuid, Gamertag, Tagline
Dataframe_Player = pd.DataFrame()
dict_player = {}

#Player_Info            DONE
#Puuid, Matchhistory, Elo, Winrate, Blue/Red Winrate, CS diff., Level diff., Gold diff., Visionscore diff
Dataframe_Player_Info = pd.DataFrame()
dict_player_info = {}
#Needed for merge
Dataframe_average_stats =pd.DataFrame()


#Matchhistory           DONE
#MatchID, Participants, Gamestart, Gameend, Gamedurattion, Tournamentcode
Dataframe_Matchhistory = pd.DataFrame()
dict_matchhistory = {}

#Match                  DONE
#Puuid, MatchID, Queuetyp, Gamertag, Tagline, Team, Champion, Championlevel, Gold earned, Position, KDA, Kills, Deaths,
#Assists, Visionscore, Controlwards, Objectives, Result(W/L)
Dataframe_Match = pd.DataFrame()
dict_match = {}
#this dict also contains extra info i will need later

#Opponent               DONE
#Puuid, MatchID, Queuetyp, Gamertag, Tagline, Team, Champion, Championlevel, Gold earned, Position, KDA, Kills, Deaths,
#Assists, Visionscore, Controlwards, Objectives, Result(W/L)
Dataframe_Opponent = pd.DataFrame()
dict_opponent = {}

#Objecives              DONE
#MatchID, Puuid, Team, Tower, Grubs, Drake, Herald, Atakhan, Baron, Inhibitor
Dataframe_Objectives = pd.DataFrame()
dict_objectives = {}

#Championpool
#Puuid, Gamertag, Tagline, Champion, Winrate, KDA, Avrg. Kills/Deaths/Assists, Winrate/Champion, KDA/Champion,
# CS/D/Champion, Leveldiff/Champion, Avrg. dmg%, Avrg. dmg taken%, Mastery, Role, Amount of Games
Dataframe_Championpool = pd.DataFrame()
dict_championpool = {}


#split gamertag, tagline
riot_ids = riot_id.split(",")
riot_gamenames_gametags = []

#seperating all riot ids
for id in riot_ids:
    gamename_tagline = id.split("#")
    riot_gamenames_gametags.append(gamename_tagline)

puuid_matchid_playerscouting = {}


for account in riot_gamenames_gametags:
    puuid_player = get_puuid(summoner_name=account[0], tag_line=account[1], region=region, api_key=api_key)
    matchhistory_player = get_matchhistory(region, puuid_player, api_key, startTime=20250108)
    # creating temp dict for player to get dict in dict for dict_player
    # for future access
    temp_dict_player = {}
    temp_dict_player["puuid"] = puuid_player
    temp_dict_player["gamertag"] = account[0]
    temp_dict_player["tagline"] = account[1]
    temp_dict_player["matchhistory"] = matchhistory_player


    # using the temp dict to put info into dict_player with puuid as key
    puuid_matchid_playerscouting[puuid_player] = temp_dict_player



for puuid in puuid_matchid_playerscouting:
    dict_stats = puuid_matchid_playerscouting[puuid]


    # get summoner id for get_ranked
    summoner_id = get_summoner_id("EUW1" , puuid , api_key)
    rank_player = get_rank("EUW1" , summoner_id["id"], api_key)

    # creating temp dict for player to get dict in dict for dict_player
    # for future access
    temp_dict_rankstats = {}

    temp_dict_rankstats["elo"] = rank_player[0]["tier"] + " " + rank_player[0]["rank"]
    temp_dict_rankstats["wins"] = rank_player[0]["wins"]
    temp_dict_rankstats["loses"] = rank_player[0]["losses"]
    temp_dict_rankstats["total_games"] = rank_player[0]["wins"] + rank_player[0]["losses"]
    # using the temp dict to put info into dict_player_info with puuid as key
    dict_stats["rankedstats"] = temp_dict_rankstats

puuid_matchhistory = {}

puuid_matches = {}

for player in puuid_matchid_playerscouting:
    # accessing dict_player_info to get matchhistory
    matchhistory = puuid_matchid_playerscouting[player]["matchhistory"]
    puuid_matchhistory[player] = matchhistory

    #matchdata per matchid (matchid=key)
    matchid_matchdata = {}

    # getting every match from the match history
    for match in matchhistory:
        match_data = get_match(region, match, api_key)
        # accessing the Dtos to process data into smaller packages
        # Match > MetadataDto
        metadata = match_data["metadata"]
        players = metadata["participants"]

        # Match > InfoDto
        info = match_data["info"]
        game_id = info["gameId"]
        game_creation = info["gameCreation"]
        game_start = info["gameStartTimestamp"]
        game_end = info["gameEndTimestamp"]
        game_duration = info["gameDuration"]
        game_mode = info["gameMode"]
        game_version = info["gameVersion"]  # wird später noch als "Patch" eingepflegt
        tournament_code = info["tournamentCode"]
        teams = info["teams"]

        # Match > InfoDto > ParticipantDt#
        participant_dto = info["participants"]

        # matchdata per match
        dict_match_data = {}
        dict_match_data["puuid"] = player
        dict_match_data["match_id"] = game_id
        dict_match_data["participants"] = players
        dict_match_data["gamestart"] = game_start
        dict_match_data["gameend"] = game_end
        dict_match_data["gameduration"] = game_duration
        dict_match_data["tournamentcode"] = tournament_code
        dict_match_data["gamemode"] = game_mode

        # for processing later
        dict_match_data["info_players"] = participant_dto
        dict_match_data["info"] = info

        matchid_matchdata[match] = dict_match_data

    puuid_matches[player] = matchid_matchdata

# filling dict_matchhistory
for puuid in puuid_matches:
    puuid_matchid_playerscouting[puuid]["matches"] = {}
    temp_dict_matchhistory = {}

    for matchid in puuid_matches[puuid]:
        # var for less writing
        single_match = puuid_matches[puuid][matchid]

        single_match_matchhistory = get_single_match(puuid, single_match)

        temp_dict_matchhistory[matchid] = single_match_matchhistory


        puuid_matchid_playerscouting[puuid]["matches"][matchid] = single_match_matchhistory

#getting playerscouting
  #opponent will also be in this to access later for opponent df/dict
for puuid in puuid_matches:
    temp_playerscouting = {}
    for matchid in puuid_matches[puuid]:
        single_match = puuid_matches[puuid][matchid]

        for player in single_match["info_players"]:
            if puuid == player["puuid"]:

                info = single_match["info"]
                playerscouting = get_playerscouting(player, info)
                temp_playerscouting[matchid] = playerscouting
                dict_matchid_playerscouting = {}
                dict_matchid_playerscouting[matchid] = temp_playerscouting


                puuid_matchid_playerscouting[puuid]["matches"][matchid]["ingame_stats"] = playerscouting #does this overwrite?


#opponent
for puuid in puuid_matchid_playerscouting:
    game_ids = puuid_matchid_playerscouting[puuid]["matches"]
    for game_id in game_ids:
        game_info = game_ids[game_id]
        all_players = puuid_matches[puuid][game_id]["info"]["participants"]
        info = puuid_matches[puuid][game_id]["info"]
        player_role = game_ids[game_id]["ingame_stats"]["position"]
        player_team = game_ids[game_id]["ingame_stats"]["team"]
        for participant in all_players:
            if player_role == participant["teamPosition"] and player_team != participant["teamId"]:
                role_opponent = get_roleopponent(participant, info)
                puuid_matchid_playerscouting[puuid]["matches"][game_id]["role_opponent"] = role_opponent

#objectives
for puuid in puuid_matchid_playerscouting:
    game_ids = puuid_matchid_playerscouting[puuid]["matches"]
    for game_id in game_ids:
        overall_match = puuid_matches[puuid][game_id]
        player_match = puuid_matchid_playerscouting[puuid]["matches"][game_id]
        opponent_match = puuid_matchid_playerscouting[puuid]["matches"][game_id]["role_opponent"]
        teams = overall_match["info"]["teams"]
        for team in teams:
            #dict that gets implemented in puuid_matchid_playerscouting[matchid]
            objectives = {}
            side = team["teamId"]
            objs = team["objectives"]
            feats = team["feats"]


            if "atakhan" in objs:
                objectives["atakhankills"] = objs["atakhan"]["kills"]
                objectives["atakhanfirst"] = objs["atakhan"]["first"]
            else:
                objectives["atakhankills"] = 0
                objectives["atakhanfirst"] = 0

            objectives["baronkills"] = objs["baron"]["kills"]
            objectives["baronfirst"] = objs["baron"]["first"]

            objectives["dragonkills"] = objs["dragon"]["kills"]
            objectives["dragonfirst"] = objs["dragon"]["first"]

            objectives["grubskills"] = objs["horde"]["kills"]
            objectives["grubsfirst"] = objs["horde"]["first"]

            objectives["rift_heraldkills"] = objs["riftHerald"]["kills"]
            objectives["rift_heraldfirst"] = objs["riftHerald"]["first"]

            objectives["towerkills"] = objs["tower"]["kills"]
            objectives["towerfirst"] = objs["tower"]["first"]

            objectives["inhibitorkills"] = objs["inhibitor"]["kills"]
            objectives["inhibitorfirst"] = objs["inhibitor"]["first"]

            epicmonster = feats["EPIC_MONSTER_KILL"]
            firstblood = feats["FIRST_BLOOD"]
            firstturret = feats["FIRST_TURRET"]
            check_feats = 0

            if epicmonster == 3:
                check_feats += 1
            if firstblood == 3:
                check_feats += 1
            if firstturret == 1:
                check_feats += 1

            if check_feats == 3:
                objectives["feats"] = True
            if check_feats < 3:
                objectives["feats"] = False

            if player_match["ingame_stats"]["team"] == side:
                player_match["objectives"] = objectives
            if opponent_match["team"] == side:
                opponent_match["objectives"] = objectives


#champpool
for puuid in puuid_matchid_playerscouting:

    puuid_matchid_playerscouting[puuid]["champpool"] = {}

    champ_stats = {}

    for matchid in puuid_matchid_playerscouting[puuid]["matches"]:
        stat_champpool = puuid_matchid_playerscouting[puuid]["matches"][matchid]["ingame_stats"]
        role_opponent = puuid_matchid_playerscouting[puuid]["matches"][matchid]["role_opponent"]
        gamemode = puuid_matchid_playerscouting[puuid]["matches"][matchid]["gamemode"]
        if gamemode == "CLASSIC":
            champ = stat_champpool["champ"]

            stats = {}


            if stat_champpool["win"] == True:
                stats["win"] = [1]
            if stat_champpool["win"] == False:
                stats["win"] = [0]
            stats["kda"] = [stat_champpool["kda"]]
            stats["kills"] = [stat_champpool["kills"]]
            stats["deaths"] = [stat_champpool["deaths"]]
            stats["assists"] = [stat_champpool["assists"]]
            stats["visionscore"] = [stat_champpool["visionscore"]]
            stats["visionscore_diff"] = [stat_champpool["visionscore"] - role_opponent["visionscore"]]
            stats["gold_diff"] = [stat_champpool["gold_earned"] - role_opponent["gold_earned"]]
            stats["cs_diff"] = [stat_champpool["cs"] - role_opponent["cs"]]
            stats["dmg_p"] = [stat_champpool["dmg%"]]
            stats["dmgtaken_p"] = [stat_champpool["dmg_taken%"]]

            if stat_champpool["champ"] in champ_stats:
                for key_stat in stats:
                    stat = stats[key_stat]

                    stat_champ = champ_stats[stat_champpool["champ"]][key_stat]
                    stat_champ.append(stat[0])

            if stat_champpool["champ"] not in champ_stats:
                champ_stats[stat_champpool["champ"]] = stats

    puuid_matchid_playerscouting[puuid]["champpool"] = champ_stats

#getting avarage stats for champpool
for puuid in puuid_matchid_playerscouting:
    access_champpool = puuid_matchid_playerscouting[puuid]["champpool"]
    for champ in access_champpool:
        access_champstats = puuid_matchid_playerscouting[puuid]["champpool"][champ]
        for key_stat in access_champstats:
            single_stat = access_champstats[key_stat]
            avrg_stat = round(sum(single_stat) / len(single_stat), 2)
            access_champstats[key_stat] = avrg_stat

#getting avarge stats per player
for puuid in puuid_matchid_playerscouting:
    dict_list_stats = {
        "kda" :[],
        "cs" :[],
        "win" : [],
        "level": [],
        "exp": [],
        "gold_earned": [],
        "visionscore": [],
        "cs_diff": [],
        "gold_diff": [],
        "exp_diff": [],
        "level_diff": [],
        "visionscore_diff": []
            }

    winrate_count = []

    for matchid in puuid_matchid_playerscouting[puuid]["matches"]:
        stats_match = {}
        gamemode = puuid_matchid_playerscouting[puuid]["matches"][matchid]["gamemode"]
        match = puuid_matchid_playerscouting[puuid]["matches"][matchid]["ingame_stats"]
        match_opponent = puuid_matchid_playerscouting[puuid]["matches"][matchid]["role_opponent"]
        if gamemode == "CLASSIC":
            if match["win"] == True:
                winrate_count.append(1)
            if match["win"] == False:
                winrate_count.append(0)

            stats_match["kda"] = match["kda"]
            stats_match["cs"] = match["cs"]
            stats_match["level"] = match["level"]
            stats_match["exp"] = match["exp"]
            stats_match["gold_earned"] = match["gold_earned"]
            stats_match["visionscore"] = match["visionscore"]
            stats_match["cs_diff"] = match["cs"] - match_opponent["cs"]
            stats_match["gold_diff"] = match["gold_earned"] - match_opponent["gold_earned"]
            stats_match["exp_diff"] = match["exp"] - match_opponent["exp"]
            stats_match["level_diff"] = match["level"] - match_opponent["level"]
            stats_match["visionscore_diff"] =match["visionscore"] - match_opponent["visionscore"]


            for stat in stats_match:
                single_stat = stats_match[stat]
                dict_list_stats[stat].append(single_stat)

    winrate = len(winrate_count) / sum(winrate_count)
    dict_list_stats["win"] = round(winrate, 2)

    avrg_stats = {}
    avrg_stats["kda"] = round(sum(dict_list_stats["kda"]) / len(dict_list_stats["kda"]), 2)
    avrg_stats["cs"] = round(sum(dict_list_stats["cs"]) / len(dict_list_stats["cs"]), 2)
    avrg_stats["level"] = round(sum(dict_list_stats["level"]) / len(dict_list_stats["level"]), 2)
    avrg_stats["exp"] = round(sum(dict_list_stats["exp"]) / len(dict_list_stats["exp"]), 2)
    avrg_stats["gold_earned"] = round(sum(dict_list_stats["gold_earned"]) / len(dict_list_stats["gold_earned"]), 2)
    avrg_stats["visionscore"] = round(sum(dict_list_stats["visionscore"]) / len(dict_list_stats["visionscore"]), 2)
    avrg_stats["cs_diff"] = round(sum(dict_list_stats["cs_diff"]) / len(dict_list_stats["cs_diff"]), 2)
    avrg_stats["gold_diff"] =round(sum(dict_list_stats["gold_diff"]) / len(dict_list_stats["gold_diff"]), 2)
    avrg_stats["exp_diff"] = round(sum(dict_list_stats["exp_diff"]) / len(dict_list_stats["exp_diff"]), 2)
    avrg_stats["level_diff"] = round(sum(dict_list_stats["level_diff"]) / len(dict_list_stats["level_diff"]), 2)
    avrg_stats["visionscore_diff"] = round(sum(dict_list_stats["visionscore_diff"]) / len(dict_list_stats["visionscore_diff"]), 2)

    puuid_matchid_playerscouting[puuid]["avrg_stats"] = avrg_stats

    print(avrg_stats)

#creating dataframes
main_dict = puuid_matchid_playerscouting
for puuid in puuid_matchid_playerscouting:

    df_player = pd.DataFrame({
        "puuid" : [main_dict[puuid]["puuid"]],
        "gamertag" : [main_dict[puuid]["gamertag"]],
        "tagline": [main_dict[puuid]["tagline"]]
    })

    df_player_info = pd.DataFrame({
        "puuid" : [main_dict[puuid]["puuid"]],
        "matchhistory" : [main_dict[puuid]["matchhistory"]],
        #"wins" : main_dict[puuid]["rankedstats"]["wins"],  #need to get only last 20 games, not all season
        #"loses": main_dict[puuid]["rankedstats"]["loses"],
        #"total_games": main_dict[puuid]["rankedstats"]["total_games"],
        "elo" : [main_dict[puuid]["rankedstats"]["elo"]],
        "cs": [main_dict[puuid]["avrg_stats"]["cs"]],
        "kda": [main_dict[puuid]["avrg_stats"]["kda"]],
        "level": [main_dict[puuid]["avrg_stats"]["level"]],
        "exp": [main_dict[puuid]["avrg_stats"]["exp"]],
        "gold_earned": [main_dict[puuid]["avrg_stats"]["gold_earned"]],
        "visionscore": [main_dict[puuid]["avrg_stats"]["visionscore"]],
        "cs_diff": [main_dict[puuid]["avrg_stats"]["cs_diff"]],
        "gold_diff": [main_dict[puuid]["avrg_stats"]["gold_diff"]],
        "exp_diff": [main_dict[puuid]["avrg_stats"]["exp_diff"]],
        "level_diff": [main_dict[puuid]["avrg_stats"]["level_diff"]],
        "visionscore_diff": [main_dict[puuid]["avrg_stats"]["visionscore_diff"]]
    })

    for matchid in main_dict[puuid]["matches"]:
        matches = main_dict[puuid]["matches"][matchid]
        df_matchhistory = pd.DataFrame({
            "KEY_PUUID_MATCHID" : [main_dict[puuid]["puuid"] + matchid],
            "puuid" : [main_dict[puuid]["puuid"]],
            "matchid" : [main_dict[puuid]["matches"][matchid]["match_id"]],
            "participants" : [main_dict[puuid]["matches"][matchid]["participants"]],
            "gamestart": [main_dict[puuid]["matches"][matchid]["gamestart"]],
            "gameend": [main_dict[puuid]["matches"][matchid]["gameend"]],
            "gameduration": [main_dict[puuid]["matches"][matchid]["gameduration"]],
            "tournamentcode": [main_dict[puuid]["matches"][matchid]["tournamentcode"]],
        })


with open("test", "w") as f:
    f.write(json.dumps(puuid_matchid_playerscouting, indent=4))







#main dicts

with open("dict_player", "w") as f:
    f.write(json.dumps(dict_player, indent=4))

with open("dict_player_info", "w") as f:
    f.write(json.dumps(dict_player_info, indent=4))

with open("dict_matchhistory", "w") as f:
    f.write(json.dumps(dict_matchhistory, indent=4))

with open("dict_match", "w") as f:
    f.write(json.dumps(dict_match, indent=4))

with open("dict_opponent", "w") as f:
    f.write(json.dumps(dict_opponent, indent=4))

with open("dict_objectives", "w") as f:
    f.write(json.dumps(dict_objectives, indent=4))

with open("dict_championpool", "w") as f:
    f.write(json.dumps(dict_championpool, indent=4))

#side dicts

with open("puuid_matchhistory", "w") as f:
    f.write(json.dumps(puuid_matchhistory, indent=4))

with open("puuid_matches", "w") as f:
    f.write(json.dumps(puuid_matches, indent=4))

with open("puuid_matchid_playerscouting", "w") as f:
    f.write(json.dumps(puuid_matchid_playerscouting, indent=4))




"""
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

# adding the data into the google sheet (some stuff needs to be fixed (obj, kda)
service_acc = pygsheets.authorize(service_account_file="json//spreadsheet-automator-449612-b3a5d5ca0942.json")

sheet = service_acc.open_by_url(
    "https://docs.google.com/spreadsheets/d/1iHweQST_7PNmN-PbfCDlZFUAhQzesQLrw60-WgrNK1I/edit?usp=sharing")

#define query
def execute_query(table, connection, sheet):
    query = f'SELECT * FROM "playerdata"."{table}"'
    df = pd.read_sql(query, connection)
    google_sheet_test = sheet.worksheet("title", f"{table}")
    google_sheet_test.set_dataframe(df, "A1")
    print(df)

#query Player
execute_query(table="Player" , connection=connection, sheet=sheet)

#query Player_Info
execute_query(table="Player_Info" , connection=connection, sheet=sheet)

#query Matchhistory
execute_query(table="Matchhistory" , connection=connection, sheet=sheet)

#query Matchdata
execute_query(table="Matchdata" , connection=connection, sheet=sheet)

#query Opponent
execute_query(table="Opponent" , connection=connection, sheet=sheet)

#query Objecives
execute_query(table="Objecives" , connection=connection, sheet=sheet)

#query Championpool
execute_query(table="Championpool" , connection=connection, sheet=sheet)

"""

"""

dict structure
{
puuid1 = 
{
	
{
	puuid = 	...
	gamertag = 	...
	tagline = 	...
	matchhistory = 	...

}
	matches = 
	{
		match_id1 = 
		{
			_matchinfo_
			_playerscouting_	
			...	
			_objectives_ =
				{
				...
				}
			_roleopponent_
			{	
				...	
				_objectives_ = 
					{
						...
					}
				...
			}
		}
	}
	champpool = 
	{
		champ1 = 
		{
			...
		}
		champ2 = 
		{
			...
		}
		...
	}
	stats = 
	{
		elo =		...
		wins = 		...
		loses = 	...
		total_games = 	...
	}
}	

"""