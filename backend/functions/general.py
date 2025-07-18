from backend.def_classes.summoners_rift import Player,Matchhistory,Match,Playerstats,Objectives, Mastery
from backend.def_classes.howling_abyss import aram_Match, aram_Playerstats
from backend.def_classes.arena import arena_Match, arena_Playerstats
from backend.process_data.c_dragon import *
from backend.functions.psql import get_query,execute_query, filter_matchhistory
from backend.functions.api import *



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

        #looping get matchhistory, so it gets more data until 
        #return from api is empty
        full_matchhistory = []
        startindex = 0
        while True:
            matchhistory = get_matchhistory(region, puuid, api_key, startindex)
            print(f"Matchhistory added {startindex}")
            startindex+=100
            
            if not matchhistory:
                break

            for match in matchhistory:
                full_matchhistory.append(match)
        #add check if match is already in sql
        #query_matchid = get_query(selection="matchid",schema="playerstats", table="match")
        
        class_matchhistory = Matchhistory(puuid, full_matchhistory)  
        classes_matchhistory.append(class_matchhistory)


    return classes_matchhistory


def create_dashboard_json(puuids, db_connection):


    tables = [
        "player",
        "playerinfo",
        "match",
        "playerstats",
        "champpool",
        "mastery"
    ]
    dashboard = {
        "player" : [], 
        "tc_Matches": []
        }

    
    for puuid in puuids:
        tc_matches = []
        account = {}
        player = {}
        for table in tables:
            if table == "player":

                query = get_query(querytype="select_json",
                        selection="puuid",
                        schema="playerdata", 
                        table=table,
                        column="puuid",
                        value=puuid
                            )
                row = execute_query(db_connection=db_connection, query=query)
                clean_row = row[0][0][0]

                for key,value in clean_row.items():
                    account[key] = value
            
            if table == "playerinfo":
                query = get_query(querytype="select_json",
                selection="puuid",
                schema="playerdata", 
                table=table,
                column="puuid",
                value=puuid
                    )
                row = execute_query(db_connection=db_connection, query=query)

                clean_row = row[0][0][0]
                account["elo"] = clean_row["division"] + clean_row["rank"]

                try:  
                    account["winrate"] = round(clean_row["wins_total"]/(clean_row["wins_total"]+clean_row["losses_total"]), 2)
                except ZeroDivisionError:
                    if clean_row["wins_total"]==0:
                        account["winrate"] = 0
                    if clean_row["losses_total"]==0:
                        account["winrate"] = 1

            if table == "champpool":
                query = get_query(querytype="top3_json+season",
                                  selection="champ, kda, games_played, winrate, fav_role",
                                  schema="playerdata",
                                  table=table,
                                  argument="puuid",
                                  value=puuid,
                                  order="games_played")

                row = execute_query(query=query, db_connection=db_connection)

                clean_row = row[0][0]
                
                player["champpool"] = clean_row


            if table == "match":
                query = get_query(querytype="select_json", 
                                  schema="playerdata", 
                                  table=table, 
                                  selection="tournamentcode!", 
                                  value="NULL")
                row = execute_query(db_connection=db_connection, query=query)
                clean_row = row[0][0]
                
                match_json = {
                    
                }
 
                for data in clean_row:
                    data["matchid"]
                    participants_string = data["participants"]
                    
                    participants_list = participants_string.split(",")
                    participants = []
                    for participant_puuid in participants_list:
                        cleanup = participant_puuid.strip('"')
                        prep = {"puuid" : cleanup}
                        participants.append(prep)


                    match_json = {
                        "matchId" : data["matchid"],
                        "participants" : participants,
                        "gameDuration" : data["gameduration"],
                        "tournamentcode" : data["tournamentcode"],
                    }

                    tc_matches.append(match_json)



            if table == "playerstats":
                for matchdata in tc_matches:
                    matchid = matchdata["matchId"]
                    
                    
                    query_playerdata = get_query(querytype="select_json", 
                                schema="playerdata",
                                table="playerstats",
                                selection="matchid",
                                value=matchid
                                )
                    rows_playerstats = execute_query(db_connection=db_connection, query=query_playerdata)
                    
                    clean_playerstat_rows = rows_playerstats[0][0]
                    
                    for playerstat in clean_playerstat_rows:
                        for participants_dict in matchdata["participants"]:
                            matchdata_puuid = participants_dict["puuid"]
                            playerstats_puuid = playerstat["puuid"]
                            if matchdata_puuid == playerstats_puuid:
                                for k, v in playerstat.items():
                                    participants_dict[k]=v

            if table == "mastery":
                query = get_query(querytype="top3_json",
                                  selection="champ, masterylevel, masterypoints",
                                  schema="playerdata",
                                  table=table,
                                  argument="puuid",
                                  value=puuid,
                                  order="masterypoints")

                rows_playerstats = execute_query(db_connection=db_connection, query=query)
                clean_rows = rows_playerstats[0][0]

                player["mastery"] = clean_rows

        player["account"] = account
        dashboard["player"].append(player)
        dashboard["tc_Matches"] = tc_matches

    with open("dashboard_json.json", "w") as f:
        json.dump(dashboard, f, indent=4)

    return dashboard

def get_masteryclasses(classes_player, region, api_key):
    list_mastery = []
    for player in classes_player:
        puuid = player.puuid

        resp_mastery = get_mastery(region=region, puuid=puuid, api_key=api_key)
        with open("mastery_resp.json", "w") as f:
            json.dump(resp_mastery, f, indent=4)
        
        for i in range(1, 11):
            championmastery = resp_mastery[i-1]
            mastery_class = Mastery(championmastery, player)
            
            mastery_class.translate_ids(dict_champ_id)
            #ADD TRANSLATE CHAMP IDS

            list_mastery.append(mastery_class)

            

    return list_mastery
        

        