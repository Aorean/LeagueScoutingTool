import psycopg2
from backend.def_classes.sql_tables import PLAYER, MATCH, PLAYERSTATS, OBJECTIVES, CHAMPPOOL, PLAYERINFO, MATCHHISTORY
import os

def create_db_connection_string(db_username, db_password, db_host, db_port, db_name):
    connection_url = "postgresql+psycopg2://" + db_username + ":" + db_password + "@" + db_host + ":" + db_port + "/" + db_name
    return connection_url

def get_query(querytype,
          selection=None,
          schema=None,
          table = None,
          tablename=None,
          values=None,
          columns_and_values=None,
          key=None,
          keyvalue=None,
          column=None,
          value=None
              ):
    #querytypes = select, insert, update
    if querytype == "select":
        query = f'SELECT {selection} FROM "{schema}"."{table}"'
        # selection = column name (alternatively "*" for all
        # schema = sql schema (here playerdata for the most part)
        # table = sql tablename
    elif querytype == "insert":
        query = f'INSERT INTO {tablename}\nVALUES ({values})'
        # tablename = sql tablename(columns) = tablename(columnname1, columnname2, columnname3, ...)
        # values = ('value1', value2, value3, ...)
    elif querytype == "update":
        query = f"UPDATE {table}\nSET {columns_and_values}\nWHERE {key} = '{keyvalue}'"
        # table = sql tablename
        # columns_and_values = column1 = "value1", column2 = "value2", ...
        # key = name of the primarykey column
        # keyvalue = value of the primary key column that should be updated
    elif querytype == "select_where":
        query = f'SELECT {selection} FROM "{schema}"."{table}"\nWHERE {column} = \'{value}\''
    else:
        print("ERROR: Wrong querytype")
        query = None

    return query

def execute_query(db_connection, query):
    # curser

    print(query)
    conn = psycopg2.connect(dbname=db_connection[0],
                            user=db_connection[1],
                            password=db_connection[2],
                            host=db_connection[3],
                            port=db_connection[4])
    cur = conn.cursor()
    #f string for whole query, to minimize diff functions, use query for every SQL method





    try:
        cur.execute(f'{query}')

        if query.strip().startswith("SELECT"):
            rows = cur.fetchall()
            return rows
        else:
            conn.commit()
    
    except psycopg2.ProgrammingError as e:
        print(f"ProgrammingError: Query couldnt be executed")
        #print(psycopg2.ProgrammingError)
    except psycopg2.DatabaseError as e:
        print(f"DatabaseError: Query couldnt be executed")
        #print(psycopg2.DatabaseError)
    except Exception as e:
        print(f"UnexpectedError: Query couldnt be executed")
    
    conn.close()
    cur.close()

def get_participants_sql(new_match):
    participants_sql = ""
    for participant in new_match.participants:
        participants_sql += '"'
        participants_sql += participant
        participants_sql += '"'
        participants_sql += ","
    participants_sql = participants_sql[:len(participants_sql) - 1]
    return participants_sql

def SELECT_PK_PLAYER(db_connection):
    # get player table from database
    query_select_player = get_query("select", '"puuid"', "playerdata", "player")
    select_player = execute_query(db_connection, query_select_player)
    # getting a list with all puuids in the sql database already
    list_select_player = []
    for player in select_player:
        str_player = "".join(player)
        list_select_player.append(str_player)
    return list_select_player

def SELECT_PK_MATCH(db_connection):
    # get match table from database
    query_select_match = get_query("select", '"PUUID_MATCHID"', "playerdata", "match")
    select_match = execute_query(db_connection, query_select_match)

    # list with str datatypes of primary key
    list_select_match = []
    for match in select_match:
        str_match = "".join(match)
        list_select_match.append(str_match)
    return list_select_match

def SELECT_PK_PLAYERSTATS(db_connection):
    # get playerstats table from database
    query_select_playerstats = get_query("select", '"PUUID_MATCHID"', "playerdata", "playerstats")
    select_playerstats = execute_query(db_connection, query_select_playerstats)

    list_select_playerstats = []
    # list with str datatypes of primary key
    for playerstats in select_playerstats:
        str_playerstats = "".join(playerstats)
        list_select_playerstats.append(str_playerstats)
    return list_select_playerstats

def SELECT_PK_OBJECTIVES(db_connection):
    # get objectives table from database
    query_select_objectives = get_query("select", '"MATCHID_TEAMID"', "playerdata", "objectives")
    select_objectives = execute_query(db_connection, query_select_objectives)

    list_select_objectives = []
    # list with str datatypes of primary key
    for playerstats in select_objectives:
        str_objectives = "".join(playerstats)
        list_select_objectives.append(str_objectives)
    return list_select_objectives

def SELECT_PK_CHAMPPOOL(db_connection):
    # get objectives table from database
    query_select_champpool = get_query("select", '"PUUID_CHAMP_SEASON"', "playerdata", "champpool")
    select_champpool = execute_query(db_connection, query_select_champpool)

    list_select_champpool = []
    # list with str datatypes of primary key
    for champpool in select_champpool:
        str_champpool = "".join(champpool)
        list_select_champpool.append(str_champpool)
    return list_select_champpool

def SELECT_PK_PLAYERINFO(db_connection):
    # get objectives table from database
    query_select_playerinfo = get_query("select", '"puuid"', "playerdata", "playerinfo")
    select_playerinfo = execute_query(db_connection, query_select_playerinfo)

    list_select_playerinfo = []
    # list with str datatypes of primary key
    for playerinfo in select_playerinfo:
        str_playerinfo = "".join(playerinfo)
        list_select_playerinfo.append(str_playerinfo)
    return list_select_playerinfo

def SELECT_PK_MATCHHISTORY(db_connection):
        # get objectives table from database
    query_select_puuid = get_query("select", '"PUUID"', "playerdata", "matchhistory")
    select_puuid = execute_query(db_connection, query_select_puuid)

    list_select_puuid = []
    # list with str datatypes of primary key
    for puuid in select_puuid:
        str_puuid = "".join(puuid)
        list_select_puuid.append(str_puuid)
    return list_select_puuid
    

def SELECT_PK_MATCH_ARAM(db_connection):
        # get objectives table from database
    query_select_puuid_matchid = get_query("select", '"PUUID_MATCHID"', "playerdata", "aram_match")
    select_aram_match = execute_query(db_connection, query_select_puuid_matchid)

    list_select_aram_match = []
    # list with str datatypes of primary key
    for puuid in select_aram_match:
        str_puuid = "".join(puuid)
        list_select_aram_match.append(str_puuid)
    return list_select_aram_match

def SELECT_PK_MATCH_ARENA(db_connection):
        # get objectives table from database
    query_select_puuid_matchid = get_query("select", '"PUUID_MATCHID"', "playerdata", "arena_match")
    select_arena_match = execute_query(db_connection, query_select_puuid_matchid)

    list_select_arena_match = []
    # list with str datatypes of primary key
    for puuid in select_arena_match:
        str_puuid = "".join(puuid)
        list_select_arena_match.append(str_puuid)
    return list_select_arena_match


def filter_matchhistory(db_connection, matchhistory):
    query_select_matchhistory = get_query("select", '"matchid"', "playerdata", "match")
    select_matches = execute_query(db_connection, query_select_matchhistory)
    




    list_matchhistory = []

    filtered_matchhistory = []
  
    for matchid in select_matches:
        striped_id = matchid[0].strip()
        list_matchhistory.append(striped_id)


    for matchid in matchhistory:
        

        if matchid not in list_matchhistory:
            filtered_matchhistory.append(matchid)
        elif matchid in list_matchhistory:
            continue


    return filtered_matchhistory

def insert_or_update_player(input_type, db_connection, classes_player = None, dict_matches = None, classes_champpool = None, classes_playerinfo = None, matchhistories = None):
    if input_type == "player":
        # SELECT to check if UPDATE or INSERT
        list_select_player = SELECT_PK_PLAYER(db_connection)
        for class_player in classes_player:
            # create sql class
            new_player = PLAYER.from_player(class_player)

            # does the class already exist?:
            # YES it exists
            # UPDATE the SQL Table with new content
            if new_player.puuid in list_select_player:
                # variables for get query
                columns_and_values = f'"gamertag" = \'{new_player.gamertag}\', "tagline" = \'{new_player.tagline}\''
                # get query
                query_update = get_query("update",
                                         table='"playerdata"."player"',
                                         columns_and_values=columns_and_values,
                                         key='"puuid"',
                                         keyvalue=new_player.puuid)
                # execute query (UPDATE)
                rows = execute_query(db_connection, query_update)

            # NO it does not exist
            # INSERT the new data
            elif new_player.puuid not in list_select_player:
                # variables for get query
                tablename = '"playerdata"."player"("puuid", "gamertag", "tagline")'
                values = f"'{new_player.puuid}', '{new_player.gamertag}', '{new_player.tagline}'"
                # get query
                query_insert = get_query("insert",
                                         tablename=tablename,
                                         values=values)
                # append the primary key to the list of primary keys to prevent double input
                list_select_player.append(new_player.puuid)
                # execute query (INSERT)
                rows = execute_query(db_connection, query_insert)

    if input_type == "match":
        # MATCH
        list_select_match = SELECT_PK_MATCH(db_connection)

        # iteration from last 20 matches, insert the ones that are new, update the ones that are _archive
        for key in dict_matches:
            #dependencies
            match = dict_matches[key]

            class_match = match[0]
            queue_type = class_match.gamemode




            # create sql class
            new_match = MATCH.from_match(class_match)
            participants_sql = get_participants_sql(new_match)


            # does the class already exist?:
            # YES it exists
            # UPDATE the SQL Table with new content
            if new_match.PUUID_MATCHID in list_select_match:
                # variables for get_query
                columns_and_values = f'"puuid" = \'{new_match.puuid}\', "matchid" = \'{new_match.matchid}\', "participants" = \'{participants_sql}\', "gamestart" = {new_match.gamestart}, "gameend" = {new_match.gameend}, "gameduration" = {new_match.gameduration}, "tournamentcode" = \'{new_match.tournamentcode}\', "gamemode" = {new_match.gamemode}, "season" = \'{new_match.season}\', "patch" = \'{new_match.patch}\', "mapid" = {new_match.mapid}, "earlysurrender_blue" = {new_match.earlysurrender_blue}, "earlysurrender_blue" = {new_match.earlysurrender_red}, "earlysurrender" = {new_match.earlysurrender}'
                query_update = get_query("update", table='"playerdata"."match"', columns_and_values=columns_and_values, key='"PUUID_MATCHID"', keyvalue=new_match.PUUID_MATCHID)
                do_i_need_equal = execute_query(db_connection, query_update)

            # NO it does not exist
            # INSERT the new data
            elif new_match.PUUID_MATCHID not in list_select_match:
                # variables for get_query
                tablename = \
                    (
                        '"playerdata"."match"'
                        '("PUUID_MATCHID", "puuid", "matchid", "participants", "gamestart", "gameend", '
                        '"gameduration", "tournamentcode", "gamemode", "season", "patch", "mapid", "earlysurrender_blue", "earlysurrender_red", "earlysurrender")'
                    )
                values = (
                    f"'{new_match.PUUID_MATCHID}', '{new_match.puuid}', '{new_match.matchid}', "
                        f"'{participants_sql}', {new_match.gamestart}, {new_match.gameend}, "
                        f"{new_match.gameduration}, '{new_match.tournamentcode}', "
                        f"{new_match.gamemode}, '{new_match.season}', '{new_match.patch}', {new_match.mapid}, "
                        f"'{new_match.earlysurrender_blue}', '{new_match.earlysurrender_red}', '{new_match.earlysurrender}'"
                )
                query_insert = get_query("insert", tablename=tablename, values=values)
                list_select_match.append(new_match.PUUID_MATCHID)
                do_i_need_equal = execute_query(db_connection, query_insert)




    if input_type == "playerstats":
        # PLAYERSTATS
        list_select_playerstats = SELECT_PK_PLAYERSTATS(db_connection)
        #upload participants
        for key in dict_matches:
            # dependencies
            match = dict_matches[key]

            class_match = match[0]
            list_class_participants = match[1]


            for participant in list_class_participants:
                
            
                new_participant = PLAYERSTATS.from_playerstats(participant)




                if new_participant.PUUID_MATCHID in list_select_playerstats:
                    columns_and_values = \
                                        (
                                        f'"puuid" = \'{new_participant.puuid}\', '
                                        f'"matchid" = \'{new_participant.matchid}\', '
                                        f'"gamertag" = \'{new_participant.gamertag}\', '
                                        f'"tagline" = \'{new_participant.tagline}\', '
                                        f'"team" = {new_participant.team}, '
                                        f'"champ" = \'{new_participant.champ}\', '
                                        f'"role" = \'{new_participant.role}\', '
                                        f'"kills" = {new_participant.kills}, '
                                        f'"deaths" = {new_participant.deaths}, '
                                        f'"assists" = {new_participant.assists}, '
                                        f'"cs" = {new_participant.cs}, '
                                        f'"level" = {new_participant.level}, '
                                        f'"exp" = {new_participant.exp}, '
                                        f'"gold" = {new_participant.gold}, '
                                        f'"visionscore" = {new_participant.visionscore}, '
                                        f'"summonerspell1" = \'{new_participant.summonerspell1}\', '
                                        f'"summonerspell2" = \'{new_participant.summonerspell2}\', '
                                        f'"item1" = \'{new_participant.item1}\', '
                                        f'"item2" = \'{new_participant.item2}\', '
                                        f'"item3" = \'{new_participant.item3}\', '
                                        f'"item4" = \'{new_participant.item4}\', '
                                        f'"item5" = \'{new_participant.item5}\', '
                                        f'"item6" = \'{new_participant.item6}\', '
                                        f'"keyrune" = \'{new_participant.keyrune}\', '
                                        f'"win" = {new_participant.win}, '
                                        f'"mapid" = {new_participant.mapid}, '
                                        f'"gamemode" = {new_participant.gamemode}'
                                        )
                    query_update = get_query("update",
                                            table='"playerdata"."playerstats"',
                                            columns_and_values=columns_and_values,
                                            key='"PUUID_MATCHID"',
                                            keyvalue=new_participant.PUUID_MATCHID
                                            )

                    again_do_i_need_equal = execute_query(db_connection,query_update)

                elif new_participant.PUUID_MATCHID not in list_select_playerstats:
                    tablename = '"playerdata"."playerstats"("PUUID_MATCHID","puuid","matchid","gamertag","tagline","team","champ","role","kills","deaths","assists","cs","level","exp","gold","visionscore","summonerspell1","summonerspell2","item1","item2","item3","item4","item5","item6","keyrune","win","season","patch","mapid", "gamemode")'

                    values = f'\'{new_participant.PUUID_MATCHID}\', \'{new_participant.puuid}\', \'{new_participant.matchid}\', \'{new_participant.gamertag}\', \'{new_participant.tagline}\', {new_participant.team}, \'{new_participant.champ}\', \'{new_participant.role}\', {new_participant.kills}, {new_participant.deaths}, {new_participant.assists}, {new_participant.cs}, {new_participant.level}, {new_participant.exp}, {new_participant.gold}, {new_participant.visionscore}, \'{new_participant.summonerspell1}\', \'{new_participant.summonerspell2}\', \'{new_participant.item1}\', \'{new_participant.item2}\', \'{new_participant.item3}\', \'{new_participant.item4}\', \'{new_participant.item5}\', \'{new_participant.item6}\', \'{new_participant.keyrune}\', {new_participant.win}, \'{new_participant.season}\', \'{new_participant.patch}\', {new_participant.mapid}, {new_participant.gamemode}'

                    query_insert = get_query("insert", tablename=tablename, values=values)

                    list_select_playerstats.append(new_participant.PUUID_MATCHID)
                    again_do_i_need_equal = execute_query(db_connection, query_insert)




    if input_type == "playerinfo":
        # PLAYERSTATS
        list_select_playerinfo = SELECT_PK_PLAYERINFO(db_connection)
        #upload participants


        for playerinfo in classes_playerinfo:
            new_playerinfo = PLAYERINFO.from_playerinfo(playerinfo)
            
            if new_playerinfo.puuid in list_select_playerinfo:
                columns_and_values = \
                                    (
                                        f'"puuid" = \'{new_playerinfo.puuid}\', '
                                        f'"summonerlevel" = {new_playerinfo.summonerlevel}, '
                                        f'"profile_icon" = {new_playerinfo.profile_icon}, '
                                        f'"division" = \'{new_playerinfo.division}\', '
                                        f'"rank" = \'{new_playerinfo.rank}\', '
                                        f'"wins_total" = {new_playerinfo.wins_total}, '
                                        f'"losses_total" = {new_playerinfo.losses_total}, '
                                        f'"stuck" = {new_playerinfo.stuck}'
                                    )
                query_update = get_query("update",
                                            table='"playerdata"."playerinfo"',
                                            columns_and_values=columns_and_values,
                                            key='"puuid"',
                                            keyvalue=new_playerinfo.puuid
                                            )

                again_do_i_need_equal = execute_query(db_connection,query_update)
            
            elif new_playerinfo.puuid not in list_select_playerinfo:
                tablename = '"playerdata"."playerinfo"("puuid","summonerlevel","profile_icon","division","rank","wins_total","losses_total","stuck")'

                values = f'\'{new_playerinfo.puuid}\', {new_playerinfo.summonerlevel}, {new_playerinfo.profile_icon}, \'{new_playerinfo.division}\', \'{new_playerinfo.rank}\', {new_playerinfo.wins_total}, {new_playerinfo.losses_total}, {new_playerinfo.stuck}'

                query_insert = get_query("insert", tablename=tablename, values=values)

                #list_select_playerinfo.append(new_playerinfo.PUUID_MATCHID)
                again_do_i_need_equal = execute_query(db_connection, query_insert)


    if input_type == "objectives":
        # OBJECTIVES
        
        list_select_objectives = SELECT_PK_OBJECTIVES(db_connection)
        #upload objectives
        for key in dict_matches:
            # dependencies
            match = dict_matches[key]

            list_class_objectives = match[2]

            for team in list_class_objectives:
                objectives = list_class_objectives[team]
                new_team = OBJECTIVES.from_objectives(objectives)
                # check for conflict

                if new_team.MATCHID_TEAMID in list_select_objectives:
                    columns_and_values = \
                                        (
                                          f'"matchid" = \'{new_team.matchid}\', '
                                          f'"teamid" = {new_team.teamid}, '
                                          f'"baronfirst" = {new_team.baronfirst}, '
                                          f'"baronkills" = {new_team.baronkills}, '
                                          f'"atakhanfirst" = {new_team.atakhanfirst}, '
                                          f'"atakhankills" = {new_team.atakhankills}, '
                                          f'"grubsfirst" = {new_team.grubsfirst}, '
                                          f'"grubskills" = {new_team.grubskills}, '
                                          f'"dragonfirst" = {new_team.dragonfirst}, '
                                          f'"dragonkills" = {new_team.dragonkills}, '
                                          f'"riftheraldfirst" = {new_team.riftheraldfirst}, '
                                          f'"riftheraldkills" = {new_team.riftheraldkills}, '
                                          f'"towerfirst" = {new_team.towerfirst}, '
                                          f'"towerkills" = {new_team.towerkills}, '
                                          f'"inhibfirst" = {new_team.inhibfirst}, '
                                          f'"inhibkills" = {new_team.inhibkills}'
                                        )
                    query_update = get_query("update",
                                             table='"playerdata"."objectives"',
                                             columns_and_values=columns_and_values,
                                             key='"MATCHID_TEAMID"',
                                             keyvalue=new_team.MATCHID_TEAMID)
                    again_do_i_need_equal_2 = execute_query(db_connection, query_update)

                elif new_team.MATCHID_TEAMID not in list_select_objectives:
                    tablename = '"playerdata"."objectives"("MATCHID_TEAMID","matchid","teamid","baronfirst","baronkills","atakhanfirst","atakhankills","grubsfirst","grubskills","dragonfirst","dragonkills","riftheraldfirst","riftheraldkills","towerfirst","towerkills","inhibfirst","inhibkills")'
                    values = f'\'{new_team.MATCHID_TEAMID}\', \'{new_team.matchid}\', {new_team.teamid}, {new_team.baronfirst}, {new_team.baronkills}, {new_team.atakhanfirst}, {new_team.atakhankills}, {new_team.grubsfirst}, {new_team.grubskills}, {new_team.dragonfirst}, {new_team.dragonkills}, {new_team.riftheraldfirst}, {new_team.riftheraldkills}, {new_team.towerfirst}, {new_team.towerkills}, {new_team.inhibfirst}, {new_team.inhibkills}'

                    query_insert = get_query("insert", tablename=tablename, values=values)

                    list_select_objectives.append(new_team.MATCHID_TEAMID)
                    again_do_i_need_equal_2 = execute_query(db_connection, query_insert)

    if input_type == "champpool":

        list_select_champpool = SELECT_PK_CHAMPPOOL(db_connection)
        for champpool in classes_champpool:
            new_champpool = CHAMPPOOL.from_champpool(champpool)

        
            
            if new_champpool.PUUID_CHAMP_SEASON in list_select_champpool:
                columns_and_values = \
                                    (
                                      f'"puuid" = \'{new_champpool.puuid}\', '
                                      f'"champ" = \'{new_champpool.champ}\', '
                                      f'"name" = \'{new_champpool.name}\', '
                                      f'"tagline" = \'{new_champpool.tagline}\', '
                                      f'"games_played" = {new_champpool.games_played}, '
                                      f'"kda" = {new_champpool.kda}, '
                                      f'"kills" = {new_champpool.kills}, '
                                      f'"deaths" = {new_champpool.deaths}, '
                                      f'"assists" = {new_champpool.assists}, '
                                      f'"cs" = {new_champpool.cs}, '
                                      f'"exp" = {new_champpool.exp}, '
                                      f'"level" = {new_champpool.level}, '
                                      f'"gold" = {new_champpool.gold}, '
                                      f'"visionscore" = {new_champpool.visionscore}, '
                                      f'"cs_diff" = {new_champpool.cs_diff}, '
                                      f'"exp_diff" = {new_champpool.exp_diff}, '
                                      f'"level_diff" = {new_champpool.level_diff}, '
                                      f'"gold_diff" = {new_champpool.gold_diff}, '
                                      f'"visionscore_diff" = {new_champpool.visionscore_diff}, '
                                      f'"summonerspell1" = \'{new_champpool.summonerspell1}\', '
                                      f'"summonerspell2" = \'{new_champpool.summonerspell2}\', '
                                      f'"fav_role" = \'{new_champpool.fav_role}\', '
                                      f'"winrate" = {new_champpool.winrate}, '
                                      f'"win_blue" = {new_champpool.win_blue}, '
                                      f'"win_red" = {new_champpool.win_red}, '
                                      f'"season" = {new_champpool.season}'
                                    )
                query_update = get_query("update",
                                         table='"playerdata"."champpool"',
                                         columns_and_values=columns_and_values,
                                         key='"PUUID_CHAMP_SEASON"',
                                         keyvalue=new_champpool.PUUID_CHAMP_SEASON)
                again_do_i_need_equal_2 = execute_query(db_connection, query_update)


            if new_champpool.PUUID_CHAMP_SEASON not in list_select_champpool:
                tablename = '"playerdata"."champpool"("PUUID_CHAMP_SEASON", "puuid", "champ","name","tagline","games_played","kda","kills","deaths","assists","cs","exp","level","gold","visionscore","cs_diff","exp_diff","level_diff","gold_diff","visionscore_diff","summonerspell1","summonerspell2","fav_role","winrate","win_blue","win_red", "season")'
                values = f'\'{new_champpool.PUUID_CHAMP_SEASON}\', \'{new_champpool.puuid}\', \'{new_champpool.champ}\', \'{new_champpool.name}\', \'{new_champpool.tagline}\', {new_champpool.games_played}, {new_champpool.kda}, {new_champpool.kills}, {new_champpool.deaths}, {new_champpool.assists}, {new_champpool.cs}, {new_champpool.exp}, {new_champpool.level}, {new_champpool.gold}, {new_champpool.visionscore}, {new_champpool.cs_diff}, {new_champpool.exp_diff}, {new_champpool.level_diff}, {new_champpool.gold_diff}, {new_champpool.visionscore_diff}, \'{new_champpool.summonerspell1}\', \'{new_champpool.summonerspell2}\', \'{new_champpool.fav_role}\', {new_champpool.winrate}, {new_champpool.win_blue}, {new_champpool.win_red}, {new_champpool.season}'

                query_insert = get_query("insert", tablename=tablename, values=values)

                #list_select_champpool.append(new_champpool.PUUID_CHAMP)
                again_do_i_need_equal_2 = execute_query(db_connection, query_insert)
    """
    if input_type =="matchhistory":
        list_select_matchhistory = SELECT_PK_MATCHHISTORY(db_connection)
        for matchhistory in matchhistories:
            new_matchhistory = MATCHHISTORY.from_matchhistory(matchhistory)

        

            if new_matchhistory.PUUID in list_select_matchhistory:
                edited_matchhistory = ""
                edited_matchhistory += "ARRAY["
                for match in new_matchhistory.matchhistory:
                        edited_matchhistory+="'"
                        edited_matchhistory+=match
                        edited_matchhistory+="'"
                        edited_matchhistory+=","
                edited_matchhistory = edited_matchhistory[:len(edited_matchhistory)-1] +"]::VARCHAR"

                ###########################################
                
                print(edited_matchhistory)        ##DEBUG##
                
                ###########################################
                columns_and_values = \
                                    (
                                      f'"puuid" = \'{new_matchhistory.PUUID}\', '
                                      f'"matchhistory" = {edited_matchhistory}, '

                                    )
                query_update = get_query("update",
                                         table='"playerdata"."matchhistory"',
                                         columns_and_values=columns_and_values,
                                         key='"PUUID"',
                                         keyvalue=new_matchhistory.PUUID)
                again_do_i_need_equal_3 = execute_query(db_connection, query_update)


            if new_matchhistory.PUUID not in list_select_matchhistory:


                tablename = '"playerdata"."matchhistory"("PUUID", "matchhistory")'
                values = f'\'{new_matchhistory.PUUID}\', ARRAY {new_matchhistory.matchhistory}::VARCHAR[]'

                query_insert = get_query("insert", tablename=tablename, values=values)

            #list_select_champpool.append(new_champpool.PUUID_CHAMP)
            again_do_i_need_equal_3 = execute_query(db_connection, query_insert)
    """



